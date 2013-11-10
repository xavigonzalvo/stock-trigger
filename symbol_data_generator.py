"""Library to process information extracted from get_historical_data."""

from google.protobuf import text_format
import matplotlib.pyplot as plt
import os

import curve_fitting
import util
import weeks_processor
import week_result_pb2
import yahoo_finance_fetcher as YFetcher


class Runner(object):

    def __init__(self, lock):
        self.__lock = lock

    def _MakePlots(self, rev_week_values, slopes, fitter,
                   poly_quadratic, poly_cubic, poly_linear):
        plt.subplot(411)
        plt.title('Histogram of gradients') 
        util.PlotHistogram(slopes)
    
        plt.subplot(412)
        plt.title('Value per week')
        plt.plot(rev_week_values)
    
        plt.subplot(413)
        plt.title('Quadratic fit')
        fitter.PlotPolynomial(poly_quadratic)
    
        # TODO(xavigonzalvo): this is disabled as still trying to
        # figure out what information can be extracted from cubic.
        #plt.subplot(514)
        #plt.title('Cubic fit')
        #fitter.PlotPolynomial(poly_cubic)
    
        plt.subplot(414)
        plt.title('Linear fit')
        fitter.PlotPolynomial(poly_linear)

    def _UpdateProto(self, fitter, result):
        poly_linear, error = fitter.Linear()
        linear_poly = result.poly.add()
        linear_poly.order = 1
        linear_poly.coef.extend(list(poly_linear))
        linear_poly.error = error
    
        poly_quadratic, error, convex = fitter.Quadratic()
        quadratic_poly = result.poly.add()
        quadratic_poly.order = 2
        quadratic_poly.coef.extend(list(poly_quadratic))
        quadratic_poly.error = error
        quadratic_poly.convex = convex
    
        # TODO(xavigonzalvo): this is disabled as still trying to
        # figure out what information can be extracted from cubic.
        poly_cubic = None
        #poly_cubic, error = fitter.Cubic()
        #cubic_poly = result.poly.add()
        #cubic_poly.order = 3
        #cubic_poly.coef.extend(list(poly_cubic))
        #cubic_poly.error = error
        return (poly_quadratic, poly_cubic, poly_linear)
    
    def Run(self, filename, num_weeks, output_path):
        # Read data.
        data = weeks_processor.ReadData(filename)
        total_num_weeks = len(data)
        print '%d weeks for analysis (%d months, %d years)' % (
            total_num_weeks, total_num_weeks / 4, total_num_weeks / 4 / 12)
    
        # Process data.
        processor = weeks_processor.WeeksProcessor(data, num_weeks)
        (slopes, week_values, mean, std) = processor.Process()
    
        result = week_result_pb2.WeekResult()
        result.mean = mean
        result.std = std
        symbol = util.GetSymbolFromFilename(filename)
        print 'Processing "%s"' % symbol
        fetcher = YFetcher.YahooFinanceFetcher()
        market_cap = fetcher.GetMarketCap(symbol)
        if market_cap:
            result.market_cap = market_cap 
    
        # Fit model.
        rev_week_values = week_values[::-1]
        fitter = curve_fitting.CurveFitting(rev_week_values)
    
        # Update results.
        (poly_quadratic, poly_cubic, poly_linear) = self._UpdateProto(fitter, result)
    
        # Save plots.
        filename = '%s-%s' % (util.Basename(filename), str(num_weeks)
                              if num_weeks > 0 else 'all')
        # Save plots.
        output_figure_path = os.path.join(output_path, '%s.png' % filename)
        with self.__lock:
            self._MakePlots(rev_week_values, slopes, fitter,
                            poly_quadratic, poly_cubic, poly_linear)
            plt.savefig(output_figure_path)
            plt.close('all')
    
        # Save result.
        output_result_path = os.path.join(output_path, '%s.res' % filename)
        with open(output_result_path, 'w') as f:
            f.write(text_format.MessageToString(result))
