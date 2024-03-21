from pydantic import BaseModel
from models.usersRequest import usersRequests
from dbmodels.users import users as Users
from passlib.context import CryptContext
from dbmodels import users
from fastapi import Depends, HTTPException,APIRouter
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import dbmodels.users
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

class login(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str
    id:int
    email:str
    username:str
    first_name:str
    last_name :str
   

SECRET_KEY = '97aa6b6f64df28a030fcc85c4e5fe523077c330dfb95ddedd2c5fcdf0b8678b7'
REFRESH_SECRET_KEY = '6c2980d5578e8cce61bc1a4e889d48149be0794e37306bf8ae8d65dcfd2290cb'
ALGORYTHM = 'HS256'

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer = OAuth2AuthorizationCodeBearer(tokenUrl='auth/token',authorizationUrl='auth/authorize')

dbmodels.users.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def creaate(db: db_dependency,user:usersRequests):
    createdeUser:users = Users(
        email = user.email,
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        hashed_password = bcrypt_context.hash(user.password) ,
        is_active = True,
        role = user.role
        
    )
    
    db.add(createdeUser)
    db.commit()
    
@router.post("/token",response_model=login)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    u = await authenticate_login(username=form_data.username,password=form_data.password,db=db)
    if not u:
        return False
    
    token = generateAccessToken(u.username,u.id,timedelta(minutes=1440))
    refresh = create_refresh_token(u.username,u.id,timedelta(minutes=(1440*150)))
    return {'access_token':token,'refresh_token':refresh,'token_type':'bearer','email' : u.email,"first_name":u.first_name,"last_name":u.last_name,"id":u.id,"username":u.username}

async def authenticate_login(username:str,password:str,db:db_dependency):
    
    u =db.query(Users).filter(Users.username == username).first()
    if not u:
        return False
    if not bcrypt_context.verify(password,u.hashed_password):
        return False
    return u

@router.post("/refresh",response_model=login)
async def refresh_login(refresh_token:str,db:db_dependency):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}        
    )
    try:
        x = 1
        payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=ALGORYTHM)
        id:int = payload.get("id")
        if id is None:
            return credential_exception
        u = db.query(Users).filter(Users.id == id).first()
        token = generateAccessToken(u.username,u.id,timedelta(minutes=1440))
        refresh = create_refresh_token(u.username,u.id,timedelta(minutes=(1440*150)))
        return {'access_token':token,'refresh_token':refresh,'token_type':'bearer','email' : u.email,"first_name":u.first_name,"last_name":u.last_name,"id":u.id,"username":u.username}
    except JWTError:
        raise credential_exception
    

        
    

def generateAccessToken(username:str,id:int,Expired_timespan:timedelta):
    encode = { 'sub': username,'id' : id}
    Expired_in = datetime.utcnow() + Expired_timespan
    encode.update({'exp' : Expired_in})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORYTHM)

def create_refresh_token(username:str,id:int,Expired_timespan:timedelta):
    encode = { 'sub':username,'id':id}
    Expired_in = datetime.utcnow() + Expired_timespan
    encode.update({'exp' : Expired_in})
    encoded_jwt = jwt.encode(encode, REFRESH_SECRET_KEY, algorithm=ALGORYTHM)
    return encoded_jwt

def verify_refresh_token(token:str):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}        
    )
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=ALGORYTHM)

        id:str = payload.get("id")
        if id is None:
            raise credential_exception
        userdata = id
    except JWTError:
        raise credential_exception

    return userdata

@router.post("/getUser")
def getUser(token: Annotated[str,Depends(oauth2_bearer)]):
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORYTHM)
    id:str = payload.get("id")
    username:str = payload.get("sub")
    if id is None or username is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item Not Found")
    return {"id":id,"username":username}

@router.get("/authorize")
async def authorize(oauth2_params: OAuth2AuthorizationCodeBearer = Depends()):
    # Redirect the user to the OAuth2 provider's authorization URL
    return {"message": "Redirect the user to the authorization URL"}
        
    
    
    
    