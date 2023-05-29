# Mat's Organizer

Mat's Organizer is a file management tool built using PyQt5, which allows you to organize and manipulate files in a user-friendly interface. The tool provides various features such as selecting files, adding folders, moving/copying files, previewing files, searching for files, and renaming files.

## Getting Started

To use Mat's Organizer, you need to have Python installed on your system along with the PyQt5 library. You can install PyQt5 by running the following command:

`pip install pyqt5`


## Usage

To run the tool, execute the script by running the following command:

`python Organizer.py`


## GUI Elements

The tool consists of the following GUI elements:

- **Selected Files**: Displays the list of selected files.
- **Preview**: Shows a preview of the selected file.
- **Add Files**: Allows you to add individual files to the selected files list.
- **Add Folder**: Lets you add a folder and its contents to the selected files list.
- **Remove**: Allows you to remove selected files from the selected files list.
- **Preview**: Displays a preview of the selected file.
- **Search Keywords**: Enables you to enter search keywords to find specific files.
- **Search**: Initiates a search based on the provided search keywords.
- **Select Target Directory**: Allows you to choose a target directory for file movement/copying.
- **Move Files**: Moves the selected files to the target directory.
- **Copy Files**: Copies the selected files to the target directory.
- **Rename Files**: Renames the selected files.

## Functionality

- **Add Files**: Clicking the "Add Files" button opens a file dialog, allowing you to select individual files to add to the selected files list.

- **Add Folder**: Clicking the "Add Folder" button opens a folder dialog, enabling you to choose a folder and add its contents to the selected files list.

- **Remove**: Select one or more files from the "Selected Files" list and click the "Remove" button to remove them from the list.

- **Preview**: Select a file from the "Selected Files" list and click the "Preview" button to display a preview of the file in the "Preview" section.

- **Search**: Enter search keywords in the "Search Keywords" field and click the "Search" button to find files containing the specified keywords in their paths. The search results will replace the current list of selected files.

- **Select Target Directory**: Click the "Select Target Directory" button to choose a target directory for file movement/copying.

- **Move Files**: Click the "Move Files" button to move the selected files to the target directory. If a file with the same name already exists in the target directory, you will be prompted to replace it.

- **Copy Files**: Click the "Copy Files" button to copy the selected files to the target directory. If a file with the same name already exists in the target directory, you will be prompted to replace it.

- **Rename Files**: Select one or more files from the "Selected Files" list and click the "Rename Files" button. Enter a format for the new file names in the displayed dialog, and the selected files will be renamed accordingly.

## Exit Confirmation

When attempting to close the application, a confirmation dialog will appear to confirm if you want to exit Mat's Organizer. Click "Yes" to exit the application, or "No" to continue using the tool.

---

That's all you need to know to use Mat's Organizer effectively. Happy file organizing!

## Autor

This tool was created by Satisfraction

## License

This project is licensed under the [MIT License](LICENSE).