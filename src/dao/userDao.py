from abc import (ABC,abstractmethod)
from po.user import User
class UserDao(ABC):

    @abstractmethod
    def find_user_by_name(self,name:str)->list:
        pass

    @abstractmethod
    def find_all_user(self)->list:
        pass

    @abstractmethod
    def insert_user(self,user:User):
        pass

    @abstractmethod
    def update_user_by_number(self,number:int,**kwargs):
        pass
    

    @abstractmethod
    def delete_user_by_number(self,number:int):
        pass

    @abstractmethod
    def find_user_by_number(self,number:int)->User:
        pass

    @abstractmethod
    def find_user_by_email(self,email:str)->User:
        pass

    @abstractmethod
    def find_id_by_number(self,number:int)->int:
        pass
    
    @abstractmethod
    def update_user_by_nickname(self,nickname:str,**kwargs):
        pass

    @abstractmethod
    def export_to_csv(self, file_path: str) -> bool:
        """导出用户数据到CSV文件
        
        Args:
            file_path: 导出文件路径
            
        Returns:
            bool: 导出是否成功
        """
        pass

    @abstractmethod
    def import_from_csv(self, file_path: str) -> bool:
        """从CSV文件导入用户数据
        
        Args:
            file_path: 导入文件路径
            
        Returns:
            bool: 导入是否成功
        """
        pass

    @abstractmethod
    def export_to_json(self, file_path: str) -> bool:
        """导出用户数据到JSON文件
        
        Args:
            file_path: 导出文件路径
            
        Returns:
            bool: 导出是否成功
        """
        pass

    @abstractmethod
    def import_from_json(self, file_path: str) -> bool:
        """从JSON文件导入用户数据
        
        Args:
            file_path: 导入文件路径
            
        Returns:
            bool: 导入是否成功
        """
        pass
