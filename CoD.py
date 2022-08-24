from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from pathlib import Path
import sys

import pp_file_counter

class WorkerSignals(QObject):
	finished = pyqtSignal()
	logger = pyqtSignal(object)
	progress = pyqtSignal(object)

class Worker(QThread):
	def __init__(self, parent):
		super(Worker, self).__init__()

		self.signals = WorkerSignals()
		self.finished = self.signals.finished
		self.progress = self.signals.progress
		self.logger = self.signals.logger
		self.file_counter = None

	def setParams(self, issues_only, directory, title_code, start_date, end_date, folders, file_types):
		self.issues_only = issues_only
		self.directory = directory
		self.title_code = title_code
		self.start_date = start_date
		self.end_date = end_date
		self.file_types = file_types
		self.folders = folders

	def stop(self):
		self.file_counter.stop()

	@pyqtSlot()
	def run(self):
		if self.file_counter:
			self.file_counter = None

		self.file_counter = pp_file_counter.FileCounter()
		self.file_counter.count_files(self.issues_only, self.directory, self.title_code, self.start_date, self.end_date, self.folders, self.file_types, self.logger, self.progress)
		self.finished.emit()


class CoDUI(QMainWindow):
	def __init__(self):
		super(CoDUI, self).__init__()
		
		uic.loadUi("CoD.ui", self)

		self.counting = False
		self.worker = None
		self.folders = set()
		self.file_types = set()
		self.issues_only = False

		self.directory_input = self.findChild(QLineEdit, "directory_input")
		self.directory_button = self.findChild(QPushButton, "directory_button")
		self.directory_button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
		self.title_code_input = self.findChild(QLineEdit, "title_code_input")
		self.start_date_input = self.findChild(QLineEdit, "start_date_input")
		self.end_date_input = self.findChild(QLineEdit, "end_date_input")
		self.start_button = self.findChild(QPushButton, "start_button")
		self.results_box = self.findChild(QTextBrowser, "results_box")
		self.progress_text = self.findChild(QTextBrowser, "progress_text")
		
		self.issue_check = self.findChild(QCheckBox, "issue_check")
		self.issue_check.stateChanged.connect(self.onStateChanged)

		self.pm_group = self.findChild(QGroupBox, "pm_group")

		self.ie_mets_group = self.findChild(QGroupBox, "ie_mets_group")

		self.mm_group = self.findChild(QGroupBox, "mm_group")
		self.mm_alto_check = self.findChild(QCheckBox, "mm_alto_check")
		self.mm_mets_check = self.findChild(QCheckBox, "mm_mets_check")
		self.mm_tiff_check = self.findChild(QCheckBox, "mm_tiff_check")

		self.ac_group = self.findChild(QGroupBox, "ac_group")
		self.ac_page_check = self.findChild(QCheckBox, "ac_page_check")
		self.ac_issue_check = self.findChild(QCheckBox, "ac_issue_check")

		date_validator = QIntValidator(0, 99999999, self)
		self.start_date_input.setValidator(date_validator)
		self.end_date_input.setValidator(date_validator)

		self.directory_button.clicked.connect(self.choose_directory)
		self.start_button.clicked.connect(self.count_files)

		self.show()
	
	@pyqtSlot()
	def onStateChanged(self):
		checkGroups = [self.ac_group, self.mm_group, self.pm_group, self.ie_mets_group]
		if self.issue_check.isChecked():
			for group in checkGroups:
				group.setEnabled(False)
		else:
			for group in checkGroups:
				group.setEnabled(True)
		
		
			

	def add_file_types(self):
		self.folders = set()
		self.file_types = set()

		if self.pm_group.isChecked():
			self.folders.add(self.pm_group.title())

		if self.ie_mets_group.isChecked():
			self.folders.add(self.ie_mets_group.title())

		if self.mm_group.isChecked():
			self.folders.add(self.mm_group.title())
			if self.mm_alto_check.isChecked():
				self.file_types.add(self.mm_alto_check.text())
			if self.mm_mets_check.isChecked():
				self.file_types.add(self.mm_mets_check.text())
			if self.mm_tiff_check.isChecked():
				self.file_types.add(self.mm_tiff_check.text())

		if self.ac_group.isChecked():
			self.folders.add(self.ac_group.title())
			if self.ac_page_check.isChecked():
				self.file_types.add(self.ac_page_check.text())
			if self.ac_issue_check.isChecked():
				self.file_types.add(self.ac_issue_check.text())

	def choose_directory(self):
		# prod:
		dialog = QFileDialog(self, "Select directory", str(Path.home()))
		# testing:
		# dialog = QFileDialog(self, "Select directory", "/media/sf_Y_DRIVE/paperspast/objects/14/other/Newspapers/OCR")

		dialog.setFileMode(QFileDialog.DirectoryOnly)
		dialog.exec_()
		selected_directory = None
		if len(dialog.selectedFiles()) == 1:
			selected_directory = dialog.selectedFiles()[0]

		if selected_directory:
			self.directory_input.setText(selected_directory)

	def progress_handler(self, value):
		self.progress_text.setText(value)

	def logger_handler(self, value):
		self.results_box.append(value)

	def finishWorker(self):
		self.start_button.setText('Start')
		self.worker.quit()
		self.counting = False

	def count_files(self):
		if self.counting:
			self.start_button.setText('Start')
			self.counting = False
			self.issues_only = False
			if self.worker:
				self.worker.stop()

		else:
			directory = self.directory_input.text().strip()
			title_code = self.title_code_input.text().strip().upper()
			start_date = self.start_date_input.text().strip()
			end_date = self.end_date_input.text().strip()
			
			if self.issue_check.isChecked():
				self.issues_only = True
			else:
				self.issues_only = False
				self.add_file_types()

			self.results_box.clear()

			if directory == '' or title_code == '' or start_date == '' or end_date == '':
				self.progress_text.setText('Please enter all fields')

			elif start_date > end_date:
				self.progress_text.setText('Make sure the start date is earlier than the end date')

			elif self.issues_only == False and 'PM_01' not in self.folders and 'IE_METS' not in self.folders and len(self.file_types) == 0:
				self.progress_text.setText('Please select a file type')

			else:
				self.worker = Worker(self)
				self.worker.setParams(self.issues_only, directory, title_code, start_date, end_date, self.folders, self.file_types)
				self.worker.logger.connect(self.logger_handler)
				self.worker.progress.connect(self.progress_handler)
				self.worker.finished.connect(self.finishWorker)

				self.start_button.setText('Cancel')
				self.results_box.clear()
				self.progress_text.setText('Starting')
				self.counting = True

				self.worker.start()


app = QApplication(sys.argv)
UIWindow = CoDUI()
app.exec_()
