# API Testing with JSONPlaceholder

This repository contains a suite of automated tests for the JSONPlaceholder API using Python's `requests` library and `pytest` for test execution. The tests are focused on performing CRUD operations (GET, POST, PUT, DELETE, PATCH) on the `/posts` endpoint of the JSONPlaceholder API and logging the results into a CSV file.

## Features

- **GET Tests**: Validates the retrieval of posts and specific post by ID.
- **POST Tests**: Verifies the creation of new posts and handles edge cases like missing fields, extra fields, and invalid payloads.
- **PUT Tests**: Checks the update functionality for posts, including handling missing fields, extra fields, and invalid post IDs.
- **PATCH Tests**: Verifies the partial update of posts, including handling invalid post IDs and empty payloads.
- **DELETE Tests**: Ensures that posts can be deleted and checks for valid error responses for non-existent posts.

### Requirements

- Python 3.x
- `requests` library
- `pytest`
- `csv` (comes built-in with Python)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/DuleenMubarak/JSONPLACEHOLDER_PYTHON_PYTEST.git
