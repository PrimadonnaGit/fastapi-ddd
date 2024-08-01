from board.domain.post.post import Post
from board.domain.post.post_repository import PostRepository
from .post_dto import PostCreateDTO, PostResponseDTO, PostUpdateDTO


class PostApplicationService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create_post(self, post_dto: PostCreateDTO, user_id: int) -> PostResponseDTO:
        post = Post(
            title=post_dto.title,
            content=post_dto.content,
            is_admin_post=post_dto.is_admin_post,
            category_id=post_dto.category_id,
            user_id=user_id,
            tags=post_dto.tags,
        )
        saved_post = self.post_repository.save(post)
        return PostResponseDTO.model_validate(saved_post)

    def get_post(self, id: int) -> PostResponseDTO:
        post = self.post_repository.find_by_id(id)
        if not post:
            raise ValueError("Post not found")
        return PostResponseDTO.model_validate(post)

    def update_post(
            self, id: int, post_dto: PostUpdateDTO, user_id: int
    ) -> PostResponseDTO:
        post = self.post_repository.find_by_id(id)
        if not post:
            raise ValueError("Post not found")
        if post.user_id != user_id:
            raise ValueError("You don't have permission to update this post")

        post.title = post_dto.title
        post.content = post_dto.content
        post.category_id = post_dto.category_id
        post.tags = post_dto.tags

        updated_post = self.post_repository.update(post)
        return PostResponseDTO.model_validate(updated_post)

    def delete_post(self, id: int, user_id: int) -> None:
        post = self.post_repository.find_by_id(id)
        if not post:
            raise ValueError("Post not found")
        if post.user_id != user_id:
            raise ValueError("You don't have permission to delete this post")
        self.post_repository.delete(id)

    def search_posts(self, query: str) -> list[PostResponseDTO]:
        posts = self.post_repository.search(query)
        return [PostResponseDTO.model_validate(post) for post in posts]
