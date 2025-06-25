import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.po.admin import Admin
from src.dao.impl.adminDaoImpl import AdminDaoImpl

class TestAdminDao(unittest.TestCase):
    def setUp(self):
        self.adminDao = AdminDaoImpl()

    def test_admin_insert(self):
        admin = Admin("152487", '李磊', 'Lilei7584', 'salt123')
        self.adminDao.insert_admin(admin)
        admin = Admin("1574892", '王刚', 'WangGang1548', 'salt123')
        self.adminDao.insert_admin(admin)
        admin = Admin("1587654", '张伟', 'ZhangWei1234', 'salt123')
        self.adminDao.insert_admin(admin)

    def test_admin_find_by_account(self):
        admin1 = self.adminDao.find_admin_by_account("123456")
        self.assertIsNotNone(admin1)
        self.assertEqual(admin1.adminName, 'Wang')

    def test_admin_find_by_name(self):
        admin2 = self.adminDao.find_admin_by_name('王刚')
        self.assertIsNotNone(admin2)
        self.assertEqual(admin2[0]['adminName'], '王刚')

    def test_admin_update(self):
        self.adminDao.update_admin_by_name('王刚', Admin("1574892", '王刚', 'NewPassword123', 'newsalt123'))
        admin2 = self.adminDao.find_admin_by_name('王刚')
        self.assertIsNotNone(admin2)
        self.assertEqual(admin2[0]['adminPassword'], 'NewPassword123')

    def test_admin_delete(self):
        self.adminDao.delete_admin_by_name('李磊')
        admin1 = self.adminDao.find_admin_by_account("152487")
        self.assertIsNotNone(admin1)

if __name__ == '__main__':
    unittest.main()
