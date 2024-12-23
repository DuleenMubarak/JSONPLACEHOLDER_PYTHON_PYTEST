from datetime import datetime
import requests 
import pytest
import json
import csv 

@pytest.fixture()
def base_url():
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture()
def test_data():
    with open("test_data.json","r") as file:
        return json.load(file)


def log_of_test_results(results, request_type, test_name, response, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(results, mode='a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Timestamp", "Request Type", "Test Name", "Response", "Result"])
            writer.writerow([timestamp, request_type, test_name, response, result])
    except Exception as e:
        print(f"Error logging test result: {e}")



# Testing GET

def test_get_post_by_id(base_url):
    test_name = "test_get_post_by_id"
    try:
        post_id = 20
        response = requests.get(f"{base_url}/posts/{post_id}")
        assert response.status_code in [200, 201]
        assert isinstance(response.json(), dict)
        assert int(response.json().get('id')) == post_id
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "GET - by id", test_name, response, result)

def test_get_post_by_invalid_id(base_url):
    test_name = "test_get_post_by_id_invalid_id"
    try:
        post_id = "invalid_id"
        response = requests.get(f"{base_url}/posts/{post_id}")
        assert response.status_code == 404
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "GET - post by invalid id", test_name, response, result)

def test_get_post_by_id_non_integer(base_url):
    test_name = "test_get_post_by_id_non_integer"
    try:
        post_id = "abc"
        response = requests.get(f"{base_url}/posts/{post_id}")
        assert response.status_code == 404
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "GET - by non integer id", test_name, response, result)


def test_get_nonexistent_post(base_url):
    test_name = "test_get_nonexistent_post"
    try:
        post_id = 10000
        response = requests.get(f"{base_url}/posts/{post_id}")
        assert response.status_code not in [200, 201]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "GET - nonexisting post", test_name, response, result)

# Testing POST

def test_create_post(base_url):
    test_name = "test_create_post"
    try:
        new_post = {
            "userId": 9,
            "title": "New Post Title",
            "body": "This is the body of the new post"
        }
        response = requests.post(f"{base_url}/posts", json=new_post)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["userId"] == new_post["userId"]
        assert response_data["title"] == new_post["title"]
        assert response_data["body"] == new_post["body"]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "POST - Valid", test_name, response, result)

def test_create_post_missing_data(base_url):
    test_name = "test_create_post_missing_data"
    try:
        incomplete_post = {
            "userId": 9,
            "title": "Post with missing body"
        }
        response = requests.post(f"{base_url}/posts", json=incomplete_post)
        assert response.status_code in [200, 201, 202, 203, 204, 205]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "POST - Missing data", test_name, response, result)

def test_create_post_with_extra_fields(base_url):
    test_name = "test_create_post_with_extra_fields"
    try:
        new_post = {
            "userId": 9,
            "title": "Post with extra fields",
            "body": "This post includes unexpected fields.",
            "extra_field": "Unexpected data",
        }
        response = requests.post(f"{base_url}/posts", json=new_post)
        assert response.status_code in [200, 201, 202, 203, 204, 205]
        response_data = response.json()
        assert "extra_field" in response_data
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "POST - Extra field", test_name, response, result)


def test_create_post_empty_payload(base_url):
    test_name = "test_create_post_empty_payload"
    try:
        response = requests.post(f"{base_url}/posts", json={})
        assert response.status_code in [200,201]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "POST - Empty payload", test_name, response, result)

# Test PATCH

def test_patch_update_post(base_url):
    test_name = "test_patch_update_post"
    try:
        post_id = 20
        update_data = {
            "title": "Updated Post Title",
            "body": "Updated post body content"
        }
        response = requests.patch(f"{base_url}/posts/{post_id}", json=update_data)
        assert response.status_code in [200, 201, 202, 203, 204, 205]
        response_data = response.json()
        assert response_data["title"] == update_data["title"]
        assert response_data["body"] == update_data["body"]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "PATCH - Valid", test_name, response, result)

def test_patch_post_with_empty_payload(base_url):
    test_name = "test_patch_post_with_empty_payload"
    try:
        post_id = 1
        response = requests.patch(f"{base_url}/posts/{post_id}", json={})
        assert response.status_code in [200,201]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "PATCH - Empty payload", test_name, response, result)

def test_patch_update_nonexistent_post(base_url):
    test_name = "test_patch_update_nonexistent_post"
    try:
        post_id = 9999
        update_data = {
            "title": "Nonexistent Post",
            "body": "Trying to update a non-existent post"
        }
        response = requests.patch(f"{base_url}/posts/{post_id}", json=update_data)
        assert response.status_code in [200,201]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "PATCH - Nonexistent post", test_name, response, result)


# Testing PUT

def test_put(base_url, test_data):
    try:
        updated_post_data = test_data[1]
        post_id = updated_post_data["id"]
        response = requests.put(f"{base_url}/posts/{post_id}", json=updated_post_data)
        assert response.status_code in [200, 201, 202, 203, 204, 205]
        response_data = response.json()
        assert response_data["userId"] == updated_post_data["userId"]
        assert response_data["title"] == updated_post_data["title"]
        assert response_data["body"] == updated_post_data["body"]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    except Exception as e:
        result = f"ERROR: {e}"
    log_of_test_results("results.csv", "Valid PUT", "test_put", response.status_code, result)


def test_put_update_post_with_invalid_id(base_url):
    test_name = "test_put_update_post_with_invalid_id"
    try:
        post_id = 99999  # Invalid post ID
        updated_data = {
            "userId": 1,
            "id": post_id,
            "title": "Updated Post Title",
            "body": "Updated post body content"
        }
        response = requests.put(f"{base_url}/posts/{post_id}", json=updated_data)
        assert response.status_code == 500
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "PU - Invalid id", test_name, response, result)


def test_put_update_post_with_extra_fields(base_url):
    test_name = "test_put_update_post_with_extra_fields"
    try:
        post_id = 1
        updated_data = {
            "userId": 1,
            "id": post_id,
            "title": "Updated Post Title",
            "body": "Updated post body content",
            "extra_field": "Extra data"
        }
        response = requests.put(f"{base_url}/posts/{post_id}", json=updated_data)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["extra_field"] == "Extra data"  # Test if extra field is returned
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("test_results.csv", "PUT - Extra field", test_name, response, result)

   
# Testing DELETE

def test_delete(base_url):
    try:
        userId = 3
        response = requests.delete(f"{base_url}/posts/{userId}")
        assert response.status_code in [200, 201, 202, 203, 204, 205]
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    except Exception as e:
        result = f"ERROR: {e}"
    log_of_test_results("results.csv", "Valid DELETE", "test_delete", response.status_code, result)

def test_delete_post_empty_id(base_url):
    test_name = "test_delete_post_empty_id"
    try:
        post_id = ""
        response = requests.delete(f"{base_url}/posts/{post_id}")
        assert response.status_code == 404  # Assertion was missing here
        result = "PASS"
    except AssertionError:
        result = "FAIL"
    log_of_test_results("results.csv", "DELETE - Empty id", test_name, response, result)












