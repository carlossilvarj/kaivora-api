"""
API Routes for Kaivora API
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
from app.models.schemas import (
    APIResponse,
    ItemCreate,
    ItemResponse,
    ItemUpdate,
    ErrorResponse
)

# Setup logger
logger = logging.getLogger(__name__)

# Create API router
api_router = APIRouter()

# In-memory storage for demonstration (replace with database in production)
items_db = {}
item_counter = 0

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
    limit: int = 100
):
    """
    List all items with optional pagination
    
    Args:
        skip (int): Number of items to skip
        limit (int): Maximum number of items to return
    
    Returns:
        List[ItemResponse]: List of items
    """
    logger.info(f"Listing items with skip={skip}, limit={limit}")
    
    items = list(items_db.values())
    paginated_items = items[skip:skip + limit]
    
    return paginated_items

@api_router.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Item",
    description="Create a new item in the system"
)
async def create_item(item: ItemCreate):
    """
    Create a new item
    
    Args:
        item (ItemCreate): Item data to create
    
    Returns:
        ItemResponse: Created item with ID
    """
    global item_counter
    item_counter += 1
    
    logger.info(f"Creating new item: {item.name}")
    
    new_item = ItemResponse(
        id=item_counter,
        name=item.name,
        description=item.description,
        price=item.price,
        is_active=True
    )
    
    items_db[item_counter] = new_item
    
    return new_item

@api_router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="Get Item",
    description="Retrieve a specific item by ID"
)
async def get_item(item_id: int):
    """
    Get a specific item by ID
    
    Args:
        item_id (int): ID of the item to retrieve
    
    Returns:
        ItemResponse: Item data
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Retrieving item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Item not found: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    return items_db[item_id]

@api_router.put(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="Update Item",
    description="Update a specific item by ID"
)
async def update_item(item_id: int, item_update: ItemUpdate):
    """
    Update a specific item
    
    Args:
        item_id (int): ID of the item to update
        item_update (ItemUpdate): Updated item data
    
    Returns:
        ItemResponse: Updated item data
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Updating item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Item not found for update: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    current_item = items_db[item_id]
    
    # Update only provided fields
    update_data = item_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(current_item, field, value)
    
    items_db[item_id] = current_item
    
    return current_item

@api_router.delete(
    "/items/{item_id}",
    response_model=APIResponse,
    summary="Delete Item",
    description="Delete a specific item by ID"
)
async def delete_item(item_id: int):
    """
    Delete a specific item
    
    Args:
        item_id (int): ID of the item to delete
    
    Returns:
        APIResponse: Deletion confirmation
    
    Raises:
        HTTPException: If item not found
    """
    logger.info(f"Deleting item with ID: {item_id}")
    
    if item_id not in items_db:
        logger.warning(f"Item not found for deletion: {item_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    
    deleted_item = items_db.pop(item_id)
    
    return APIResponse(
        message=f"Item '{deleted_item.name}' deleted successfully",
        data={"deleted_item_id": item_id}
    )
