import os
from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


# Class for a dialog prompting the user on what to do if a specified output file already exists
class OutputFileExistsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.output_file_path = parent.output_file_path
        self.path = self.get_default_path()
        # 2028 10 29 jcm changed to use a default path were 'exe' file is located, which is the output_file_path
        # self.path = parent.output_file_path
        self.setWindowModality(2)
        self.setLayout(QVBoxLayout())
        self.init_ui()

    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Oh no!')

        # Create UI elements
        self.create_label()
        self.create_textbox()
        self.create_buttons()

    def create_label(self):
        label = QLabel()
        label.setText('Report file with this name already exists. Replace it or give this report file another name?')
        label.adjustSize()
        self.layout().addWidget(label)

    def create_textbox(self):
        textbox = QLineEdit()
        textbox.setPlaceholderText(os.path.basename(self.path))
        textbox.setObjectName('textbox')
        self.layout().addWidget(textbox)

    def create_buttons(self):
        cancel_button = QPushButton('Cancel')
        cancel_button.clicked.connect(lambda: self.done(0))
        replace_button = QPushButton('Replace')
        replace_button.clicked.connect(lambda: self.done(1))
        rename_button = QPushButton('Rename')
        rename_button.clicked.connect(self.on_rename_clicked)

        hbox = QHBoxLayout()
        hbox.addWidget(replace_button)
        hbox.addWidget(rename_button)
        hbox.addWidget(cancel_button)
        self.layout().addLayout(hbox)

    #def resizeEvent(self, event):
     #   self.resize_textbox()
        #self.resize_buttons()

    def resize_textbox(self):
        textbox = self.findChild(QLineEdit, 'textbox')
        #textbox.setGeometry(10, 10, 100, 100)

    def on_rename_clicked(self):
        self.get_new_path()
        self.done(2)

    def get_new_path(self):
        path = self.findChild(QLineEdit, 'textbox').text()
        if path:
            self.path = path

    def get_default_path(self):
        i = 1
        while True:
            new_path = self.output_file_path + ' (' + str(i) + ')'
            if not os.path.exists(new_path + '.txt'):
                return new_path
            i += 1
