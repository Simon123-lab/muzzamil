"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from views import admin_views, user_views

admin_urlpatterns = [
    #------- Admin Index
    path('', admin_views.admin_index),
    # ------ Admin REGISTER
    path('register', admin_views.admin_register),
    path('register_resp', admin_views.admin_register_response),
    # ------- Admin Account Deactivate
    path('deactivate', admin_views.admin_delete),
    # ------- Admin Account Update
    path('update', admin_views.admin_update),
    path('update_resp', admin_views.admin_update_response),
    #------- Admin Fetch USER lIST
    path('user', admin_views.user_list),
    #------ Admin Edit User
    path('EditUser', admin_views.user_edit),
    path('EditUser_resp', admin_views.user_edit_response),
    # ------- Admin Region page (ADD/ DELETE: COUNTRY, CITY)
    path('region', admin_views.admin_region),
    path('country', admin_views.country_add),
    path('country_del', admin_views.country_delete),
    path('city', admin_views.city_add),
    path('city_del', admin_views.city_delete),
    # ------- Admin Category
    path('category', admin_views.category_add),
    path('category_add', admin_views.category_add_response),
    path('category_del', admin_views.category_del),
    # ------- Ads List ------
    path('Ad', admin_views.ad_list),
    # ------- Ad Delete -------
    path('Ad_del', admin_views.ad_delete),
    # ------- Contact List -------
    path('Contact_list', admin_views.contact_list),
    # ------- Contact Delete -------
    path('Contact_del', admin_views.contact_delete),

    # search admin
    path('admin_search', admin_views.admin_search),
    # search user
    path('user_search', admin_views.user_search),
    # search country
    path('country_search', admin_views.country_search),
    # search ads
    path('ad_search', admin_views.ad_search),

]

user_urlpatterns = [
    #----- USER INDEX -----------
    path('', user_views.user_index),
    #------ USER REGISTER ----------
    path('register', user_views.register),
    path('register_resp', user_views.register_response),
    #------ USER ACCOUNT ACTIVE (email verification response) ----
    path('AccountActivate/<code>', user_views.activate_account),
    # ------ USER ACCOUNT Forget Password  ----
    path('ForgetPassword', user_views.forget_password),
    path('ForgetPassword_resp', user_views.forget_password_response),
    path('ChangePassword/<code>', user_views.forget_password_link),
    path('ChangePassword_resp', user_views.forget_password_link_response),

    # ---- USER DASHBOARD --- show all user ads
    path('Dashboard', user_views.dashboard),
    # ---- USER DASHBOARD --- show active user ads
    path('ActiveSell', user_views.user_active_sell),
    # ---- USER DASHBOARD --- show inactive user ads
    path('InActiveSell', user_views.user_inactive_sell),
    # ---- USER EDIT PROFILE---
    path('EditProfile', user_views.edit_profile),
    path('EditProfile_resp', user_views.edit_profile_response),
    #----- USER PROFILE PICTURE ----
    path('UploadProfilePicture', user_views.user_picture),
    #----- USER / Admin Login ----
    path('login', user_views.login),
    path('login_resp', user_views.login_response),
    #----- USER / Admin Logout ----
    path('logout', user_views.logout),
    #----- USER ADD ADS----
    path('AddSell', user_views.sell_add),
    path('AddSell_resp', user_views.sell_add_response),
    #----- USER Fetch all Ads ----
    path('ListSell', user_views.sell_list),
    # ------ Ads Changes Status -- (By Dashboard)
    path('AdChangeStatus/<item_id>', user_views.item_change_status),
    # ------ Ads Edit ---
    path('AdEdit/<item_code>', user_views.user_edit_sell),
    path('AdEdit_resp', user_views.user_edit_sell_response),
    # ------- Delete Ad Images (in edit ad) --
    path('Del_Image/<item_image_id>/<item_id>', user_views.delete_item_images),
    # ------- Delete Items -----
    path('DelAd/<item_code>', user_views.delete_item),
    # ------- Single Ad -------
    path('Ad/<item_code>', user_views.single_item),
    # ------- Ad Comment -------
    path('Comment', user_views.comment_item),
    # ------- Delete Comment (only by admin)
    path('Comment_del', user_views.comment_del),
    # ------- Item Search ------
    path('AdSearch', user_views.item_search),
    # ------- About us  ------
    path('About-us', user_views.aboutus),
    # ------- Contact us  ------
    path('Contact-us', user_views.contactus),
    path('Contact_resp', user_views.contactus_resp),
    # ------- User Account delete  ------
    path('User_Account_Deactivate', user_views.user_account_deactive),

    # ====== ajax
    # --- fetch city of country ---
    path('register/<str:user_country>', user_views.ajax_find_city),
    # --- item search auto complete ---
    path('item_search', user_views.item_search_autocomplete),
    *(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    *(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

# ==== MAIN URL
urlpatterns = [
    path('hello/', admin.site.urls),
    #-- All Admin paths ---
    path('admin/', include(admin_urlpatterns)),

    # ---- All User paths
    path('', include(user_urlpatterns)),
]
)