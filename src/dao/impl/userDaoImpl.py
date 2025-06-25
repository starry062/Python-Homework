from dao.userDao import UserDao
from po.user import User
from util.dbutil import DBUtil
import bcrypt
import csv
import json
from bson import ObjectId

class UserDaoImpl(UserDao):
    def __init__(self):
        self.db = DBUtil.connect()
        self.collection = self.db["users"]
        self.collection.create_index("phone_number", unique=True)
        self.collection.create_index("email", unique=True)
        self.collection.create_index("nickname", unique=True)

    def find_all_user(self) -> list:
        try:
            return list(self.collection.find())
        except Exception as e:
            raise ValueError(f"Failed to find all users: {str(e)}")
    
    def find_user_by_name(self, name: str) -> list:
        try:
            return list(
                self.collection.find({"nickname":  {"$regex": name, "$options": "i"}})
            )
        except Exception as e:
            raise ValueError(f"Failed to find user by name: {str(e)}")
    
    def insert_user(self, user: User):
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(user.password.encode(), salt)
            
            user_data = {
                "nickname": user.nickname,
                "phone_number": user.phone_number,
                "email": user.email,
                "password": hashed_password.decode(),
                "salt": salt.decode()
            }
            self.collection.insert_one(user_data)
        except Exception as e:
            raise ValueError(f"Failed to insert user: {str(e)}")
    
    def update_user_by_number(self, number: int, **kwargs):
        try:
            update_data = {"$set": kwargs}
            result = self.collection.update_one(
                {"phone_number": number},
                update_data
            )
            if result.matched_count == 0:
                raise ValueError(f"No user found with phone number: {number}")
        except Exception as e:
            raise ValueError(f"Failed to update user: {str(e)}")
    
    def delete_user_by_number(self, number: int):
        try:
            result = self.collection.delete_one({"phone_number": number})
            if result.deleted_count == 0:
                raise ValueError(f"No user found with phone number: {number}")
        except Exception as e:
            raise ValueError(f"Failed to delete user: {str(e)}")
    
    def find_user_by_number(self, number: int) -> User:
        try:
            user_data = self.collection.find_one({"phone_number": number})
            if not user_data:
                raise ValueError(f"No user found with phone number: {number}")
                
            return User(
                nickname=user_data["nickname"],
                phone_number=user_data["phone_number"],
                email=user_data["email"],
                password=user_data["password"],
                salt=user_data["salt"]
            )
        except Exception as e:
            raise ValueError(f"Failed to find user by phone number: {str(e)}")
    
    def find_user_by_email(self, email: str) -> User:
        try:
            user_data = self.collection.find_one({"email": email})
            if not user_data:
                raise ValueError(f"No user found with email: {email}")
                
            return User(
                nickname=user_data["nickname"],
                phone_number=user_data["phone_number"],
                email=user_data["email"],
                password=user_data["password"],
                salt=user_data["salt"]
            )
        except Exception as e:
            raise ValueError(f"Failed to find user by email: {str(e)}")
        
    def find_id_by_number(self, number: int) -> int:
        try:
            user_data = self.collection.find_one({"phone_number": number})
            if not user_data:
                raise ValueError(f"No user found with phone number: {number}")
            return user_data["_id"]
        except Exception as e:
            raise ValueError(f"Failed to find user ID by phone number: {str(e)}")
        
    def update_user_by_nickname(self, nickname: str, **kwargs):
        try:
            update_data = {"$set": kwargs}
            result = self.collection.update_one(
                {"nickname": nickname},update_data)
            if result.matched_count == 0:
                raise ValueError(f"No user found with nickname: {nickname}")
        except Exception as e:
            raise ValueError(f"Failed to update user by nickname: {str(e)}")

    def export_to_csv(self, file_path: str) -> bool:
        """导出用户数据到CSV文件"""
        try:
            users = self.find_all_user()
            if not users:
                return False
                
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['_id', 'nickname', 'phone_number', 'email']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for user in users:
                    writer.writerow({
                        '_id': str(user['_id']),
                        'nickname': user['nickname'],
                        'phone_number': user['phone_number'],
                        'email': user['email']
                    })
            return True
        except Exception as e:
            raise ValueError(f"Failed to export to CSV: {str(e)}")

    def import_from_csv(self, file_path: str) -> bool:
        """从CSV文件导入用户数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user = User(
                        nickname=row['nickname'],
                        phone_number=int(row['phone_number']),
                        email=row['email'],
                        password="default_password"  # 需要用户后续修改
                    )
                    self.insert_user(user)
            return True
        except Exception as e:
            raise ValueError(f"Failed to import from CSV: {str(e)}")

    def export_to_json(self, file_path: str) -> bool:
        """导出用户数据到JSON文件"""
        try:
            users = self.find_all_user()
            if not users:
                return False
                
            # 转换ObjectId为字符串
            for user in users:
                user['_id'] = str(user['_id'])
                
            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(users, jsonfile, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            raise ValueError(f"Failed to export to JSON: {str(e)}")

    def import_from_json(self, file_path: str) -> bool:
        """从JSON文件导入用户数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                users = json.load(jsonfile)
                for user_data in users:
                    user = User(
                        nickname=user_data['nickname'],
                        phone_number=int(user_data['phone_number']),
                        email=user_data['email'],
                        password="default_password"  # 需要用户后续修改
                    )
                    self.insert_user(user)
            return True
        except Exception as e:
            raise ValueError(f"Failed to import from JSON: {str(e)}")
