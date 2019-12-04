from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.db.models import Count

from .models import (
    Hospital,
    Department,
    Users,
    Physician,
    Patient,
    PatientTreatment,
    Treatment,
    Disease,
)
from .form import (
    DepartmentForm,
    UserForm,
    PhysicianForm,
    PatientForm,
    PatientUpdateForm,
    PatientTreatmentForm,
    TreatmentForm,
    DiseaseForm,
    CaseUpdateForm,
)

# pylint: disable=no-member


class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "hospital"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Hospital.objects.all()


class HospitalView(generic.ListView):
    model = Hospital
    template_name = "hospitals.html"


class HospitalDetailView(generic.DetailView):
    model = Hospital
    template_name = "hospital.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DepartmentForm()
        context["add_form"] = form
        return context


class DepartmentView(generic.ListView):
    model = Department
    template_name = "departments.html"


class DepartmentDetailView(generic.DetailView):
    model = Department
    template_name = "department-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserForm(self.kwargs["pk"])
        context["add_form"] = form
        return context


@login_required(login_url="login")
def add_department(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    form = DepartmentForm(request.POST)
    if form.is_valid:
        f = form.save(commit=False)
        f.hid = hospital
        f.save()
        # check whether it's valid:
    return redirect(reverse("hospital-detail", args=(hospital.hid,)))


class PermissionMixin(object):
    def get_object(self, *args, **kwargs):
        obj = super(PermissionMixin, self).get_object(*args, **kwargs)
        if self.request.user.is_authenticated:
            self.success_url = self.request.META.get("HTTP_REFERER") or self.success_url
            return obj
        else:
            raise PermissionDenied()


class CreateViewPermissionMixin(object):
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            self.success_url = self.request.META.get("HTTP_REFERER") or self.success_url
            return super(CreateViewPermissionMixin, self).form_valid(form)
        else:
            raise PermissionDenied()

    def form_invalid(self, form):
        if self.request.user.is_authenticated:
            self.success_url = self.request.META.get("HTTP_REFERER") or self.success_url
            return super(CreateViewPermissionMixin, self).form_invalid(form)
        else:
            raise PermissionDenied()


class DepartmentDelete(PermissionMixin, generic.DeleteView):
    model = Department
    success_url = reverse_lazy("hospitals")
    template_name = "department_confirm_delete.html"


class UserCreate(generic.CreateView):
    model = Users
    fields = ["ufname", "ulname", "urole", "did"]
    template_name = "user-create.html"

    def form_valid(self, form):
        self.success_url = reverse_lazy(
            "department-detail", args=(form.cleaned_data.get("did").did,)
        ) or reverse("index")
        return super(UserCreate, self).form_valid(form)


class UserDelete(PermissionMixin, generic.DeleteView):
    model = Users
    success_url = reverse_lazy("index")
    template_name = "user_confirm_delete.html"


class PhysicianView(generic.DetailView):
    model = Hospital
    template_name = "physicians.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = PhysicianForm(self.kwargs["pk"])
        context["add_form"] = form
        return context


class PhysicianCreate(generic.CreateView):
    model = Physician
    template_name = "physician-create.html"
    fields = ["phfname", "phtel", "phspl", "hid"]

    def form_valid(self, form):
        self.success_url = reverse_lazy(
            "hospital-physician", args=(form.cleaned_data.get("hid").hid,)
        ) or reverse("index")
        # print(form.cleaned_data)
        return super(PhysicianCreate, self).form_valid(form)


class PhysicianDelete(PermissionMixin, generic.DeleteView):
    model = Physician
    success_url = reverse_lazy("index")
    template_name = "physician-confirm-delete.html"


class PhysicianDetailView(generic.DetailView):
    model = Physician
    template_name = "physician-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["unique_patients"] = (
            self.get_object().patient.values("pid").distinct().count()
        )
        context["patient_form"] = PatientForm()
        context["patienttreatment_form"] = PatientTreatmentForm(self.kwargs["pk"])
        context["treatment_form"] = TreatmentForm()
        context["disease_form"] = DiseaseForm()

        cases = []
        status = self.request.GET.get("status")
        status = {"successful": "S", "repeated": "R", "failed": "F"}.get(status, None)
        if status:
            qs = Physician.objects.get(
                pk=self.kwargs["pk"]
            ).patienttreatment_set.filter(tstatus=status)
        else:
            qs = Physician.objects.get(pk=self.kwargs["pk"]).patienttreatment_set.all()

        for i in qs:
            t = CaseUpdateForm(instance=i)
            cases.append((i, t))
        context["cases"] = cases

        return context


class PatientView(generic.ListView):
    model = Patient
    template_name = "patients.html"

    def get_context_data(self, **kwargs):
        context = super(PatientView, self).get_context_data(**kwargs)
        forms = []
        for i in context["patient_list"]:
            forms.append(PatientUpdateForm(instance=i))

        context["patient_list"] = zip(context["patient_list"], forms)
        context["patient_form"] = PatientForm()
        return context


class PatientCreateView(CreateViewPermissionMixin, generic.CreateView):
    model = Patient
    template_name = "patient-create.html"
    fields = ["pfname", "plname", "pgender", "pbd", "prace", "pstatus"]
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super(PatientCreateView, self).get_context_data(**kwargs)
        # context["patient_form"] = context["form"]
        return context


class PatientUpdate(CreateViewPermissionMixin, generic.UpdateView):
    model = Patient
    form_class = PatientUpdateForm
    template_name = "create.html"

    def get_context_data(self, **kwargs):
        context = super(PatientUpdate, self).get_context_data(**kwargs)
        # context["patient_form"] = context["form"]
        context["modal"] = "patient-update-modal.html"
        return context


class PatientDeleteView(PermissionMixin, generic.DeleteView):
    model = Patient
    success_url = reverse_lazy("index")
    template_name = "patient-confirm-delete.html"


class CaseCreateView(CreateViewPermissionMixin, generic.CreateView):
    model = PatientTreatment
    template_name = "create.html"
    fields = ["pid", "tdate", "tfreq", "tstatus", "tid", "phid"]
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super(CaseCreateView, self).get_context_data(**kwargs)
        # context["patient_form"] = context["form"]
        context["modal"] = "patienttreatment-create-modal.html"
        return context


class CaseUpdate(CreateViewPermissionMixin, generic.UpdateView):
    model = PatientTreatment
    form_class = CaseUpdateForm
    # fields = ["pid", "tdate", "tfreq", "tstatus", "tid"]
    template_name = "create.html"

    def get_context_data(self, **kwargs):
        context = super(CaseUpdate, self).get_context_data(**kwargs)
        # context["patient_form"] = context["form"]
        context["modal"] = "case-update-modal.html"
        return context


class CaseDeleteView(PermissionMixin, generic.DeleteView):
    model = PatientTreatment
    success_url = reverse_lazy("index")
    template_name = "patient-confirm-delete.html"


class TreatmentView(generic.ListView):
    model = Treatment
    template_name = "treatments.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["treatment_form"] = TreatmentForm()
        return context

    def get_queryset(self):
        order = self.request.GET.get("order")
        order = {"name":"tname","type": "ttype", "diease": "deid", "count": "count"}.get(order)
        if order:
            if order == "count":
                return (
                    super()
                    .get_queryset()
                    .annotate(num_diease=Count("patienttreatment"))
                    .order_by("-num_diease")
                )
            else:
                return super().get_queryset().order_by(order)
        return super().get_queryset()


class TreatmentCreateView(CreateViewPermissionMixin, generic.CreateView):
    # model = Treatment
    template_name = "create.html"
    # fields = ["tname", "ttype", "deid"]
    form_class = TreatmentForm
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super(TreatmentCreateView, self).get_context_data(**kwargs)
        # context["patient_form"] = context["form"]
        context["modal"] = "treatment-create-modal.html"
        return context


class DiseaseView(generic.ListView):
    model = Disease
    template_name = "diseases.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disease_form"] = DiseaseForm()
        return context


class DiseaseCreateView(CreateViewPermissionMixin, generic.CreateView):
    # model = Disease
    template_name = "create.html"
    # fields = ["deid", "dename"]
    form_class = DiseaseForm
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super(DiseaseCreateView, self).get_context_data(**kwargs)
        # context["patient_form"] = context["form"]
        context["modal"] = "disease-create-modal.html"
        return context


def login_request(request):
    if request.user.is_authenticated:
        return redirect(reverse("index"))

    error_message = ""
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(
                    reverse("index"),
                    context={"message": f"You are now logged in as {username}"},
                )
            else:
                error_message = "Invalid username or password."
        else:
            error_message = "Invalid username or password."

    return render(
        request=request,
        template_name="login.html",
        context={"error_message": error_message},
    )


def logout_request(request):
    logout(request)
    return redirect(reverse("index"))

