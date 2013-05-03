import matplotlib.pyplot as plt
import os

import curve_fitting
import flags
import util
import weeks_processor

flags.FLAGS.add_argument("--filename", required=True,
                         help="Path to the data file")
flags.FLAGS.add_argument("--output_path", required=True,
                         help="Output folder")
flags.FLAGS.add_argument("--num_weeks", type=int, default=-1,
                         help="Number of weeks. Starting from last")
FLAGS = flags.Parse()


class Result(object):

    def __init__(self):
        self.mean = 0.0
        self.std = 0.0
        self.convex = False
        self.quadratic_poly = None
        self.quadratic_error = 0.0
        self.cubic_poly = None
        self.cubic_error = 0.0

    def ToString(self):
        return ('Mean: %f, Std: %f\n'
                'Estimated quadratic polynomial (%s): %s (error: %f)\n'
                'Estimated cubic polynomial (%s) (error: %f)\n') % (
                    self.mean, self.std, 'convex' if self.convex else 'concave',
                    str(self.quadratic_poly), self.quadratic_error,
                    str(self.cubic_poly), self.cubic_error)



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
    result = Result()
    result.mean = mean
    result.std = std

    plt.subplot(412)
    rev_week_values = week_values[::-1]
    plt.plot(rev_week_values)

    plt.subplot(413)
    fitter = curve_fitting.CurveFitting(rev_week_values)
    poly, error, convex = fitter.Quadratic()
    result.quadratic_poly = poly
    result.quadratic_error = error
    result.convex = convex

    plt.subplot(414)
    poly, error = fitter.Cubic()
    result.cubic_poly = poly
    result.cubic_error = error

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
        f.write(result.ToString())


if __name__ == "__main__":    
    main()
