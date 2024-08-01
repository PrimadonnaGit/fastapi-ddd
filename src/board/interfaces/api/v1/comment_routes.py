from fastapi import APIRouter, Depends, HTTPException

from board.application.comment.comment_dto import (
    CommentCreateDTO,
    CommentResponseDTO,
    CommentUpdateDTO,
)
from board.application.comment.comment_service import CommentApplicationService
from board.domain.user.user import User
from ..dependencies import get_comment_service, get_current_user

router = APIRouter()


@router.post("/", response_model=CommentResponseDTO)
def create_comment(
        comment: CommentCreateDTO,
        comment_service: CommentApplicationService = Depends(get_comment_service),
        current_user: User = Depends(get_current_user),
):
    return comment_service.create_comment(comment, current_user.id)


@router.get("/post/{post_id}", response_model=list[CommentResponseDTO])
def get_comments_by_post(
        post_id: int,
        comment_service: CommentApplicationService = Depends(get_comment_service),
):
    return comment_service.get_comments_by_post(post_id)


@router.put("/{comment_id}", response_model=CommentResponseDTO)
def update_comment(
        comment_id: int,
        comment: CommentUpdateDTO,
        comment_service: CommentApplicationService = Depends(get_comment_service),
        current_user: User = Depends(get_current_user),
):
    try:
        return comment_service.update_comment(comment_id, comment, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.delete("/{comment_id}")
def delete_comment(
        comment_id: int,
        comment_service: CommentApplicationService = Depends(get_comment_service),
        current_user: User = Depends(get_current_user),
):
    try:
        comment_service.delete_comment(comment_id, current_user.id)
        return {"message": "Comment deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
