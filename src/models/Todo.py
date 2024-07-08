from sqlalchemy import Column,String,ForeignKey,DateTime,Boolean
from datetime import datetime
import uuid
from database.database import Base




class Todo(Base):
    __tablename__ = 'TodoInfo'
    
    id = Column(String(100), primary_key=True, default=str(uuid.uuid4()))
    title = Column(String(500), nullable=False)
    description = Column(String(1000), nullable=False)
    status = Column(String(200), nullable=False, default="pending")  
    priority = Column(String(100), nullable=False)  
    priority_No = Column(String(100),nullable=False)
    assignee = Column(String(100), nullable=False)
    category_id = Column(String(100), ForeignKey('CategoryInfo.id'), nullable=False)
    u_id = Column(String(100), ForeignKey('UserInfo.id'), nullable=False)
    create_at = Column(DateTime, default=datetime.now)
    modified_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
  