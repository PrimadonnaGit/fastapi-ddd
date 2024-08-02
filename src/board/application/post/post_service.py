from board.domain.post.post import Post
from board.domain.post.post_repository import PostRepository
from .post_dto import PostCreateDTO, PostResponseDTO, PostUpdateDTO, PostSearchDTO
from ...domain.comment.comment import Comment
from ...domain.post.post_aggregate import PostAggregate


class PostApplicationService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create_post(self, post_dto: PostCreateDTO, user_id: int) -> PostResponseDTO:
        post = Post(
            title=post_dto.title,
            content=post_dto.content,
            user_id=user_id,
            category_id=post_dto.category_id,
        )
        post_aggregate = PostAggregate(post)
        saved_aggregate = self.post_repository.save(post_aggregate)
        return PostResponseDTO.from_aggregate(saved_aggregate)

    def get_post(self, post_id: int) -> PostResponseDTO:
        post_aggregate = self.post_repository.find_by_id(post_id)
        return PostResponseDTO.from_aggregate(post_aggregate)

    def add_comment(self, post_id: int, content: str, user_id: int) -> PostResponseDTO:
        post_aggregate = self.post_repository.find_by_id(post_id)
        comment = Comment(content=content, user_id=user_id, post_id=post_id)
        post_aggregate.add_comment(comment)
        updated_aggregate = self.post_repository.save(post_aggregate)
        return PostResponseDTO.from_aggregate(updated_aggregate)

    def update_post(
        self, post_id: int, post_dto: PostUpdateDTO, user_id: int
    ) -> PostResponseDTO:
        post_aggregate = self.post_repository.find_by_id(post_id)
        if post_aggregate.post.user_id != user_id:
            raise ValueError("User does not have permission to update this post")

        post_aggregate.update_post(
            post_dto.title, post_dto.content, post_dto.category_id
        )
        updated_aggregate = self.post_repository.save(post_aggregate)
        return PostResponseDTO.from_aggregate(updated_aggregate)

    def delete_post(self, id: int, user_id: int) -> None:
        post = self.post_repository.find_by_id(id)
        if not post:
            raise ValueError("Post not found")
        if post.user_id != user_id:
            raise ValueError("You don't have permission to delete this post")
        self.post_repository.delete(id)

    def search_posts(
        self, query: str, skip: int = 0, limit: int = 20
    ) -> list[PostSearchDTO]:
        post_aggregates = self.post_repository.search(query, skip, limit)
        return [
            PostSearchDTO.from_aggregate(aggregate) for aggregate in post_aggregates
        ]
