import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.dao.userDao import UserDao
from src.dao.impl.userDaoImpl import UserDaoImpl
from src.po.user import User

class TestUserDao(unittest.TestCase):
    def setUp(self):
        self.userDao = UserDaoImpl()

    def test_user_insert(self):
        user1 = User(nickname="Amy0989", phone_number=15975245, email="amy5245@163.com", password="Amy&900s")
        # user2 = User("David7545", 158765, "Dav1234", "David1578")
        self.userDao.insert_user(user1)
        # self.userDao.insert_user(user2)

    def test_user_find_by_id(self):
        user1 = self.userDao.find_user_by_number(15975245)
        self.assertIsNotNone(user1)
        self.assertEqual(user1.nickname, "Amy0989")

    def test_user_find_by_email(self):
        user2 = self.userDao.find_user_by_email("Dav1234")
        self.assertIsNotNone(user2)
        self.assertEqual(user2.nickname, "David7545")

    def test_user_update(self):
        self.userDao.update_user_by_number(158765, nickname="David7545", phone_number=158765, email="Dav1234@qq.com", password="NewPassword123")
        user2 = self.userDao.find_user_by_number(158765)
        self.assertIsNotNone(user2)
        self.assertEqual(user2.password, "NewPassword123")

    def test_user_delete(self):
        self.userDao.delete_user_by_number(15975245)
        user1 = self.userDao.find_user_by_number(15975245)
        self.assertIsNone(user1)

if __name__ == '__main__':
    unittest.main()
