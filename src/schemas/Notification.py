from pydantic import BaseModel
from typing import Optional




class NotificationAll(BaseModel):
    message : str
    recipient : str
    status : str
    u_id : str

class NotificationPatch(BaseModel):
    message : Optional[str] = None
    recipient : Optional[str] = None
    status: Optional[str] = None
    u_id  : Optional[str] = None    