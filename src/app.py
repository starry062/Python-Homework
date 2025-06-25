from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_wtf.csrf import CSRFProtect
from api.adminView import AdminView
from api.postView import PostView
from api.userView import UserSearchView, UserView, UserImportExportView
from api.adminLoginView import AdminLoginView
import os

from dao.impl.adminDaoImpl import AdminDaoImpl
from po.admin import Admin

app = Flask(__name__, template_folder='../templates')

app.config['WTF_CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'your-secret-key-here'
csrf = CSRFProtect(app)
api = Api(app)
CORS(app)

# 注册API路由
api.add_resource(AdminView, '/admin', endpoint='adminview')
api.add_resource(AdminView, '/adminview', endpoint='admin')  # For backward compatibility
api.add_resource(UserView, "/user")
api.add_resource(PostView, "/post")
api.add_resource(UserSearchView, "/user_search")
api.add_resource(AdminLoginView, "/api/admin_login")
api.add_resource(UserImportExportView, "/user_import_export")

# 添加模板路由
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST','GET'])
def register_page():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def register():
    try:
        if not request.is_json:
            return jsonify({
                'code': 400,
                'message': '请求必须是JSON格式',
                'data': None
            }), 400

        data = request.get_json()
        username = data.get('adminName')
        account = data.get('adminAccount')
        password = data.get('adminPassword')
        
        # 这里添加用户注册逻辑
        dao = AdminDaoImpl().insert_admin(Admin(account,username,password))
        # 如果注册成功
        return jsonify({
            'code': 200,
            'message': '注册成功',
            'data': None
        }), 200
    except Exception as e:
        return jsonify({
            'code': 500,
            'message': f'注册失败: {str(e)}',
            'data': None
        }), 500

@app.route('/admin_dashboard')
def admin_dashboard():
    # 获取管理员信息
    from dao.impl.adminDaoImpl import AdminDaoImpl
    admin_account = request.cookies.get('adminAccount')
    if not admin_account:
        return redirect('/login')
    
    try:
        admin = AdminDaoImpl().find_admin_by_account(admin_account)
    except ValueError:
        return redirect('/login')
    
    # 获取帖子信息
    from dao.impl.postDaoImpl import PostDaoImpl
    posts = PostDaoImpl().find_all_posts()
    
    # 获取用户信息
    from dao.impl.userDaoImpl import UserDaoImpl
    users = UserDaoImpl().find_all_user()
    print(f"DEBUG: Found {len(users)} users")  # Debug output
    for i, user in enumerate(users):
        print(f"User {i}: {user}")
    
    return render_template('admin.html',
        admin=admin,
        posts=posts,
        users=users
    )

if __name__ == '__main__':
    app.run(debug=True)
