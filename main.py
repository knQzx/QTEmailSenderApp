# importing the required libraries

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
import sys
from yandex_send_message_email import yandex_send_message_email
import asyncio
from getEmailOrTextFromFile import DataParser
from is_valid_mail import Is_Valid_Mail


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("QT Email Sender")

        # setting the fixed width of window
        self.setFixedSize(650, 650)

        # login
        self.loginQLabel = QLabel(self)
        self.loginQLabel.setText('Email:')
        self.loginQLineEdit = QLineEdit(self)

        self.loginQLineEdit.move(80, 20)
        self.loginQLineEdit.resize(200, 32)
        self.loginQLabel.move(20, 20)

        # password
        self.passwordQLabel = QLabel(self)
        self.passwordQLabel.setText('Password:')
        self.passwordQLineEdit = QLineEdit(self)

        self.passwordQLineEdit.move(380, 20)
        self.passwordQLineEdit.resize(200, 32)
        self.passwordQLabel.move(300, 20)


        self.pybutton = QPushButton('Connect', self)
        self.pybutton.resize(300, 30)
        self.pybutton.move(650 // 4, 70)
        self.pybutton.clicked.connect(self.connection_)
        self.pybutton.setStyleSheet("QPushButton {background-color : grey; border: 1px solid black; border-radius: 10px; }")

        # EMAIL ADDRESSES GET

        # first variant to get their emails
        self.emailAddToSendQLabel = QLabel(self)
        self.emailAddToSendQLabel.setText('Email addresses')
        self.emailAddToSendQLabel.move(650 // 8, 110)

        self.emailAddToSendQPushButton = QPushButton('Input File (*txt, *docx)', self)
        self.emailAddToSendQPushButton.resize(200, 30)
        self.emailAddToSendQPushButton.move(650 // 16, 150)
        self.emailAddToSendQPushButton.clicked.connect(self.get_file)
        self.emailAddToSendQPushButton.setStyleSheet("QPushButton {background-color : #527a5d; border: 1px solid black; border-radius: 10px; }")

        # second alternative variant to get emails
        self.orQLabel = QLabel(self)
        self.orQLabel.setStyleSheet("QLabel{font-size: 25pt;}")
        self.orQLabel.setText('OR')
        self.orQLabel.move(650 // 6, 210)

        self.orQLabel = QLabel(self)
        self.orQLabel.setText('Email addresses')
        self.orQLabel.move(650 // 8, 270)

        self.emailAddToSendQPlainTextEdit = QPlainTextEdit(self)
        self.emailAddToSendQPlainTextEdit.move(650 // 16, 300)
        self.emailAddToSendQPlainTextEdit.resize(200, 200)

        # TEXT TO SEND GET

        # first variant to get their text
        self.textToSendQLabel = QLabel(self)
        self.textToSendQLabel.setText('Text To Send')
        self.textToSendQLabel.move(455, 110)

        self.textToSendQPushButton = QPushButton('Input File (*txt, *docx)', self)
        self.textToSendQPushButton.resize(200, 30)
        self.textToSendQPushButton.move(410, 150)
        self.textToSendQPushButton.clicked.connect(self.get_text)
        self.textToSendQPushButton.setStyleSheet(
            "QPushButton {background-color : #527a5d; border: 1px solid black; border-radius: 10px; }")

        # second alternative variant to get text
        self.orQLabel = QLabel(self)
        self.orQLabel.setStyleSheet("QLabel{font-size: 25pt;}")
        self.orQLabel.setText('OR')
        self.orQLabel.move(475, 210)

        self.orQLabel = QLabel(self)
        self.orQLabel.setText('Text To Send')
        self.orQLabel.move(455, 270)

        self.textToSendQPlainTextEdit = QPlainTextEdit(self)
        self.textToSendQPlainTextEdit.move(410, 300)
        self.textToSendQPlainTextEdit.resize(200, 200)

        # SEND THIS TEXT TO ALL ADDRESSES

        self.sendPreviewQPushButton = QPushButton('Send (Preview)', self)
        self.sendPreviewQPushButton.resize(300, 30)
        self.sendPreviewQPushButton.move(650 // 4, 580)
        self.sendPreviewQPushButton.clicked.connect(self.send_preview_)
        self.sendPreviewQPushButton.setStyleSheet("QPushButton {background-color : grey; border: 1px solid black; border-radius: 10px; }")

        # show all the widgets
        self.show()

    def send_preview_(self):
        # small check that user got us something
        if self.textToSendQPlainTextEdit.toPlainText().replace(' ', '') != '' and self.emailAddToSendQPlainTextEdit.toPlainText().replace(' ', '') != '' and self.pybutton.text() == 'Disconnect':
            # change window
            self.w2 = Window1(email_addresses=[self.emailAddToSendQPlainTextEdit.toPlainText()], text_to_send=[self.textToSendQPlainTextEdit.toPlainText()], email_from_send={'login': self.loginQLineEdit.text(), 'password': self.passwordQLineEdit.text()})
            self.w2.show()
        else:
            msg_failed = QMessageBox()
            msg_failed.about(self, "Incomplete fields", f"Please fill in all fields!")
            msg_failed.setIcon(QMessageBox.Critical)
            msg_failed.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def get_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if fname.split('.')[-1] in ['txt', 'docx']:
            # TODO: GET VALUE OF THIS FILE
            fileNameToShow = str(fname.split('/')[-1])[:22] + '...'
            self.emailAddToSendQPushButton.setText(fileNameToShow)
            # set text on QPlainTextEdit area
            emailAddresses = DataParser(file_path=fname).parsing_data()
            self.emailAddToSendQPlainTextEdit.clear()
            self.emailAddToSendQPlainTextEdit.insertPlainText(emailAddresses)
        else:
            self.emailAddToSendQPushButton.setText('Input File (*txt, *docx)')
            msg_failed = QMessageBox()
            msg_failed.about(self, "Wrong file type", f"We only support the formats txt, docx!")
            msg_failed.setIcon(QMessageBox.Critical)
            msg_failed.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def get_text(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')[0]
        if fname.split('.')[-1] in ['txt', 'docx']:
            # TODO: GET VALUE OF THIS FILE
            fileNameToShow = str(fname.split('/')[-1])[:22] + '...'
            self.textToSendQPushButton.setText(fileNameToShow)
            # set text on QPlainTextEdit area
            textFromUser = DataParser(file_path=fname).parsing_data()
            self.textToSendQPlainTextEdit.clear()
            self.textToSendQPlainTextEdit.insertPlainText(textFromUser)
        else:
            self.emailAddToSendQPushButton.setText('Input File (*txt, *docx)')
            msg_failed = QMessageBox()
            msg_failed.about(self, "Wrong file type", f"We only support the formats txt, docx!")
            msg_failed.setIcon(QMessageBox.Critical)
            msg_failed.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def connection_(self):
        login_text = self.loginQLineEdit.text()
        password_text = self.passwordQLineEdit.text()
        # make request to Is_Valid_Mail
        req = Is_Valid_Mail(account_={'login': login_text, 'password': password_text}).is_valid_mail()
        if req:
            if self.pybutton.text() == 'Disconnect':
                msg_success = QMessageBox()
                msg_success.about(self, "Disconnected", f"Connection to {login_text} was broke.")
                msg_success.setIcon(QMessageBox.Information)
                msg_success.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                self.pybutton.setStyleSheet(
                    "QPushButton {background-color : grey; border: 1px solid black; border-radius: 10px; }")
                self.pybutton.setText("Connect")
                # change access for login and password (can't )
                self.loginQLineEdit.setDisabled(False)
                self.passwordQLineEdit.setDisabled(False)
            else:
                msg_success = QMessageBox()
                msg_success.about(self, "Connection created", f"Connection to {login_text} created successfully.")
                msg_success.setIcon(QMessageBox.Information)
                msg_success.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                # change access for login and password (can't )
                self.loginQLineEdit.setDisabled(True)
                self.passwordQLineEdit.setDisabled(True)
                # change parameters of button
                self.pybutton.setStyleSheet("QPushButton {background-color : red; border: 1px solid black; border-radius: 10px; }")
                self.pybutton.setText("Disconnect")
        else:
            msg_failed = QMessageBox()
            msg_failed.about(self, "Connection lost", f"Failed to establish a connection.")
            msg_failed.setIcon(QMessageBox.Critical)
            msg_failed.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)


class Window1(QWidget):
    def __init__(self, email_addresses, text_to_send, email_from_send):
        super(Window1, self).__init__()
        self.setWindowTitle('Send (Preview)')
        # setting the fixed width of window
        self.setFixedSize(650, 650)

        # load data what we got from another class of user
        self.email_addresses = email_addresses
        self.text_to_send = text_to_send
        self.email_from_send = email_from_send

        # close window button
        self.closeWindowQPushButton = QPushButton(self)
        self.closeWindowQPushButton.setText('⬅ Exit')
        self.closeWindowQPushButton.show()
        self.closeWindowQPushButton.clicked.connect(self.connect_main_window_)

        # insert the main text of page
        self.mainTextQLabel = QLabel(self)
        self.mainTextQLabel.setStyleSheet("QLabel{font-size: 25pt;}")
        self.mainTextQLabel.setText('Send (Preview)')
        self.mainTextQLabel.move(650 // 3, 30)

        # tell user that there is the final version
        self.mainTextQLabel = QLabel(self)
        self.mainTextQLabel.setStyleSheet("QLabel{font-size: 12pt;}")
        self.mainTextQLabel.setText('Please note that this is the final version!')
        self.mainTextQLabel.move(200, 65)

        # create emails and text areas to show their to user
        self.emailToSendQPlainTextEdit = QPlainTextEdit(self)
        self.emailToSendQPlainTextEdit.move(650 // 16, 130)
        self.emailToSendQPlainTextEdit.resize(200, 400)
        self.emailToSendQPlainTextEdit.insertPlainText(self.email_addresses[0])
        self.emailToSendQPlainTextEdit.setDisabled(True)

        self.finalTextToSendQPlainTextEdit = QPlainTextEdit(self)
        self.finalTextToSendQPlainTextEdit.move(410, 130)
        self.finalTextToSendQPlainTextEdit.resize(200, 400)
        self.finalTextToSendQPlainTextEdit.insertPlainText(self.text_to_send[0])
        self.finalTextToSendQPlainTextEdit.setDisabled(True)

        # create labels for these areas
        self.emailQLabel = QLabel(self)
        self.emailQLabel.setText('Email addresses')
        self.emailQLabel.move(650 // 16 + 30, 110)

        self.textQLabel = QLabel(self)
        self.textQLabel.setText('Text To Send')
        self.textQLabel.move(440, 110)

        # final button send
        self.pybutton = QPushButton('Send', self)
        self.pybutton.resize(300, 30)
        self.pybutton.move(650 // 4, 600)
        self.pybutton.clicked.connect(self.send_)
        self.pybutton.setStyleSheet("QPushButton {background-color : red; border: 1px solid black; border-radius: 10px; }")

    def send_(self) -> True | False:
        for emalToSend in self.email_addresses:
            try:
                yandex_send_message_email(text_message=self.text_to_send[0], account_to_send={'login': emalToSend}, account_from_send={'login': self.email_from_send['login'], 'password': self.email_from_send['password']})
            except BaseException:
                msg_failed = QMessageBox()
                msg_failed.about(self, "Error", f"Check your input data!")
                msg_failed.setIcon(QMessageBox.Critical)
                msg_failed.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                break
        msg_failed = QMessageBox()
        msg_failed.about(self, "Success", f"Successfully sent message for all email's!")
        msg_failed.setIcon(QMessageBox.Information)
        msg_failed.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    def connect_main_window_(self):
        self.close()


if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)
    # create the instance of our Window
    window = Window()
    # start the app
    sys.exit(App.exec())
