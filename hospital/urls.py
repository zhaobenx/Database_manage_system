from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("hospital/", views.HospitalView.as_view(), name="hospitals"),
    path("hospital/<int:pk>/", views.HospitalDetailView.as_view(), name="hospital-detail"),
    path("hospital/<int:pk>/physician", views.PhysicianView.as_view(), name="hospital-physician"),
    path("physician/<int:pk>", views.PhysicianDetailView.as_view(), name="physician-detail"),
    path("physician/add", views.PhysicianCreate.as_view(), name="physician-add"),
    path("physician/<int:pk>/delete", views.PhysicianDelete.as_view(), name="physician-delete"),
    path("hospital/<int:pk>/add/", views.add_department, name="department-add"),
    path("department/", views.DepartmentView.as_view(), name="departments"),
    path("department/<int:pk>/", views.DepartmentDetailView.as_view(), name="department-detail"),
    path("department/<int:pk>/delete/", views.DepartmentDelete.as_view(), name="department-delete"),
    path("user/add/", views.UserCreate.as_view(), name="user-add"),
    path("user/<int:pk>/delete/", views.UserDelete.as_view(), name="user-delete"),
    path("patient/", views.PatientView.as_view(), name="patients"),
    path("patient/add/", views.PatientCreateView.as_view(), name="patient-add"),
    path("patient/<int:pk>/update/", views.PatientUpdate.as_view(), name="patient-update"),
    path("patient/<int:pk>/delete/", views.PatientDeleteView.as_view(), name="patient-delete"),
    path("case/add/", views.CaseCreateView.as_view(), name="case-add"),
    path("case/<int:pk>/update/", views.CaseUpdate.as_view(), name="case-update"),
    path("case/<int:pk>/delete/", views.CaseDeleteView.as_view(), name="case-delete"),
    path("treatment/", views.TreatmentView.as_view(), name="treatments"),
    path("treatment/add/", views.TreatmentCreateView.as_view(), name="treatment-add"),
    path("disease/", views.DiseaseView.as_view(), name="diseases"),
    path("disease/add/", views.DiseaseCreateView.as_view(), name="disease-add"),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

