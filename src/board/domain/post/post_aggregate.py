from datetime import datetime

from board.domain.comment.comment import Comment
from board.domain.file.file import File
from board.domain.post.post import Post


class PostAggregate:
    def __init__(self, post: Post):
        self.post = post
        self.comments: list[Comment] = []
        self.files: list[File] = []

    def add_comment(self, comment: Comment) -> None:
        if comment.post_id != self.post.id:
            raise ValueError("Comment does not belong to this post")
        self.comments.append(comment)

    def remove_comment(self, comment_id: int) -> None:
        self.comments = [c for c in self.comments if c.id != comment_id]

    def add_file(self, file: File) -> None:
        if file.post_id != self.post.id:
            raise ValueError("File does not belong to this post")
        self.files.append(file)

    def remove_file(self, file_id: int) -> None:
        self.files = [f for f in self.files if f.id != file_id]

    def update_post(self, title: str, content: str, category_id: int) -> None:
        self.post.title = title
        self.post.content = content
        self.post.category_id = category_id
        self.post.updated_at = datetime.utcnow()
