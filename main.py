# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl, QPoint, pyqtSlot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

title = '  JPM'
version = 'v0.1'
width = 300
height = 400
btn_size = 25
class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.width = width / 1.5
        self.height = height / 2.5
        self.setFixedSize(self.width, self.height)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(35, 35, 35))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(0, 0,255))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(self.title + ' - Login')
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet("""
                                        background-color: #121212;
                                        color: #143f85;
                                        """)

        self.btn_close = HoverButtonExit(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("""background-color: #8b0000;
                                    border-radius: 3px; 
                                    border-style: none;
                                    border: 1px solid black;""")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setText('X')

        self.btn_min = HoverButtonMinimize(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("""background-color: #444444;
                                   border-radius: 3px;
                                   border-style: none; 
                                   border: 1px solid black;""")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        
    # MOVE WINDOW START
    #center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # BUTTON END
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    # MOVE WINDOW END
    
    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()
        
class HoverButtonExit(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonExit, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #9f0000; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;")
class HoverButtonModify(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonModify, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #109f00; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
class HoverButtonMinimize(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonMinimize, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #565656; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
class Button(QToolButton):
    def __init__(self, parent=None):
        super(Button, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #143c85; border-radius: 3px; border-style: none; border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #144a85; border-radius: 3px; border-style: none; border: 1px solid black;")
class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.readyToEdit = True

    def mousePressEvent(self, e, Parent=None):
        super(LineEdit, self).mousePressEvent(e) #required to deselect on 2e click
        if self.readyToEdit:
            self.selectAll()
            self.readyToEdit = False

    def focusOutEvent(self, e):
        super(LineEdit, self).focusOutEvent(e) #required to remove cursor on focusOut
        self.deselect()
        self.readyToEdit = True
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    login = Login()
    login.setStyleSheet("""QMainWindow
                            {
                                border: 2px solid #121212; 
                                border-radius: 1px;
                            }
                            /*QPushButton
                            {
                                color: white; 
                                background-color: #144a85; 
                                border-radius: 3px; 
                                border-style: none;
                                border: 1px solid black;
                                width: 100%;
                                font-size: 16px;
                                height: 30%;
                            }
                            QLineEdit
                            {
                                background-color :#202020;
                                color: #144a85;
                                border-radius: 3px;
                                border-style: none; 
                                border: 1px solid darkblue;;
                            }*/
                            """)
    login.show()
    sys.exit(app.exec_())