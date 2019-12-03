# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.db.backends.mysql.base import DatabaseWrapper


class Department(models.Model):
    did = models.AutoField(primary_key=True)
    dname = models.CharField(max_length=20)
    dtel = models.CharField(max_length=13)
    hid = models.ForeignKey("Hospital", models.CASCADE, db_column="hid")

    def __str__(self):
        return self.dname

    class Meta:
        # managed = False
        db_table = "department"


class Disease(models.Model):
    deid = models.CharField(primary_key=True, max_length=6)
    dename = models.CharField(max_length=30)

    def __str__(self):
        return f"({self.deid}): {self.dename}"

    class Meta:
        # managed = False
        db_table = "disease"


class Hospital(models.Model):
    hid = models.AutoField(primary_key=True)
    hname = models.CharField(max_length=30)
    hst_address = models.CharField(max_length=30)
    hst_city = models.CharField(max_length=30)
    hstate = models.CharField(max_length=20)
    hzip = models.IntegerField()

    class Meta:
        # managed = False
        db_table = "hospital"


class Patient(models.Model):
    GENDER = [("M", "Male"), ("F", "Female"), ("U", "Unkown")]
    RACE = [
        ("ASIAN", "Asian"),
        ("HISPANIC", "Hispanic"),
        ("LATINO", "Latin American"),
        ("AFRICAN", "African American"),
        ("OTHER", "Other"),
    ]
    STATUS = [
        ("M", "Married"),
        ("S", "Single"),
        ("D", "Devoiced"),
        ("W", "Widow or widower"),
    ]
    pid = models.AutoField(primary_key=True)
    pfname = models.CharField(max_length=30)
    plname = models.CharField(max_length=20)
    pgender = models.CharField(max_length=1, choices=GENDER)
    pbd = models.DateTimeField()
    prace = models.CharField(max_length=20, blank=True, null=True, choices=RACE)
    pstatus = models.CharField(max_length=1, choices=STATUS)

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.pfname.title()} {self.plname.title()}-{self.get_pgender_display()}-{self.get_prace_display()}-{self.pbd.strftime('%m/%d/%Y')}"

    class Meta:
        # managed = False
        db_table = "patient"


class PatientTreatment(models.Model):
    STATUS = [("S", "Successful"), ("R", "Repeat"), ("F", "Failed")]
    tdate = models.DateTimeField()
    tfreq = models.BigIntegerField(default=0)
    tstatus = models.CharField(max_length=1, blank=True, null=True, choices=STATUS)
    pid = models.ForeignKey(Patient, models.CASCADE, db_column="pid")
    tid = models.ForeignKey("Treatment", models.DO_NOTHING, db_column="tid")
    phid = models.ForeignKey("Physician", models.DO_NOTHING, db_column="phid")

    class Meta:
        # managed = False
        db_table = "patient_treatment"
        unique_together = (("pid", "phid", "tid", "tdate", "tfreq"),)


class Treatment(models.Model):
    TYPE = [("Pharma", "Pharma"), ("Procedure", "Procedure"), ("Surgery", "Surgery")]
    tid = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=50)
    ttype = models.CharField(max_length=10,choices=TYPE)
    deid = models.ForeignKey(Disease, models.DO_NOTHING, db_column="deid")

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.tname.title()}-{self.ttype}-{self.deid}"

    class Meta:
        # managed = False
        db_table = "treatment"


class Physician(models.Model):
    phid = models.AutoField(primary_key=True)
    phfname = models.CharField(max_length=30)
    phtel = models.CharField(max_length=13)
    phspl = models.CharField(max_length=30)
    hid = models.ForeignKey(Hospital, models.CASCADE, db_column="hid")
    patient = models.ManyToManyField(
        Patient, through="PatientTreatment", related_name="physician"
    )
    treatment = models.ManyToManyField(
        Treatment, through=PatientTreatment, related_name="physician"
    )

    def __str__(self):
        # pylint: disable=no-member
        return f"{self.phfname.title()}-{self.phspl}"

    class Meta:
        # managed = False
        db_table = "physician"


class Users(models.Model):
    uid = models.AutoField(
        db_column="UID", primary_key=True
    )  # Field name made lowercase.
    ufname = models.CharField(max_length=20)
    ulname = models.CharField(max_length=20)
    urole = models.CharField(max_length=20)
    did = models.ForeignKey(Department, models.DO_NOTHING, db_column="did")

    class Meta:
        # managed = False
        db_table = "users"
