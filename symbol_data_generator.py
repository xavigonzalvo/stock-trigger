"""Library to process information extracted from get_historical_data.

The MIT License (MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import matplotlib.pyplot as plt
import json
import os

import curve_fitting
import logging
import util
import weeks_processor
import finance_fetcher


class Runner(object):

  def __init__(self, lock, iexcloud_token):
    self._lock = lock
    self._iexcloud_token = iexcloud_token

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

  def _Update(self, fitter, result):
    if "poly" not in result:
      result["poly"] = []

    poly_linear, error = fitter.Linear()
    linear_poly = {}
    linear_poly["order"] = 1
    linear_poly["coef"] = list(poly_linear)
    linear_poly["error"] = error
    result["poly"].append(linear_poly)

    poly_quadratic, error, convex = fitter.Quadratic()
    quadratic_poly = {}
    quadratic_poly["order"] = 2
    quadratic_poly["coef"] = list(poly_quadratic)
    quadratic_poly["error"] = error
    quadratic_poly["convex"] = convex
    result["poly"].append(quadratic_poly)

    # TODO(xavigonzalvo): this is disabled as still trying to
    # figure out what information can be extracted from cubic.
    poly_cubic = None
    #poly_cubic, error = fitter.Cubic()
    #cubic_poly = result.poly.add()
    #cubic_poly.order = 3
    #cubic_poly.coef.extend(list(poly_cubic))
    #cubic_poly.error = error
    return (poly_quadratic, poly_cubic, poly_linear)

  def Run(self, filename, num_weeks, output_path, make_graphs):
    # Save plots.
    res_filename = '%s-%s' % (util.Basename(filename), str(num_weeks)
                              if num_weeks > 0 else 'all')
    # Output paths.
    output_figure_path = os.path.join(output_path, '%s.png' % res_filename)
    output_result_path = os.path.join(output_path, '%s.res' % res_filename)

    # Read data.
    data = weeks_processor.ReadData(filename)
    total_num_weeks = len(data)
    logging.info('%d weeks for analysis (%d months, %d years)' % (
        total_num_weeks, total_num_weeks / 4, total_num_weeks / 4 / 12))

    # Process data.
    processor = weeks_processor.WeeksProcessor(data, num_weeks)
    (percentual_change, week_values, mean, std, _) = processor.Process()

    result = {}
    result["mean"] = mean
    result["std"] = std
    symbol = util.GetSymbolFromFilename(filename)
    logging.info('Processing "%s"' % symbol)
    fetcher = finance_fetcher.FinanceFetcher(
        iexcloud_token=self._iexcloud_token)
    market_cap = fetcher.GetMarketCap(symbol)
    if market_cap:
      result["market_cap"] = market_cap / 1e6
    result["name"] = fetcher.GetName(symbol)

    # Fit model.
    rev_week_values = week_values[::-1]
    fitter = curve_fitting.CurveFitting(rev_week_values)

    # Update results.
    (poly_quadratic, poly_cubic, poly_linear) = self._Update(fitter, result)

    # Save plots.
    if make_graphs:
      with self._lock:
        self._MakePlots(rev_week_values, percentual_change, fitter,
                        poly_quadratic, poly_cubic, poly_linear)
        plt.savefig(output_figure_path)
        plt.close('all')

    # Save result.
    with open(output_result_path, 'wt') as f:
      json.dump(result, f)
