"""
API Routes for Kaivora API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import logging
from app.models.schemas import (
    APIResponse,
    ItemCreate,
    ItemResponse,
    ItemUpdate,
    ErrorResponse
)
from app.db.base import get_db
from app.db.models import Item

# Setup logger
logger = logging.getLogger(__name__)

# Create API router
api_router = APIRouter()

@api_router.get(
    "/",
    response_model=APIResponse,
    summary="API Information",
    description="Get basic information about the Kaivora API"
)
async def api_info():
    """
    Get API information and available endpoints
    
    Returns:
        APIResponse: API information
    """
    return APIResponse(
        message="Kaivora API is running successfully",
        data={
            "endpoints": [
                "GET /api/v1/ - API Information",
                "GET /api/v1/items - List all items",
                "POST /api/v1/items - Create new item",
                "GET /api/v1/items/{item_id} - Get specific item",
                "PUT /api/v1/items/{item_id} - Update specific item",
                "DELETE /api/v1/items/{item_id} - Delete specific item"
            ]
        }
    )

@api_router.get(
    "/items",
    response_model=List[ItemResponse],
    summary="List Items",
    description="Retrieve all items from the system"
)
async def list_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all items with optional pagination
    
    Args:
        skip (int): Number of items to skip
        limit (int): Maximum number of items to return
        db (Session): Database session
    
    Returns:
        List[ItemResponse]: List of items
    """
    logger.info(f"Listing items with skip={skip}, limit={limit}")
    
    items = db.query(Item).offset(skip).limit(limit).all()
    
    return [ItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        is_active=item.is_active,
        created_at=item.created_at,
        updated_at=item.updated_at
    ) for item in items]

@api_router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Item",
    description="Create a new item in the system"
)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item
    
    Args:
        item (ItemCreate): Item data to create
        db (Session): Database session
    
    Returns:
        ItemResponse: Created item with ID
    """
    logger.info(f"Creating new item: {item.name}")
    
    db_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        is_active=True
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return ItemResponse(
        id=db_item.id,
        name=db_item.name,
        description=db_item.description,
        price=db_item.price,
        is_active=db_item.is_active,
        created_at=db_item.created_at,
        updated_at=db_item.updated_at
    )

@api_router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="Get Item",
    description="Retrieve a specific item by ID"
)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific item by ID
    
    Args:
        item_id (int): ID of the item to retrieve
        db (Session): Database session
    
    Returns:
        ItemResponse: Item data
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Retrieving item with ID: {item_id}")
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    if db_item is None:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    return ItemResponse(
        id=db_item.id,
        name=db_item.name,
        description=db_item.description,
        price=db_item.price,
        is_active=db_item.is_active,
        created_at=db_item.created_at,
        updated_at=db_item.updated_at
    )

@api_router.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="Update Item",
    description="Update a specific item by ID"
)
async def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    """
    Update a specific item
    
    Args:
        item_id (int): ID of the item to update
        item_update (ItemUpdate): Updated item data
        db (Session): Database session
    
    Returns:
        ItemResponse: Updated item data
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Updating item with ID: {item_id}")
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    if db_item is None:
        logger.warning(f"Item not found for update: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    # Update only provided fields
    update_data = item_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    
    return ItemResponse(
        id=db_item.id,
        name=db_item.name,
        description=db_item.description,
        price=db_item.price,
        is_active=db_item.is_active,
        created_at=db_item.created_at,
        updated_at=db_item.updated_at
    )

@api_router.delete(
    "/items/{item_id}",
    response_model=APIResponse,
    summary="Delete Item",
    description="Delete a specific item by ID"
)
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific item
    
    Args:
        item_id (int): ID of the item to delete
        db (Session): Database session
    
    Returns:
        APIResponse: Deletion confirmation
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Deleting item with ID: {item_id}")
    
    db_item = db.query(Item).filter(Item.id == item_id).first()
    
    if db_item is None:
        logger.warning(f"Item not found for deletion: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    item_name = db_item.name
    db.delete(db_item)
    db.commit()
    
    return APIResponse(
        message=f"Item '{item_name}' deleted successfully",
        data={"deleted_item_id": item_id}
    )