from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())