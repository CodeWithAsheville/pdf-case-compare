import os
import sys
from PyQt5.QtCore import QSettings
import PyQt5.QtWidgets as qtw
from pisgah_pdf import file_comparison
from button import Button
from output_file_exists_dialog import OutputFileExistsDialog


# The main class for the Pisgah PDF GUI program
class PisgahGui(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # 2021 10 29 jcm added code to find 'exe' path (pyinstaller --onefile) and make that default for output file
        self.default_output_file_dir = os.path.dirname(sys.executable)
        self.default_output_file_path = os.path.join(self.default_output_file_dir, 'comparison')
        self.output_file_path = self.default_output_file_path
        self.output_file_display = qtw.QTextEdit()
        self.output_file_display.resize(1000, 500)
        self.dynamic_font = self.font()
        self.init_ui()

    # Initializes the program user interface. Inspiration from here: https://zetcode.com/gui/pyqt5/
    def init_ui(self):
        # Set window properties
        self.setWindowTitle('Pisgah Lexis vs. CIPRS Case Comparison')
        self.setMinimumSize(750, 650)
        #self.setBaseSize(750, 650)

        # Create UI elements
        self.create_buttons()
        self.create_textbox()
        self.create_submit_button()
        # 2021 10 28 jcm removed because confusing interface for user
        # self.create_config_button()

        # Display
        self.show()

    # Create buttons
    def create_buttons(self):
        button1 = Button('LEXIS PDF File (drag and drop or click to pick)', self)
        button1.setObjectName('button1')
        button1.file_selected.connect(self.on_selection)

        button2 = Button('CIPRS PDF File (drag and drop or click to pick', self)
        button2.setObjectName('button2')
        button2.file_selected.connect(self.on_selection)

    # Create textbox to enter output file_path
    def create_textbox(self):
        textbox = qtw.QLineEdit(self)
        textbox.setPlaceholderText('Enter report file name (default is \'comparison\')')
        textbox.setObjectName('textbox')

    # Create submission button
    def create_submit_button(self):
        submit = qtw.QPushButton('Submit', self)
        submit.setObjectName('submit')
        submit.setEnabled(False)
        submit.clicked.connect(self.on_submit)

    # 2021 10 28 jcm removed because confusing interface for user
    # Create configuration button
    # def create_config_button(self):
    #     config = qtw.QPushButton('Choose where to save output files by default', self)
    #     config.setObjectName('config')
    #     config.clicked.connect(self.write_settings)

    # Dynamically adjusts the size of all window elements as the window is resized
    def resizeEvent(self, event):
        self.resize_font()
        self.resize_buttons()
        self.resize_textbox()
        self.resize_submit_button()
        # self.resize_config_button()

    # Resize buttons based on the current size of the window
    def resize_buttons(self):
        button1 = self.findChild(Button, 'button1')
        button1.setGeometry(50, 50, (self.width() - 150) / 2, self.height() * 300 / 650)
        button1.setFont(self.dynamic_font)
        button2 = self.findChild(Button, 'button2')
        button2.setGeometry(100 + button1.width(), 50, button1.width(), button1.height())
        button2.setFont(self.dynamic_font)

    # Resize textbox based on the current size of the window and other elements
    def resize_textbox(self):
        button1 = self.findChild(Button, 'button1')
        self.findChild(qtw.QLineEdit, 'textbox').setGeometry(50, button1.height() + 100, self.width() - 100, 40)

    # Resizes the submit button based on the current size of the window and other elements
    def resize_submit_button(self):
        textbox = self.findChild(qtw.QLineEdit, 'textbox')
        top_height = textbox.y() + textbox.height() + 50
        submit = self.findChild(qtw.QPushButton, 'submit')
        submit.setGeometry(50, top_height, self.width() - 100, self.height() - top_height - 50)
        submit.setFont(self.dynamic_font)

    # 2021 10 28 jcm removed because confusing interface for user
    # Resizes the config button based on the current size of the window and other elements
    # def resize_config_button(self):
    #     submit = self.findChild(qtw.QPushButton, 'submit')
    #     top_height = submit.y() + submit.height() + 50
    #     config = self.findChild(qtw.QPushButton, 'config')
    #     #config.setGeometry(50, top_height, self.width() - 100, self.height() - top_height - 50)
    #     config.setFont(self.dynamic_font)

    # Resizes font for all elements that use dynamic font
    def resize_font(self):
        self.dynamic_font.setPointSizeF(self.width() * 8 / 750)

    def on_selection(self):
        self.input_file_path_lexis = self.findChild(Button, 'button1').file_path
        self.input_file_path_ciprs = self.findChild(Button, 'button2').file_path
        if self.input_file_path_lexis and self.input_file_path_ciprs:
            self.findChild(qtw.QPushButton, 'submit').setEnabled(True)

    # Checks to see if the specified output file already exists. If so, creates a dialog prompting the user about what
    # to do. Otherwise initiates generation of the output file.
    def on_submit(self):
        output_file_path = self.findChild(qtw.QLineEdit, 'textbox').text()
        if output_file_path:
            self.output_file_path = output_file_path
        else:
            self.output_file_path = self.default_output_file_path
        while os.path.exists(self.output_file_path + '.txt'):
            dialog = OutputFileExistsDialog(self)
            result = dialog.exec()
            if result == 0:
                return
            elif result == 1:
                break
            elif result == 2:
                self.output_file_path = dialog.path
        self.generate_outfile()

    # Runs the output file generator in 'pisgah_pdf.py'
    def generate_outfile(self):
        if os.path.exists(self.input_file_path_lexis) and os.path.exists(self.input_file_path_ciprs):
            # 2021 10 28 jcm added for debug testing to find where the output file was going
            # 2021 10 28 jcm need to build pyinstaller without -w to get an output window
            print('self.output_file_path = ' + self.output_file_path)
            file_comparison(self.input_file_path_lexis, self.input_file_path_ciprs, self.output_file_path + '.txt')
            comparison_text = open(self.output_file_path + '.txt').read()
            self.output_file_display.setWindowTitle(os.path.split(self.output_file_path)[1])
            self.output_file_display.setPlainText(comparison_text)
            self.output_file_display.show()

    # 2021 10 28 jcm removed because doesn't work with pyinstaller, which uses temp directories
    # # Reads settings from the settings object
    # def read_settings(self):
    #     return QSettings('CyborgOctopus', 'Pisgah Legal Services PDF GUI').value('dir')

    # # Creates and saves default save directory settings
    # def write_settings(self):
    #     dir_selector = qtw.QFileDialog(self)
    #     #dir_selector.setOption(Sh)
    #     directory = dir_selector.getExistingDirectory(self)

    #     settings = QSettings('CyborgOctopus', 'Pisgah Legal Services PDF GUI')
    #     settings.setValue('dir', directory)
