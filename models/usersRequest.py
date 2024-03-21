from pydantic import BaseModel


class usersRequests(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    is_active:bool
    role:str
    phonenumber:str    
    def __init__(self,email,username,first_name,last_name,password,is_active,role,phonenumber):
        super().__init__(email=email,username=username,first_name=first_name,last_name=last_name,password=password,is_active=is_active,role=role,phonenumber=phonenumber)
   
    class Config:
        json_schema_extra = {
            "example":{
            "email": "joe@gmail.com",
            "username":"joe@gmail.com",
            "first_name":"Joe",
            "last_name":"Criden",
            "password":"1234Zz",
            "role":"Manager",
            "is_active":False,
            "phonenumber":"04-8222022"
            }
            
        }
