from django.urls import path,include
from .views import SearchCandidate, SearchByName, CreateCandidateApi


urlpatterns = [
    path("create/candidate", CreateCandidateApi.as_view(), name="create_candidate"),
    path("search/candidate", SearchCandidate.as_view(), name="search_candidate"),
    path("search/candidate/by_name", SearchByName.as_view(), name="search_by_name"),
]