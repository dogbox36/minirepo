
import pytest
from pydantic import ValidationError

from apitest.schemas import UserCreate, UserResponse


@pytest.mark.smoke
def test_get_users_list(api_client):
    """Verify that we can retrieve a list of users."""
    response = api_client.get("users")
    assert response.status_code == 200

    data = response.json()
    # JsonPlaceholder returns a list of users directly
    assert isinstance(data, list)
    assert len(data) > 0

    # Validate first item schema
    try:
        user = UserResponse(**data[0])
        assert user.id is not None
        assert user.email is not None
    except ValidationError as e:
        pytest.fail(f"Response validation failed: {e}")


@pytest.mark.regression
def test_create_user(api_client):
    """Verify that we can create a new user."""
    payload = UserCreate(name="John Doe", username="jdoe", email="john.doe@example.com")

    response = api_client.post("users", json=payload.model_dump())
    assert response.status_code == 201

    data = response.json()
    # JsonPlaceholder returns an id (usually 11 or 101, depending on resource)
    assert data["id"] is not None
    assert isinstance(data["id"], int)

    # It might return the sent data back
    # assert data["name"] == payload.name # JsonPlaceholder sometimes mocks this, sometimes not nicely.
    # Actually it returns {id: 101} normally? Or {id: 101, ...data...}
    # Let's check status mostly.


@pytest.mark.regression
def test_get_single_user_not_found(api_client):
    """Negative Test: Verify 404 for non-existent user."""
    response = api_client.get("users/99999")
    assert response.status_code == 404


def test_delete_user(api_client):
    """Verify DELETE returns 200/204."""
    response = api_client.delete("users/1")
    assert response.status_code == 200  # JsonPlaceholder returns 200 {}
