from typing import Optional
from fastapi import FastAPI, HTTPException, Path,Request,Body
from pydantic import BaseModel, Field
from fastapi import status

class taskRequest(BaseModel):
    title:str = Field(min_length=3)
    Description:str = Field(min_length=3)
    priority:int = Field(gt=0)
    complete:bool
    
    
    def __init__(self,title,Description,priority,complete):
        super().__init__(Description=Description,title=title,priority=priority,complete=complete)
   
    class Config:
        json_schema_extra = {
            "example":{
            "Description": "Details about my task",
            "title":"Do some learning",
            "priority":1,
            "complete":False
            }
            
        }
    