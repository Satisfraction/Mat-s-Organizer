import os, sys, shutil
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QApplication, QInputDialog

# Define a new class called FileOrganizer that inherits from QWidget
class FileOrganizer(QWidget):
    # Initialize the class
    def __init__(self, parent=None):
        super(FileOrganizer, self).__init__(parent)

        # Set the window title
        self.setWindowTitle("Mat´s Organizer")

        # Initialize class variables
        self.selected_files = []    # List to store selected files
        self.keywords = ""          # String to store search keywords
        self.target_directory = ""  # String to store target directory for file movement/copying
        self.copy_mode = False      # Boolean to indicate whether files should be copied or moved

        # Create GUI elements
        self.create_widgets()

        # Set stylesheet
        self.setStyleSheet("background-color: black; color: lightgreen")


    # Method to create the GUI elements
    def create_widgets(self):
        # Create labels
        files_label = QLabel("Selected Files:")  # Label to indicate that selected files are being displayed
        preview_label = QLabel("Preview:")        # Label to indicate that a preview of selected files will be displayed

        # Create table to list selected files
        self.files_table = QTableWidget()                     # Table widget to display selected files
        self.files_table.setColumnCount(1)                     # Set the number of columns to 1
        self.files_table.setHorizontalHeaderLabels(["File Path"])  # Set the column header to "File Path"
        self.files_table.horizontalHeader().setStretchLastSection(True)  # Stretch the last section of the header to fill available space
        self.files_table.setSelectionBehavior(QTableWidget.SelectRows)  # Set the selection behavior to select entire rows
        self.files_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Disable editing of table cells

        # Create preview image label
        self.preview_image = QLabel()                            # Label to display preview images
        self.preview_image.setFixedSize(200, 200)                # Set size of preview image label
        self.preview_image.setAlignment(Qt.AlignCenter)           # Center preview image label contents
        self.preview_image.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)  # Set frame style for preview image label

        # Set file type filter
        self.file_type_filter = QFileDialog.Options(QFileDialog.DontUseNativeDialog)  # Filter for file types
        self.file_type_filter |= QFileDialog.DontResolveSymlinks                        # Do not resolve symlinks

        # Create buttons
        add_files_button = QPushButton("Add Files")                            # Button to add files to the selected files list
        add_files_button.clicked.connect(self.add_files)                        # Connect button click event to add_files method

        add_folder_button = QPushButton("Add Folder")                            # Button to add a folder and its contents to the selected files list
        add_folder_button.clicked.connect(self.add_folder)                        # Connect button click event to add_folder method

        remove_button = QPushButton("Remove")                                    # Button to remove selected files from the selected files list
        remove_button.clicked.connect(self.remove_files)                        # Connect button click event to remove_files method

        preview_button = QPushButton("Preview")                                # Button to preview selected file(s)
        preview_button.clicked.connect(self.preview_file)                        # Connect button click event to preview_file method

        select_target_button = QPushButton("Select Target Directory")            # Button to select target directory for file movement/copying
        select_target_button.clicked.connect(self.select_target_directory)        # Connect button click event to select_target_directory method

        search_button = QPushButton("Search")                                    # Button to search for files based on search keywords
        search_button.clicked.connect(self.search_files)                        # Connect button click event to search_files method

        move_files_button = QPushButton("Move Files")                            # Button to move selected files to target directory
        move_files_button.clicked.connect(self.move_files)                        # Connect button click event to move_files method

        copy_files_button = QPushButton("Copy Files")                            # Button to copy selected files to target directory
        copy_files_button.clicked.connect(self.copy_files)                        # Connect button click event to copy_files method

        rename_files_button = QPushButton('Rename Files')                        # Button to rename selected files
        rename_files_button.clicked.connect(self.rename_files)                    # Connect button click event to rename_files method

        # Create text edit for keywords
        self.keywords_edit = QLineEdit()                            # Text edit widget for search keywords
        self.keywords_edit.textChanged.connect(self.keywords_changed)    # Connect text changed event to keywords_changed method

        # Create layout
        files_layout = QVBoxLayout()    # Vertical layout for files-related GUI elements
        files_layout.addWidget(files_label)  # Add files label to layout
        files_layout.addWidget(self.files_table)  # Add files table to layout
        files_layout.addWidget(remove_button)  # Add remove button to layout
        remove_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for remove button
        files_layout.addWidget(add_files_button)  # Add add files button to layout
        add_files_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for add files button
        files_layout.addWidget(add_folder_button)  # Add add folder button to layout
        add_folder_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for add folder button

        preview_layout = QVBoxLayout()  # Vertical layout for preview-related GUI elements
        preview_layout.addWidget(preview_label)  # Add preview label to layout
        preview_layout.addWidget(self.preview_image)  # Add preview image label to layout
        preview_layout.addWidget(preview_button)  # Add preview button to layout
        preview_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for preview button

        search_layout = QHBoxLayout()  # Horizontal layout for search-related GUI elements
        search_layout.addWidget(QLabel("Search Keywords:"))  # Add search keywords label to layout
        search_layout.addWidget(self.keywords_edit)  # Add keywords text edit to layout
        search_layout.addWidget(search_button)  # Add search button to layout
        search_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for search button

        button_layout = QHBoxLayout()  # Horizontal layout for buttons
        button_layout.addWidget(select_target_button)  # Add select target directory button to layout
        select_target_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for select target directory button
        button_layout.addWidget(move_files_button)  # Add move files button to layout
        move_files_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for move files button
        button_layout.addWidget(copy_files_button)  # Add copy files button to layout
        copy_files_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for copy files button
        button_layout.addWidget(rename_files_button)  # Add rename files button to layout
        rename_files_button.setStyleSheet("border: 2px solid lightgreen")  # Set border for rename files button

        main_layout = QVBoxLayout(self)  # Main vertical layout for all GUI elements
        main_layout.addLayout(files_layout)  # Add files-related layout to main layout
        main_layout.addLayout(preview_layout)  # Add preview-related layout to main layout
        main_layout.addLayout(button_layout)  # Add button-related layout to main layout
        main_layout.addLayout(search_layout)  # Add search-related layout to main layout


    # Define a function to move files
    def move_files(self):
        # Check if the target directory has been set
        if not self.target_directory:
            # If not, show a warning message and return
            QMessageBox.warning(self, "Error", "Target directory not set.")
            return

        # Check if any files have been selected for moving
        if not self.selected_files:
            # If not, show a warning message and return
            QMessageBox.warning(self, "Error", "No files selected.")
            return

        # Loop through each selected file
        for file_path in self.selected_files:
            # Get the file name from the full path
            file_name = os.path.basename(file_path)
            # Create the target path by joining the target directory with the file name
            target_path = os.path.join(self.target_directory, file_name)

            # If the target path already exists
            if os.path.exists(target_path):
                # Ask the user if they want to replace the existing file
                reply = QMessageBox.question(self, "File Exists", f"{target_path} already exists. Replace it?")
                # If the user answers yes, delete the existing file
                if reply == QMessageBox.Yes:
                    os.remove(target_path)
                # If the user answers no, skip over this file
                else:
                    continue
            # Move the file to the target path
            shutil.move(file_path, target_path)

        # Reset the list of selected files and update the files table
        self.selected_files = []
        self.update_files_table()
        # Show a message indicating that the files were moved successfully
        QMessageBox.information(self, "Files Moved", "Selected files moved successfully.")

    def copy_files(self):
        # Check if target directory is set
        if not self.target_directory:
            # If not set, show a warning message
            QMessageBox.warning(self, "Error", "Target directory not set.")
            return

        # Check if any files are selected
        if not self.selected_files:
            # If no files selected, show a warning message
            QMessageBox.warning(self, "Error", "No files selected.")
            return

        # Loop through each selected file and copy to target directory
        for file_path in self.selected_files:
            # Get the file name from the file path
            file_name = os.path.basename(file_path)
            # Create the target path by joining the target directory and file name
            target_path = os.path.join(self.target_directory, file_name)
            # Check if target file already exists
            if os.path.exists(target_path):
                # If target file exists, ask the user if they want to replace it
                reply = QMessageBox.question(self, "File Exists", f"{target_path} already exists. Replace it?")
                if reply == QMessageBox.Yes:
                    # If user chooses to replace the file, delete the existing file
                    os.remove(target_path)
                else:
                    # If user chooses not to replace the file, skip to the next file
                    continue
            # Copy the file to the target path
            shutil.copy2(file_path, target_path)

        # Clear the list of selected files and update the files table
        self.selected_files = []
        self.update_files_table()
        # Show a message indicating that files were copied successfully
        QMessageBox.information(self, "Files Copied", "Selected files copied successfully.")
        
    # This method renames multiple files based on a user-specified format.
    # It first checks if any files are selected for renaming, and if not, shows a warning and returns.
    # Then, it displays a dialog box asking the user to enter the format for the new file names and stores the input.
    # Next, it iterates through each of the selected files, renaming them according to the user-specified format.
    # Finally, it clears the selection and updates the files table, and displays a success message.

    def rename_files(self):
        # check if any files are selected
        if not self.selected_files:
            # display warning and return if no files are selected
            QMessageBox.warning(self, 'Error', 'No files selected.')
            return

        # create dialog box to get user input for new file name format
        format_dialog = QInputDialog()
        format_dialog.setLabelText('Enter the format for the new file names:')
        format_dialog.setTextValue('file_{}.txt') # set default value
        format_dialog.exec_()
        format_text = format_dialog.textValue() # get user input

        # iterate through each selected file and rename them based on the user-specified format
        for i, file_path in enumerate(self.selected_files):
            new_name = format_text.format(i) # generate new file name based on user input
            os.rename(file_path, os.path.join(os.path.dirname(file_path), new_name)) # rename file

        # clear selection and update files table
        self.selected_files = []
        self.update_files_table()

        # display success message
        QMessageBox.information(self, 'Files Renamed', 'Selected files renamed successfully.')

   # Define a method named `add_files` that takes `self` as an argument.
    def add_files(self):
        # Create a new instance of the QFileDialog class.
        file_dialog = QFileDialog()
        # Set the file mode of the created QFileDialog instance to `ExistingFiles`.
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        # Display a dialog for the user to select files and save the selected files into the `files` list variable.
        # `_` is a throwaway variable used to discard the second value returned by the `getOpenFileNames` method.
        files, _ = file_dialog.getOpenFileNames(self, "Select Files", filter="All Files (*);;")
        # Add the selected files to the `selected_files` list variable of the class instance.
        self.selected_files.extend(files)
        # Update the files table.
        self.update_files_table()

    # Define a method that adds a folder to the selected_files list
    def add_folder(self):
        # Create a file dialog object
        file_dialog = QFileDialog()
        # Set the file dialog to only allow directory selection
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        # Open the file dialog and get the path of the selected directory
        directory = file_dialog.getExistingDirectory(self, "Select Folder")
        # If a directory was selected
        if directory:
            # Walk through the directory and its subdirectories
            for root, dirs, files in os.walk(directory):
                # For each file in the directory, add its path to the selected_files list
                for file in files:
                    self.selected_files.append(os.path.join(root, file))
            # Update the files table with the selected files
            self.update_files_table()

    def remove_files(self):
        # Get a list of row indexes corresponding to the currently selected files in a table.
        indexes = [index.row() for index in self.files_table.selectedIndexes()]

        # Delete the selected files from the list, starting from the last one to avoid index errors.
        for index in sorted(indexes, reverse=True):
            del self.selected_files[index]

        # Update the table to reflect the new list of selected files.
        self.update_files_table()

    # This method updates the files table with the selected files
    def update_files_table(self):
        # Remove all the rows from the table
        self.files_table.setRowCount(0)

        # Loop through each selected file
        for file_path in self.selected_files:
            # Get the current row count and insert a new row at the bottom
            row_position = self.files_table.rowCount()
            self.files_table.insertRow(row_position)

            # Set the item at the current row and first column to the file path
            self.files_table.setItem(row_position, 0, QTableWidgetItem(file_path))

    # Define a method called preview_file that takes self as an argument
    def preview_file(self):
        # Create a list called indexes by extracting each row of the selected indexes in the files_table
        indexes = [index.row() for index in self.files_table.selectedIndexes()]
        # Check if there are any indexes in the list
        if indexes:
            # Select the first file that was selected from the list of selected files
            selected_file = self.selected_files[indexes[0]]
            # Create a pixmap using the selected file
            pixmap = QPixmap(selected_file)
            # Set the pixmap to be displayed in the preview_image widget
            self.preview_image.setPixmap(pixmap)
        else:
            # If there are no selected files, clear the preview_image widget
            self.preview_image.clear()

    # Define a method select_target_directory that takes in self as a parameter.
    def select_target_directory(self):
        # Create an instance of the QFileDialog class.
        file_dialog = QFileDialog()
        # Set the file mode to DirectoryOnly.
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        # Display the file dialog and get the selected directory.
        directory = file_dialog.getExistingDirectory(self, "Select Target Directory")
        # If a directory was selected.
        if directory:
            # Set the target_directory attribute of the object to the selected directory.
            self.target_directory = directory

    # This function updates the keywords attribute of the current instance of the class with the given text.
    def keywords_changed(self, text):
        self.keywords = text

    # This function searches for files that match the given keywords and updates the selected_files attribute of the current instance of the class.
    # If no keywords are entered or no files are selected, an error message is displayed.
    # If matching files are found, the selected_files attribute is updated with the matching files and the files table is updated.
    # Finally, an information message is displayed indicating how many files were found and what keywords were used.
    def search_files(self):
        # Check if keywords are entered
        if not self.keywords:
            QMessageBox.warning(self, "Error", "No keywords entered.")
            return

        # Check if files are selected
        if not self.selected_files:
            QMessageBox.warning(self, "Error", "No files selected.")
            return

        # Search for matching files and update selected_files
        matching_files = []
        for file_path in self.selected_files:
            if self.keywords.lower() in file_path.lower():
                matching_files.append(file_path)
        self.selected_files = matching_files

        # Update files table and display search results
        self.update_files_table()
        QMessageBox.information(self, "Search Results", f"{len(matching_files)} files found matching the keyword(s): {self.keywords}")

    def matches_keywords(self, file_name):
        # Check if there are any keywords to match against
        if not self.keywords:
            # If no keywords, return True to match all file names
            return True
        else:
            # Check if all keywords are in the file name
            # Split the keywords string into a list of individual keywords
            # Then check if each keyword is in the file name using the 'in' keyword
            # Return True if all keywords are present, otherwise False
            return all(keyword in file_name for keyword in self.keywords.split())

    def closeEvent(self, event):
        # Display a confirmation dialog box asking if the user wants to exit
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit Mat's Organizer?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        # If the user selects 'Yes', accept the event (allow the window to close)
        if reply == QMessageBox.Yes:
            event.accept()
        # Otherwise, ignore the event (prevent the window from closing)
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_organizer = FileOrganizer()  
    file_organizer.show()
    sys.exit(app.exec_())
