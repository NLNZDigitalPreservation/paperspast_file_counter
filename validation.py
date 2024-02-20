import re

def year_folder(year, path, log_handler):
    if not year.is_dir():
        log_handler(f"Unexpected file {year.name} in {path} \n")
        return False
    elif not year.name.isdigit():
        log_handler(f"Unexpected folder {year.name} in {path} \n")
        return False
    else:
        return True

def issue_folder(issue, path, log_handler):
    issue_name_pattern = re.compile('[A-Z]{1,8}[_][\d]{8}')
    issue_folder = re.sub('_\d{1,3}$', '', issue.name)
    if not issue.is_dir():
        log_handler(f"Unexpected file {issue.name} in {path} \n")
        return False
    elif not issue_name_pattern.match(issue_folder):
        log_handler(f"Unexpected folder {issue.name} in {path} \n")
        return False
    else:
        return True

def file_type_folders(folder, path, log_handler):
    folders = ['IE_METS', 'PM_01', 'MM_01', 'AC_01']
    if not folder.is_dir():
        log_handler(f"Unexpected file {folder.name} in {path} \n")
        return False
    elif folder.name not in folders:
        log_handler(f"Unexpected folder {folder.name} in {path} \n")
        return False
    else:
        return True

def file_types(file, path, extensions, log_handler):
    if file.suffix not in extensions:
        log_handler(f"Unexpected file {file} in {path} \n")
        return False
    else:
        return True

def ie_mets_file(file, issue, path, log_handler):
    if not file.name == (issue + '_IE_METS.xml'):
        log_handler(f"Unexpected file {file} in {path} \n")
        return False
    else:
        return True

def pm_file(file, path, log_handler):
    return file_types(file, path ['.tif', '.tiff'], log_handler)

def mm_file(file, path, log_handler):
    return file_types(file, path ['.tif', '.tiff', '.xml'], log_handler)

def ac_file(file, path, log_handler):
    return file_types(file, path ['.pdf'], log_handler)
