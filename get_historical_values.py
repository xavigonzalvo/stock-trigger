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
    print "Mean: %f, Std: %f" % (mean, std)

    plt.subplot(412)
    rev_week_values = week_values[::-1]
    plt.plot(rev_week_values)

    plt.subplot(413)
    fitter = curve_fitting.CurveFitting(rev_week_values)
    poly, error, convex = fitter.Quadratic()
    print 'Estimated quadratic polynomial (%s): %s (error: %f)' % (
        'convex' if convex else 'concave', str(poly), error)
    plt.subplot(414)
    poly, error = fitter.Cubic()
    print 'Estimated cubic polynomial: %s (error: %f)' % (
        str(poly), error)

    # Save figures
    output_figure_path = os.path.join(
        FLAGS.output_path,
        '%s-%s.png' % (util.Basename(FLAGS.filename),
                       str(FLAGS.num_weeks) if FLAGS.num_weeks > 0 else 'all'))
    plt.savefig(output_figure_path)



if __name__ == "__main__":    
    main()
