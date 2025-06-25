from po.post import Post
from abc import (ABC,abstractmethod)

class PostDao(ABC):
    @abstractmethod
    def insert_post(self,post:Post):
        pass

        
    @abstractmethod
    def find_post_by_userId(self,user_id:str)->Post:
        pass

    @abstractmethod
    def find_post_by_title(self,title:str)->list:
        pass

    @abstractmethod
    def update_post_by_userId(self,user_id:str,**kwargs):
        pass

    @abstractmethod
    def delete_post_by_userId(self,user_id:str):
        pass

    @abstractmethod
    def export_to_csv(self, file_path: str) -> bool:
        """导出帖子数据到CSV文件
        
        Args:
            file_path: 导出文件路径
            
        Returns:
            bool: 导出是否成功
        """
        pass

    @abstractmethod
    def import_from_csv(self, file_path: str) -> bool:
        """从CSV文件导入帖子数据
        
        Args:
            file_path: 导入文件路径
            
        Returns:
            bool: 导入是否成功
        """
        pass

    @abstractmethod
    def export_to_json(self, file_path: str) -> bool:
        """导出帖子数据到JSON文件
        
        Args:
            file_path: 导出文件路径
            
        Returns:
            bool: 导出是否成功
        """
        pass

    @abstractmethod
    def import_from_json(self, file_path: str) -> bool:
        """从JSON文件导入帖子数据
        
        Args:
            file_path: 导入文件路径
            
        Returns:
            bool: 导入是否成功
        """
        pass

    @abstractmethod
    def find_all_posts(self) -> list:
        """获取所有帖子
        
        Returns:
            list: 包含所有帖子的列表
        """
        pass
