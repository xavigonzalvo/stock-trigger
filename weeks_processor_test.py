import unittest

import weeks_processor


class WeeksProcessorTest(unittest.TestCase):

    def setUp(self):
        linear_data = []
        _NUM_WEEKS = 10
        _NUM_WEEKS_PROCESS = 4
        for week in range(_NUM_WEEKS, 1, -1):
            linear_data.append({'close': week})
        self.runner = weeks_processor.WeeksProcessor(linear_data,
                                                     _NUM_WEEKS_PROCESS,
                                                     "mockname")

    def testProcess(self):
        (perc_change, week_values, mean, std,
         mean_values) = self.runner._Process()
        self.assertEquals([10.0, 9.0, 8.0, 7.0], week_values)
        self.assertEquals(week_values[0],
                          week_values[1] + week_values[1] *
                          perc_change[0] * 5 / 100)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
