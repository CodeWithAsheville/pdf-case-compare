import os
from PyQt5.QtCore import QMimeDatabase, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QFileDialog


# Custom button class which accepts drag and drop events and clicks
class Button(QPushButton):
    file_selected = pyqtSignal()

    def __init__(self, default_text, parent=None):
        super().__init__(default_text, parent)
        self.setAcceptDrops(True)
        self.file_path = ''
        self.clicked.connect(self.get_file)

    # Changes the appearance of the button when a file is selected and emits a signal indicating it occured
    def on_file_selection(self):
        self.set_file_selected_style()
        self.set_file_selected_message()
        self.file_selected.emit()

    # Adds a background color style to indicate a file has been selected
    def set_file_selected_style(self):
        self.setStyleSheet('background-color: #c2f0c2')

    # Sets the message for when a file is selected
    def set_file_selected_message(self):
        self.setText(os.path.basename(self.file_path) + ' has been selected')

    def dragEnterEvent(self, e):
        paths = e.mimeData().urls()
        if len(paths) == 1 and QMimeDatabase().mimeTypeForUrl(paths[0]).name() == 'application/pdf':
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.file_path = e.mimeData().urls()[0].toLocalFile()
        self.on_file_selection()

    # Opens a QFileDialog and stores the user-selected file_path
    def get_file(self):
        file_path = QFileDialog.getOpenFileName(self, filter='*.pdf')[0]
        if file_path:
            self.file_path = file_path
            self.on_file_selection()
