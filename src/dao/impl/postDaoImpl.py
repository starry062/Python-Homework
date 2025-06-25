from dao.postDao import PostDao
from po.post import Post
from util.dbutil import DBUtil
from datetime import datetime
import csv
import json
from bson import ObjectId

class PostDaoImpl(PostDao):
    def __init__(self):
        """Initialize the PostDaoImpl with a MongoDB connection"""
        self.db = DBUtil.connect()
        self.collection = self.db["posts"]

    def insert_post(self, post: Post):
        try:
            post_data = {
                "user_id": post.user_id,
                "title": post.title,
                "content": post.content,
                "date": post.date
            }
            self.collection.insert_one(post_data)
        except Exception as e:
            raise Exception(f"Failed to insert post: {str(e)}")
    
    def find_post_by_userId(self, user_id: str) -> Post:
        try:
            post_data = self.collection.find_one({"user_id": user_id})
            if not post_data:
                raise ValueError(f"No post found for user_id: {user_id}")
            
            return Post(
                user_id=post_data["user_id"],
                title=post_data["title"],
                content=post_data["content"],
                date=post_data["date"]
            )
        except Exception as e:
            raise Exception(f"Failed to find post by user_id: {str(e)}")
    
    def find_post_by_title(self, title: str) -> list:
        try:
            posts_data = list(self.collection.find(
                {"title": {"$regex": title, "$options": "i"}}
            ))
            posts = []
            for post_data in posts_data:
                posts.append(Post(
                    user_id=post_data["user_id"],
                    title=post_data["title"],
                    content=post_data["content"],
                    date=post_data["date"]
                ))
            return posts
        except Exception as e:
            raise Exception(f"Failed to find posts by title: {str(e)}")
    
    def update_post_by_userId(self, user_id: str, **kwargs):
        try:
            valid_fields = ['title', 'content', 'date']
            update_data = {k: v for k, v in kwargs.items() if k in valid_fields}
            
            if not update_data:
                raise ValueError("No valid fields provided for update")
            
            result = self.collection.update_many(
                {"user_id": user_id},
                {"$set": update_data}
            )
            if result.matched_count == 0:
                raise ValueError(f"No post found for user_id: {user_id}")
        except Exception as e:
            raise Exception(f"Failed to update post by user_id: {str(e)}")
    
    def delete_post_by_userId(self, user_id: str):
        try:
            result = self.collection.delete_many({"user_id": user_id})
            if result.deleted_count == 0:
                raise ValueError(f"No post found for user_id: {user_id}")
        except Exception as e:
            raise Exception(f"Failed to delete post by user_id: {str(e)}")

    def export_to_csv(self, file_path: str) -> bool:
        """导出帖子数据到CSV文件"""
        try:
            posts = list(self.collection.find())
            if not posts:
                return False
                
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['_id', 'user_id', 'title', 'content', 'date']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for post in posts:
                    writer.writerow({
                        '_id': str(post['_id']),
                        'user_id': post['user_id'],
                        'title': post['title'],
                        'content': post['content'],
                        'date': post['date'].isoformat() if post['date'] else ''
                    })
            return True
        except Exception as e:
            raise Exception(f"Failed to export to CSV: {str(e)}")

    def import_from_csv(self, file_path: str) -> bool:
        """从CSV文件导入帖子数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    post = Post(
                        user_id=row['user_id'],
                        title=row['title'],
                        content=row['content'],
                        date=datetime.fromisoformat(row['date']) if row['date'] else datetime.now()
                    )
                    self.insert_post(post)
            return True
        except Exception as e:
            raise Exception(f"Failed to import from CSV: {str(e)}")

    def export_to_json(self, file_path: str) -> bool:
        """导出帖子数据到JSON文件"""
        try:
            posts = list(self.collection.find())
            if not posts:
                return False
                
            # 转换ObjectId为字符串并处理日期
            for post in posts:
                post['_id'] = str(post['_id'])
                if 'date' in post and post['date']:
                    post['date'] = post['date'].isoformat()
                
            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(posts, jsonfile, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            raise Exception(f"Failed to export to JSON: {str(e)}")

    def import_from_json(self, file_path: str) -> bool:
        """从JSON文件导入帖子数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                posts = json.load(jsonfile)
                for post_data in posts:
                    post = Post(
                        user_id=post_data['user_id'],
                        title=post_data['title'],
                        content=post_data['content'],
                        date=datetime.fromisoformat(post_data['date']) if post_data.get('date') else datetime.now()
                    )
                    self.insert_post(post)
            return True
        except Exception as e:
            raise Exception(f"Failed to import from JSON: {str(e)}")

    def find_all_posts(self) -> list:
        """获取所有帖子
        
        Returns:
            list: 包含所有Post对象的列表
        """
        try:
            posts_data = list(self.collection.find())
            posts = []
            for post_data in posts_data:
                posts.append(Post(
                    user_id=post_data["user_id"],
                    title=post_data["title"],
                    content=post_data["content"],
                    date=post_data["date"]
                ))
            return posts
        except Exception as e:
            raise Exception(f"Failed to find all posts: {str(e)}")
