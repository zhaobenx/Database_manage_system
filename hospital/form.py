from django.forms import (
    ModelForm,
    HiddenInput,
    IntegerField,
    DateInput,
    NumberInput,
    TextInput,
)


from .models import (
    Department,
    Users,
    Physician,
    Patient,
    PatientTreatment,
    Disease,
    Treatment,
)


class DepartmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Department
        exclude = ["did", "hid"]


class UserForm(ModelForm):
    did = IntegerField(widget=HiddenInput, label="")

    def __init__(self, did, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        # print(did)
        self.fields["did"].initial = did

    class Meta:
        model = Users
        exclude = ["uid", "did"]
        # widgets = {"did": HiddenInput()}


class PhysicianForm(ModelForm):
    hid = IntegerField(widget=HiddenInput, label="")

    def __init__(self, hid, *args, **kwargs):
        super(PhysicianForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        # print(did)
        self.fields["hid"].initial = hid

    class Meta:
        model = Physician
        exclude = ["phid", "hid", "patient", "treatment"]


class PatientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Patient
        exclude = ["pid"]
        widgets = {"pbd": DateInput(attrs={"type": "date"})}
        labels = {
            "pbd": "Birthday",
            "pgender": "Gender",
            "pfname": "First Name",
            "plname": "Last Name",
            "prace": "Race",
            "pstatus": "Martial Status",
        }

class PatientUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PatientUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Patient
        exclude = ["pid"]
        widgets = {"pbd": DateInput(attrs={"type": "date"})}
        labels = {
            "pbd": "Birthday",
            "pgender": "Gender",
            "pfname": "First Name",
            "plname": "Last Name",
            "prace": "Race",
            "pstatus": "Martial Status",
        }


class PatientTreatmentForm(ModelForm):
    phid = IntegerField(widget=HiddenInput, label="")

    def __init__(self, phid, *args, **kwargs):
        super(PatientTreatmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        self.fields["phid"].initial = phid

    class Meta:
        model = PatientTreatment
        fields = ["pid", "tdate", "tfreq", "tstatus", "tid"]
        widgets = {
            "tdate": DateInput(attrs={"type": "date"}),
            "tfreq": TextInput(attrs={"type": "number", "min": "0"}),
        }
        labels = {
            "tdate": "Start Date",
            "tfreq": "Frequency",
            "tstatus": "Status",
            "pid": "Patient",
            "tid": "Treatment",
        }


class CaseUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CaseUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = PatientTreatment
        fields = ["pid", "tdate", "tfreq", "tstatus", "tid", "phid"]
        widgets = {
            "tdate": DateInput(attrs={"type": "date"}),
            "tfreq": TextInput(attrs={"type": "number", "min": "0"}),
        }
        labels = {
            "tdate": "Start Date",
            "tfreq": "Frequency",
            "tstatus": "Status",
            "pid": "Patient",
            "tid": "Treatment",
            "phid": "Physician",
        }


class TreatmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(TreatmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Treatment
        exclude = ["tid"]
        labels = {"tname": "Name", "ttype": "Type", "deid": "Disease"}


class DiseaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiseaseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Disease
        exclude = []
        labels = {"deid": "Disease", "dename": "Name"}
