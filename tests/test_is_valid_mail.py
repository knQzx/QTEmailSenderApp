import unittest
from is_valid_mail import Is_Valid_Mail


class Testing(unittest.TestCase):
    def test_string(self):
        login = 'login'
        password = 'password'
        self.assertEqual(True, Is_Valid_Mail(account_={'login': login, 'password': password}).is_valid_mail())


if __name__ == '__main__':
    unittest.main()
