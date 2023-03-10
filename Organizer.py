import os, sys, shutil
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QFileDialog, QLineEdit, QApplication


class FileOrganizer(QWidget):
    def __init__(self, parent=None):
        super(FileOrganizer, self).__init__(parent)

        self.setWindowTitle("Mat´s Organizer")

        # Initialize class variables
        self.selected_files = []
        self.keywords = ""
        self.target_directory = ""
        self.copy_mode = False

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Create labels
        files_label = QLabel("Selected Files:")
        preview_label = QLabel("Preview:")

        # Create table to list selected files
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(1)
        self.files_table.setHorizontalHeaderLabels(["File Path"])
        self.files_table.horizontalHeader().setStretchLastSection(True)
        self.files_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.files_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Create preview image label
        self.preview_image = QLabel()
        self.preview_image.setFixedSize(200, 200)
        self.preview_image.setAlignment(Qt.AlignCenter)
        self.preview_image.setFrameStyle(QLabel.StyledPanel | QLabel.Sunken)

        # Create file type filter dropdown
        self.file_type_filter = QFileDialog.Options(QFileDialog.DontUseNativeDialog)
        self.file_type_filter |= QFileDialog.DontResolveSymlinks

        # Create buttons
        add_files_button = QPushButton("Add Files")
        add_files_button.clicked.connect(self.add_files)

        add_folder_button = QPushButton("Add Folder")
        add_folder_button.clicked.connect(self.add_folder)

        remove_button = QPushButton("Remove")
        remove_button.clicked.connect(self.remove_files)

        preview_button = QPushButton("Preview")
        preview_button.clicked.connect(self.preview_file)

        select_target_button = QPushButton("Select Target Directory")
        select_target_button.clicked.connect(self.select_target_directory)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_files)

        move_files_button = QPushButton("Move Files")
        move_files_button.clicked.connect(self.move_files)

        copy_files_button = QPushButton("Copy Files")
        copy_files_button.clicked.connect(self.copy_files)

        # Create text edit for keywords
        self.keywords_edit = QLineEdit()
        self.keywords_edit.textChanged.connect(self.keywords_changed)

        # Create layout
        files_layout = QVBoxLayout()
        files_layout.addWidget(files_label)
        files_layout.addWidget(self.files_table)
        files_layout.addWidget(remove_button)
        files_layout.addWidget(add_files_button)
        files_layout.addWidget(add_folder_button)

        preview_layout = QVBoxLayout()
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.preview_image)
        preview_layout.addWidget(preview_button)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search Keywords:"))
        search_layout.addWidget(self.keywords_edit)
        search_layout.addWidget(search_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(select_target_button)
        button_layout.addWidget(move_files_button)
        button_layout.addWidget(copy_files_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(files_layout)
        main_layout.addLayout(preview_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(search_layout)


    def move_files(self):
        if not self.target_directory:
            QMessageBox.warning(self, "Error", "Target directory not set.")
            return

        if not self.selected_files:
            QMessageBox.warning(self, "Error", "No files selected.")
            return

        for file_path in self.selected_files:
            file_name = os.path.basename(file_path)
            target_path = os.path.join(self.target_directory, file_name)
            if os.path.exists(target_path):
                reply = QMessageBox.question(self, "File Exists", f"{target_path} already exists. Replace it?")
                if reply == QMessageBox.Yes:
                    os.remove(target_path)
                else:
                    continue
            shutil.move(file_path, target_path)

        self.selected_files = []
        self.update_files_table()
        QMessageBox.information(self, "Files Moved", "Selected files moved successfully.")

    def copy_files(self):
            if not self.target_directory:
                QMessageBox.warning(self, "Error", "Target directory not set.")
                return

            if not self.selected_files:
                QMessageBox.warning(self, "Error", "No files selected.")
                return

            for file_path in self.selected_files:
                file_name = os.path.basename(file_path)
                target_path = os.path.join(self.target_directory, file_name)
                if os.path.exists(target_path):
                    reply = QMessageBox.question(self, "File Exists", f"{target_path} already exists. Replace it?")
                    if reply == QMessageBox.Yes:
                        os.remove(target_path)
                    else:
                        continue
                shutil.copy2(file_path, target_path)

            self.selected_files = []
            self.update_files_table()
            QMessageBox.information(self, "Files Copied", "Selected files copied successfully.")
        
    def set_mode(self, mode):
        self.mode = mode
        if mode == "move":
            self.move_files_button.setText("Move Files")
            self.move_files_button.clicked.disconnect()
            self.move_files_button.clicked.connect(self.move_files)
        elif mode == "copy":
            self.move_files_button.setText("Copy Files")
            self.move_files_button.clicked.disconnect()
            self.move_files_button.clicked.connect(self.copy_files)

    def add_files(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        files, _ = file_dialog.getOpenFileNames(self, "Select Files", filter="All Files (*);;")
        self.selected_files.extend(files)
        self.update_files_table()

    def add_folder(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        directory = file_dialog.getExistingDirectory(self, "Select Folder")
        if directory:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    self.selected_files.append(os.path.join(root, file))
            self.update_files_table()

    def remove_files(self):
        indexes = [index.row() for index in self.files_table.selectedIndexes()]
        for index in sorted(indexes, reverse=True):
            del self.selected_files[index]
        self.update_files_table()

    def update_files_table(self):
        self.files_table.setRowCount(0)
        for file_path in self.selected_files:
            row_position = self.files_table.rowCount()
            self.files_table.insertRow(row_position)
            self.files_table.setItem(row_position, 0, QTableWidgetItem(file_path))

    def preview_file(self):
        indexes = [index.row() for index in self.files_table.selectedIndexes()]
        if indexes:
            selected_file = self.selected_files[indexes[0]]
            pixmap = QPixmap(selected_file)
            self.preview_image.setPixmap(pixmap)
        else:
            self.preview_image.clear()

    def select_target_directory(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        directory = file_dialog.getExistingDirectory(self, "Select Target Directory")
        if directory:
            self.target_directory = directory

    def keywords_changed(self, text):
        self.keywords = text

    def search_files(self):
        if not self.keywords:
            QMessageBox.warning(self, "Error", "No keywords entered.")
            return

        if not self.selected_files:
            QMessageBox.warning(self, "Error", "No files selected.")
            return

        matching_files = []
        for file_path in self.selected_files:
            if self.keywords.lower() in file_path.lower():
                matching_files.append(file_path)

        self.selected_files = matching_files
        self.update_files_table()
        QMessageBox.information(self, "Search Results", f"{len(matching_files)} files found matching the keyword(s): {self.keywords}")

    def matches_keywords(self, file_name):
        if not self.keywords:
            return True
        else:
            return all(keyword in file_name for keyword in self.keywords.split())

    def move_files(self, mode):
        if not self.target_directory:
            QMessageBox.warning(self, "Error", "Target directory not set.")
            return

        if not self.selected_files:
            QMessageBox.warning(self, "Error", "No files selected.")
            return

        for file_path in self.selected_files:
            file_name = os.path.basename(file_path)
            target_path = os.path.join(self.target_directory, file_name)
            if os.path.exists(target_path):
                reply = QMessageBox.question(self, "File Exists", f"{target_path} already exists. Replace it?")
                if reply == QMessageBox.Yes:
                    os.remove(target_path)
                else:
                    continue
            if mode == "move":
                shutil.move(file_path, target_path)
            elif mode == "copy":
                shutil.copy(file_path, target_path)

        self.selected_files = []
        self.update_files_table()

        if mode == "move":
            QMessageBox.information(self, "Files Moved", "Selected files moved successfully.")
        elif mode == "copy":
            QMessageBox.information(self, "Files Copied", "Selected files copied successfully.")

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit Mat's Organizer?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_organizer = FileOrganizer()  
    file_organizer.show()
    sys.exit(app.exec_())
