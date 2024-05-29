from django.db import models


class JobStatus:
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"


class Gender:
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHERS = "OTHERS"
    CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHERS, "Others"),
    ]


class Experience(models.Model):
    years_of_exp = models.FloatField()
    current_salary = models.DecimalField(max_digits=10, decimal_places=2)
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2)


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=Gender.CHOICES)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default=JobStatus.APPLIED)
    reason = models.TextField(blank=True, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
