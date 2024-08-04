from fastapi import APIRouter, Depends, HTTPException, Body, Path

from board.application.user.user_dto import (
    UserRegisterDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from board.application.user.user_service import UserApplicationService
from board.domain.user.user import User
from ..dependencies import get_user_service, get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponseDTO)
def register_user(
    user_register_dto: UserRegisterDTO = Body(...),
    user_service: UserApplicationService = Depends(get_user_service),
):
    try:
        return user_service.register_user(user_register_dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(
    user_id: int = Path(...),
    user_service: UserApplicationService = Depends(get_user_service),
):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(
    user_id: int = Path(...),
    user_update_dto: UserUpdateDTO = Body(...),
    user_service: UserApplicationService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        return user_service.update_user(user_id, user_update_dto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete_user(
    user_id: int = Path(...),
    user_service: UserApplicationService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Permission denied")

    user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}
