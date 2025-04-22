from unittest.mock import patch


@patch("app.v1.events.email_publisher.EmailPublisher.publish_email")
def test_register_success(mock_publish_email, client, db_session):
    mock_publish_email.return_value = None
    response = client.post(
        "/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+8412345678xx",
        },
    )
    assert response.status_code == 201
    assert "message" in response.json
    mock_publish_email.assert_called_once()


def test_update_user_info(authorized_client, db_session, test_user):
    update_payload = {
        "first_name": "New First Name",
        "last_name": "New Last Name",
        "phone_number": "+84xxxxxxxx",
    }
    response = authorized_client.put("/v1/users/profile", json=update_payload)
    assert response.status_code == 200
    assert response.json["user"]["phone_number"] == "+84xxxxxxxx"
