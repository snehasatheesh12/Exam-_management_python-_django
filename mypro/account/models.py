from django.db import models
from django.contrib.auth.models import User


class Institute(models.Model):
    inst_name = models.CharField(max_length=40)
    code = models.CharField(max_length=40, unique=True)
    email = models.EmailField()
    address = models.TextField()
    status = models.CharField(max_length=12, default="pending")
    phone = models.CharField(max_length=12, default="null")
    registration_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    established_date = models.DateField(null=True, blank=True)
    contact_person = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    number_of_students = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.inst_name


class qualification(models.Model):
    qualification_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.qualification_name
class Principal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualifications = models.ManyToManyField(qualification, related_name='principals')  
    years_of_experience = models.IntegerField() 
    photo = models.ImageField(upload_to="principal/", null=True, blank=True)
    institute = models.OneToOneField(Institute, on_delete=models.CASCADE)
    certifications = models.CharField(max_length=255, blank=True, null=True) 
    professional_summary = models.TextField(blank=True, null=True) 
    contact_number = models.CharField(max_length=15, blank=True, null=True) 
    address = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Principal'
        verbose_name_plural = 'Principals'