from audioop import add
from re import T
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import request, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from pyexcel_xlsx import get_data as xlsx_get
from django.contrib.auth.hashers import make_password

from .models import CustomUser, Products, FormulationPackaging, Labelling, ManufacturingDetails, Registration, RegisterMaintenance, SaveDocument, NationalSave, InternationalSave
from .serialization import CustomUserSerialization
# Create your views here.

def login_view(request):

    if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to='/dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                user_obj = CustomUser.objects.get(username = user)
                request.session['username'] = user_obj.username
                request.session['is_student'] = user_obj.is_student
                request.session['is_school_coordinator'] = user_obj.is_school_coordinator
                return HttpResponseRedirect(redirect_to='/dashboard')

            else:
                return HttpResponseRedirect(redirect_to='/login')

    return render(request, 'login.html')

def registration_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('fstnm')
        last_name = request.POST.get('lstnm')
        user_name = request.POST.get('usnm')
        gender = request.POST.get('inlineRadioOptions')
        email = request.POST.get('emil')
        phone_number = request.POST.get('phnm')
        document = request.FILES.get('docs')
        password = request.POST.get('pswd')

        user = CustomUser(first_name=first_name, last_name=last_name, username=user_name, gender=gender, email=email, mobile_no=phone_number, document=document)
        user.password = make_password(password)
        user.is_active = False
        user.save()

        return HttpResponse("User created Successfully, but able to get login once get approve from Superuser", content_type='text/plain')

    return render(request, 'registraion.html')

@login_required()
@api_view(['GET'])
def notification(request):
    
    for_approval = CustomUser.objects.filter(is_active = False).all()
    data = CustomUserSerialization(for_approval, many=True)
    return Response(data)

@login_required()
def approval_list(request):
    obj = CustomUser.objects.filter(is_active = False).all()
    return render(request, 'notifications.html', {"data": obj})

@login_required()
@api_view(['GET'])
def get_approve_user(request):
    user_id = request.query_params['user_id']

    us_obj = CustomUser.objects.get(id=user_id)
    us_obj.is_active = True
    us_obj.is_superuser = True
    us_obj.is_school_coordinator = True
    us_obj.is_student = True
    us_obj.save()
    return Response({"Success": "User Approved Successfully"})


@login_required()
def logout_view(request):
    del request.session['username']
    del request.session['is_student']
    del request.session['is_school_coordinator']
    logout(request)
    return HttpResponseRedirect(redirect_to='/login')


@login_required(login_url="/login/")
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url="/login/")
def products_page(request):
    return render(request, 'products.html')


# new app
@login_required
@api_view(['GET'])
def saveProducts(request):

    preffered_product_name=request.query_params['productName']
    product_line=request.query_params['productLine']
    product_type=request.query_params['productType']
    product_number=request.query_params['productNumber']
    dosage_form=request.query_params['dosageForm']
    date_type=request.query_params['dateFormat']
    date=request.query_params['date']
    route_of_admin=request.query_params['role']
    country=request.query_params['country']
    primary=request.query_params['primary']
    active_ingredient_name=request.query_params['activeIngredient']
    strength=request.query_params['strength']
    quantity_unit=request.query_params['quantity']
    compendium=request.query_params['compendium']
    registration_department=request.query_params['registrationDept']
    marketing_department=request.query_params['marketingDept']
    labbeling_department=request.query_params['lebelingDept']
    prod_imp_department=request.query_params['prodImpDept']
    priority=request.query_params['priority']
    maintenance=request.query_params['maintenance']
    ranking=request.query_params['ranking']
    person=request.query_params['person']
    role=request.query_params['role']
    comments=request.query_params['comments']
    created_by=request.user

    is_exists = Products.objects.filter(preffered_product_name=preffered_product_name)

    reg_id_obj = Products.objects.values('reg_id').last()
    print(reg_id_obj)

    if reg_id_obj['reg_id']!='':
        reg_id = reg_id_obj['reg_id']
        last_no = int(reg_id[-1])
        last_no = last_no+1
        new_reg_id = reg_id[:-1] + str(last_no)
    else:
        new_reg_id = "prod0001"

    # reg_id = reg_id_obj['reg_id']

    # last_no = int(reg_id[-1])

    # last_no = last_no + 1

    # new_reg_id = reg_id[:-1] + str(last_no)

    if is_exists:
        Products.objects.filter(preffered_product_name=preffered_product_name).update(preffered_product_name=preffered_product_name, product_line = product_line, product_type = product_type, product_number = product_number, dosage_form = dosage_form,
            date_type = date_type, date = date, route_of_admin = route_of_admin, country = country, primary = primary, active_ingredient_name = active_ingredient_name,
            strength = strength, quantity_unit = quantity_unit, compendium = compendium, registration_department = registration_department, marketing_department = marketing_department,
            labbeling_department = labbeling_department, prod_imp_department = prod_imp_department, priority = priority, maintenance = maintenance, ranking = ranking, person = person,
            role = role, comments = comments)
        
        return Response({"success": "Product Updated Successfully"})
    
    else:
        product_obj = Products(preffered_product_name=preffered_product_name, product_line = product_line, product_type = product_type, product_number = product_number, dosage_form = dosage_form,
        date_type = date_type, date = date, route_of_admin = route_of_admin, country = country, primary = primary, active_ingredient_name = active_ingredient_name,
        strength = strength, quantity_unit = quantity_unit, compendium = compendium, registration_department = registration_department, marketing_department = marketing_department,
        labbeling_department = labbeling_department, prod_imp_department = prod_imp_department, priority = priority, maintenance = maintenance, ranking = ranking, person = person,
        role = role, comments = comments, reg_id = new_reg_id, created_by = created_by)

        product_obj.save()

        return Response({"success": "Product Created Successfully"})


# new app
@login_required
@api_view(['GET'])
def saveFormulationPackaging(request):

    from_product = request.query_params['fromProduct']
    formulation_no = request.query_params['formulationNo']
    basic_formulation_no = request.query_params['basicFormulationNo']
    version_no = request.query_params['versionNo']
    dosage_form = request.query_params['dosageForm']
    remarks = request.query_params['remark']
    composition_name = request.query_params['compositionName']
    description = request.query_params['description']
    ingredient = request.query_params['ingredient']
    qty_type = request.query_params['quantityType']
    quantity = request.query_params['quantity']
    quantity_unit = request.query_params['quantityUnit']
    function = request.query_params['function']
    packaging_code = request.query_params['packagingCode']
    basic_packaging_code = request.query_params['basicPackagingCode']
    remarks_packaging = request.query_params['packRemak']
    packaging_type = request.query_params['packageType']
    packaging_material = request.query_params['packageMaterial']
    closure = request.query_params['closure']
    full_volume_text = request.query_params['fullVolumeText']
    full_volume_drpdwn = request.query_params['fullVolumeDrpdwn']
    packaging_size_txt = request.query_params['packagingSizeText']
    packaging_size_drpdwn = request.query_params['packagingSizeDrpdwn']
    nominal_volume_text = request.query_params['nominalVolumeText']
    nominal_volume_drpdwn = request.query_params['nominalVolumeDrpdwn']
    packaging_size_text = request.query_params['packagingSizeTxt']
    created_by = request.user

    is_exists = FormulationPackaging.objects.filter(from_product=from_product)

    reg_id_obj = Products.objects.values('reg_id').last()
    if reg_id_obj:
        reg_id = reg_id_obj['reg_id']
        last_no = int(reg_id[-1])
        last_no = last_no+1
        new_reg_id = reg_id[:-1] + str(last_no)
    else:
        new_reg_id = "prod0001"

    # reg_id = reg_id_obj['reg_id']

    # last_no = int(reg_id[-1])

    # last_no = last_no + 1

    # new_reg_id = reg_id[:-1] + str(last_no)

    if is_exists:
        FormulationPackaging.objects.filter(from_product=from_product).update(from_product = from_product, formulation_no = formulation_no, basic_formulation_no = basic_formulation_no, version_no = version_no,
                        dosage_form = dosage_form, remarks = remarks, composition_name = composition_name, description = description,
                        ingredient = ingredient, qty_type = qty_type, quantity = quantity, quantity_unit = quantity_unit, function = function, packaging_code = packaging_code,
                        basic_packaging_code = basic_packaging_code, remarks_packaging=remarks_packaging,
                        packaging_type = packaging_type,  packaging_material = packaging_material, closure = closure, full_volume_text = full_volume_text,
                        full_volume_drpdwn = full_volume_drpdwn, packaging_size_txt = packaging_size_txt, packaging_size_drpdwn = packaging_size_drpdwn, 
                        nominal_volume_text = nominal_volume_text, nominal_volume_drpdwn = nominal_volume_drpdwn, packaging_size_text = packaging_size_text)
        
        return Response({"success": "Formulation and Packaging Updated Successfully"})
    
    else:
        obj = FormulationPackaging(from_product = from_product, formulation_no = formulation_no, basic_formulation_no = basic_formulation_no, version_no = version_no,
                        dosage_form = dosage_form, remarks = remarks, composition_name = composition_name, description = description,
                        ingredient = ingredient, qty_type = qty_type, quantity = quantity, quantity_unit = quantity_unit, function = function, packaging_code = packaging_code,
                        basic_packaging_code = basic_packaging_code, remarks_packaging=remarks_packaging,
                        packaging_type = packaging_type,  packaging_material = packaging_material, closure = closure, full_volume_text = full_volume_text,
                        full_volume_drpdwn = full_volume_drpdwn, packaging_size_txt = packaging_size_txt, packaging_size_drpdwn = packaging_size_drpdwn, 
                        nominal_volume_text = nominal_volume_text, nominal_volume_drpdwn = nominal_volume_drpdwn, reg_id = new_reg_id, packaging_size_text = packaging_size_text,  created_by = created_by)

        obj.save()

    return Response({"success": "Formulation and Packaging Created Successfully"})


# new app
@api_view(['GET'])
def labelling(request):
    preffered_product_name=request.query_params['productName']
    indication = request.query_params['indication']
    med_dra_code = request.query_params['medDraCOde']
    atc_class = request.query_params['ateClass']
    icd_term = request.query_params['icdTerm']
    labelling_remarks = request.query_params['labellingRemark']
    dosage_schedule = request.query_params['dosageSchedule']
    direction_for_usage = request.query_params['directionForUsage']
    created_by = request.user

    is_exists = Labelling.objects.filter(preffered_product_name=preffered_product_name)

    if is_exists:
        Labelling.objects.filter(preffered_product_name=preffered_product_name).update(preffered_product_name=preffered_product_name, indication = indication, med_dra_code = med_dra_code, atc_class = atc_class, icd_term = icd_term,
                        labelling_remarks = labelling_remarks, dosage_schedule = dosage_schedule, direction_for_usage = direction_for_usage)
        return Response({"success": "Labelling Updated Successfully"})
    
    else:
        obj = Labelling(preffered_product_name=preffered_product_name, indication = indication, med_dra_code = med_dra_code, atc_class = atc_class, icd_term = icd_term,
                        labelling_remarks = labelling_remarks, dosage_schedule = dosage_schedule, direction_for_usage = direction_for_usage, created_by = created_by)

        obj.save()

    return Response({"success": "Labelling Created Successfully"})


# new app
@api_view(['GET'])
def manufacturingDetails(request):
    preffered_product_name=request.query_params['productName']
    manufactureingStep = request.query_params['manufactureingStep']
    manufacturing_site_city = request.query_params['manufactureingSiteCity']
    manufactureingSiteState = request.query_params['manufactureingSiteState']
    ControlSiteCity = request.query_params['ControlSiteCity']
    ControlSiteState = request.query_params['ControlSiteState']
    batchSize = request.query_params['batchSize']
    batchSizeDropdown = request.query_params['batchSizeDropdown']
    shelfLife = request.query_params['shelfLife']
    recomendedStorageCondition = request.query_params['recomendedStorageCondition']
    application_fee = request.query_params['applicationFee']
    verification_level = request.query_params['verificationLevel']
    expiry_date = request.query_params['expiryDate']
    created_by = request.user

    exists = ManufacturingDetails.objects.filter(preffered_product_name=preffered_product_name)

    if exists:
        ManufacturingDetails.objects.filter(preffered_product_name=preffered_product_name).update(preffered_product_name=preffered_product_name, manufacturing_step=manufactureingStep, manufacturing_site_city=manufacturing_site_city, manufacturing_site_state=manufactureingSiteState,
                                control_site_city=ControlSiteCity, control_site_state=ControlSiteState, batch_size= batchSize,
                                  batch_size_dropdown=batchSizeDropdown, shelf_life=shelfLife, recomended_storage_conditions=recomendedStorageCondition, application_fee = application_fee, verification_level = verification_level, expiryDate = expiry_date)
        return Response({"success": "Manufacturing Details Updated Successfully"})
    
    obj = ManufacturingDetails(preffered_product_name=preffered_product_name, manufacturing_step=manufactureingStep, manufacturing_site_city=manufacturing_site_city, manufacturing_site_state=manufactureingSiteState,
                                control_site_city=ControlSiteCity, control_site_state=ControlSiteState, batch_size= batchSize,
                                  batch_size_dropdown=batchSizeDropdown, shelf_life=shelfLife, recomended_storage_conditions=recomendedStorageCondition, application_fee = application_fee, verification_level = verification_level, expiryDate = expiry_date, created_by = created_by)

    obj.save()

    return Response({"success": "ManufacturingDetails Created Successfully"})

from qrcode import *

def qr_code_generator_page(request):
    if request.method=="POST":

        product = request.POST['data']

        formulation_details = (FormulationPackaging.objects.filter(from_product = product).values("ingredient", "qty_type"))
        data = {"ProductName": product, "ingredient": formulation_details[0]['ingredient'], "Quantity": formulation_details[0]['qty_type']}

        img=make(data)
        img.save("static/linercost/qr/test.png")
        return render(request,"qr_code.html",{'data':data})

    else:
        obj = Products.objects.all().values("preffered_product_name")
        return render(request, 'qr_code.html', {"obj": obj})

# new app
def registration_wizard(request):
    obj = Products.objects.all().values("preffered_product_name")
    return render(request, 'registration_wizard.html', {"obj": obj})

# new app
@api_view(['GET'])
def get_manfac_details(request):
    preffered_product_name=request.query_params['productName']
    obj = ManufacturingDetails.objects.filter(preffered_product_name=preffered_product_name).values("manufacturing_step", "manufacturing_site_city", "manufacturing_site_state")
    return Response({"obj": obj[0]})


@api_view(['GET'])
def fetch_products_details_to_product_contents_page(request):
    product_name=request.query_params['productName']
    
    list_product_name = product_name.split(',')

    response = []

    for a in list_product_name:
        obj = FormulationPackaging.objects.filter(from_product = a).values('from_product', 'version_no', 'packaging_code', 'packaging_type', 'packaging_material', 'basic_packaging_code', 'closure', 'packaging_size_txt')
        response.append(obj[0])

    return Response({"obj": response})


# new app
@api_view(['GET'])
def save_registration_details(request):
    select_products = request.query_params['productName']
    select_procedure_types = request.query_params['selectProcedureType']
    select_countries = request.query_params['selectCountries']
    select_companies = request.query_params['selectCompanies']
    drom_product = request.query_params['fromProduct']
    mfg_step = request.query_params['mfgStep']
    mfg_site = request.query_params['mfgSite']
    component = request.query_params['component']
    reference_number = request.query_params['referenceNumber']
    version = request.query_params['version']
    title = request.query_params['title']
    document_class = request.query_params['documentClass']
    issue_date = request.query_params['issueDate']
    reg_set_number = request.query_params['regSetNumber']
    local_trade_name = request.query_params['localTradeNo']
    legal_product_category = request.query_params['legalProductCategory']
    dispensing_class = request.query_params['dispensingClass']
    strategic_priority = request.query_params['strategicPriority']
    prescription_statement = request.query_params['prescriptionStatement']
    person = request.query_params['person']
    role = request.query_params['role']
    comments = request.query_params['comments']
    created_on = request.query_params['createdOn']
    print('Test.....',request.query_params['applicationStage'])
    application_stage = request.query_params['applicationStage']
    registration_holder = request.query_params['registrationHolder']
    resp_reg_dept = request.query_params['respRegDept']
    basic_info_comments = request.query_params['basicInfocomments']
    status_group = request.query_params['statusGroup']
    status = request.query_params['status']
    status_date = request.query_params['statusDate']
    remarks = request.query_params['remarks']
    created_by = request.user

    obj = Registration(select_products = select_products, select_procedure_types = select_procedure_types, select_countries = select_countries, select_companies = select_companies,
            drom_product = drom_product, mfg_step = mfg_step, mfg_site = mfg_site, component = component,
            reference_number = reference_number, version = version, title = title, document_class = document_class,
            issue_date = issue_date, reg_set_number = reg_set_number, local_trade_name = local_trade_name, legal_product_category = legal_product_category,
            dispensing_class = dispensing_class, strategic_priority = strategic_priority, prescription_statement = prescription_statement, person = person,
            role = role, comments = comments, created_on = created_on, application_stage = application_stage, registration_holder = registration_holder,
            resp_reg_dept = resp_reg_dept, basicInfoComments = basic_info_comments, status_group = status_group, status = status, status_date = status_date,
            remarks = remarks, created_by = created_by)
    
    obj.save()

    return Response({"success": "Registration Details Saved Successfully"})
# new app
def register_maintenance(request):
    obj = Products.objects.all().values("preffered_product_name")
    return render(request, 'register_maintenance.html', {"obj": obj})

# new app
@api_view(['GET'])
def fetch_details_asper_product_name_to_maintainance_page(request):

    product_name = request.query_params['productName']

    formulation_obj = FormulationPackaging.objects.filter(from_product = product_name).values('from_product', 'reg_id', 'created_date_time', 'formulation_no', 'version_no', 'composition_name')
    
    return Response({"formulation_obj": formulation_obj})

# new app
@api_view(['GET'])
def updated_maintenance(request):

    product_name = request.query_params['productName']
    formulation_no = request.query_params['formulationNo']
    version_no = request.query_params['versionNo']
    composition_name = request.query_params['compositionName']
    created_field = request.query_params['createdField']
    renewal_date = request.query_params['renewalField']
    product_rename = request.query_params['productRename']
    new_reg_id = request.query_params['newRegID']
    application_type = request.query_params['applicationType']
    document_link = request.query_params['documentLink']
    status = request.query_params['status']
    reason = request.query_params['reason']
    application_fees = request.query_params['applicationFees']
    verification_level = request.query_params['verificationLevel']
    updated_by = request.user
    
    obj = RegisterMaintenance(product_name = product_name,formulation_no = formulation_no, version_no = version_no, composition_name = composition_name,
                            created_field = created_field, renewal_date = renewal_date, product_rename = product_rename, new_reg_id = new_reg_id,
                        application_type = application_type, document_link = document_link, status = status, reason = reason, application_fees = application_fees,
                        verification_level = verification_level, updated_by = updated_by)
    
    obj.save()
    return Response({"response": "Updated Successfully"})


# new app
def documentation(request):

    product_obj = list(Products.objects.values('preffered_product_name', 'created_date_time', 'created_by'))


    maintenance_status_obj = RegisterMaintenance.objects.all().values('status', 'version_no')


    for ind, item in enumerate(product_obj):

        # product_obj[ind]['status'] = maintenance_status_obj[a]['status']
        # product_obj[ind]['version_no'] = maintenance_status_obj[a]['version_no']

        product_obj[ind]['status'] = "Status"
        product_obj[ind]['version_no'] = "253"

    return render(request, 'documents.html', {"product_obj": product_obj})


# new app
@api_view(['GET'])
def save_documentation(request):

    product_name = request.query_params['productName']
    product_status = request.query_params['ProductStatus']
    creation_date = request.query_params['creationDate']
    creator_name = request.query_params['creatorName']
    version_no = request.query_params['versionName']
    company_final_status = request.query_params['companyFinalStatus']
    remark = request.query_params['remark']
    govt_approval = request.query_params['govtApproval']
    govt_remark = request.query_params['govtRemark']

    docs_obj = SaveDocument(product_name = product_name, product_status = product_status, creation_date = creation_date,
                            creator_name = creator_name, version_no = version_no, company_final_status = company_final_status,
                            remark = remark, govt_approval = govt_approval, govt_remark = govt_remark)
    docs_obj.save()

    return Response({"response": "Data saved Successfully"})


# new app
def national_verification(request):

    formulation_obj = list(FormulationPackaging.objects.values('from_product', 'version_no', 'created_date_time'))


    manufacturing_obj = ManufacturingDetails.objects.all().values('manufacturing_site_state', 'expiryDate')


    for ind, item in enumerate(formulation_obj):

        # manufacturing_obj[ind]['status'] = manufacturing_obj[a]['status']
        # manufacturing_obj[ind]['version_no'] = manufacturing_obj[a]['version_no']

        formulation_obj[ind]['state'] = "dummu"
        formulation_obj[ind]['expiry_date'] = "dummy 12/12/2023"

    return render(request, 'national_verification.html', {"formulation_obj": formulation_obj})


@api_view(['GET'])
def save_national_verification(request):

    product_name = request.query_params['productName']
    version = request.query_params['version']
    creation_date = request.query_params['creationDate']
    govt_approval = request.query_params['govtApproval']
    state = request.query_params['state']
    remark = request.query_params['remark']

    national_docs_obj = NationalSave(product_name = product_name, version = version, creation_date = creation_date,
                govt_approval = govt_approval, state = state, remark=remark)
    
    national_docs_obj.save()

    return Response({"response": "Data saved Successfully"})


# new app
def inter_national_verification(request):

    formulation_obj = list(FormulationPackaging.objects.values('from_product', 'version_no', 'created_date_time'))

    for ind,i in enumerate(formulation_obj):

        x = i['from_product']

        registration_obj = list(Registration.objects.filter(select_products__icontains = x ).values('select_countries'))

        if registration_obj:
            formulation_obj[ind]['country'] = registration_obj[0]['select_countries']
        else:
            formulation_obj[ind]['country'] = "Germany, Austria, Egypt"

    return render(request, 'international_verification.html', {"formulation_obj": formulation_obj})


@api_view(['get'])
def save_inter_national_verification(request):
    product_name = request.query_params['productName']
    version = request.query_params['version']
    creation_date = request.query_params['creationDate']
    govt_approval = request.query_params['govtApproval']
    country = request.query_params['country']
    mou = request.query_params['mou']

    int_national_docs_obj = InternationalSave(product_name = product_name, version = version, creation_date = creation_date,
                govt_approval = govt_approval, country = country, mou=mou)
    
    int_national_docs_obj.save()

    return Response({"response": "Data saved Successfully"})

from django.db.models import Count

def register_list(request):
    return render(request, 'register_list.html')

@api_view(['GET'])
def fetch_register_list(request):
    national_obj = list(NationalSave.objects.values("product_name", "version", "creation_date", "govt_approval", "expiry_date", "state", "remark").annotate(dcount=Count('govt_approval')))
    # intnational_obj = list(InternationalSave.objects.values("product_name", "version", "creation_date", "govt_approval", "country", "mou").annotate(dcount=Count('govt_approval')))
    print(national_obj)
    return Response({"national_response": national_obj})

@api_view(['GET'])
def fetch_int_register_list(request):
    
    intnational_obj = list(InternationalSave.objects.values("product_name", "version", "creation_date", "govt_approval", "country", "mou").annotate(dcount=Count('govt_approval')))

    return Response({"inter_national_response": intnational_obj})

@api_view(['GET'])
def graph(request):
    national_obj = list(NationalSave.objects.values("govt_approval").annotate(dcount=Count('govt_approval')))
    intnational_obj = list(InternationalSave.objects.values("govt_approval").annotate(dcount=Count('govt_approval')))

    print(national_obj, intnational_obj)
    
    return Response({"national_obj": national_obj, "intnational_obj": intnational_obj})