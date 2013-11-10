"""Tool to process information extracted from get_historical_data."""

import matplotlib.pyplot as plt
import os
from google.protobuf import text_format

import curve_fitting
import flags
import util
import weeks_processor
import week_result_pb2

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_weeks", type=int, default=-1,
                         help="Number of weeks to process. Starting from last")
FLAGS = flags.Parse()


def main():
    # Read data.
    data = weeks_processor.ReadData(FLAGS.filename)
    total_num_weeks = len(data)
    print '%d weeks for analysis (%d months, %d years)' % (
        total_num_weeks, total_num_weeks / 4, total_num_weeks / 4 / 12)

    # Process data.
    runner = weeks_processor.WeeksProcessor(data, FLAGS.num_weeks)
    (slopes, week_values, mean, std) = runner.Process()
    rev_week_values = week_values[::-1]

    result = week_result_pb2.WeekResult()
    result.mean = mean
    result.std = std

    # Fit model.
    fitter = curve_fitting.CurveFitting(rev_week_values)

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

    poly_cubic, error = fitter.Cubic()
    cubic_poly = result.poly.add()
    cubic_poly.order = 3
    cubic_poly.coef.extend(list(poly_cubic))
    cubic_poly.error = error

    # Plots.
    plt.subplot(511)
    plt.title('Histogram of gradients') 
    util.PlotHistogram(slopes)

    plt.subplot(512)
    plt.title('Value per week') 
    plt.plot(rev_week_values)

    plt.subplot(513)
    plt.title('Quadratic fit')
    fitter.PlotPolynomial(poly_quadratic)

    plt.subplot(514)
    plt.title('Cubic fit')
    fitter.PlotPolynomial(poly_cubic)

    plt.subplot(515)
    plt.title('Linear fit')
    fitter.PlotPolynomial(poly_linear)

    # Save.
    filename = '%s-%s' % (
        util.Basename(FLAGS.filename),
        str(FLAGS.num_weeks) if FLAGS.num_weeks > 0 else 'all')
    # Save figures.
    output_figure_path = os.path.join(FLAGS.output_path, '%s.png' % filename)
    plt.savefig(output_figure_path)

    # Save result.
    output_result_path = os.path.join(FLAGS.output_path, '%s.res' % filename)
    print output_result_path
    with open(output_result_path, 'w') as f:
        f.write(text_format.MessageToString(result))


if __name__ == "__main__":    
    main()
