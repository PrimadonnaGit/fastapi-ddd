from fastapi import APIRouter, Depends, HTTPException

from board.application.post.post_dto import (
    PostCreateDTO,
    PostResponseDTO,
    PostUpdateDTO,
)
from board.application.post.post_service import PostApplicationService
from board.domain.user.user import User
from ..dependencies import get_post_service, get_current_user

router = APIRouter()


@router.post("/", response_model=PostResponseDTO)
def create_post(
    post: PostCreateDTO,
    post_service: PostApplicationService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    return post_service.create_post(post, current_user.id)


@router.get("/{post_id}", response_model=PostResponseDTO)
def get_post(
    post_id: int, post_service: PostApplicationService = Depends(get_post_service)
):
    try:
        return post_service.get_post(post_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{post_id}", response_model=PostResponseDTO)
def update_post(
    post_id: int,
    post: PostUpdateDTO,
    post_service: PostApplicationService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    try:
        return post_service.update_post(post_id, post, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    post_service: PostApplicationService = Depends(get_post_service),
    current_user: User = Depends(get_current_user),
):
    try:
        post_service.delete_post(post_id, current_user.id)
        return {"message": "Post deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.get("/search", response_model=list[PostResponseDTO])
def search_posts(
    query: str, post_service: PostApplicationService = Depends(get_post_service)
):
    return post_service.search_posts(query)
