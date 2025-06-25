from flask import request
from flask_restful import Resource
from dao.impl.postDaoImpl import PostDaoImpl
from po.post import Post
from datetime import datetime
from bson import ObjectId

class PostView(Resource):
    """帖子视图类，提供帖子相关的RESTful API接口"""
    def __init__(self):
        self.dao = PostDaoImpl()

    def get(self):
        """获取帖子信息
        
        Args:
            user_id (str, optional): 通过URL参数传递的用户ID
            title (str, optional): 通过URL参数传递的帖子标题
            
        Returns:
            dict: 包含状态码和查询结果的字典
                - 成功: 200状态码和帖子数据
                - 失败: 400/404/500状态码和错误信息
        """
        try:
            # Get posts by user ID
            user_id = request.args.get("user_id")
            if user_id:
                post = self.dao.find_post_by_userId(user_id)
                if not post:
                    return {"code": 404, "message": f"没有用户id为{user_id}的帖子"}
                
                post_dict = {
                    "user_id": post.user_id,
                    "title": post.title,
                    "date": post.date,
                    "content": post.content
                }
                return {"code": 200, "data": post_dict}

            # Search posts by title
            title = request.args.get("title")
            if title:
                posts = self.dao.find_post_by_title(title)
                if not posts:
                    return {"code": 404, "message": f"没有找到标题为'{title}'的帖子"}
                
                post_list = []
                for post in posts:
                    post_list.append({
                        "user_id": post.user_id,
                        "title": post.title,
                        "date": post.date.isoformat(),
                        "content": post.content
                    })
                return {"code": 200, "data": post_list}
            posts = self.dao.find_all_posts()
            post_list = []
            for post in posts:
                post_list.append({
                    "user_id": post.user_id,
                    "title": post.title,
                    "date": post.date.isoformat(),
                    "content": post.content
                })
            return {"code": 200, "data": post_list}

        except Exception as e:
            return {"code": 500, "message": f"查找帖子出现错误：{str(e)}"}

    def post(self):
        """创建新帖子
        
        Args:
            通过请求体JSON传递帖子信息，格式:
            {
                "user_id": "用户ID",
                "title": "帖子标题",
                "content": "帖子内容" (可选)
            }
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 201状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        try:
            data = request.get_json()
            if not data:
                return {"code": 400, "message": "请求体不能为空"}

            # Validate required fields
            required_fields = ["user_id", "title"]
            for field in required_fields:
                if field not in data:
                    return {"code": 400, "message": f"未填写字段：{field}"}
            
            # Create post object
            post = Post(
                user_id=data["user_id"],
                title=data["title"],
                date=datetime.now(),
                content=data.get("content", "")
            )

            # Insert post
            self.dao.insert_post(post)
            
            return {"code": 201, "message": "成功创建帖子"}

        except Exception as e:
            return {"code": 400, "message": f"创建帖子失败: {str(e)}"}
    
    def put(self):
        """更新帖子信息
        
        Args:
            user_id (str): 通过URL参数传递的用户ID
            通过请求体JSON传递更新的帖子信息，可更新字段:
            {
                "title": "新标题",
                "content": "新内容"
            }
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        try:
            user_id = request.args.get("user_id")
            if not user_id:
                return {"code": 400, "message": "未填写user_id字段"}

            data = request.get_json()
            if not data:
                return {"code": 400, "message": "请求体不能为空"}

            # Only allow updating title and content
            update_data = {}
            allowed_fields = ["title", "content"]
            for field in allowed_fields:
                if field in data:
                    update_data[field] = data[field]

            if not update_data:
                return {"code": 400, "message": "没有字段可更新"}

            # Update post
            self.dao.update_post_by_userId(user_id, **update_data)
            
            return {"code": 200, "message": "Post updated successfully"}

        except Exception as e:
            return {"code": 400, "message": f"Failed to update post: {str(e)}"}

    def delete(self):
        """删除帖子
        
        Args:
            user_id (str): 通过URL参数传递的用户ID
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        try:
            user_id = request.args.get("user_id")
            if not user_id:
                return {"code": 400, "message": "Missing user_id parameter"}

            # Delete post
            self.dao.delete_post_by_userId(user_id)
            
            return {"code": 200, "message": "Post deleted successfully"}

        except Exception as e:
            return {"code": 400, "message": f"Failed to delete post: {str(e)}"}
