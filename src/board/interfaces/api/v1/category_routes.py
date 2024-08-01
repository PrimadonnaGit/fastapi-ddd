from fastapi import APIRouter, Depends, HTTPException

from board.application.category.category_dto import (
    CategoryCreateDTO,
    CategoryResponseDTO,
)
from board.application.category.category_service import CategoryApplicationService
from board.domain.user.user import User
from ..dependencies import get_category_service, get_current_user

router = APIRouter()


@router.post("/", response_model=CategoryResponseDTO)
def create_category(
        category: CategoryCreateDTO,
        category_service: CategoryApplicationService = Depends(get_category_service),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can create categories")
    return category_service.create_category(category)


@router.get("/", response_model=list[CategoryResponseDTO])
def get_all_categories(
        category_service: CategoryApplicationService = Depends(get_category_service),
):
    return category_service.get_all_categories()


@router.put("/{category_id}", response_model=CategoryResponseDTO)
def update_category(
        category_id: int,
        category: CategoryCreateDTO,
        category_service: CategoryApplicationService = Depends(get_category_service),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can update categories")
    try:
        return category_service.update_category(category_id, category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{category_id}")
def delete_category(
        category_id: int,
        category_service: CategoryApplicationService = Depends(get_category_service),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admins can delete categories")
    try:
        category_service.delete_category(category_id)
        return {"message": "Category deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
