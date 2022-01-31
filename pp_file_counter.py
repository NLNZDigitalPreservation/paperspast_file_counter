import math, re, sys, time
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

	def count_files(self, directory, titlecode, start_date, end_date, folders, file_types, logger=None, progress=None):
		self.logger = logger
		self.progress = progress

		issue_name_pattern = re.compile('[A-Z]{2,5}[_][\d]{8}')

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

		total = 0;
		size = 0;

		self.log_handler("Directory: " + directory)
		self.log_handler("Titlecode: " + titlecode)
		self.log_handler("Start date: " + start_date)
		self.log_handler("End date: " + end_date + "\n")

		start_time = time.time()
		for year in path_with_titlecode.glob("*"):
			if int(year.name) >= start_year and int(year.name) <= end_year:
				self.progress_handler("Counting files for " + year.name)
				for issue in year.glob("*"):
					# Pull out the date from the folder name
					date = int(re.sub(r'^.*?_', '', issue.name))
					if (issue_name_pattern.match(issue.name)) and (date >= int(start_date) and date <= int(end_date)):
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
										if folder.name == 'PM_01' and (item.suffix == '.tif' or item.suffix == '.tiff'):
											total += 1
											size += item.stat().st_size
										if folder.name == 'MM_01':
											if (item.suffix == '.tif' or item.suffix == '.tiff') and 'TIFF' in file_types:
												total += 1
												size += item.stat().st_size
											if item.name == 'mets.xml' and 'METS' in file_types:
												total += 1
												size += item.stat().st_size
											if item.suffix == '.xml' and item.name != 'mets.xml' and 'ALTO' in file_types:
												total += 1
												size += item.stat().st_size
										if folder.name == 'AC_01':
											if item.name == issue.name + '.pdf' and 'Issue PDF' in file_types:
												total += 1
												size += item.stat().st_size
											if item.name != issue.name + '.pdf' and item.suffix == '.pdf' and 'Page PDF' in file_types:
												total += 1
												size += item.stat().st_size 

										if progress:
											progress.emit(str(total))
										else:
											print(".", sep='', end='', flush=True)
				if logger == None:							
					print("\n")

		end_time = time.time()
		self.progress_handler("Finished in %.2f seconds" % (end_time - start_time))

		if self.logger == None:	
			print("Directory: " + directory)
			# print("File type: " + file_type)
			print("Titlecode: " + titlecode)
			print("Start date: " + start_date)
			print("End date: " + end_date + "\n")

		self.log_handler("Number of matching files: " + str(total))
		self.log_handler("Total size of files: " + self.convert_size(size) + "\n")

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
	