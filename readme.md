# Rule Engine API

## Overview

This project is a Django-based API for creating and evaluating rules using an Abstract Syntax Tree (AST). The rules determine user eligibility based on attributes like age, department, income, and experience.

## Features

- Create rules using logical expressions.
- Evaluate rules against user data.
- Handle complex conditions with an AST.

## Requirements

- Python 3.8+
- Django 3.2+
- SQLite (default database)

## Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd rule_engine
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Run the server:**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Create Rule

- **URL:** `/create_rule/`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "rule_string": "(age > 30 AND department = Sales) OR (experience > 5)",
    "name": "Sample Rule",
    "description": "Test rule"
  }
  ```

- **Response:**

  ```json
  {
    "message": "Rule created",
    "rule_id": 1
  }
  ```

### Evaluate Rule

- **URL:** `/evaluate_rule/`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "rule_id": 1,
    "user_data": {
      "age": 35,
      "department": "Sales",
      "salary": 60000,
      "experience": 3
    }
  }
  ```

- **Response:**

  ```json
  {
    "result": true
  }
  ```

## Error Handling

- Returns `400 Bad Request` for invalid JSON or missing attributes.
- Handles missing rule IDs gracefully.

## Security Considerations

- Ensure CSRF protection is enabled for production.
- Validate and sanitize all user inputs.

## Future Enhancements

- Extend parsing logic for more complex conditions.
- Implement user-defined functions within rules.
- Add support for more data types and comparisons.
