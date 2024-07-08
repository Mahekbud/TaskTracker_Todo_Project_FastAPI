from pydantic import BaseModel
from typing import Optional




class TodoAll(BaseModel):
    title : str
    description : str
    status : str
    priority : str
    priority_No : str
    assignee : str
    category_id : str
    u_id  : str
    
    
class TodoPatch(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    status: Optional[str] = None
    priority : Optional[str] = None
    assignee : Optional[str] = None
    category_id : Optional[str] = None
    u_id  : Optional[str] = None
    