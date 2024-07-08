from  fastapi import HTTPException,APIRouter
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.Todo import TodoAll,TodoPatch
from src.models.Todo import Todo
import uuid
from logs.Log_config import logger




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

Todos = APIRouter(tags=["TODO"])

db = Sessionlocal()

#---------------------------create todo---------------------------------

@Todos.post("/create_Todo",response_model=TodoAll)
def create_Todo(user:TodoAll):
    logger.info("Creating a new todo")
  
    new_user= Todo(
        id = str(uuid.uuid4()),
        title = user.title,
        description = user.description,
        status = user.status,
        priority = user.priority,
        priority_No = user.priority_No,
        assignee = user.assignee,
        category_id = user.category_id,
        u_id = user.u_id
           
    )
    logger.success("todo is created.")
    logger.info("todo adding to database.......")
    
    db.add(new_user)
    logger.info("todo loaded successfully")
    
    db.commit()
    logger.success("todo database has been saved successfully.")
    
    return new_user

#-------------------------------get todos by id----------------------------

@Todos.get("/get_todos_by_id", response_model=TodoAll)
def get_todos_by_id(todo_id: str):
    logger.info(f"Getting todo by id: {todo_id}")
    todo = db.query(Todo).filter(Todo.id == todo_id,Todo.is_active ==True,Todo.is_deleted == False).first()
    
    if todo is None:
        logger.warning(f"Todo not found with id: {todo_id}")
        raise HTTPException(status_code=404, detail="todo is not found")
    
    logger.success("Getting todo by id successfully")
    return todo

#----------------------------get todos all------------------------------

@Todos.get("/get_all_todo",response_model=list[TodoAll])
def get_all_todo():
    logger.info("Getting all todos")
    todo = db.query(Todo).filter(Todo.is_active ==True,Todo.is_deleted == False).all()
    
    if todo is  None:
        logger.warning("No todos found")
        raise HTTPException(status_code=404,detail="todo not found")
    
    logger.success("Getting todos by id successfully")
    return todo

#---------------------------update todos----------------------------

@Todos.put("/todos_update", response_model=TodoAll)
def update_todo(todo_id: str, todo: TodoAll):
    logger.info(f"Updating todo with id: {todo_id}")
    db_todo = db.query(Todo).filter(Todo.id == todo_id,Todo.is_active ==True,Todo.is_deleted == False).first()
    
    if db_todo is None:
        logger.warning(f"Todo not found with id: {todo_id}")
        raise HTTPException(status_code=404, detail= "todos not found")
    
    db_todo.title= todo.title,
    db_todo.description= todo.description,
    db_todo.status= todo.status,
    db_todo.priority= todo.priority,
    db_todo.assignee= todo.assignee,
    db_todo.category_id= todo.category_id,
    db_todo.u_id= todo.u_id
   
    db.commit()
    logger.success("todo database has updated saved successfully.")
    
    return db_todo

#------------------------patch todos--------------------------

@Todos.patch("/update_todo_by_patch",response_model=TodoPatch)
def update_todo_patch(todos : TodoPatch ,todos_id : str):
    logger.info(f"Updating todo with id: {todos_id} using patch")
    
    db_todo = db.query(Todo).filter(Todo.id == todos_id , Todo.is_active ==True,Todo.is_deleted == False).first()
  
    if db_todo is None:
        logger.warning(f"Todo not found with id: {todos_id}")
        raise HTTPException (status_code=404,detail="todo not found")
    
    for key,value in todos.dict(exclude_unset=True).items():
        setattr(db_todo,key,value)
    
    db.commit()
    logger.success("Todo updated successfully using patch")
    
    return db_todo


#---------------------delete todos---------------------------


@Todos.delete("/delete_user_by_id")
def delete_user(todo_id : str ):
    logger.info(f"Deleting todo with id: {todo_id}")
    db_todo = db.query(Todo).filter(Todo.id == todo_id ,Todo.is_active ==True,Todo.is_deleted == False).first()
    if db_todo is None:
        logger.warning(f"Todo not found with id: {todo_id}")
        raise HTTPException(status_code=404,detail= "todos not found")
    
    db_todo.is_active=False
    db_todo.is_deleted =True
    db.commit()
    logger.success(f"Deleted todo with id: {todo_id} successfully")
    return {"message": "todos deleted successfully"}


#---------------------list todos by category_id-----------------------

@Todos.get("/search_todo_by_category_id")
def read_todo_by_category(category_id: str):
    logger.info(f"Fetching todos for category id: {category_id}")
    
    db_todo = db.query(Todo).filter(Todo.category_id == category_id,Todo.is_active==True,Todo.is_deleted==False).all()
    
    if not db_todo:
        logger.warning(f"No todos found for category id: {category_id}")
        raise HTTPException(status_code=404, detail="No todos found for the given category")
    
    logger.success("Fetching todos successfully")
    return db_todo

#---------------------list todos by status-----------------------

@Todos.get("/search_todo_by_status")
def read_todo_by_status(status: str):
    logger.info(f"Fetching todos with status: {status}")
    
    if status not in ["pending", "progress", "completed"]:
        logger.error(f"Invalid status provided: {status}")
        raise HTTPException(status_code=400, detail="Invalid status provided.")

    db_todos = db.query(Todo).filter(Todo.status == status,Todo.is_active,Todo.is_deleted == False).all()
    
    if not db_todos:
        logger.warning(f"No todos found with status: {status}")
        raise HTTPException(status_code=404, detail=f"No todos found with status '{status}'")
    
    logger.success(f"Retrieved todos with status '{status}' successfully")
    return db_todos

#--------------------list todos by priority----------------------------

@Todos.get("/search_todo_by_priority")
def read_todo_by_priority(priority: str):
    logger.info(f"Fetching todos with priority: {priority}")
    
    if priority not in ["low", "mid", "high"]:
        logger.error(f"Invalid priority provided: {priority}")
        raise HTTPException(status_code=400, detail="Invalid priority provided.")

    db_todos = db.query(Todo).filter(Todo.priority == priority,Todo.is_active,Todo.is_deleted == False).all()
    
    if not db_todos:
        logger.warning(f"No todos found with priority: {priority}")
        raise HTTPException(status_code=404, detail=f"No todos found with priority '{priority}'")
    
    logger.success(f"Retrieved todos with priority '{priority}' successfully")
    return db_todos

#---------------------list todos by priority no----------------------------


@Todos.get("/search_todo_by_priority_no", response_model=list[TodoAll])
def read_todo_by_priority_no(priority: str):
    logger.info(f"Fetching todos ordered by priority number for priority: {priority}")
    
    if priority not in ["low", "mid", "high"]:
        logger.error(f"Invalid priority provided: {priority}")
        raise HTTPException(status_code=400, detail="Invalid priority provided.")

    db_todos = db.query(Todo).filter(Todo.priority == priority,Todo.is_active == True,Todo.is_deleted == False).all()
    
    if not db_todos:
        logger.warning(f"No todos found with priority: {priority}")
        raise HTTPException(status_code=404, detail="No todos found with priority")
    
    sorted_todos = sorted(db_todos, key=lambda todo: todo.priority_No)
    
    # def get_priority_no(todo: Todo):
    #      return todo.priority_No
     
    # sorted_todos = sorted(db_todos, key=get_priority_no)
    
    logger.success(f"Retrieved and sorted todos with priority '{priority}' by priority number successfully")
    return sorted_todos

#--------------------------list todods by user id-------------------------------

@Todos.get("/search_todo_by_user_id")
def read_todo_by_user(u_id: str):
    logger.info(f"Fetching todos for user with id: {u_id}")
    
    db_todo = db.query(Todo).filter(Todo.u_id == u_id,Todo.is_active==True,Todo.is_deleted==False).all()
    
    if not db_todo:
        logger.warning(f"No todos found for user with id: {u_id}")
        raise HTTPException(status_code=404, detail="No todos found for the given user")
    
    logger.success(f"Retrieved todos for user with id: {u_id} successfully")
    return db_todo
