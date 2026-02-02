import pytest


@pytest.mark.parametrize(
    "user_id, expected_email",
    [
        (1, "Sincere@april.biz"),
        (2, "Shanna@melissa.tv"),
        (3, "Nathan@yesenia.net"),
    ],
)
def test_check_user_emails(api_client, user_id, expected_email):
    """Parametrized test to check specific user data."""
    response = api_client.get(f"users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == expected_email


# JsonPlaceholder doesn't support ?delay param like Reqres, so we remove that test
# Or allow it to fail/remove it. I'll replace it with a post comment test perhaps?
# Or just simple pagination check if supported? (JsonPlaceholder supports ?_limit=X)


@pytest.mark.slow
@pytest.mark.parametrize("limit", [1, 2, 5])
def test_users_limit(api_client, limit):
    """Test response with limit."""
    response = api_client.get(f"users?_limit={limit}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == limit
