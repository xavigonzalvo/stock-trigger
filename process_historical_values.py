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
                         help="Number of weeks. Starting from last")
FLAGS = flags.Parse()


def main():
    # Read data.
    data = weeks_processor.ReadData(FLAGS.filename)
    total_num_weeks = len(data)
    print '%d weeks for analysis (%d months, %d years)' % (
        total_num_weeks, total_num_weeks / 4, total_num_weeks / 4 / 12)

    # Process.
    runner = weeks_processor.WeeksProcessor(data, FLAGS.num_weeks)
    plt.subplot(411)
    (week_values, mean, std) = runner.Process()
    result = week_result_pb2.WeekResult()
    result.mean = mean
    result.std = std

    plt.subplot(412)
    rev_week_values = week_values[::-1]
    plt.plot(rev_week_values)

    plt.subplot(413)
    fitter = curve_fitting.CurveFitting(rev_week_values)
    poly, error, convex = fitter.Quadratic()
    quadratic_poly = result.poly.add()
    quadratic_poly.order = 2
    quadratic_poly.coef.extend(list(poly))
    quadratic_poly.error = error
    quadratic_poly.convex = convex

    plt.subplot(414)
    poly, error = fitter.Cubic()
    cubic_poly = result.poly.add()
    cubic_poly.order = 3
    cubic_poly.coef.extend(list(poly))
    cubic_poly.error = error

    filename = '%s-%s' % (
        util.Basename(FLAGS.filename),
        str(FLAGS.num_weeks) if FLAGS.num_weeks > 0 else 'all')
    # Save figures.
    output_figure_path = os.path.join(
        FLAGS.output_path,
        '%s.png' % filename)
    plt.savefig(output_figure_path)

    # Save result.
    output_result_path = os.path.join(
        FLAGS.output_path,
        '%s.res' % filename)
    print output_result_path
    with open(output_result_path, 'w') as f:
        f.write(text_format.MessageToString(result))


if __name__ == "__main__":    
    main()
