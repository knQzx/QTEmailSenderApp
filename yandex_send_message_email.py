import smtplib

from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML


def yandex_send_message_email(text_message: str, account_to_send: dict, account_from_send: dict) -> True | False:
    try:
        msg = MIMEMultipart()  # Создаем сообщение

        msg['From'] = account_from_send['login']  # Адресат
        msg['To'] = account_to_send['login']  # Получатель
        msg['Subject'] = 'Тема сообщения'

        body = text_message
        msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)  # Создаем объект SMTP
        # server.starttls()             # Начинаем шифрованный обмен по TLS
        server.login(account_from_send['login'], account_from_send['password'])  # Получаем доступ
        server.send_message(msg)  # Отправляем сообщение
        server.quit()  # Выходим
        return True
    except BaseException:
        return False
