from fastapi import FastAPI,HTTPException,APIRouter,Header
from database.database import Sessionlocal
from passlib.context import CryptContext
from src.schemas.Category import categoryAll,categorypatch
from src.models.Category import Category
import uuid
from logs.Log_config import logger



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

categories = APIRouter(tags=["category"])

db = Sessionlocal()

#-----------------------create category--------------------------------

@categories.post("/create_category",response_model=categoryAll)
def create_category(user:categoryAll):
    logger.info("create new category")
  
    new_category= Category(
        id = str(uuid.uuid4()),
        name = user.name,
        description = user.description
    )
    logger.success("category is created.")
    logger.info("category adding to database.......")
    
    db.add(new_category)
    db.commit()
    logger.success("category created successfully")
    return new_category

#-------------------------------get id by category------------------------

@categories.get("/get_by_id_category",response_model=categoryAll)
def get_category(category_id : str):
    logger.info(f"Fetching category with id: {category_id}")
    
    db_category = db.query(Category).filter(Category.id == category_id,Category.is_active == True, Category.is_deleted == False).first()
    
    if db_category is None:
        logger.warning(f"Category not found with id: {category_id}")
        raise HTTPException(status_code=404, detail="category is not found")
    
    logger.success("Fetching Category successfully")
    return db_category

#-------------------------------get all category-----------------------------

@categories.get("/get_all_category",response_model=list[categoryAll])
def get_all_category():
    logger.info("Fetching all categories")
    
    db_category = db.query(Category).filter(Category.is_active == True, Category.is_deleted == False).all()
    
    if db_category is  None:
        logger.warning("No categories found")
        raise HTTPException(status_code=404,detail="category not found")
    
    logger.success("Fetching all Category successfully")
    return db_category

#---------------------------update category-------------------------

@categories.put("/update_category_by_put", response_model=categoryAll)
def update_category(cate: categoryAll,category_id : str):
    logger.info(f"Updating category with id: {category_id}")
    
    db_category = db.query(Category).filter(Category.id == category_id, Category.is_active == True, Category.is_deleted == False).first()
    
    if db_category is None:
        logger.warning(f"Category not found with id: {category_id}")
        raise HTTPException(status_code=404, detail="category not found")
    
    db_category.name = cate.name
    db_category.description = cate.description
    
    db.commit()
    logger.success("Category updated successfully")
    return db_category

#---------------------------update patch category----------------------------------


@categories.patch("/update_categories_by_patch",response_model=categorypatch)
def update_todo_patch(todos : categorypatch ,category_id : str):
    logger.info(f"Updating category with id: {category_id} using patch")

    db_category = db.query(Category).filter(Category.id == category_id , Category.is_active == True, Category.is_deleted == False).first()
  
    if db_category is None:
        logger.warning(f"Category not found with id: {category_id}")
        raise HTTPException (status_code=404,detail="category not found")
    
    for key,value in todos.dict(exclude_unset=True).items():
        setattr(db_category,key,value)
    
    db.commit()
    logger.success("Category updated successfully using patch")
    
    return db_category

#------------------------------delete category--------------------------------

@categories.delete("/delete_category_by_id")
def delete_category_by_id(category_id : str ):
    logger.info(f"Deleting category with id: {category_id}") 
    
    db_category = db.query(Category).filter(Category.id == category_id ,Category.is_active ==True,Category.is_deleted == False).first()
    if db_category is None:
        logger.warning(f"Category not found with id: {category_id}")
        raise HTTPException(status_code=404,detail= "category not found")
    
    db_category.is_active=False
    db_category.is_deleted =True
    db.commit()
    logger.success("Category deleted successfully")
    return {"message": "category deleted successfully"}

