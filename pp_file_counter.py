import datetime, math, re, sys, time
from pathlib import Path

class FileCounter():
	def __init__(self):
		self.terminate = False

	def stop(self):
		self.terminate = True

	def convert_size(self, size_bytes):
	   if size_bytes == 0:
	       return "0B"
	   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	   i = int(math.floor(math.log(size_bytes, 1024)))
	   p = math.pow(1024, i)
	   s = round(size_bytes / p, 2)
	   return "%s %s" % (s, size_name[i])

	def log_handler(self, message):
		if self.logger:
			self.logger.emit(message)
		elif self.logger == None:
			print(message)

	def progress_handler(self, message):
		if self.progress:
			self.progress.emit(message)
		elif self.progress == None:
			print(message)

	def count_files(self, issues_only, directory, titlecode, start_date, end_date, folders, file_types, total_only, logger=None, progress=None):
		self.logger = logger
		self.progress = progress

		issue_name_pattern = re.compile('[A-Z]{1,8}[_][\d]{8}')

		DIR = Path(directory)
		if not DIR.is_dir():
			self.progress_handler("Directory dosen't exist")
			return

		titlecode = titlecode.upper()

		if DIR.stem != titlecode:	
			path_with_titlecode = DIR / titlecode
			if not path_with_titlecode.is_dir():
				self.progress_handler("Title code not found in that directory")
				return
		else:
			path_with_titlecode = DIR

		start_year = int(start_date[0:4])
		end_year = int(end_date[0:4])

		total = 0
		size = 0
		created = 0
		modified = 0

		PM_total = 0
		IE_METS_total = 0
		MM_tiff_total = 0
		MM_alto_total = 0
		MM_mets_total = 0
		AC_page_total = 0
		AC_issue_total = 0

		PM_size = 0
		IE_METS_size = 0
		MM_tiff_size = 0
		MM_alto_size = 0
		MM_mets_size = 0
		AC_page_size = 0
		AC_issue_size = 0

		year_folders = 0
		non_matching_folders = 0

		self.log_handler("Directory: " + directory)
		self.log_handler("Titlecode: " + titlecode)
		self.log_handler("Start date: " + start_date)
		self.log_handler("End date: " + end_date + "\n")

		start_time = time.time()
		for year in path_with_titlecode.glob("*"):
			year_folders += 1
			if year.name.isdigit() and int(year.name) >= start_year and int(year.name) <= end_year:
				self.progress_handler("Counting files for " + year.name)
				for issue in year.glob("*"):
					# Srip any issue suffixes
					issue_folder = re.sub('_\d{1,3}$', '', issue.name)
					# Pull out the date from the folder name
					date = int(re.sub(r'^.*?_', '', issue_folder))
					if (issue_name_pattern.match(issue_folder)) and (date >= int(start_date) and date <= int(end_date)):
						# Count issues only
						if issues_only:
							total += 1
							if self.terminate:
								self.progress_handler("Process cancelled")
								self.terminate = False
								return
							if progress:
								progress.emit(str(total))
							else:
								print(".", sep='', end='', flush=True)
						# Otherwise count specific file types
						else:
							for folder in issue.glob("*"):
								if folder.name in folders:
									for item in folder.iterdir():
										if self.terminate:
											self.progress_handler("Process cancelled")
											self.terminate = False
											return
										if item.is_file:
											if folder.name == 'IE_METS' and item.name == (issue.name + '_IE_METS.xml'):
												total += 1												
												size += item.stat().st_size
												if not total_only:
													IE_METS_total += 1
													IE_METS_size += item.stat().st_size
											if folder.name == 'PM_01' and (item.suffix == '.tif' or item.suffix == '.tiff'):
												total += 1
												size += item.stat().st_size
												if not total_only:
													PM_total += 1
													PM_size += item.stat().st_size
											if folder.name == 'MM_01':
												if (item.suffix == '.tif' or item.suffix == '.tiff') and 'TIFF' in file_types:
													total += 1
													size += item.stat().st_size
													if not total_only:
														MM_tiff_total += 1
														MM_tiff_size += item.stat().st_size
												if item.name == 'mets.xml' and 'METS' in file_types:
													total += 1
													size += item.stat().st_size
													if not total_only:
														MM_mets_total += 1
														MM_mets_size += item.stat().st_size
												if item.suffix == '.xml' and item.name != 'mets.xml' and 'ALTO' in file_types:
													total += 1
													size += item.stat().st_size
													if not total_only:
														MM_alto_total += 1
														MM_alto_size += item.stat().st_size
											if folder.name == 'AC_01':
												if item.name == issue.name + '.pdf' and 'Issue PDF' in file_types:
													total += 1
													size += item.stat().st_size
													if not total_only:
														AC_issue_total += 1
														AC_issue_size += item.stat().st_size
												if item.name != issue.name + '.pdf' and item.suffix == '.pdf' and 'Page PDF' in file_types:
													total += 1
													size += item.stat().st_size
													if not total_only:
														AC_page_total += 1
														AC_page_size += item.stat().st_size
											if item.stat().st_ctime > created:
												created = item.stat().st_ctime
											if item.stat().st_mtime > modified:
												modified = item.stat().st_mtime

											if progress:
												progress.emit(str(total))
											else:
												print(".", sep='', end='', flush=True)
				if logger == None:							
					print("\n")

			elif not year.name.isdigit():
				non_matching_folders += 1

		end_time = time.time()
		self.progress_handler("Finished in %.2f seconds" % (end_time - start_time))

		if non_matching_folders == year_folders:
			self.log_handler("Unexpected folder structure in " + str(path_with_titlecode))

		else:	
			if self.logger == None:	
				print("Directory: " + directory)
				print("Titlecode: " + titlecode)
				print("Start date: " + start_date)
				print("End date: " + end_date + "\n")

			self.log_handler("Number of matching " + ("issues: " if issues_only else "files: ") + str(total))
			if not issues_only:
				self.log_handler("Total size of files: " + self.convert_size(size) + "\n")

				if (total > 0):
					if not total_only:
						if 'IE_METS' in folders:
							self.log_handler("IE_METS files: " + str(IE_METS_total))
							self.log_handler("IE_METS size: " + self.convert_size(IE_METS_size) + "\n")
						if 'PM_01' in folders:
							self.log_handler("PM TIFF files: " + str(PM_total))
							self.log_handler("PM TIFF size: " + self.convert_size(PM_size) + "\n")
						if 'MM_01' in folders:
							if 'TIFF' in file_types:
								self.log_handler("MM TIFF files: " + str(MM_tiff_total))
								self.log_handler("MM TIFF size: " + self.convert_size(MM_tiff_size) + "\n")
							if 'METS' in file_types:
								self.log_handler("MM METS files: " + str(MM_mets_total))
								self.log_handler("MM METS size: " + self.convert_size(MM_mets_size) + "\n")
							if 'ALTO' in file_types:
								self.log_handler("MM ALTO files: " + str(MM_alto_total))
								self.log_handler("MM ALTO size: " + self.convert_size(MM_alto_size) + "\n")
						if 'AC_01' in folders:
							if 'Page PDF' in file_types:
								self.log_handler("AC Page PDF files: " + str(AC_page_total))
								self.log_handler("AC Page PDF size: " + self.convert_size(AC_page_size) + "\n")
							if 'Issue PDF' in file_types:
								self.log_handler("AC Issue PDF files: " + str(AC_issue_total))
								self.log_handler("AC Issue PDF files: " + self.convert_size(AC_issue_size) + "\n")

					self.log_handler("Latest created date: " + datetime.datetime.fromtimestamp(created).strftime("%b %d %Y %H:%M"))
					self.log_handler("Latest modified date: " + datetime.datetime.fromtimestamp(modified).strftime("%b %d %Y %H:%M") + "\n")
					
		return [total, self.convert_size(size)]

# if __name__ == '__main__':
# 	commands = {'directory': '', 'titlecode': '', 'start_date': '', 'end_date': '', 'file_type': ''}
# 	if len(sys.argv) < len(commands):
# 		print("Please enter all fields")
# 		exit()
		
# 	for i in range(len(sys.argv)-1):
# 		try:
# 			params = sys.argv[i+1].split('=', 1)
# 			commands[params[0]] = params[1]
# 		except Exception as e:
# 			print(e)

# 	file_counter = FileCounter()
# 	file_counter.count_files(commands['directory'], commands['titlecode'], commands['start_date'], commands['end_date'], commands['file_type'])
	
