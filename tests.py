import unittest
from unittest.mock import MagicMock
from pathlib import Path
import re
from pp_file_counter import FileCounter
from validation import year_folder, issue_folder, file_type_folders, file_types, ie_mets_file, pm_file, mm_file, ac_file

class TestConvertSize(unittest.TestCase):
	def test_convert_size(self):
		file_counter = FileCounter()
		to_kb = 1234
		to_mb = 4567760
		to_gb = 4567760000
		self.assertEqual(file_counter.convert_size(to_kb), '1.21 KB')
		self.assertEqual(file_counter.convert_size(to_mb), '4.36 MB')
		self.assertEqual(file_counter.convert_size(to_gb), '4.25 GB')

class TestYearFolderValidation(unittest.TestCase):
    def test_year_folder_not_dir(self):
        year = MagicMock()
        year.is_dir.return_value = False
        log_handler = MagicMock()
        result = year_folder(year, "/some/path", log_handler)
        self.assertFalse(result)
        log_handler.assert_called_once_with(f"Unexpected file {year.name} in /some/path \n")

    def test_year_folder_not_valid(self):
        year = MagicMock()
        year.is_dir.return_value = True
        year.name = "not_a_digit"
        log_handler = MagicMock()
        result = year_folder(year, "/some/path", log_handler)
        self.assertFalse(result)
        log_handler.assert_called_once_with("Unexpected folder not_a_digit in /some/path \n")

    def test_year_folder_valid(self):
        year = MagicMock()
        year.is_dir.return_value = True
        year.name = "2023"
        log_handler = MagicMock()
        result = year_folder(year, "/some/path", log_handler)
        self.assertTrue(result)
        log_handler.assert_not_called()

class TestIssueFolderValidation(unittest.TestCase):
    def test_issue_folder_not_dir(self):
        issue = MagicMock()
        issue.is_dir.return_value = False
        issue.name = 'AC_18420101'
        log_handler = MagicMock()
        result = issue_folder(issue, "/some/path", log_handler)
        self.assertFalse(result)
        log_handler.assert_called_once_with(f"Unexpected file {issue.name} in /some/path \n")

    def test_issue_folder_invalid_name(self):
        issue = MagicMock()
        issue.is_dir.return_value = True
        issue.name = "invalid_name"
        log_handler = MagicMock()
        result = issue_folder(issue, "/some/path", log_handler)
        self.assertFalse(result)
        log_handler.assert_called_once_with(f"Unexpected folder {issue.name} in /some/path \n")

    def test_issue_folder_valid(self):
        issue = MagicMock()
        issue.is_dir.return_value = True
        issue.name = "AC_18420101"
        log_handler = MagicMock()
        result = issue_folder(issue, "/some/path", log_handler)
        self.assertTrue(result)
        log_handler.assert_not_called()

class TestFileTypeFolderValidation(unittest.TestCase):
    def test_folder_invalid(self):
        folder = MagicMock()
        folder.name = "invalid_name"
        log_handler = MagicMock()
        result = file_type_folders(folder, "/some/path", log_handler)
        self.assertFalse(result)
        log_handler.assert_called_once_with(f"Unexpected folder {folder.name} in /some/path \n")

    def test_folder_valid(self):
        folder = MagicMock()
        folder.name = "AC_01"
        log_handler = MagicMock()
        result = file_type_folders(folder, "/some/path", log_handler)
        self.assertTrue(result)
        log_handler.assert_not_called()

class TestFileTypesValidation(unittest.TestCase):
    def test_file_types_valid_extension(self):
        file = MagicMock()
        file.suffix = ".tif"
        path = "/some/path"
        extensions = [".pdf", ".xml", ".tif"]
        log_handler = MagicMock()
        result = file_types(file, path, extensions, log_handler)
        self.assertTrue(result)
        log_handler.assert_not_called()

    def test_file_types_invalid_extension(self):
        file = MagicMock()
        file.suffix = ".docx"
        path = "/some/path"
        extensions = [".xml", ".tif"]
        log_handler = MagicMock()
        result = file_types(file, path, extensions, log_handler)
        self.assertFalse(result)
        log_handler.assert_called_once_with(f"Unexpected file {file.name} in /some/path \n")

class TestIEMetsFileValidation(unittest.TestCase):
    def test_ie_mets_file_valid(self):
        file = MagicMock()
        file.name = "20230001_IE_METS.xml"
        issue = "20230001"
        path = "/some/path"
        log_handler = MagicMock()
        result = ie_mets_file(file, issue, path, log_handler)
        self.assertTrue(result)
        log_handler.assert_not_called()

    def test_ie_mets_file_invalid(self):
        file = MagicMock()
        file.name = "20230001_PM.xml"
        issue = "20230001"
        path = "/some/path"
        log_handler = MagicMock()
        result = ie_mets_file(file, issue, path, log_handler)
        self.assertFalse(result)
        log_handler.assert_called_once_with(f"Unexpected file {file.name} in /some/path \n")

if __name__ == '__main__':
	unittest.main()