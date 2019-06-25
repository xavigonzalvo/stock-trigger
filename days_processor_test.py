import unittest
from days_processor import DaysProcessor


class TestDaysProcessor(unittest.TestCase):

  def test_process(self):
    data = [3, 3, 2, 2, 1, 1]
    processor = DaysProcessor(data, period=6, window=2)
    (percentage_changes_per_day, averaged_data,
     mean_percentage_changes_per_day,
     std_percentage_changes_per_day,
     mean_averaged_data) = processor.process()

    self.assertEqual([3, 2, 1], averaged_data)
    self.assertEqual([25., 50.], percentage_changes_per_day)
    self.assertEqual(75. / 2., mean_percentage_changes_per_day)


if __name__ == '__main__':
    unittest.main()
