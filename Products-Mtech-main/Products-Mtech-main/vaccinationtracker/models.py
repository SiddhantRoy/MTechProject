from statistics import mode
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    mobile_no = models.CharField(max_length=10, default='9778481904')
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    # address = models.CharField(max_length=250, default="Nalco colony")
    # city = models.CharField(max_length=50, default="Bhubaneswar")
    # state = models.CharField(max_length=50, default="Odisha")
    # zip = models.IntegerField(default=751023)
    gender = models.CharField(max_length=5, default='Female')
    is_student = models.BooleanField(default=False)
    is_school_coordinator = models.BooleanField(default=False)
    vaccination_status = models.BooleanField(default=False)
    vaccination_date = models.CharField(max_length=10, default='08-10-2022')
    name_of_vaccination = models.CharField(max_length=20, default="covaxin")

    @property
    def imageurl(self):
        return self.document.url

class VaccinationDrive(models.Model):
    date = models.CharField(max_length=10, unique=True)
    no_of_slots = models.IntegerField()
    is_slote_done = models.BooleanField(default=False)

    def __str__(self):
        return self.date


class Products(models.Model):
    preffered_product_name = models.CharField(max_length=250, unique=True)
    product_line = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    product_number = models.CharField(max_length=100)
    dosage_form = models.CharField(max_length=100)
    date_type = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    route_of_admin = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    primary = models.CharField(max_length=100)
    active_ingredient_name = models.CharField(max_length=100)
    strength = models.CharField(max_length=100)
    quantity_unit = models.CharField(max_length=100)
    compendium = models.CharField(max_length=100)
    registration_department = models.CharField(max_length=100)
    marketing_department = models.CharField(max_length=100)
    labbeling_department = models.CharField(max_length=100)
    prod_imp_department = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    maintenance = models.CharField(max_length=50)
    ranking = models.CharField(max_length=100)
    person = models.CharField(max_length=150)
    role  = models.CharField(max_length=150)
    comments = models.CharField(max_length=150)
    reg_id = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.preffered_product_name
    
class FormulationPackaging(models.Model):
    from_product = models.CharField(max_length=250)
    formulation_no = models.CharField(max_length=250)
    basic_formulation_no = models.CharField(max_length=250)
    version_no = models.CharField(max_length=250)
    dosage_form = models.CharField(max_length=250)
    remarks = models.CharField(max_length=250)
    composition_name = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    ingredient = models.CharField(max_length=250)
    qty_type = models.CharField(max_length=250)
    quantity = models.CharField(max_length=250)
    quantity_unit = models.CharField(max_length=250)
    function = models.CharField(max_length=250)
    packaging_code = models.CharField(max_length=250)
    basic_packaging_code = models.CharField(max_length=250)
    version_no = models.CharField(max_length=250)
    remarks_packaging = models.CharField(max_length=250)
    packaging_type = models.CharField(max_length=250)
    packaging_material = models.CharField(max_length=250)
    closure = models.CharField(max_length=250)
    full_volume_text = models.CharField(max_length=250)
    full_volume_drpdwn = models.CharField(max_length=250)
    packaging_size_txt = models.CharField(max_length=250)
    packaging_size_drpdwn = models.CharField(max_length=250)
    nominal_volume_text = models.CharField(max_length=250)
    nominal_volume_drpdwn = models.CharField(max_length=250)
    packaging_size_text = models.CharField(max_length=250)
    reg_id = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.from_product
    
class Labelling(models.Model):
    preffered_product_name = models.CharField(max_length=250, unique=True)
    indication = models.CharField(max_length=250)
    med_dra_code = models.CharField(max_length=250)
    atc_class = models.CharField(max_length=250)
    icd_term = models.CharField(max_length=250)
    labelling_remarks = models.CharField(max_length=250)
    dosage_schedule = models.CharField(max_length=250)
    direction_for_usage = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.indication
    
class ManufacturingDetails(models.Model):
    preffered_product_name = models.CharField(max_length=250, unique=True)
    manufacturing_step = models.CharField(max_length=250)
    manufacturing_site_city = models.CharField(max_length=250)
    manufacturing_site_state = models.CharField(max_length=250)
    control_site_city = models.CharField(max_length=250)
    control_site_state = models.CharField(max_length=250)
    batch_size = models.CharField(max_length=250)
    batch_size_dropdown = models.CharField(max_length=250)
    shelf_life = models.CharField(max_length=250)
    recomended_storage_conditions = models.CharField(max_length=250)
    application_fee = models.CharField(max_length=200)
    verification_level = models.CharField(max_length=200)
    created_by = models.CharField(max_length=100)
    expiryDate = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.manufacturing_step
    

class Registration(models.Model):
    select_products = models.CharField(max_length=250)
    select_procedure_types = models.CharField(max_length=250)
    select_countries = models.CharField(max_length=250)
    select_companies = models.CharField(max_length=250)
    # select_product_to_review_manfac_details = models.CharField(max_length=250)
    # include_step = models.CharField(max_length=250)
    # include_test = models.CharField(max_length=250)
    drom_product = models.CharField(max_length=250)
    mfg_step = models.CharField(max_length=250)
    mfg_site = models.CharField(max_length=250)
    component = models.CharField(max_length=250)
    # select_product_to_review_document = models.CharField(max_length=250)
    # document_type = models.CharField(max_length=250)
    reference_number = models.CharField(max_length=250)
    version = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    document_class = models.CharField(max_length=250)
    issue_date = models.CharField(max_length=250)
    # registration_products = models.CharField(max_length=250)
    reg_set_number = models.CharField(max_length=250)
    local_trade_name = models.CharField(max_length=250)
    legal_product_category = models.CharField(max_length=250)
    dispensing_class = models.CharField(max_length=250)
    strategic_priority = models.CharField(max_length=250)
    prescription_statement = models.CharField(max_length=250)
    person = models.CharField(max_length=250)
    role = models.CharField(max_length=250)
    comments = models.CharField(max_length=250)
    created_on = models.CharField(max_length=250)
    application_stage = models.CharField(max_length=250)
    registration_holder = models.CharField(max_length=250)
    resp_reg_dept = models.CharField(max_length=250)
    basicInfoComments = models.CharField(max_length=250)
    status_group = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    status_date = models.CharField(max_length=250)
    remarks = models.CharField(max_length=250)
    created_by = models.CharField(max_length=100)
    created_date_time = models.DateTimeField(auto_now_add=True)


class RegisterMaintenance(models.Model):
    product_name = models.CharField(max_length=250)
    formulation_no = models.CharField(max_length=250)
    version_no = models.CharField(max_length=250)
    composition_name = models.CharField(max_length=250)
    created_field = models.CharField(max_length=250)
    renewal_date = models.CharField(max_length=250)
    product_rename = models.CharField(max_length=250)
    new_reg_id = models.CharField(max_length=250)
    application_type = models.CharField(max_length=250)
    document_link = models.CharField(max_length=250)
    status = models.CharField(max_length=250)
    reason = models.CharField(max_length=250)
    application_fees = models.CharField(max_length=250)
    verification_level = models.CharField(max_length=250)
    updated_by = models.DateField(auto_now_add=True)


class SaveDocument(models.Model):
    product_name = models.CharField(max_length=250)
    product_status = models.CharField(max_length=250)
    creation_date = models.CharField(max_length=250)
    creator_name = models.CharField(max_length=250)
    version_no = models.CharField(max_length=250)
    company_final_status = models.CharField(max_length=250)
    remark = models.CharField(max_length=250)
    govt_approval = models.CharField(max_length=250)
    govt_remark = models.CharField(max_length=250)

class NationalSave(models.Model):
    product_name = models.CharField(max_length=250)
    version = models.CharField(max_length=250)
    creation_date = models.CharField(max_length=250)
    govt_approval = models.CharField(max_length=250)
    expiry_date = models.CharField(max_length=250)
    state  = models.CharField(max_length=250)
    remark = models.CharField(max_length=250)


class InternationalSave(models.Model):
    product_name = models.CharField(max_length=250)
    version = models.CharField(max_length=250)
    creation_date = models.CharField(max_length=250)
    govt_approval = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    mou = models.CharField(max_length=250)

