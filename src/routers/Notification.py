from fastapi import HTTPException, APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.Notification import NotificationAll
from src.models.User import User
from src.models.Todo import Todo
from src.models.Notification import Notification
from dotenv import load_dotenv
from src.utils.Email import send_notification_via_email
from logs.Log_config import logger
import uuid
from src.utils.Token import decode_token_user_id


load_dotenv()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Notifications = APIRouter(tags=["Notification"])
db = Sessionlocal()


#----------------------------create notification--------------------------------

@Notifications.post("/notifications/", response_model=list[NotificationAll])
def create_notification(token : str):
    logger.info("Creating a new notification")
    user_id = decode_token_user_id(token)
    pending_todos = db.query(Todo).filter(Todo.status == "pending", Todo.u_id == user_id, Todo.is_active == True, Todo.is_deleted == False).all()
    
    if not pending_todos:
        logger.info("No pending todos found to send notifications")
        raise HTTPException(status_code=404,detail="No pending todos found to send notifications")
       
    todo_messages = "\n".join([f"- {todo.title}" for todo in pending_todos])
    message = f"Tasks pending and needing attention:\n{todo_messages}"
    
    notifications_sent = []
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"User not found for todo with ID: {user_id}")
        raise HTTPException(status_code=404,detail="user not found")

        
    notification_record = Notification(
            id=str(uuid.uuid4()),
            message=message,
            recipient=user.email,
            status='unread',
            u_id=user.id
    
        )
    logger.success("Notification is created.")
    logger.info("Notification adding to database...")

    db.add(notification_record)
    db.commit()
        
    logger.success("Notification created successfully")
    logger.info(f"Notification created for user: {user.email}, Message: {notification_record.message}")

    if send_notification_via_email(user.email, notification_record.message):
            logger.success(f"Notification sent via email successfully to {user.email}")
            notification_record.status = 'read'
            db.commit()
            notifications_sent.append(notification_record)
    else:
            logger.error(f"Failed to send notification via email to {user.email}")
            raise HTTPException(status_code=500, detail="Failed to send notification via email")
    
    logger.success("Notification send successfully")
    
    return notifications_sent




