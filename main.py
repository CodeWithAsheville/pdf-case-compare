import sys
from PyQt5.QtWidgets import QApplication
from pisgah_gui import PisgahGui


def main():
    app = QApplication([])
    gui = PisgahGui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
