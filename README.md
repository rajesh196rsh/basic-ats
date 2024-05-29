# basic-ats
### Overview

The Candidate Management API is designed to handle the creation, retrieval, updating, and searching of candidate records. It provides a robust system for managing candidate data including their experience, contact details, and job status. This API is built using Django REST framework.
Features

    Create Candidate: Add a new candidate with details like name, age, gender, phone number, email, experience, etc.
    Get Candidate: Retrieve candidate details by their ID.
    Update Candidate Status: Update the job status of a candidate.
    Search Candidates: Search for candidates based on various criteria such as expected salary, age, years of experience, phone number, email, and name.
    Search By Name: Search candidates by their name with relevance scoring.

### Endpoints
1. CreateCandidateApi
GET /candidate/<pk>/

Retrieve a candidate by their ID.

    Parameters:
        pk: Candidate ID
    Response:
        200 OK: Returns candidate details
        400 Bad Request: If there is an error

POST /candidate/

Create a new candidate.

    Request Body:
    json
    {
        "name": "John Doe",
        "age": 30,
        "gender": "male",
        "phone_number": "1234567890",
        "email": "john.doe@example.com",
        "years_of_exp": 5,
        "current_salary": 50000,
        "expected_salary": 60000
    }

    Response:
        200 OK: If the candidate is successfully created
        400 Bad Request: If there is a validation error or any other error

PUT /candidate/

Update the status of a candidate.

    Request Body:
    json
    {
        "id": 1,
        "status": "INTERVIEWED",
        "reason": "Interview completed successfully"
    }

    Response:
        200 OK: If the status is successfully updated
        400 Bad Request: If there is an error

2. SearchCandidate
POST /candidate/search/

Search for candidates based on various criteria.

    Request Body (all fields are optional):
    json
    {
        "expected_salary_min": 50000,
        "expected_salary_max": 70000,
        "age_min": 25,
        "age_max": 35,
        "years_of_exp_min": 3,
        "phone_number": "1234567890",
        "email": "john.doe@example.com",
        "name": "John"
    }

    Response:
        200 OK: Returns a list of candidates that match the search criteria
        400 Bad Request: If there is an error

3. SearchByName
POST /candidate/search/name/

Search candidates by their name.

    Request Body:
    json
    {
        "name": "John Doe"
    }

    Response:
        200 OK: Returns a list of candidates that match the name search
        400 Bad Request: If there is an error

## Setup
Prerequisites

    Python 3.x
    Django
    Django REST framework

Installation
    Clone the repository:
    sh

https://github.com/rajesh196rsh/basic-ats.git
cd basic-ats

### Install the dependencies:
pip install -r requirements.txt

### Apply the migrations:
python manage.py migrate

### Run the development server:
python manage.py runserver

Configuration

    Update the constants.py file with appropriate messages and settings.
    Ensure that your database settings in settings.py are configured correctly.

### Utils
utils.py

    verify_gender: Validates and converts gender input.
    verify_phone_number: Validates and formats phone numbers.
    verify_email_address: Validates email addresses.
    validate_create_candidate_request_body: Validates the request body for creating a candidate.
    prepare_candidate_response_json: Prepares the response JSON for candidate data.
    verify_job_status: Validates job status transitions.

### Models
models.py

    Candidate: Model representing a candidate with fields like name, age, gender, phone number, email, experience, and status.
    Experience: Model representing the experience details of a candidate.
    JobStatus: Enumeration for various job statuses like APPLIED, INTERVIEWED, HIRED, etc.

### Error Handling

    DEFAULT_ERROR_MESSAGE: A generic error message for unexpected issues.
    MISSING_KEYS_ERROR: Error message for missing keys in the request.
    INCORRECT_DATATYPE_ERROR: Error message for incorrect data types.
    STATUS_UPDATION_FAILURE: Error message for status update failures.
    SUCCESSFUL_CREATION: Message indicating successful creation of a candidate.
    STATUS_UPDATION_SUCCESSFUL: Message indicating successful status update.
    INCORRECT_PAYLOAD: Error message for incorrect request payloads.
