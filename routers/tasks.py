from fastapi import Depends, HTTPException,APIRouter
import dbmodels.task 
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from dbmodels.task import task
from models.taskRequest import taskRequest
from .auth import getUser


router = APIRouter()


dbmodels.task.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(getUser)]

@router.get("/tasks")
async def read_all(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    return db.query(task).filter(task.CreatedBy == user.get('id')).all()

@router.get("/task/{id}")
async def read_by_id(db: db_dependency,id:int):
    retval = db.query(task).filter(task.id == id).first()
    if retval is not None:
        return retval
    else:
        raise HTTPException(status_code=404,detail="Item not found")


@router.post("/task")
async def create(user:user_dependency,db: db_dependency,t:taskRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    obj = task(**t.model_dump(),CreatedBy = user.get('id'))    
    db.add(obj)
    db.commit()
    
# @router.post("/task")
# async def create(db: db_dependency,t:taskRequest):
   
#     obj = task(**t.model_dump(),CreatedBy = 1)    
#     db.add(obj)
#     db.commit()

@router.put("/task{id}")
async def create(user:user_dependency,db: db_dependency,id:int,t:taskRequest):
    if user is None:
        raise HTTPException(status_code=401,detail="Authentication failed")
    valToUpdate = db.query(task).filter(task.id == id).filter(task.CreatedBy == user.get('id')).first()
    if valToUpdate is None:
        return HTTPException(status_code=404,detail="Item not found")
    valToUpdate.complete = t.complete
    valToUpdate.Description = t.Description
    valToUpdate.priority = t.priority
    valToUpdate.title = t.title
    db.add(valToUpdate)
    db.commit()
    
@router.delete("/task{id}")
async def create(db: db_dependency,id:int):
    valToUpdate = db.query(task).filter(task.id == id).first()
    if valToUpdate is None:
        return HTTPException(status_code=404,detail="Item not found")
    db.query(task).filter(task.id == id).delete()
    db.commit()
    