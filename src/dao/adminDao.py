from abc import(ABC,abstractmethod)
from po.admin import Admin
#接口AdminDao
class AdminDao(ABC):
    #插入Admin(用于Admin注册)
    @abstractmethod
    def insert_admin(self,admin:Admin) -> None:
        pass

    #通过名字更新Admin
    @abstractmethod
    def update_admin_by_name(self,name:str,admin:Admin) -> None:
        pass

    #通过名字删除Admin
    @abstractmethod
    def delete_admin_by_name(self,name:str) -> None:
        pass

    #通过名字找到Admin
    @abstractmethod
    def find_admin_by_name(self,name:str) -> list:
        pass

    @abstractmethod
    def find_admin_by_account(self,account:str) -> Admin:
        pass
