from dataclasses import dataclass

@dataclass
class Admin:
    #管理员账号
    adminAccount:str
    #管理员名字
    adminName:str
    #管理员密码
    adminPassword:str
    #管理员盐值
    salt:str = "123456"
