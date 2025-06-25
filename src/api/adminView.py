from flask import request
from flask_restful import Resource
from dao.impl.adminDaoImpl import AdminDaoImpl
from po.admin import Admin
import bcrypt

class AdminView(Resource):
    """管理员视图类，提供管理员相关的RESTful API接口"""
    def __init__(self):
        self.dao = AdminDaoImpl()

    def get(self):
        """根据名称查询管理员信息
        
        Args:
            name (str): 通过URL参数传递的管理员名称
            
        Returns:
            dict: 包含状态码和查询结果的字典
                - 成功: 200状态码和管理员数据
                - 失败: 400/404状态码和错误信息
        """
        name = request.args.get("name")
        result = []
        if not name:
            return {"code": 400, "message": "缺少参数 name"}, 400
        admins = self.dao.find_admin_by_name(name)
        if not admins:
            return {"code": 404, "message": f"未找到管理员: {name}"}
        for admin in admins:
            if "_id" in admin:
                admin.pop("_id")
                result.append(admin)
        return {"code": 200, "data": result}

    def put(self):
        """更新管理员信息
        
        Args:
            name (str): 通过URL参数传递的要更新的管理员名称
            通过请求体JSON传递更新的管理员信息
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        name = request.args.get("name")
        data = request.get_json()
        try:
            admin = Admin(**data)
            if name is not None:
                self.dao.update_admin_by_name(name, admin)
            else:
                return {"code" : 400,"message" : "参数没有名字"}
            return {"code": 200, "message": f"管理员 {name} 更新成功"}
        except Exception as e:
            return {"code": 400, "message": f"更新失败: {str(e)}"}

    def delete(self):
        """删除管理员
        
        Args:
            name (str): 通过URL参数传递的要删除的管理员名称
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400/404状态码和错误信息
        """
        name = request.args.get("name")
        if not name:
            return {"code": 400, "message": "缺少参数 name"}
        try:
            self.dao.delete_admin_by_name(name)
            return {"code": 200, "message": f"管理员 {name} 删除成功"}
        except Exception as e:
            return {"code": 404, "message": f"删除失败: {str(e)}"}

    def post(self):
        """创建新的管理员
        
        Args:
            通过请求体JSON传递管理员信息
                
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 201状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        data = request.get_json()
        try:
            admin = Admin(**data)
            self.dao.insert_admin(admin)
            return {"code": 201, "message": "注册成功"}
        except Exception as e:
            return {"code": 400, "message": f"创建失败: {str(e)}"}
