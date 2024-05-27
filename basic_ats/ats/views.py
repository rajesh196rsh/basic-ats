# candidates/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Candidate, Experience, JobStatus
from . import constants
from .serializers import CandidateSerializer, ExperienceSerializer
from django.db.models import Q
from collections import defaultdict


class CreateCandidateApi(APIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get(self, request, pk):
        status = status.HTTP_400_BAD_REQUEST

        try:
            candidates = self.queryset
            candidates = candidates.filter(id=pk)
            serializer = self.get_serializer(candidates, many=True)
            res = serializer.data
            status = status.HTTP_200_OK
        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.DEFAULT_ERROR_MESSAGE
            }

        return Response(res, status=status)

    def post(self, request):
        status = status.HTTP_400_BAD_REQUEST

        try:
            data = request.data
            experience_obj = Experience.objects.create(years_of_exp=data["years_of_exp"], current_salary=data["current_salary"],
                                    expected_salary=data["expected_salary"])
            candidate = Candidate.objects.create(name=data["name"], age=data["age"], gender=data["gender"], phone_number=data["phone_number"],
                                    email=data["email"], experience=experience_obj)
            res = {
                "id": candidate.id,
                "message": constants.SUCCESSFUL_CREATION
            }
            status = status.HTTP_200_OK
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

        return Response(res, status=status)

    def put(self, request):
        status = status.HTTP_400_BAD_REQUEST

        try:
            candidates = self.queryset
            data = request.data
            current_status = data["status"]
            candidates = candidates.filter(id=data["id"])
            if candidates:
                candidates = candidates[0]
                if current_status.upper() == JobStatus.SHORTLISTED:
                    candidates.status = JobStatus.SHORTLISTED
                elif current_status.upper() == JobStatus.REJECTED:
                    candidates.status = JobStatus.REJECTED
                candidates.reason = data.get("reason", "")
                candidates.save()
                res = {
                    "id": data["id"],
                    "status": current_status,
                    "message": constants.STATUS_UPDATION_SUCCESSFUL
                }
                status = status.HTTP_200_OK
            else:
                res = {
                    "id": data["id"],
                    "status": current_status,
                    "error": "Given id does not exists",
                    "message": constants.STATUS_UPDATION_FAILURE
                }
        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.STATUS_UPDATION_FAILURE
            }

        return Response(res, status=status)



class SearchCandidate(APIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    def get(self, request):
        query_params = request.query_params
        candidates = self.queryset

        expected_salary_min = query_params.get('expected_salary_min')
        expected_salary_max = query_params.get('expected_salary_max')
        age_min = query_params.get('age_min')
        age_max = query_params.get('age_max')
        years_of_exp_min = query_params.get('years_of_exp_min')
        phone_number = query_params.get('phone_number')
        email = query_params.get('email')
        name = query_params.get('name')

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

        serializer = self.get_serializer(candidates, many=True)
        return Response(serializer.data)


class SearchByName(APIView):
    serializer_class = CandidateSerializer

    def get(self, request):
        status = status.HTTP_400_BAD_REQUEST

        try:
            query = request.query_params.get('q', '').strip()
            if not query:
                return Response([])

            query_words = set(query.lower().split())
            candidates = Candidate.objects.all()
            candidate_scores = defaultdict(list)

            for candidate in candidates:
                name_words = set(candidate.name.lower().split())
                common_words = query_words & name_words
                score = len(common_words)
                if score > 0:
                    candidate_scores[score].append(candidate)

            sorted_candidates = []
            for score in sorted(candidate_scores.keys(), reverse=True):
                sorted_candidates.extend(candidate_scores[score])

            serializer = self.get_serializer(sorted_candidates, many=True)
            res = serializer.data
            status = status.HTTP_200_OK

        except Exception as e:
            res = {
                "error": str(e),
                "message": constants.DEFAULT_ERROR_MESSAGE
            }

        return Response(res, status=status)
