from PyQt6 import QtWidgets
from gui.main_window import MainWindow
import sys

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
