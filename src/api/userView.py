from flask import request, redirect, url_for, flash
from flask_restful import Resource
from dao.impl.userDaoImpl import UserDaoImpl
from po.user import User
from bson import ObjectId
import json

class UserView(Resource):
    """用户视图类，提供用户相关的RESTful API接口"""
    def __init__(self):
        self.dao = UserDaoImpl()

    def get(self):
        """获取用户信息
        
        Args:
            name (str, optional): 通过URL参数传递的用户昵称
            email (str, optional): 通过URL参数传递的用户邮箱
            phone_number (str, optional): 通过URL参数传递的用户手机号
            all (str, optional): 值为"true"时获取所有用户
            
        Returns:
            dict: 包含状态码和查询结果的字典
                - 成功: 200状态码和用户数据
                - 失败: 400/404/500状态码和错误信息
        """
        try:
            # 获取所有用户
            if request.args.get("all") == "true":
                users = self.dao.find_all_user()
                if not users:
                    return {"code": 404, "message": "未找到任何用户"}
                
                # 转换MongoDB文档为可序列化的格式
                user_list = []
                for user in users:
                    user_dict = {
                        "_id": str(user._id),
                        "nickname": user.nickname,
                        "phone_number": user.phone_number,
                        "email": user.email
                    }
                    user_list.append(user_dict)
                
                return {"code": 200, "data": user_list, "message": f"找到 {len(user_list)} 个用户"}

            # 根据昵称查询
            name = request.args.get("name")
            if name:
                users = self.dao.find_user_by_name(name)
                if not users:
                    return {"code": 404, "message": f"未找到昵称为 {name} 的用户"}
                
                user_list = []
                for user in users:
                    user_dict = {
                        "_id": str(user._id),
                        "nickname": user.nickname,
                        "phone_number": user.phone_number,
                        "email": user.email
                    }
                    user_list.append(user_dict)
                
                return {"code": 200, "data": user_list}

            # 根据邮箱查询
            email = request.args.get("email")
            if email:
                user = self.dao.find_user_by_email(email)
                if not user:
                    return {"code": 404, "message": f"未找到邮箱为 {email} 的用户"}
                
                user_dict = {
                    "nickname": user.nickname,
                    "phone_number": user.phone_number,
                    "email": user.email
                }
                
                return {"code": 200, "data": user_dict}

            # 根据手机号查询
            phone_number = request.args.get("phone_number")
            if phone_number:
                try:
                    phone_num = int(phone_number)
                    user = self.dao.find_user_by_number(phone_num)
                    if not user:
                        return {"code": 404, "message": f"未找到手机号为 {phone_number} 的用户"}
                    
                    user_dict = {
                        "nickname": user.nickname,
                        "phone_number": user.phone_number,
                        "email": user.email,
                    }
                    
                    return {"code": 200, "data": user_dict}
                except ValueError:
                    return {"code": 400, "message": "手机号格式不正确"}

            return {"code": 400, "message": "请提供查询参数: name, email, phone_number 或 all=true"}

        except Exception as e:
            return {"code": 500, "message": f"查询失败: {str(e)}"}

    def post(self):
        """创建新用户
        
        Args:
            通过请求体JSON传递用户信息，格式:
            {
                "nickname": "用户昵称",
                "phone_number": 手机号(整数),
                "email": "邮箱地址",
                "password": "密码"
            }
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 201状态码和用户数据
                - 失败: 400状态码和错误信息
        """
        try:
            data = request.get_json()
            if not data:
                return {"code": 400, "message": "请求体不能为空"}

            # 验证必需字段
            required_fields = ["nickname", "phone_number", "email", "password"]
            for field in required_fields:
                if field not in data:
                    return {"code": 400, "message": f"缺少必需字段: {field}"}

            # 验证手机号格式
            try:
                phone_number = int(data["phone_number"])
            except (ValueError, TypeError):
                return {"code": 400, "message": "手机号必须是数字"}

            # 创建用户对象
            user = User(
                nickname=data["nickname"],
                phone_number=phone_number,
                email=data["email"],
                password=data["password"]
            )

            # 插入用户
            self.dao.insert_user(user)
            
            return {"code": 201, "message": "用户创建成功", "data": {
                "nickname": user.nickname,
                "phone_number": user.phone_number,
                "email": user.email
            }}

        except Exception as e:
            return {"code": 400, "message": f"创建用户失败: {str(e)}"}

    def put(self):
        """更新用户信息
        
        Args:
            nickname (str): 通过URL参数传递的要更新的用户昵称
            通过请求体JSON传递更新的用户信息，可更新字段:
            {
                "nickname": "新昵称",
                "phone_number": 新手机号,
                "email": "新邮箱",
                "password": "新密码"
            }
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        try:
            nickname = request.args.get("nickname")
            if not nickname:
                return {"code": 400, "message": "缺少参数 nickname"}

            data = request.get_json()
            if not data:
                return {"code": 400, "message": "请求体不能为空"}

            # 移除不允许更新的字段
            update_data = {}
            allowed_fields = ["nickname", "phone_number", "email", "password"]
            
            for field, value in data.items():
                if field in allowed_fields:
                    if field == "phone_number":
                        try:
                            update_data[field] = int(value)
                        except (ValueError, TypeError):
                            return {"code": 400, "message": "手机号必须是数字"}
                    else:
                        update_data[field] = value

            if not update_data:
                return {"code": 400, "message": "没有可更新的字段"}

            # 更新用户
            self.dao.update_user_by_nickname(nickname, **update_data)
            
            return {"code": 200, "message": f"用户 {nickname} 更新成功"}

        except Exception as e:
            return {"code": 400, "message": f"更新用户失败: {str(e)}"}

    def delete(self):
        """删除用户
        
        Args:
            nickname (str): 通过URL参数传递的用户昵称
            phone_number (str): 通过URL参数传递的用户手机号
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400/404状态码和错误信息
        """
        try:
            nickname = request.args.get("nickname")
            phone_number = request.args.get("phone_number")
            
            if not nickname or not phone_number:
                return {"code": 400, "message": "缺少参数: nickname 和 phone_number 都是必需的"}

            # 删除用户
            self.dao.delete_user_by_number(int(phone_number))
            
            return {"code": 200, "message": f"用户 {nickname} 删除成功"}

        except Exception as e:
            return {"code": 404, "message": f"删除用户失败: {str(e)}"}


class UserSearchView(Resource):
    """用户搜索视图类，提供额外的用户搜索API"""
    def __init__(self):
        self.dao = UserDaoImpl()

    def get(self):
        """高级用户搜索
        
        Args:
            phone_number (str): 通过URL参数传递的用户手机号
            
        Returns:
            dict: 包含状态码和搜索结果的字典
                - 成功: 200状态码和用户数据
                - 失败: 400/404状态码和错误信息
        """
        try:
            phone_number = request.args.get("phone_number")
            if phone_number:
                try:
                    phone_num = int(phone_number)
                    user = self.dao.find_user_by_number(phone_num)
                    return {"code": 200, "data": {"user": user.__dict__}}
                except ValueError:
                    return {"code": 400, "message": "手机号格式不正确"}
            
            return {"code": 400, "message": "请提供查询参数: phone_number"}

        except Exception as e:
            return {"code": 404, "message": f"搜索失败: {str(e)}"}


class UserImportExportView(Resource):
    """用户数据导入导出视图类"""
    def __init__(self):
        self.dao = UserDaoImpl()

    def get(self):
        """导出用户数据为JSON文件
        
        Args:
            file_path (str): 通过URL参数传递的导出文件路径
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        try:
            file_path = request.args.get("file_path")
            if not file_path:
                return {"code": 400, "message": "缺少参数 file_path"}
            
            if self.dao.export_to_json(file_path):
                return {"code": 200, "message": f"用户数据已成功导出到 {file_path}"}
            return {"code": 400, "message": "导出失败，没有用户数据"}
        except Exception as e:
            return {"code": 400, "message": f"导出失败: {str(e)}"}

    def post(self):
        """从上传的JSON文件导入用户数据
        
        Args:
            json_file: 通过表单上传的JSON文件
            
        Returns:
            dict: 包含状态码和操作结果的字典
                - 成功: 200状态码和成功消息
                - 失败: 400状态码和错误信息
        """
        try:
            if 'json_file' not in request.files:
                return {"code": 400, "message": "请选择要上传的JSON文件"}
                
            file = request.files['json_file']
            if not file or not file.filename:
                return {"code": 400, "message": "未选择文件"}
                
            filename = file.filename
            if not isinstance(filename, str):
                return {"code": 400, "message": "无效的文件名"}
                
            if not filename.lower().endswith('.json'):
                return {"code": 400, "message": "只支持JSON文件"}
                
            # 保存临时文件
            import tempfile
            import os
            from werkzeug.utils import secure_filename
            
            temp_dir = tempfile.mkdtemp()
            safe_filename = secure_filename(filename)
            file_path = os.path.join(temp_dir, safe_filename)
            
            try:
                file.save(file_path)
                
                # 导入数据
                result = self.dao.import_from_json(file_path)
                
                if result:
                    flash("用户数据导入成功", "success")
                    return redirect(url_for('adminview'))
                flash("导入失败", "danger")
                return redirect(url_for('adminview'))
                
            except Exception as e:
                flash(f"文件处理失败: {str(e)}", "danger")
                return redirect(url_for('adminview'))
                
            finally:
                # 确保删除临时文件
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    if os.path.exists(temp_dir):
                        os.rmdir(temp_dir)
                except Exception as e:
                    print(f"清理临时文件失败: {str(e)}")
                    
        except Exception as e:
            flash(f"导入失败: {str(e)}", "danger")
            return redirect(url_for('admin'))
