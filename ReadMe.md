# Paperspast File Counter (CoD)

CoD (Child of DiRT) is a tool built for the paperspast team to get basic reporting on files within the paperspast file system.

DiRT was the name of the old paperspast validation tool, which was replaced by a new tool. The new tool doesn't include the basic reporting which this tool aims to address. 

It can count either the total number of issues, or the totals of specific types of files given a directory in the paperspast file system, a title code, and a date range.

The directory must be the parent folder containing the title code folders.

## Running CoD
Install dependencies:
```bash
pip install pathlib PyQt5 datetime
``` 

Start the app:
```bash
python CoD.py
```

### For paperspast staff
Python must be installed - request through My Service Portal, software requests.

Download the latest version from https://github.com/NLNZDigitalPreservation/paperspast_file_counter/releases

Unzip the downloaded folder and put the resulting extracted folder where you want to keep it on your device. All files in the folder are required and need to be kept together.

You will first need to install the required python libraries by running the following command 
```bash
pip install pathlib PyQt5 datetime
``` 
You can do this by entering it into the windows search bar and clicking on the `command` option that appears in the menu.

If this doesn't work. Try opening the windows `Run` app (search for it in the serach bar). Then enter and run the command `cmd /k pip install pathlib PyQt5 datetime`

Double click on `CoD.py` to launch the app.

## Development
The UI is defined in `CoD.ui`

This was built using the PyQt5 Designer app https://www.pythonguis.com/installation/install-qt-designer-standalone/

The logic for counting files is defined in `pp_file_counter.py`

The functionality of the UI is defined in `CoD.py`, and the app is launched by runnng this file.

