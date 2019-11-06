# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl, QPoint, pyqtSlot, QRegExp
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# pip install passlib
# from passlib.context import CryptContext
import base64

title = '  JPM'
version = 'v0.1'
width = 300
height = 400
btn_size = 25
# pwd_context = CryptContext(
#         schemes=["pbkdf2_sha256"],
#         default="pbkdf2_sha256",
#         pbkdf2_sha256__default_rounds=30000
# )
import getpass, tempfile, os, json, re
username = getpass.getuser()
password_dir = tempfile.gettempdir() + '/JMP/'
master_password = ''

                
class Login(QWidget):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.check_if_file_exists()
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.width = width / 1.5
        self.height = height / 2.5
        self.setFixedSize(self.width, self.height)

        
        app.setStyle("Fusion")

        # Now use a palette to switch to dark colors:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(self.title + ' - Login')
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setText('X')

        self.btn_min = ButtonGray(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        self.lblInfo = QLabel(self)
        self.lblInfo.setText('Hi')
        self.lblInfo.move(7, 30)
        self.lblInfo.resize(self.width - (7 * 2), 50)
        # LOGIN ITEMS START
        self.btnLogin = ButtonGreen(self)
        self.btnLogin.setText('Login')
        self.btnLogin.move(7,self.height/1.3)
        self.btnLogin.resize(self.width - (7 * 2), 30)
        self.btnLogin.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnLogin.setToolTip('Login to account.')
        self.btnLogin.setFont(QFont('Calibri', 12))
        self.btnLogin.clicked.connect(self.login)
        
        self.txtPassword = LineEdit(self)
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setText('Password')
        self.txtPassword.setToolTip('Your Password')
        self.txtPassword.move(7, self.height / 2)
        self.txtPassword.resize(self.width - (7 * 2), 30)
        self.txtPassword.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        # self.create_master_password()
        # lOGIN ITEMS END
    def login(self):
        temp = self.txtPassword.text()
        temp_master = base64.urlsafe_b64decode(master_password)
        temp_master = temp_master.decode('utf-8')

        if temp == temp_master:
            print('yeaa')
        else:
            print('wrong')
            
    def check_if_file_exists(self):
        if not os.path.exists(password_dir):
            os.makedirs(password_dir)
            
        if not os.path.exists(password_dir + 'master.txt'):
            file = open(password_dir + "master.txt", "w")
            file.write('')
            file.close()
        else:
            file = open(password_dir + "master.txt", "rb")
            if os.stat(password_dir + 'master.txt').st_size != 0:
                global master_password
                master_password = file.read()
                file.close()
            else:
                self.create_pass_popup = create_password()
                self.create_pass_popup.setFixedSize(width / 1.5, height / 2.5)
                self.create_pass_popup.setWindowTitle('Create Password')
                self.create_pass_popup.setWindowFlags(Qt.FramelessWindowHint)
                self.create_pass_popup.show()
                self.close
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





class create_password(QWidget):
    def __init__(self, parent=None):
        super(create_password, self).__init__(parent)
        self.check_if_file_exists()
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.width = width / 1.5
        self.height = height / 2.5
        self.setFixedSize(self.width, self.height)

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(self.title + ' - Create')
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setText('X')

        self.btn_min = ButtonGray(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        # self.lblInfo = QLabel(self)
        # self.lblInfo.setText('Hi')
        # self.lblInfo.move(7, 30)
        # self.lblInfo.resize(self.width - (7 * 2), 50)
        # LOGIN ITEMS START
        self.btnCreatePassword = ButtonGreen(self)
        self.btnCreatePassword.setText('Create')
        self.btnCreatePassword.move(7,self.height/1.3)
        self.btnCreatePassword.resize(self.width - (7 * 2), 30)
        self.btnCreatePassword.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnCreatePassword.setToolTip('Create Password.')
        self.btnCreatePassword.setFont(QFont('Calibri', 12))
        self.btnCreatePassword.clicked.connect(self.create_master_password)
        
        rx = QRegExp('[A-Za-z0-9@#$%^&+=]{8,}')
        validator = QRegExpValidator(rx, self)
        
        self.txtPassword = LineEdit(self)
        self.txtPassword.setValidator(validator)
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setToolTip('Your Password')
        self.txtPassword.move(7, self.height / 3)
        self.txtPassword.resize(self.width - (7 * 2), 30)
        self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        self.txtPassword.textChanged.connect(self.verify_text)
        
        self.txtPasswordConfirm = LineEdit(self)
        self.txtPasswordConfirm.setEchoMode(QLineEdit.Password)
        self.txtPasswordConfirm.setToolTip('Your Password')
        self.txtPasswordConfirm.move(7, self.height / 1.8)
        self.txtPasswordConfirm.resize(self.width - (7 * 2), 30)
        self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        self.txtPasswordConfirm.textChanged.connect(self.verify_text)
        self.verify_text()
        # self.create_master_password()
        # lOGIN ITEMS END
    def verify_text(self):
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', self.txtPassword.text()):
            self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        else:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
            if self.txtPasswordConfirm.text() == self.txtPassword.text():
                self.btnCreatePassword.setEnabled(True)
                self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
                self.btnCreatePassword.setStyleSheet("QPushButton:disabled{background-color: black;}")
            else:
                self.btnCreatePassword.setEnabled(False)
                self.btnCreatePassword.setStyleSheet("color: white; background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;")
                self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
            
    def create_master_password(self):
        global master_password
        if self.txtPasswordConfirm.text() == self.txtPassword.text():
            text = self.txtPasswordConfirm.text()
            text = text.encode('utf-8')
            new_pass = base64.urlsafe_b64encode(text)
            new_pass = new_pass.decode('utf-8')
            file = open(password_dir + "master.txt", "w")
            file.write(new_pass)
            file.close()
            file = open(password_dir + "master.txt", "rb")
            master_password = file.read()
            file.close()
        
    def check_if_file_exists(self):
        if not os.path.exists(password_dir):
            os.makedirs(password_dir)
            
        if not os.path.exists(password_dir + 'master.txt'):
            file = open(password_dir + "master.txt", "w")
            file.write('')
            file.close()
        else:
            file = open(password_dir + "master.txt", "rb")
            global master_password
            master_password = file.read()
            file.close()
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
class ButtonRed(QToolButton):
    def __init__(self, parent=None):
        super(ButtonRed, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #9f0000; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;")
class ButtonGreen(QToolButton):
    def __init__(self, parent=None):
        super(ButtonGreen, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet('QPushButton:disabled{background-color: white;}')
        self.setStyleSheet("color: white; background-color: #109f00; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet('QPushButton:disabled{background-color: white;}')
        self.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black; QPushButton:disabled{background-color: white;}")
class ButtonGray(QToolButton):
    def __init__(self, parent=None):
        super(ButtonGray, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #565656; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
class ButtonBlue(QToolButton):
    def __init__(self, parent=None):
        super(ButtonBlue, self).__init__(parent)
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
    login.setStyleSheet("""
                            QMainWindow
                            {
                                border: 2px solid #121212; 
                                border-radius: 1px;
                            }QDialog
                            {
                                border: 2px solid #121212; 
                                border-radius: 1px;
                            }QWidget
                            {
                                border: 2px solid #121212; 
                                border-radius: 1px;
                            }
                            QPushButton:disabled {
                                background-color: #dddddd;
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
