from pydantic import BaseModel
from typing import Optional



class categoryAll(BaseModel):
    name : str
    description : str
    
class categorypatch(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None