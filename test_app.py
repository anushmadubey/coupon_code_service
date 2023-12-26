import pytest
from app import create_app
import json

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    yield app
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_request_example(client):
    response = client.get("/test")
    res = json.loads(response.data.decode("utf-8"))
    assert res['message'] == "hello!"

def test_get_coupon(client):
    response = client.get("/coupon")
    res = json.loads(response.data.decode("utf-8"))
    assert res['message'] == []
    assert response.status_code == 200

def test_add_coupon(client):
    response = client.post(
                "/coupon",
                data={
                "code": "ABCD", 
                "discount_percentage": "5", 
                "expiry_date":"2024-10-10"
            }
            )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert res['message'] == 'Coupon created successfully'

        

def test_get_coupon2(client):
    response = client.get("/coupon")
    res = json.loads(response.data.decode("utf-8"))
    assert len(res['message']) == 1
    assert response.status_code == 200

def test_create_user(client):
    response = client.post(
                "/user",
                data={
                "name": "Anushma", 
                "email_id": "anushma@email.com"
                }
            )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert res['message'] == 'User created successfully'

def test_create_user2(client):
    response = client.post(
                "/user",
                data={
                "name": "Anushma Dubey", 
                "email_id": "anushma@email.com"
                }
            )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 400
    assert res == 'User with the same email id exists'


def test_add_repeat_count(client):
    response = client.put(
        "/coupon/ABCD/repeat_count",
        data={
            "user_total_repeat_count": 5,
            "global_total_repeat_count" : 1000,
            "user_daily_repeat_count": 3,
            "user_weekly_repeat_count": 3
        }
    )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert res['message'] == "Coupon repeat counts updated"
    

def test_add_repeat_count2(client):
    response = client.put(
        "/coupon/DEFGD/repeat_count",
        data={
            "user_total_repeat_count": 5,
            "global_total_repeat_count" : 1000,
            "user_daily_repeat_count": 3,
            "user_weekly_repeat_count": 3
        }
    )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 404
    assert res['message'] == "Coupon not found"


def test_apply_coupon(client):
    response = client.post(
                "/coupon/apply",
                data={
                "user_id": "1", 
                "coupon_code": "ABCD"
                }
            )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert res['message'] == 'Successfully coupon applied.'

def test_add_repeat_count3(client):
    response = client.put(
        "/coupon/ABCD/repeat_count",
        data={
            "user_daily_repeat_count": 1
        }
    )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert res['message'] == "Coupon repeat counts updated"
    

def test_apply_coupon2(client):
    response = client.post(
                "/coupon/apply",
                data={
                "user_id": "1", 
                "coupon_code": "ABCD"
                }
            )
    res = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 400
    assert res['message'] == 'User daily redemption count reached.'



