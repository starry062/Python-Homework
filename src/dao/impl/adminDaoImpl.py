from dao.adminDao import AdminDao
from po.admin import Admin
from util.dbutil import DBUtil
import bcrypt

class AdminDaoImpl(AdminDao):
    def __init__(self):
        """Initialize the AdminDaoImpl with a MongoDB connection"""
        self.db = DBUtil.connect()
        # Create or connect to the "admins" collection
        self.collection = self.db["admins"]
        # Create a unique index on the adminAccount field
        self.collection.create_index("adminAccount", unique=True)

    def insert_admin(self, admin: Admin) -> None:
        """Insert admin using PyMongo"""
        try:
            # Configure bcrypt for password hashing
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(admin.adminPassword.encode(), salt)
            admin_data = {
                "adminAccount": admin.adminAccount,
                "adminName": admin.adminName,
                "adminPassword": hashed.decode(),
                "salt": salt.decode()
            }
            
            self.collection.insert_one(admin_data)
        except Exception as e:
            raise ValueError(f"Failed to insert admin: {str(e)}")

    def update_admin_by_name(self, name: str, admin: Admin) -> None:
        """Update admin by name using PyMongo"""
        try:
            update_data = {
                "$set": {
                    "adminAccount": admin.adminAccount,
                    "adminName": admin.adminName,
                    "adminPassword": admin.adminPassword,
                    "salt": admin.salt
                }
            }
            result = self.collection.update_one(
                {"adminName": name},
                update_data
            )
            if result.matched_count == 0:
                raise ValueError(f"No admin found with name: {name}")
        except Exception as e:
            raise ValueError(f"Failed to update admin: {str(e)}")

    def delete_admin_by_name(self, name: str) -> None:
        """Delete admin by name using PyMongo"""
        try:
            result = self.collection.delete_one({"adminName": name})
            if result.deleted_count == 0:
                raise ValueError(f"No admin found with name: {name}")
        except Exception as e:
            raise ValueError(f"Failed to delete admin: {str(e)}")

    def find_admin_by_name(self, name: str) -> list:
        """Find admin by name using PyMongo"""
        try:
            admins = list(
                self.collection.find({"adminName": {"$regex": name, "$options": "i"}})
            )
            return admins
        except Exception as e:
            raise ValueError(f"Failed to find admin by name: {str(e)}")

    def find_admin_by_account(self, account: str) -> Admin:
        """Find admin by account using PyMongo"""
        admin_data = self.collection.find_one({"adminAccount": account})
        if admin_data is None:
            raise ValueError(f"No admin found with account: {account}")
                
        return Admin(
                adminAccount=admin_data["adminAccount"],
                adminName=admin_data["adminName"],
                adminPassword=admin_data["adminPassword"],
                salt=admin_data["salt"]
            )
