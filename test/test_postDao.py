import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.dao.postDao import PostDao
from src.dao.impl.postDaoImpl import PostDaoImpl
from src.po.post import Post
from src.dao.impl.userDaoImpl import UserDaoImpl
from src.dao.userDao import UserDao
from datetime import datetime


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.django_settings')


class TestPostDao(unittest.TestCase):
    def setUp(self):
        self.postDao = PostDaoImpl()
        self.userDao = UserDaoImpl()

    def test_post_insert(self):
        user_id = self.userDao.find_id_by_number(15975245)
        post = Post(str(user_id), datetime.now(), "测试")
        self.postDao.insert_post(post)

if __name__ == '__main__':
    unittest.main()
