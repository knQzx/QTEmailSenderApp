import smtplib


class Is_Valid_Mail:
    def __init__(self, account_: dict):
        self.account_login = account_['login']
        self.account_password = account_['password']

    def is_valid_mail(self) -> True | False:
        try:
            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
            server.login(self.account_login, self.account_password)  # Получаем доступ
            server.quit()  # Выходим
            return True
        except BaseException:
            return False
