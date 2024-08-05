from unittest.mock import Mock

import pytest

from board.application.post.post_dto import PostCreateDTO, PostUpdateDTO
from board.application.post.post_service import PostApplicationService
from board.domain.post.post import Post
from board.domain.post.post_aggregate import PostAggregate


@pytest.fixture
def mock_post_repository():
    return Mock()


@pytest.fixture
def post_service(mock_post_repository):
    return PostApplicationService(mock_post_repository)


def test_create_post(post_service, mock_post_repository):
    post_create_dto = PostCreateDTO(title="Test Post", content="Content", category_id=1)
    user_id = 1

    mock_post_repository.save.return_value = PostAggregate(
        Post(id=1, title="Test Post", content="Content", user_id=user_id, category_id=1)
    )

    result = post_service.create_post(post_create_dto, user_id)

    assert result.title == "Test Post"
    assert result.content == "Content"
    mock_post_repository.save.assert_called_once()


def test_get_post(post_service, mock_post_repository):
    post_id = 1
    mock_post_repository.find_by_id.return_value = PostAggregate(
        Post(id=post_id, title="Test Post", content="Content", user_id=1, category_id=1)
    )

    result = post_service.get_post(post_id)

    assert result.id == post_id
    assert result.title == "Test Post"
    mock_post_repository.find_by_id.assert_called_once_with(post_id)


def test_update_post(post_service, mock_post_repository):
    post_id = 1
    user_id = 1
    post_update_dto = PostUpdateDTO(title="Updated Title", content="Updated Content")

    mock_post_repository.find_by_id.return_value = PostAggregate(
        Post(
            id=post_id,
            title="Original Title",
            content="Original Content",
            user_id=user_id,
            category_id=1,
        )
    )
    mock_post_repository.update.return_value = PostAggregate(
        Post(
            id=post_id,
            title="Updated Title",
            content="Updated Content",
            user_id=user_id,
            category_id=1,
        )
    )

    result = post_service.update_post(post_id, post_update_dto, user_id)

    assert result.title == "Updated Title"
    assert result.content == "Updated Content"
    mock_post_repository.find_by_id.assert_called_once_with(post_id)
    mock_post_repository.update.assert_called_once()


def test_delete_post(post_service, mock_post_repository):
    post_id = 1
    user_id = 1

    mock_post_repository.find_by_id.return_value = PostAggregate(
        Post(
            id=post_id,
            title="To be deleted",
            content="Content",
            user_id=user_id,
            category_id=1,
        )
    )

    post_service.delete_post(post_id, user_id)

    mock_post_repository.find_by_id.assert_called_once_with(post_id)
    mock_post_repository.delete.assert_called_once_with(post_id)


def test_search_posts(post_service, mock_post_repository):
    query = "test"
    skip = 0
    limit = 20

    mock_post_repository.search.return_value = [
        PostAggregate(
            Post(
                id=1, title="Test Post 1", content="Content 1", user_id=1, category_id=1
            )
        ),
        PostAggregate(
            Post(
                id=2, title="Test Post 2", content="Content 2", user_id=1, category_id=1
            )
        ),
    ]

    results = post_service.search_posts(query, skip, limit)

    assert len(results) == 2
    assert results[0].title == "Test Post 1"
    assert results[1].title == "Test Post 2"
    mock_post_repository.search.assert_called_once_with(query, skip, limit)
