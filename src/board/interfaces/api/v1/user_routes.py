from fastapi import APIRouter, Depends, HTTPException

from board.application.user.user_dto import UserRegisterDTO, UserResponseDTO
from board.application.user.user_service import UserApplicationService
from ..dependencies import get_user_service

router = APIRouter()


@router.post("/register", response_model=UserResponseDTO)
def register_user(
        user: UserRegisterDTO,
        user_service: UserApplicationService = Depends(get_user_service),
):
    try:
        return user_service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(
        user_id: int, user_service: UserApplicationService = Depends(get_user_service)
):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(
        user_id: int,
        user: UserRegisterDTO,
        user_service: UserApplicationService = Depends(get_user_service),
):
    try:
        return user_service.update_user(user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{user_id}")
def delete_user(
        user_id: int, user_service: UserApplicationService = Depends(get_user_service)
):
    user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}
