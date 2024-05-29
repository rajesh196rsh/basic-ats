from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate, Experience, JobStatus
from .utils import verify_gender, verify_phone_number, verify_email_address, validate_ceate_candidate_request_body, prepare_candidate_response_json, verify_job_status
from . import constants
from collections import defaultdict


class CreateCandidateApi(APIView):

    def get(self, request, pk):
        response_status = status.HTTP_400_BAD_REQUEST

        try:
            candidates = Candidate.objects.filter(id=pk)
            res = prepare_candidate_response_json(candidates)
            response_status = status.HTTP_200_OK
        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.DEFAULT_ERROR_MESSAGE
            }

        return Response(res, status=response_status)

    def post(self, request):
        response_status = status.HTTP_400_BAD_REQUEST

        try:
            data = request.data

            validation_status, error = validate_ceate_candidate_request_body(data)
            if validation_status:
                gender = verify_gender(data["gender"])
                phone_number = verify_phone_number(data["phone_number"])
                email = verify_email_address(data["email"])
                experience_obj = Experience.objects.create(years_of_exp=data["years_of_exp"], current_salary=data["current_salary"],
                                        expected_salary=data["expected_salary"])
                candidate = Candidate.objects.create(name=data["name"], age=data["age"], gender=gender, phone_number=phone_number,
                                        email=email, experience=experience_obj)
                res = {
                    "id": candidate.id,
                    "message": constants.SUCCESSFUL_CREATION
                }
                response_status = status.HTTP_200_OK
            else:
                res = {
                    "error": error,
                    "message": constants.INCORRECT_PAYLOAD
                }
        except KeyError as e:
            res = {
                "error": str(e),
                "message": constants.MISSING_KEYS_ERROR
            }
        except TypeError as e:
            res = {
                "error": str(e),
                "message": constants.INCORRECT_DATATYPE_ERROR
            }
        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.DEFAULT_ERROR_MESSAGE
            }

        return Response(res, status=response_status)

    def put(self, request):
        response_status = status.HTTP_400_BAD_REQUEST

        try:
            data = request.data
            current_status = data["status"]
            candidates = Candidate.objects.filter(id=data["id"])
            if candidates:
                candidates = candidates[0]
                if candidates.status == JobStatus.APPLIED:
                    current_status = verify_job_status(current_status)
                    candidates.status = current_status
                    candidates.reason = data.get("reason", "")
                    candidates.save()
                    res = {
                        "id": data["id"],
                        "status": current_status,
                        "message": constants.STATUS_UPDATION_SUCCESSFUL
                    }
                    response_status = status.HTTP_200_OK
                else:
                    res = {
                        "id": data["id"],
                        "status": current_status,
                        "error": f"Status cannot be updated. Candidate is already {candidates.status}",
                        "message": constants.STATUS_UPDATION_FAILURE
                    }
            else:
                res = {
                    "id": data["id"],
                    "status": current_status,
                    "error": "Candidate with given id does not exists",
                    "message": constants.STATUS_UPDATION_FAILURE
                }
        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.STATUS_UPDATION_FAILURE
            }

        return Response(res, status=response_status)


class SearchCandidate(APIView):

    def post(self, request):
        response_status = status.HTTP_400_BAD_REQUEST
        try:
            data = request.data
            candidates = Candidate.objects.all()

            expected_salary_min = data.get("expected_salary_min")
            expected_salary_max = data.get("expected_salary_max")
            age_min = data.get("age_min")
            age_max = data.get("age_max")
            years_of_exp_min = data.get("years_of_exp_min")
            phone_number = data.get("phone_number")
            email = data.get("email")
            name = data.get("name")

            if expected_salary_min and expected_salary_max:
                candidates = candidates.filter(experience__expected_salary__range=(expected_salary_min, expected_salary_max))
            if age_min and age_max:
                candidates = candidates.filter(age__range=(age_min, age_max))
            if years_of_exp_min:
                candidates = candidates.filter(experience__years_of_exp__gte=years_of_exp_min)
            if phone_number:
                candidates = candidates.filter(phone_number=phone_number)
            if email:
                candidates = candidates.filter(email=email)
            if name:
                candidates = candidates.filter(name__icontains=name)

            res = prepare_candidate_response_json(candidates)
            response_status = status.HTTP_200_OK

        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.DEFAULT_ERROR_MESSAGE
            }
        return Response(res, status=response_status)


class SearchByName(APIView):

    def post(self, request):
        response_status = status.HTTP_400_BAD_REQUEST

        try:
            data = request.data
            query = data["name"]
            if not query:
                return Response([])

            query_words = set(query.lower().split())
            candidates = Candidate.objects.all()
            candidate_scores = defaultdict(list)

            for candidate in candidates:
                name_words = set(candidate.name.lower().split())
                if query.lower() == candidate.name.lower():
                    score = 99
                else:
                    common_words = query_words & name_words
                    score = len(common_words)
                if score > 0:
                    candidate_scores[score].append(candidate)

            sorted_candidates = []
            for score in sorted(candidate_scores.keys(), reverse=True):
                sorted_candidates.extend(candidate_scores[score])

            res = prepare_candidate_response_json(sorted_candidates)
            response_status = status.HTTP_200_OK

        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.DEFAULT_ERROR_MESSAGE
            }

        return Response(res, status=response_status)
