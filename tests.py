import unittest
from pp_file_counter import FileCounter

class TestMethods(unittest.TestCase):

	def test_convert_size(self):
		file_counter = FileCounter()
		to_kb = 1234
		to_mb = 4567760
		to_gb = 4567760000
		self.assertEqual(file_counter.convert_size(to_kb), '1.21 KB')
		self.assertEqual(file_counter.convert_size(to_mb), '4.36 MB')
		self.assertEqual(file_counter.convert_size(to_gb), '4.25 GB')

if __name__ == '__main__':
	unittest.main()