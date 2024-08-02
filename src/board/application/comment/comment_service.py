from board.domain.comment.comment import Comment
from board.domain.comment.comment_repository import CommentRepository
from .comment_dto import CommentCreateDTO, CommentResponseDTO, CommentUpdateDTO


class CommentApplicationService:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def create_comment(
        self, comment_dto: CommentCreateDTO, user_id: int
    ) -> CommentResponseDTO:
        comment = Comment(
            content=comment_dto.content,
            post_id=comment_dto.post_id,
            user_id=user_id,
            parent_comment_id=comment_dto.parent_comment_id,
        )
        saved_comment = self.comment_repository.save(comment)
        return CommentResponseDTO.model_validate(saved_comment)

    def get_comments_by_post(self, post_id: int) -> list[CommentResponseDTO]:
        comments = self.comment_repository.find_by_post_id(post_id)
        return [CommentResponseDTO.model_validate(comment) for comment in comments]

    def update_comment(
        self, id: int, comment_dto: CommentUpdateDTO, user_id: int
    ) -> CommentResponseDTO:
        comment = self.comment_repository.find_by_id(id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.user_id != user_id:
            raise ValueError("You don't have permission to update this comment")

        comment.content = comment_dto.content
        updated_comment = self.comment_repository.update(comment)
        return CommentResponseDTO.model_validate(updated_comment)

    def delete_comment(self, id: int, user_id: int) -> None:
        comment = self.comment_repository.find_by_id(id)
        if not comment:
            raise ValueError("Comment not found")
        if comment.user_id != user_id:
            raise ValueError("You don't have permission to delete this comment")
        self.comment_repository.delete(id)
