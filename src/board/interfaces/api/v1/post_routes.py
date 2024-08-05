from fastapi import APIRouter, Depends, HTTPException, Body, Path, Query

from board.application.post.post_dto import (
    PostCreateDTO,
    PostResponseDTO,
    PostUpdateDTO,
    PostSearchDTO,
)
from board.application.post.post_service import PostApplicationService
from board.domain.user.user import User
from ..dependencies import get_post_service, get_current_user

router = APIRouter()


@router.post("/", response_model=PostResponseDTO)
def create_post(
    post_create_dto: PostCreateDTO = Body(...),
    post_service: PostApplicationService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    return post_service.create_post(post_create_dto, current_user.id)


@router.get("/search", response_model=list[PostSearchDTO])
def search_posts(
    query: str = Query(min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    post_service: PostApplicationService = Depends(get_post_service),
):
    return post_service.search_posts(query, skip, limit)


@router.get("/{post_id}", response_model=PostResponseDTO)
def get_post(
    post_id: int = Path(...),
    post_service: PostApplicationService = Depends(get_post_service),
):
    try:
        return post_service.get_post(post_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{post_id}", response_model=PostResponseDTO)
def update_post(
    post_id: int = Path(...),
    post_update_dto: PostUpdateDTO = Body(...),
    post_service: PostApplicationService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return post_service.update_post(post_id, post_update_dto, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{post_id}")
def delete_post(
    post_id: int = Path(...),
    post_service: PostApplicationService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    try:
        post_service.delete_post(post_id, current_user.id)
        return {"message": "Post deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
