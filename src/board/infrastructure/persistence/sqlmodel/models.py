from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True, index=True)
    nickname: str = Field(unique=True, index=True)
    password: str
    is_admin: bool = Field(default=False)
    create_time: datetime = Field(default_factory=datetime.utcnow)
    is_withdraw: bool = Field(default=False)


class CategoryModel(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    posts: list["PostModel"] = Relationship(back_populates="category")


class PostModel(SQLModel, table=True):
    __tablename__ = "posts"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    content: str
    is_admin_post: bool = Field(default=False)
    views: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)

    category_id: int | None = Field(default=None, foreign_key="categories.id")
    user_id: int = Field(foreign_key="users.id")

    category: CategoryModel | None = Relationship(back_populates="posts")
    comments: list["CommentModel"] = Relationship(back_populates="post")
    files: list["FileModel"] = Relationship(back_populates="post")


class CommentModel(SQLModel, table=True):
    __tablename__ = "comments"

    id: int | None = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)

    post_id: int = Field(foreign_key="posts.id")
    user_id: int = Field(foreign_key="users.id")
    parent_comment_id: int | None = Field(default=None, foreign_key="comments.id")

    post: PostModel = Relationship(back_populates="comments")


class FileModel(SQLModel, table=True):
    __tablename__ = "files"

    id: int | None = Field(default=None, primary_key=True)
    filename: str
    filepath: str

    post_id: int = Field(foreign_key="posts.id")

    post: PostModel = Relationship(back_populates="files")
