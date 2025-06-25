from dataclasses import dataclass
@dataclass
class User:
    #用户昵称
    nickname:str
    #用户手机号
    phone_number:int
    #用户邮箱
    email:str
    #用户密码
    password:str
    #盐值(密码加密)
    salt:str = "123456"