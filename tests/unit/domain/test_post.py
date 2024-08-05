# tests/unit/domain/test_post_aggregate.py

import pytest

from board.domain.comment.comment import Comment
from board.domain.file.file import File
from board.domain.post.post import Post
from board.domain.post.post_aggregate import PostAggregate


@pytest.fixture
def post():
    return Post(id=1, title="Test Post", content="Content", user_id=1, category_id=1)


@pytest.fixture
def post_aggregate(post):
    return PostAggregate(post)


def test_add_comment(post_aggregate):
    comment = Comment(id=1, content="Test comment", user_id=1, post_id=1)
    post_aggregate.add_comment(comment)
    assert len(post_aggregate.comments) == 1
    assert post_aggregate.comments[0] == comment


def test_add_comment_wrong_post_id(post_aggregate):
    comment = Comment(id=1, content="Test comment", user_id=1, post_id=2)
    with pytest.raises(ValueError):
        post_aggregate.add_comment(comment)


def test_remove_comment(post_aggregate):
    comment1 = Comment(id=1, content="Comment 1", user_id=1, post_id=1)
    comment2 = Comment(id=2, content="Comment 2", user_id=1, post_id=1)
    post_aggregate.comments = [comment1, comment2]

    post_aggregate.remove_comment(1)
    assert len(post_aggregate.comments) == 1
    assert post_aggregate.comments[0] == comment2


def test_add_file(post_aggregate):
    file = File(id=1, filename="test.txt", post_id=1, filepath="path/to/file.txt")
    post_aggregate.add_file(file)
    assert len(post_aggregate.files) == 1
    assert post_aggregate.files[0] == file


def test_add_file_wrong_post_id(post_aggregate):
    file = File(id=1, filename="test.txt", post_id=2, filepath="path/to/file.txt")
    with pytest.raises(ValueError):
        post_aggregate.add_file(file)


def test_remove_file(post_aggregate):
    file1 = File(id=1, filename="file1.txt", post_id=1, filepath="path/to/file1.txt")
    file2 = File(id=2, filename="file2.txt", post_id=1, filepath="path/to/file2.txt")
    post_aggregate.files = [file1, file2]

    post_aggregate.remove_file(1)
    assert len(post_aggregate.files) == 1
    assert post_aggregate.files[0] == file2


def test_update_post(post_aggregate):
    post_aggregate.update_post("New Title", "New Content", 2)
    assert post_aggregate.post.title == "New Title"
    assert post_aggregate.post.content == "New Content"
    assert post_aggregate.post.category_id == 2
    assert post_aggregate.post.updated_at is not None


def test_update_post_partial(post_aggregate):
    original_title = post_aggregate.post.title
    original_category_id = post_aggregate.post.category_id
    post_aggregate.update_post(None, "New Content", None)
    assert post_aggregate.post.title == original_title
    assert post_aggregate.post.content == "New Content"
    assert post_aggregate.post.category_id == original_category_id
    assert post_aggregate.post.updated_at is not None
