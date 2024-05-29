import re
import jsonschema
from jsonschema import validate
from .models import Gender, JobStatus


def verify_gender(gender: str) -> str:
    """
        This function verifies gender
    """
    if gender.upper() == Gender.MALE:
        gender = Gender.MALE
    elif gender.upper() == Gender.FEMALE:
        gender = Gender.FEMALE
    elif gender.upper() == Gender.OTHERS:
        gender = Gender.OTHERS
    else:
        raise ValueError("Gender is not correct. Add from choices ['Male', 'Female', 'Others']")

    return gender


def verify_job_status(job_status: str) -> str:
    """
        This function verifies gender
    """
    if job_status.upper() == JobStatus.APPLIED:
        job_status = JobStatus.APPLIED
    elif job_status.upper() == JobStatus.SHORTLISTED:
        job_status = JobStatus.SHORTLISTED
    elif job_status.upper() == JobStatus.REJECTED:
        job_status = JobStatus.REJECTED
    else:
        raise ValueError("Job Status is not correct. Add from choices ['Applied', 'Shortlisted', 'Rejected']")

    return job_status


def verify_phone_number(phone_number):
    pattern = r'^\d{10}$'
    if re.match(pattern, str(phone_number)):
        return phone_number
    raise ValueError(f"{phone_number} is an invalid phone number.")


def verify_email_address(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return email
    raise ValueError(f"{email} is an invalid email.")


def validate_ceate_candidate_request_body(data):
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "User Information",
        "type": "object",
        "properties": {
            "years_of_exp": {
                "type": "number",
                "minimum": 0
            },
            "current_salary": {
                "type": "number",
                "minimum": 0
            },
            "expected_salary": {
                "type": "number",
                "minimum": 0
            },
            "name": {
                "type": "string",
                "minLength": 1
            },
            "age": {
                "type": "integer",
                "minimum": 0
            },
            "gender": {
                "type": "string",
                "enum": ["Male", "Female", "Other"]
            },
            "phone_number": {
                "type": "number",
                "pattern": "^\\d{10}$"
            },
            "email": {
                "type": "string",
                "format": "email"
            },
            "status": {
                "type": "string"
            }
        },
        "required": ["years_of_exp", "current_salary", "expected_salary", "name", "age", "gender", "phone_number", "email"],
        "additionalProperties": False
    }

    # Validate the data
    status = True
    error = ""
    try:
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        error = err.message
        status = False

    return status, error


def prepare_candidate_response_json(candidates):
    candidates_response = []
    for a_candidate in candidates:
        a_candidate_json = {
            "name": a_candidate.name,
            "age": a_candidate.age,
            "gender": a_candidate.gender,
            "phone_number": a_candidate.phone_number,
            "email": a_candidate.email,
            "years_of_exp": a_candidate.experience.years_of_exp,
            "current_salary": a_candidate.experience.current_salary,
            "expected_salary": a_candidate.experience.expected_salary,
            "status": a_candidate.status,
            "reason": a_candidate.reason
        }
        candidates_response.append(a_candidate_json)
    return candidates_response
