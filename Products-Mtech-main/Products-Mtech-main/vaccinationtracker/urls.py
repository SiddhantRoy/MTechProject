

from django.urls import path
from .views import (login_view, registration_page, notification, approval_list, get_approve_user, dashboard, logout_view, products_page, saveProducts, saveFormulationPackaging, labelling, manufacturingDetails,
                      registration_wizard, get_manfac_details, qr_code_generator_page, fetch_products_details_to_product_contents_page, save_registration_details,
                      register_maintenance, fetch_details_asper_product_name_to_maintainance_page, updated_maintenance, documentation, save_documentation, national_verification,
                      save_national_verification, inter_national_verification, save_inter_national_verification, register_list, fetch_register_list, fetch_int_register_list,
                      graph)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registraion/', registration_page, name='registraion'),
    path('notification/', notification, name='notification'),
    path('approval_list/', approval_list, name='approval_list'),
    path('get_approve_user/', get_approve_user, name='get_approve_user'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('products/', products_page, name='products'),
    path('save_products/', saveProducts, name='save_products'),
    path('saveFormulationPackaging/', saveFormulationPackaging, name='saveFormulationPackaging'),
    path('labelling/', labelling, name='labelling'),
    path('manufacturingDetails/', manufacturingDetails, name='manufacturingDetails'),
    path('registration_wizard/', registration_wizard, name='registration_wizard'),
    path('get_manfac_details/', get_manfac_details, name='get_manfac_details'),
    path('qr_code_generator_page/', qr_code_generator_page, name='qr_code_generator_page'),
    path('send/', qr_code_generator_page),
    path('fetch_products_details_to_product_contents_page/', fetch_products_details_to_product_contents_page, name='fetch_products_details_to_product_contents_page'),
    path('save_registration_details/', save_registration_details, name='save_registration_details'),
    path('register_maintenance/', register_maintenance, name='register_maintenance'),
    path('fetch_details_asper_product_name_to_maintainance_page/', fetch_details_asper_product_name_to_maintainance_page, name='fetch_details_asper_product_name_to_maintainance_page'),
    path('updated_maintenance/', updated_maintenance, name='updated_maintenance'),
    path('documentation/', documentation, name='documentation'),
    path('save_documentation/', save_documentation, name='save_documentation'),
    path('national_verification/', national_verification, name='national_verification'),
    path('save_national_verification/', save_national_verification, name='save_national_verification'),
    path('inter_national_verification/', inter_national_verification, name='inter_national_verification'),
    path('save_inter_national_verification/', save_inter_national_verification, name='save_inter_national_verification'),
    path('register_list/', register_list, name='register_list'),
    path('fetch_register_list/', fetch_register_list, name='fetch_register_list'),
    path('fetch_int_register_list/', fetch_int_register_list, name='fetch_int_register_list'),
    path('graph/', graph, name='graph'),

]
