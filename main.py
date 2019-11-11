# pip install pyqt5
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtTest
from PyQt5 import *
from functools import partial

from cryptography.fernet import Fernet
import base64

title = '  JPM'
version = 'v0.1'
width = 300
height = 400
btn_size = 25

import getpass, tempfile, os, json, re, pyperclip, csv, subprocess
username = getpass.getuser()
password_dir = tempfile.gettempdir() + '/JMP/'
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
master_password = ''
usernames = []
passwords = []
keys = []
site_names = []
passwords_json = []
class MainMenu(QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.resized_bool = False
        self.last_pos_x = 0
        self.last_pos_w= 0
        self.last_size_h = 0
        self.last_size_w= 0
        self.sizeObject = QDesktopWidget().screenGeometry(-1)
        self.title = title + ' ' + version
        self.width = width + 200
        self.height = height
        self.num_of_lower_buttons = 3

        self.setMinimumSize(self.width, self.height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        app.setStyle("Fusion")
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
        app.setPalette(palette)
        self.setStyleSheet("""QMainWindow{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(self.title)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setStyleSheet("text-align:left; background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")
        # self.menuBarTitle.clicked.connect(self.on_click)
        # self.menuBarTitle.doubleClicked.connect(self.on_doubleclick)


        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.close)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setIcon(QIcon('icons/exit.png'))

        self.btn_max = ButtonGreen(self)
        self.btn_max.clicked.connect(self.max)
        self.btn_max.resize(btn_size + 10, btn_size)
        self.btn_max.setStyleSheet("background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_max.setFont(QFont('Calibri', 20))
        self.btn_max.setToolTip('Maximize.')
        self.btn_max.setIcon(QIcon('icons/max.png'))

        self.btn_min = ButtonYellow(self)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("color: black; background-color: #e6cc1a; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')

        self.txtSearch = LineEdit(self)
        self.txtSearch.move(7, 30)
        self.txtSearch.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        self.txtSearch.textChanged.connect(self.refresh_password_list)
        self.txtSearch.setToolTip('Search for password with the name of the website.')
        self.txtSearch.setText('')

        self.btnRefresh = ButtonGreen(self)
        self.btnRefresh.setToolTip('Refresh Passwords.')
        self.btnRefresh.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnRefresh.setIcon(QIcon('icons/refresh.png'))
        self.btnRefresh.resize(30,30)
        self.btnRefresh.clicked.connect(self.refresh_password_list)
        # global passwords, site_names
        # passwords = ['password', 'abc123', 'dragon', 'test', 'test2', 'test', 'test2','password', 'abc123', 'dragon', 'test', 'test2', 'test', 'test2']
        # site_names = ['google', 'microsoft', 'sdasad', 'test', 'test2', 'test', 'test2','google', 'microsoft', 'facebook', 'test', 'test2', 'test', 'test2']

        self.sizegrip = QSizeGrip(self)
        self.btnLogout = ButtonRed(self)
        self.btnLogout.setText('Logout')
        self.btnLogout.resize(100, 30)
        self.btnLogout.setStyleSheet("color: white; background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnLogout.clicked.connect(self.logout)
        self.btnLogout.setToolTip('Go to Login screen.')

        self.btnAdd = ButtonGreen(self)
        self.btnAdd.setText('Add Password')
        self.btnAdd.resize(100, 30)
        self.btnAdd.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnAdd.clicked.connect(self.add_password)
        self.btnAdd.setToolTip('Add a password.')

        self.btnExport = ButtonGreen(self)
        self.btnExport.setText('Export')
        self.btnExport.resize(100, 30)
        self.btnExport.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnExport.clicked.connect(self.export_passwords)
        self.btnExport.setToolTip('Export all files into a .csv file to view in excel.')

        self.scroll = QScrollArea(self)

        self.sizegrip.setStyleSheet('''QSizeGrip {
            image: url("icons/exit.png");
            //background-color: white;
        }''')
        self.sizegrip.setCursor(QtCore.Qt.SplitVCursor)
        self.resized.connect(self.someFunction)
        self.refresh_password_list()
    def updateUI(self):
        mainWindow = QWidget()
        w = self.geometry().width()
        h = self.geometry().height()
        self.height = h
        self.width = w
        # print(str(self.w) + ' x ' + str(self.h))
        # self.resize(200, 200)

        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_max.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.move(self.width - (btn_size + btn_size + btn_size + 30),0)
        self.txtSearch.resize(self.width - (7 * 2) - 35, 30)
        self.btnRefresh.move(self.width - (7 * 2) - 25, 30)

        self.btnAdd.resize(self.width / self.num_of_lower_buttons - 10, 30)
        self.btnAdd.move(5, self.height - 35)

        self.btnLogout.resize(self.width / self.num_of_lower_buttons, 30)
        self.btnLogout.move(self.width / (self.num_of_lower_buttons / self.num_of_lower_buttons) - (self.width / self.num_of_lower_buttons) - 5, self.height - 35)

        self.btnExport.resize(self.width / self.num_of_lower_buttons, 30)
        self.btnExport.move(self.width / self.num_of_lower_buttons - 5, self.height - 35)

        self.scroll.resize(self.width - (7 * 2), self.height - 110)
        self.sizegrip.move(self.width - 10, self.height - 10)

    @pyqtSlot()
    def on_click(self):
        print("Click")

    @pyqtSlot()
    def on_doubleclick(self):
        self.max()
    def resizeEvent(self, event):
        self.resized.emit()
        return super(MainMenu, self).resizeEvent(event)
    def max(self):
        if not self.resized_bool:
            self.last_pos_x = self.pos().x()
            self.last_pos_y = self.pos().y()
            self.last_size_h =  self.geometry().height()
            self.last_size_w = self.geometry().width()
            screen = app.primaryScreen()
            rect = screen.availableGeometry()
            self.setGeometry(0, 0, rect.width(), rect.height())
            self.resized_bool = True
        elif self.resized_bool:
            screen = app.primaryScreen()
            rect = screen.availableGeometry()
            self.setGeometry(self.last_pos_x, self.last_pos_y, self.last_size_w, self.last_size_h)
            self.resized_bool = False
        self.updateUI()
    def someFunction(self):
        self.updateUI()

    def export_passwords(self):
        options = QFileDialog.Options()
        # options.setAcceptMode(QFileDialog.AcceptSave)
        # options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Export","Passwords","Excell File (*.csv)", options=options)
        if fileName:
            if fileName.endswith('.csv'):
                fileName = fileName.replace('.csv','')
            with open(password_dir + 'passwords.json') as file:
                x = json.load(file)

            passwords_list = []
            for i, j in enumerate(site_names):
                f = Fernet( keys[i].encode('utf-8'))
                p = passwords[i].encode('utf-8')
                decrypted_password = f.decrypt(p)
                decrypted_password = base64.urlsafe_b64decode(decrypted_password)
                decrypted_password = decrypted_password.decode('utf-8')
                passwords_list.append(decrypted_password)
            with open(fileName + ".csv", "w") as file:
                csv_file = csv.writer(file)
                csv_file.writerow(['Site name', 'Username', 'Password'])
                for i, j in enumerate(x):
                    csv_file.writerow([site_names[i], usernames[i], passwords_list[i]])
            # fileName = fileName.rsplit('/', 1)[0]
            explore(fileName + '.csv')
    def refresh_password_list(self):
        # scroll = QScrollArea(self)
        self.scroll.setStyleSheet("QScrollArea {background-color:white;}");
        self.scroll.move(7, 70)
        self.scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.scroll.setWidget(self.content)
        lay = QGridLayout(self.content)
        self.content.setStyleSheet('background-color: #181818;')
        # lay.setColumnStretch(0, 1)
        y = 0
        self.lblName = QLabel(self)
        self.lblName.setText('Name:')
        self.lblName.setAlignment(Qt.AlignLeft)
        self.lblName.setFont(QFont('Calibri', 14))
        self.lblName.setStyleSheet("color: #008a11;")
        lay.addWidget((self.lblName), 0, 0)

        self.lblPassword = QLabel(self)
        self.lblPassword.setText('Username:')
        self.lblPassword.setAlignment(Qt.AlignLeft)
        self.lblPassword.setFont(QFont('Calibri', 14))
        self.lblPassword.setStyleSheet("color: #e0d725;")
        lay.addWidget((self.lblPassword), 0, 1)

        self.lblPassword = QLabel(self)
        self.lblPassword.setText('Passwords:')
        self.lblPassword.setAlignment(Qt.AlignLeft)
        self.lblPassword.setFont(QFont('Calibri', 14))
        self.lblPassword.setStyleSheet("color: #144a85;")
        lay.addWidget((self.lblPassword), 0, 2)
        if not site_names:
            self.lblError = QLabel(self)
            self.lblError.setText('No passwords added.')
            self.lblError.setAlignment(Qt.AlignLeft)
            self.lblError.setFont(QFont('Calibri', 14))
            self.lblError.setStyleSheet("color: #8b0000;")
            lay.addWidget((self.lblError), 1, 1)
        for i, j in enumerate(site_names):
            if self.txtSearch.text() == '' or self.txtSearch.text() == ' ' or self.txtSearch.text() == None:
                f = Fernet( keys[i].encode('utf-8'))
                p = passwords[i].encode('utf-8')

                decrypted_password = f.decrypt(p)
                decrypted_password = base64.urlsafe_b64decode(decrypted_password)
                decrypted_password = decrypted_password.decode('utf-8')
                y += 1

                self.txtWebsite = QLineEdit(self)
                self.txtWebsite.setReadOnly(True)
                self.txtWebsite.setStyleSheet("background-color :#202020; text-align: left; color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
                self.txtWebsite.setFont(QFont('Calibri', 11))
                self.txtWebsite.setToolTip('{}'.format(j))
                self.txtWebsite.setText(j)
                lay.addWidget((self.txtWebsite), y, 0)
                # LABEL END
                # TEXT START

                self.txtUsername = QLineEdit(self)
                self.txtUsername.setReadOnly(True)
                self.txtUsername.setStyleSheet("background-color :#202020; text-align: left; color: #e0d725;border-radius: 3px;border-style: none; border: 1px solid rgb(170,136,0);")
                self.txtUsername.setFont(QFont('Calibri', 11))
                self.txtUsername.setToolTip('{}'.format(usernames[i]))
                self.txtUsername.setText(usernames[i])
                lay.addWidget((self.txtUsername), y, 1)

                self.txtPassword = QLineEdit(self)
                self.txtPassword.setReadOnly(True)
                self.txtPassword.setStyleSheet("background-color :#202020; text-align: left; color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
                self.txtPassword.setFont(QFont('Calibri', 11))
                self.txtPassword.setEchoMode(QLineEdit.Password)
                self.txtPassword.setToolTip('{}'.format(decrypted_password))
                self.txtPassword.setText(decrypted_password)
                lay.addWidget((self.txtPassword), y, 2)
                # BUTTON EDIT START
                btnCopy = partial(self.copy_password, self.txtPassword.text())
                self.btnCopy = ButtonGreen(self)
                self.btnCopy.setIcon(QIcon('icons/copy.png'))
                self.btnCopy.resize(30,30)
                self.btnCopy.setStyleSheet("text-align: center;background-color: #008a11; border-radius: 3px;  border-style: none; border: 1px solid black;")
                self.btnCopy.setToolTip('Copy "{}"'.format(self.txtPassword.text()))
                self.btnCopy.clicked.connect(btnCopy)
                lay.addWidget((self.btnCopy), y, 3)

                btnEdit = partial(self.edit_password, self.txtUsername.text(), self.txtWebsite.text(), self.txtPassword.text())
                self.btnEdit = ButtonBlue(self)
                self.btnEdit.setIcon(QIcon('icons/edit.png'))
                self.btnEdit.resize(30,30)
                self.btnEdit.setStyleSheet("text-align: center;background-color: #144a85; border-radius: 3px;  border-style: none; border: 1px solid black;")
                self.btnEdit.setToolTip('Edit "{}"'.format(self.txtWebsite.text()))
                self.btnEdit.clicked.connect(btnEdit)
                lay.addWidget((self.btnEdit), y, 4)
                # BUTTON EDIT END
                # BUTTON DELETE START
                btnDelete = partial(self.delete_password, self.txtWebsite.text())
                self.btnDelete = ButtonRed(self)
                self.btnDelete.setIcon(QIcon('icons/delete.png'))
                self.btnDelete.resize(30,30)
                self.btnDelete.setStyleSheet("text-align: center;background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
                self.btnDelete.setToolTip('Delete "{}"'.format(self.txtWebsite.text()))
                self.btnDelete.clicked.connect(btnDelete)
                lay.addWidget((self.btnDelete), y, 5)
                # BUTTON DELETE END
            elif self.txtSearch.text() in str(site_names[i]):
                f = Fernet( keys[i].encode('utf-8'))
                p = passwords[i].encode('utf-8')

                decrypted_password = f.decrypt(p)
                decrypted_password = base64.urlsafe_b64decode(decrypted_password)
                decrypted_password = decrypted_password.decode('utf-8')
                y += 1

                self.txtWebsite = QLineEdit(self)
                self.txtWebsite.setReadOnly(True)
                self.txtWebsite.setStyleSheet("background-color :#202020; text-align: left; color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
                self.txtWebsite.setFont(QFont('Calibri', 11))
                self.txtWebsite.setToolTip('{}'.format(j))
                self.txtWebsite.setText(j)
                lay.addWidget((self.txtWebsite), y, 0)
                # LABEL END
                # TEXT START

                self.txtUsername = QLineEdit(self)
                self.txtUsername.setReadOnly(True)
                self.txtUsername.setStyleSheet("background-color :#202020; text-align: left; color: #e0d725;border-radius: 3px;border-style: none; border: 1px solid rgb(170,136,0);")
                self.txtUsername.setFont(QFont('Calibri', 11))
                self.txtUsername.setToolTip('{}'.format(usernames[i]))
                self.txtUsername.setText(usernames[i])
                lay.addWidget((self.txtUsername), y, 1)

                self.txtPassword = QLineEdit(self)
                self.txtPassword.setReadOnly(True)
                self.txtPassword.setStyleSheet("background-color :#202020; text-align: left; color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
                self.txtPassword.setFont(QFont('Calibri', 11))
                self.txtPassword.setEchoMode(QLineEdit.Password)
                self.txtPassword.setToolTip('{}'.format(decrypted_password))
                self.txtPassword.setText(decrypted_password)
                lay.addWidget((self.txtPassword), y, 2)

                # BUTTON EDIT START
                btnCopy = partial(self.copy_password, self.txtPassword.text())
                self.btnCopy = ButtonGreen(self)
                self.btnCopy.setIcon(QIcon('icons/copy.png'))
                self.btnCopy.resize(30,30)
                self.btnCopy.setStyleSheet("text-align: center;background-color: #008a11; border-radius: 3px;  border-style: none; border: 1px solid black;")
                self.btnCopy.setToolTip('Copy "{}"'.format(self.txtPassword.text()))
                self.btnCopy.clicked.connect(btnCopy)
                lay.addWidget((self.btnCopy), y, 3)

                btnEdit = partial(self.edit_password, self.txtUsername.text(), self.txtWebsite.text(), self.txtPassword.text())
                self.btnEdit = ButtonBlue(self)
                self.btnEdit.setIcon(QIcon('icons/edit.png'))
                self.btnEdit.resize(30,30)
                self.btnEdit.setStyleSheet("text-align: center;background-color: #144a85; border-radius: 3px;  border-style: none; border: 1px solid black;")
                self.btnEdit.setToolTip('Edit "{}"'.format(self.txtWebsite.text()))
                self.btnEdit.clicked.connect(btnEdit)
                lay.addWidget((self.btnEdit), y, 4)
                # BUTTON EDIT END
                # BUTTON DELETE START
                btnDelete = partial(self.delete_password, self.txtWebsite.text())
                self.btnDelete = ButtonRed(self)
                self.btnDelete.setIcon(QIcon('icons/exit.png'))
                self.btnDelete.resize(30,30)
                self.btnDelete.setStyleSheet("text-align: center;background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
                self.btnDelete.setToolTip('Delete "{}"'.format(self.txtWebsite.text()))
                self.btnDelete.clicked.connect(btnDelete)
                lay.addWidget((self.btnDelete), y, 5)
                # BUTTON DELETE END
        self.layout().addWidget(self.scroll)
        self.scroll.setStyleSheet("QScrollArea{background-color: #131313; border-radius: 3px;border-style: none; border: 1px solid black;}")
        # lay.setStyleSheet("QGridLayout{border-radius: 3px;border-style: none; border: 1px solid darkblue;}")

    def edit_password(self, u, w, p):
        self.addPopup = add_passwords(u,w,p, True)
        self.addPopup.show()
    def delete_password(self, name):
        with open(password_dir + 'passwords.json') as file:
            passwords_json = json.load(file)

        # DELETE ELEMENT START
        for i in range(len(passwords_json)):
            if(passwords_json[i]["site name"] == [name]):
                passwords_json.pop(i)
                break
        open(password_dir + 'passwords.json', "w").write(
            json.dumps(passwords_json, sort_keys=True, indent=4, separators=(',', ': '))
            )
        # DELETE ELEMENT END
        with open(password_dir + 'passwords.json') as file:
            passwords_json = json.load(file)
            usernames.clear()
            passwords.clear()
            keys.clear()
            site_names.clear()
            for info in passwords_json:
                for username in info['username']:
                    usernames.append(username)
                for password in info['password']:
                    passwords.append(password)
                for key in info['key']:
                    keys.append(key)
                for site in info['site name']:
                    site_names.append(site)

        self.m = MsgBox('Password Deleted!', 'Success!', False)
        self.m.show()
        self.refresh_password_list()
    def add_password(self):
        self.addPopup = add_passwords('','','', False)
        self.addPopup.show()
    def logout(self):
        self.close()
        self.login = Login()
        self.login.setWindowTitle('Login')
        self.login.show()
    def copy_password(self,b):
        pyperclip.copy(b)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.updateUI()


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
        try:
            delta = QPoint (event.globalPos() - self.oldPos)
            # print(delta)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            print('oh no')
    # MOVE WINDOW END


class add_passwords(QDialog):
    def __init__(self, u, w, p, delete_password, parent=None):
        super(add_passwords, self).__init__(parent)
        self.name = w
        self.delete = delete_password
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""QDialog{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")
        self.width = width / 1.5
        self.height = height / 1.7
        self.setFixedSize(self.width, self.height)

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        if self.delete:
            self.menuBarTitle.setText(self.title + ' - Change')
        else:
            self.menuBarTitle.setText(self.title + ' - Add')

        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.close)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setIcon(QIcon('icons/exit.png'))

        self.btn_min = ButtonYellow(self)
        self.btn_min.clicked.connect(self.showMinimized)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("color: black; background-color: #e6cc1a; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        self.lblInfo = QLabel(self)
        self.lblInfo.setText('Password:')
        self.lblInfo.move(7, 145)

        self.lblInfo = QLabel(self)
        self.lblInfo.setText('Website:')
        self.lblInfo.move(7, 45)

        self.lblInfo = QLabel(self)
        self.lblInfo.setText('Username:')
        self.lblInfo.move(7, 95)
        # self.lblInfo.resize(self.width - (7 * 2), 50)
        # ADD ITEMS START
        self.btnAdd = ButtonGreen(self)
        self.btnAdd.move(7, 200)
        self.btnAdd.resize(self.width - (7 * 2), 30)
        self.btnAdd.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        if self.delete:
            self.btnAdd.setText('Change')
            self.btnAdd.setToolTip('Change Password.')
        else:
            self.btnAdd.setText('Add')
            self.btnAdd.setToolTip('Add Password.')

        self.btnAdd.setFont(QFont('Calibri', 12))
        self.btnAdd.clicked.connect(self.add)

        self.txtWebsite = LineEdit(self)
        self.txtWebsite.move(7, 60)
        self.txtWebsite.resize(self.width - (7 * 2), 30)
        self.txtWebsite.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        self.txtWebsite.setText(w)
        self.txtWebsite.setToolTip('Your Website')
        self.txtWebsite.setFocus()
        self.txtWebsite.textChanged.connect(self.verify_text)

        self.txtUsername = LineEdit(self)
        self.txtUsername.move(7, 110)
        self.txtUsername.resize(self.width - (7 * 2), 30)
        self.txtUsername.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        self.txtUsername.setText(u)
        self.txtUsername.setToolTip('Your Username')
        self.txtUsername.textChanged.connect(self.verify_text)


        self.txtPassword = LineEdit(self)
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.move(7, 160)
        self.txtPassword.resize(self.width - (7 * 2), 30)
        self.txtPassword.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        self.txtPassword.setText(p)
        self.txtPassword.textChanged.connect(self.verify_text)

        # ADD ITEMS END
        self.verify_text()

    def add(self):
        global passwords_json, passwords, keys, site_names, usernames

        if self.delete:
            with open(password_dir + 'passwords.json') as file:
                passwords_json = json.load(file)

            # DELETE ELEMENT START
            for i in range(len(passwords_json)):
                if(passwords_json[i]["site name"] == [self.name]):
                    passwords_json.pop(i)
                    break
            open(password_dir + 'passwords.json', "w").write(
                json.dumps(passwords_json, sort_keys=True, indent=4, separators=(',', ': '))
                )
            # DELETE ELEMENT END
            with open(password_dir + 'passwords.json') as file:
                passwords_json = json.load(file)
                usernames.clear()
                passwords.clear()
                keys.clear()
                site_names.clear()
                for info in passwords_json:
                    for username in info['username']:
                        usernames.append(username)
                    for password in info['password']:
                        passwords.append(password)
                    for key in info['key']:
                        keys.append(key)
                    for site in info['site name']:
                        site_names.append(site)


            self.btnAdd.setText('Add')
            self.btnAdd.setToolTip('Add Password.')
            self.menuBarTitle.setText(self.title + ' - Add')


        for x, j in enumerate(site_names):
            if self.txtWebsite.text() in j:
                self.m = MsgBox('"{}" already exists, Choose\na diffrent website name!'.format(self.txtWebsite.text()), 'Oh oh!', False)
                self.m.show()
                return
        # print(passwords_json)
        temp_password = self.txtPassword.text()
        temp_password = temp_password.encode('utf-8')
        temp_password = base64.urlsafe_b64encode(temp_password)
        temp_key = Fernet.generate_key()
        f = Fernet(temp_key)
        temp_key = temp_key.decode('utf8')
        encrypted = f.encrypt(temp_password)
        # print(f.decrypt(encrypted))
        encrypted = encrypted.decode('utf8')
        passwords_json.append({
            'username': [self.txtUsername.text()],
            'site name': [self.txtWebsite.text()],
            'key': [temp_key],
            'password': [encrypted]
            }
        )
        # sort json file
        sorted_obj = sorted(passwords_json, key=lambda x : x['site name'], reverse=False)
        # Write to passwords file
        with open(password_dir + 'passwords.json', mode='w+', encoding='utf-8') as file:
            json.dump(sorted_obj, file, ensure_ascii=True, indent=4, sort_keys=True)

        # update added passwords
        with open(password_dir + 'passwords.json') as file:
            passwords_json = json.load(file)
            usernames.clear()
            passwords.clear()
            keys.clear()
            site_names.clear()
            for info in passwords_json:
                for username in info['username']:
                    usernames.append(username)
                for password in info['password']:
                    passwords.append(password)
                for key in info['key']:
                    keys.append(key)
                for site in info['site name']:
                    site_names.append(site)


        if self.delete:
            self.m = MsgBox('Password Changed!', 'Success!', False)
            self.m.show()
            self.delete = False
            # self.close()
        else:
            self.m = MsgBox('Password Added!', 'Success!', False)
            self.m.show()
    def write_key(self):
        key = Fernet.generate_key()
        return key
    def load_key(self):
        return open(password_dir + "key.key", "rb").read()

    def verify_text(self):
        x = list(self.txtPassword.text())
        y = list(self.txtWebsite.text())
        z = list(self.txtUsername.text())
        self.txtPassword.setToolTip(self.txtPassword.text())
        # if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', self.txtPassword.text()):

        if len(x) > 0:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
        else:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")

        if len(y) > 0:
            self.txtWebsite.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
        else:
            self.txtWebsite.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")

        if len(z) > 0:
            self.txtUsername.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
        else:
            self.txtUsername.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")

        if len(x) > 0 and len(y) > 0 and len(z) > 0:
            self.btnAdd.setEnabled(True)
            self.btnAdd.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        else:
            self.btnAdd.setEnabled(False)
            self.btnAdd.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")

    def keyPressEvent(self, event):
        x = list(self.txtPassword.text())
        y = list(self.txtWebsite.text())
        z = list(self.txtUsername.text())
        if event.key() == Qt.Key_Return:
            if len(x) >= 0 and len(y) >= 0 and  len(y) > 0:
                self.add()
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
        try:
            delta = QPoint (event.globalPos() - self.oldPos)
            #print(delta)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            print('oh no')
    # MOVE WINDOW END



class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""QDialog{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")
        self.width = width / 1.5
        self.height = height / 2.5
        self.setFixedSize(self.width, self.height)

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(self.title + ' - Login')
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setIcon(QIcon('icons/exit.png'))

        self.btn_min = ButtonYellow(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("color: black; background-color: #e6cc1a; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        self.lblInfo = QLabel(self)
        self.lblInfo.setText('Password:')
        self.lblInfo.move(7, 60)
        # self.lblInfo.resize(self.width - (7 * 2), 50)
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
        # self.txtPassword.setText('Password')
        self.txtPassword.setToolTip('Your Password')
        self.txtPassword.move(7, self.height / 2)
        self.txtPassword.resize(self.width - (7 * 2), 30)
        self.txtPassword.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        self.txtPassword.textChanged.connect(self.verify_text)
        self.get_password()
        self.txtPassword.setFocus()
        # lOGIN ITEMS END

    def verify_text(self):
        x = list(self.txtPassword.text())
        if len(x) > 0:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.login()

    def login(self):
        temp = self.txtPassword.text()
        key = load_key()
        f = Fernet(key)
        # master_password = master_password.decode('utf-8')
        decrypted_encrypted = f.decrypt(master_password)
        temp_master = base64.urlsafe_b64decode(decrypted_encrypted)
        temp_master = temp_master.decode('utf-8')

        if temp == temp_master:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
            QtTest.QTest.qWait(1000)
            self.main = MainMenu()
            self.main.setWindowTitle('Main')
            # self.main.setFixedSize(width, height)
            # self.main.setWindowFlags(Qt.FramelessWindowHint)
            self.main.show()
            self.close()
        else:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")

    def get_password(self):
        file = open(password_dir + "master.key", "rb")
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




class MsgBox(QDialog):
    def __init__(self, message, msgtitle, show_login, parent=None):
        super(MsgBox, self).__init__(parent)
        self.show_login = show_login
        self.title = msgtitle
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.width = width / 1.5
        self.height = height / 4.5
        self.setFixedSize(self.width, self.height)

        self.setStyleSheet("""QDialog{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")
        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText('  ' + self.title)
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_proceed)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setIcon(QIcon('icons/exit.png'))

        self.btn_min = ButtonYellow(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("color: black; background-color: #e6cc1a; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')


        self.lblMessage = QLabel(self)
        self.lblMessage.setText(message)
        self.lblMessage.move(7, 30)

        self.btnOk = ButtonGreen(self)
        self.btnOk.setText('Ok')
        if self.show_login:
            self.btnOk.clicked.connect(self.btn_proceed)
        else:
            self.btnOk.clicked.connect(self.close)
        self.btnOk.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnOk.move(5,  60)
        self.btnOk.resize(self.width - 10, btn_size)

    def btn_proceed(self):
        self.login_popup = Login()
        self.login_popup.setFixedSize(width / 1.5, height / 2.5)
        self.login_popup.setWindowTitle('Login')
        self.login_popup.setWindowFlags(Qt.FramelessWindowHint)
        self.login_popup.show()
        self.close()
    def btn_min_clicked(self):
        self.showMinimized()
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.show_login:
                self.login_popup = Login()
                self.login_popup.setFixedSize(width / 1.5, height / 2.5)
                self.login_popup.setWindowTitle('Login')
                self.login_popup.setWindowFlags(Qt.FramelessWindowHint)
                self.login_popup.show()
                self.close()
            else:
                self.close()
    # MOVE WINDOW END
class create_password(QDialog):
    def __init__(self, parent=None):
        super(create_password, self).__init__(parent)
        self.check_if_file_exists()
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.width = width / 1.5
        self.height = height / 2.5
        self.setFixedSize(self.width, self.height)

        self.setStyleSheet("""QDialog{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")
        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText('  Create a Password')
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 8))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setIcon(QIcon('icons/exit.png'))

        self.btn_min = ButtonYellow(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("color: black; background-color: #e6cc1a; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        # self.lblInfo = QLabel(self)
        # self.lblInfo.setText('Create a Password')
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
        # self.txtPassword.setValidator(validator)
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setToolTip('Create a Password')
        self.txtPassword.move(7, self.height / 3)
        self.txtPassword.resize(self.width - (7 * 2), 30)
        self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        self.txtPassword.textChanged.connect(self.verify_text)

        self.txtPasswordConfirm = LineEdit(self)
        self.txtPasswordConfirm.setEchoMode(QLineEdit.Password)
        self.txtPasswordConfirm.setToolTip('Confirm Your Password')
        self.txtPasswordConfirm.move(7, self.height / 1.8)
        self.txtPasswordConfirm.resize(self.width - (7 * 2), 30)
        self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        self.txtPasswordConfirm.textChanged.connect(self.verify_text)
        self.verify_text()
        # self.create_master_password()
        # lOGIN ITEMS END

    def verify_text(self):
        x = list(self.txtPassword.text())
        y = list(self.txtPasswordConfirm.text())
        # if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', self.txtPassword.text()):

        if len(x) < 8:
            self.menuBarTitle.setText('  Create a Password')
            self.btnCreatePassword.setEnabled(False)
            self.btnCreatePassword.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
            self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
            self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        elif len(x) >= 8:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
            self.menuBarTitle.setText('  Confirm Password')
            if self.txtPasswordConfirm.text() == self.txtPassword.text():
                self.menuBarTitle.setText('  Save Password')
                self.btnCreatePassword.setEnabled(True)
                self.btnCreatePassword.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
                self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
            else:
                if len(y) >= 1:
                    self.menuBarTitle.setText('  Password Doesn\'t Match')
                self.btnCreatePassword.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
                self.btnCreatePassword.setEnabled(False)
                self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")

    def keyPressEvent(self, event):
        x = list(self.txtPassword.text())
        y = list(self.txtPasswordConfirm.text())
        if event.key() == Qt.Key_Return:
            if len(x) >= 8 and len(y) >= 1 and  self.txtPasswordConfirm.text() == self.txtPassword.text() and self.btnCreatePassword.isEnabled():
                self.create_master_password()

    def create_master_password(self):
        global master_password
        if self.txtPasswordConfirm.text() == self.txtPassword.text():
            text = self.txtPasswordConfirm.text()
            text = text.encode('utf-8')
            new_pass = base64.urlsafe_b64encode(text)
            write_key()
            key = load_key()
            f = Fernet(key)
            encrypted = f.encrypt(new_pass)
            file = open(password_dir + "master.key", "wb")
            file.write(encrypted)
            file.close()
            file = open(password_dir + "master.key", "rb")
            master_password = file.read()
            file.close()
            # buttonReply = QMessageBox.information(self, 'Notice', "Password Saved!\nDo not forget this password!", QMessageBox.Ok, QMessageBox.Ok)
            self.m = MsgBox('Password Saved!\nDo not forget this password!', 'Notice!', True)
            self.m.show()

            self.close()

    def check_if_file_exists(self):
        if not os.path.exists(password_dir):
            os.makedirs(password_dir)

        if not os.path.exists(password_dir + 'key.key'):
            file = open(password_dir + "key.key", "wb")
            file.write('')
            file.close()
        else:
            file = open(password_dir + "key.key", "rb")
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
        self.setStyleSheet("QToolTip {color: white; background-color: #9f0000; border-radius: 3px; border-style: none;  border: 1.4px solid black;}QToolButton{color: white; background-color: #9f0000; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;} QToolButton:pressed {background-color: #4f0000; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;}")

    def leaveEvent(self,event):
        self.setStyleSheet("QToolButton{color: white; background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;}")
class ButtonGreen(QToolButton):
    def __init__(self, parent=None):
        super(ButtonGreen, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        if self.isEnabled():
            self.setStyleSheet("QToolTip {color: white; background-color: #109f00; border-radius: 3px; border-style: none;  border: 1.4px solid black;}QToolButton{color: white; background-color: #109f00; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;} QToolButton:pressed {background-color: #106f00; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;}")
        else:
            self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")

    def leaveEvent(self,event):
        if self.isEnabled():
            self.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        else:
            self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
class ButtonGray(QToolButton):
    def __init__(self, parent=None):
        super(ButtonGray, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("QToolTip {color: white; background-color: #565656; border-radius: 3px; border-style: none;  border: 1.4px solid black;}QToolButton{color: white; background-color: #565656; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;} QToolButton:pressed {background-color: #333333; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;}")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
class ButtonBlue(QToolButton):
    def __init__(self, parent=None):
        super(ButtonBlue, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("QToolTip {color: white; background-color: #143c85; border-radius: 3px; border-style: none;  border: 1.4px solid black;}QToolButton{color: white; background-color: #143c85; border-radius: 3px; border-style: none; border: 1.4px solid black;}  QToolButton:pressed {background-color: #142c85; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;}")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #144a85; border-radius: 3px; border-style: none; border: 1px solid black;")

class ButtonYellow(QToolButton):
    def __init__(self, parent=None):
        super(ButtonYellow, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("QToolTip {color: black; background-color: #c9cd27; border-radius: 3px; border-style: none;  border: 1.4px solid black;}QToolButton{color: black; background-color: #c9cd27; border-radius: 3px; border-style: none; border: 1.4px solid black;}  QToolButton:pressed {color: black; background-color: #dad503; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;}")

    def leaveEvent(self,event):
        self.setStyleSheet("color: black; background-color: #e6cc1a; border-radius: 3px; border-style: none; border: 1px solid black;")
class QDoublePushButton(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)
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

def write_key():
    key = Fernet.generate_key()
    with open(password_dir +"key.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    return open(password_dir + "key.key", "rb").read()

def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)
    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # m = MainMenu()
    # m.show()
    if not os.path.exists(password_dir):
            os.makedirs(password_dir)
    if os.path.exists(password_dir + 'passwords.json'):
        with open(password_dir + 'passwords.json') as file:
            passwords_json = json.load(file)
            for info in passwords_json:
                for username in info['username']:
                    usernames.append(username)
                for password in info['password']:
                    passwords.append(password)
                for key in info['key']:
                    keys.append(key)
                for site in info['site name']:
                    site_names.append(site)

    elif not os.path.exists(password_dir + 'password.json'):
        file = open(password_dir + "passwords.json", "w+")
        file.write("[]")
        file.close()
        with open(password_dir + 'passwords.json') as file:
            passwords_json = json.load(file)
    if not os.path.exists(password_dir + 'key.key'):
        file = open(password_dir + "key.key", "w")
        file.write('')
        file.close()
        create_pass_popup = create_password()
        create_pass_popup.setFixedSize(width / 1.5, height / 2.5)
        create_pass_popup.setWindowTitle('Create Password')
        create_pass_popup.setWindowFlags(Qt.FramelessWindowHint)
        create_pass_popup.show()
    else:
        if os.stat(password_dir + 'key.key').st_size != 0:
            login = Login()
            login.setWindowTitle('Login')
            login.show()
        else:
            create_pass_popup = create_password()
            create_pass_popup.setFixedSize(width / 1.5, height / 2.5)
            create_pass_popup.setWindowTitle('Create Password')
            create_pass_popup.setWindowFlags(Qt.FramelessWindowHint)
            create_pass_popup.show()

    if not os.path.exists(password_dir + 'master.key'):
        file = open(password_dir + "master.key", "w")
        file.write('')
        file.close()
        create_pass_popup = create_password()
        create_pass_popup.setFixedSize(width / 1.5, height / 2.5)
        create_pass_popup.setWindowTitle('Create Password')
        create_pass_popup.setWindowFlags(Qt.FramelessWindowHint)
        create_pass_popup.show()
    else:
        file = open(password_dir + "master.key", "rb")
        master_password = file.read()
        file.close()
    sys.exit(app.exec_())
