from flask import request, make_response, jsonify
from flask_restful import Resource
from dao.impl.adminDaoImpl import AdminDaoImpl
from po.admin import Admin
import bcrypt

class AdminLoginView(Resource):
    """管理员登录视图类，处理管理员登录相关API"""
    def __init__(self):
        self.dao = AdminDaoImpl()

    def post(self):
        """处理管理员登录请求
        
        Args:
            通过请求体JSON传递账号和密码:
                - adminAccount: 管理员账号
                - adminPassword: 管理员密码
                
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400/401状态码和错误信息
        """
        data = request.get_json()
        if not data or "adminAccount" not in data or "adminPassword" not in data:
            return {"code": 400, "message": "缺少账号或密码参数"}
            
        try:
            admin = self.dao.find_admin_by_account(data["adminAccount"])
            if not admin:
                return {"code": 401, "message": "账号或密码错误"}
                
            # 验证密码
            if bcrypt.checkpw(data["adminPassword"].encode(), admin.adminPassword.encode()):
                response = make_response(jsonify({
                    'code': 200,
                    'message': '登录成功',
                    'data': {
                        'adminAccount': admin.adminAccount,
                        'adminName': admin.adminName
                    }
                }))
                response.set_cookie('adminAccount', admin.adminAccount)
                return response
            else:
                return {"code": 401, "message": "账号或密码错误"}
        except Exception as e:
            return {"code": 400, "message": f"登录失败: {str(e)}"}
