from datetime import datetime, date
import hashlib
import random
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from admin_app import models
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

# Create your views here.

# ====== Ajax
# ----------- FIND CITY BY COUNTRY
def ajax_find_city(request, user_country):
    country = models.Country.objects.get(country_name= user_country)
    city = models.City.objects.filter(fk_country=country).values('city_id', 'city_name').order_by('city_name')
    return JsonResponse({'data': list(city)})
    return HttpResponse('Wrong request')

# ----------- Item Search AutoComplete
def item_search_autocomplete(request):
    search_value = request.GET['term']
    if search_value != None:
        item_data = models.Item.objects.filter(item_title__icontains=search_value)
        titles = list()
        for item in item_data:
            titles.append(item.item_title)
        return JsonResponse(titles, safe=False)
    return HttpResponse('Wrong request')




# ============= user index
def user_index(request):
    if request.session.get('UserId') != None:
        item_data = models.Item.objects.filter(item_status='Active').order_by('-item_id') # fresh recomandation
        city_data = models.City.objects.filter().order_by('city_name') # location dropdown search
        category_data = models.Category.objects.filter().order_by('category_name')  # location dropdown search
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'item_data': item_data,
            'city_data': city_data,
            'category_data': category_data
        }
        return render(request, 'user/index.html', context)
    else:
        item_data = models.Item.objects.filter(item_status='Active').order_by('-item_id')
        return render(request, 'user/index.html', {'item_data': item_data})

# ============ User Register
def register(request):
    if request.session.get('UserId') != None:
        return redirect('/')
    else:
        country_data = models.Country.objects.all().order_by('country_name')
        context = {
            'country_data': country_data
        }
        return render(request, 'user/register.html', context)

def register_response(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        useremail = request.POST['user_email']
        userpassword = request.POST['user_password']
        userconfirmpassword = request.POST['user_confirm_password']
        userphone = request.POST['user_phone']
        userregisterfor = request.POST['user_register_for']
        usercountry = request.POST['user_country']
        usercity = request.POST['user_city']

        if userpassword == userconfirmpassword:
            checkuser = models.User.objects.filter(user_email=useremail).count()
            if checkuser == 0:
                encrypt_code= hashlib.md5(str(random.randint(1000, 9999)).encode("utf-8")).hexdigest()
                email_to = useremail
                firstname = username
                html_content = render_to_string("Mail/EmailVerification.html", {'name': firstname, 'activelink': encrypt_code})
                text_content = strip_tags(html_content)
                emailsend = EmailMultiAlternatives(
                    "Classimax",
                    text_content,
                    EMAIL_HOST_USER,
                    [email_to]
                )
                emailsend.attach_alternative(html_content, "text/html")
                emailsend.send()
                # add user data
                add_user = models.User()
                add_user.user_name = username
                add_user.user_email = useremail
                add_user.user_pass = hashlib.md5(userpassword.encode("utf-8")).hexdigest()
                add_user.user_phone = userphone
                add_user.user_mode = userregisterfor
                add_user.save()

                # get data for foreign keys
                fk_getuser = models.User.objects.get(user_email=useremail)
                fk_getcountry= models.Country.objects.get(country_name=usercountry)
                fk_getcity = models.City.objects.get(city_name=usercity)

                if fk_getuser :
                    # add user city
                    add_user_city = models.User_City()
                    add_user_city.fk_user = fk_getuser
                    add_user_city.fk_country = fk_getcountry
                    add_user_city.fk_city = fk_getcity
                    add_user_city.save()
                    # save otp code
                    account = models.Account_status()
                    account.account_code = encrypt_code
                    account.account_status = '0'
                    account.fk_user = fk_getuser
                    account.save()
                    messages.success(request, "Please check your e-mail to verify your account")
                    return redirect('/register')
                else:
                    messages.error(request, "Error, Please Try Again ...")
                    return redirect('/register')
            else:
                messages.error(request, "Account Already Registered")
                return redirect('/register')
        else:
            messages.error(request, "Confirm Password Doesn't Matched ...")
            return redirect('/register')
    else:
        messages.error(request, "Invalid Request ...")
        return redirect('/register')

# ============= User Account Activate
def activate_account(request, code):
    if code != None:
        account = models.Account_status.objects.filter(account_code=code).count()
        if account == 1:
            account = models.Account_status.objects.get(account_code=code)
            account_status = account.account_status
            account_id = account.account_id
            if account_status == "0":
                account = models.Account_status.objects.get(account_id = account_id)
                account.account_status = "1"
                account.save()
                messages.success(request, "Account verification successfull, please login...")
                return redirect('/login')
            else:
                messages.error(request, "Account already verified....")
                return redirect('/login')
        else:
            messages.error(request, "Incorrect Request...")
            return redirect('/login')
    else:
        return redirect('/')

# =========== Forget Password
def forget_password(request):
    if request.session.get('UserId') != None:
        return redirect('/login')
    else:
        return render(request, 'user/forget_password.html')

# =========== Forget Password Response
def forget_password_response(request):
    if request.method == 'POST':
        user_email = request.POST['email']
        user_data = models.User.objects.get(user_email= user_email)
        check_email = models.User.objects.filter(user_email= user_email).count()
        if check_email == 1:
            code = hashlib.md5(str(random.randint(1000, 9999)).encode("utf-8")).hexdigest()
            account = models.Account_status.objects.get(fk_user= user_data)
            account.account_code = code
            account.save()
            # send mail
            email_to = user_email
            firstname = user_data.user_name
            html_content = render_to_string("Mail/ForgetPassword.html",{'name': firstname, 'activelink': code})
            text_content = strip_tags(html_content)
            emailsend = EmailMultiAlternatives(
                "Classimax",
                text_content,
                EMAIL_HOST_USER,
                [email_to]
            )
            emailsend.attach_alternative(html_content, "text/html")
            emailsend.send()
            messages.success(request, 'Please check your email')
            return redirect('/ForgetPassword')
        elif check_email == 0:
            messages.error(request, 'Account is not registered..')
            return redirect('/ForgetPassword')
    else:
        messages.error(request, 'Invalid Request...')
        return redirect('/ForgetPassword')

# =========== Forget Password Link
def forget_password_link(request, code):
    if request.session.get('UserId') != None:
        return redirect('/login')
    else:
        if code != None:
            account = models.Account_status.objects.filter(account_code=code).count()
            if account == 1:
                return render(request, 'user/change_password.html', { 'code': code })
            else:
                messages.error(request, "Incorrect Request...")
                return redirect('/ForgetPassword')
        else:
            messages.error(request, 'Invalid Request...')
            return redirect('/ForgetPassword')

# =========== Forget Password Link Response
def forget_password_link_response(request):
    if request.method == 'POST':
        code = request.POST['code']
        user_password = request.POST['user_password']
        user_confirm_password = request.POST['user_confirm_password']
        if user_password == user_confirm_password:
            # get user email from account status
            account = models.Account_status.objects.get(account_code= code)
            user_email = account.fk_user.user_email
            # get user data by user email
            get_user = models.User.objects.get(user_email= user_email)
            get_user.user_pass = hashlib.md5(user_password.encode("utf-8")).hexdigest()
            get_user.save()
            messages.success(request, 'Password change, Login to your Account...')
            return redirect('/login')
        else:
            messages.error(request, 'Password and Confirm Password are not same ...')
            return redirect('/ChangePassword/' +code)
    else:
        messages.error(request, 'Invalid Request...')
        return redirect('/ForgetPassword')

# ============ User Profile Picture =====
def user_picture(request):
    if request.session.get('UserId') != None:
        if request.method == 'POST':
            user_picture = request.FILES['imageUpload']
            get_user = models.User.objects.get(user_id= request.session.get('UserId'))
            # Delete old picture
            del_old_picture = models.User_Images.objects.filter(fk_user = get_user)
            del_old_picture.delete()
            # Add new picture
            user_profile = models.User_Images()
            user_profile.user_img_name= user_picture
            user_profile.fk_user = get_user
            user_profile.save()
            messages.success(request, 'New Profile Uploaded')
            return redirect('/Dashboard')
        else:
            messages.error(request, 'Something went wrong...')
            return redirect('/Dashboard')
    else:
        return redirect('/')

# ============= login
def login(request):
    if request.session.get('UserId') != None :
        return redirect('/')
    elif request.session.get('AdminId') != None:
        return redirect('/admin/')
    else:
        return render(request, 'user/login.html')

def login_response(request):
     if(request.method == 'POST'):
          login_email = request.POST['login_email']
          login_password = hashlib.md5(request.POST['login_password'].encode("utf-8")).hexdigest()
          admin_check = models.Admin.objects.filter(admin_email= login_email).filter(admin_pass= login_password).count()
          user_check = models.User.objects.filter(user_email= login_email).filter( user_pass= login_password).count()
          if(admin_check == 1):
               admin_data = models.Admin.objects.get(admin_email= login_email, admin_pass= login_password)
               request.session['AdminId'] = admin_data.admin_id
               request.session['AdminName'] = admin_data.admin_name
               request.session['AdminEmail'] = admin_data.admin_email
               return redirect('/admin/')
          elif(user_check == 1):
              user_data = models.User.objects.get(user_email= login_email, user_pass= login_password)
              account = models.Account_status.objects.get(fk_user=user_data)
              account_status = account.account_status
              if(account_status == '1'):
                  request.session['UserId'] = user_data.user_id
                  request.session['UserName'] = user_data.user_name
                  request.session['UserEmail'] = user_data.user_email
                  return redirect('/')
              else:
                  messages.error(request,"Please check your e-mail to verify account")
                  return redirect('/login')
          else:
               messages.error(request, "Email OR Password Incorrect...")
               return redirect('/login')
     else:
          messages.error(request, "INVALID FIELDS...")
          return redirect('/login')

# =========== Profile Page
def edit_profile(request):
    if request.session.get('UserId') != None:
        logged_user_id= request.session.get('UserId')
        if logged_user_id:
            logged_user_data = models.User.objects.get(user_id= logged_user_id)
            country_data = models.Country.objects.all().order_by('country_name')
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'user_data': logged_user_data,
            'country_data': country_data, # all country list
        }
        return render(request, 'user/profile_edit.html', context)
    else:
        messages.error(request, 'First need to be login...')
        return render(request, 'user/login.html')

def edit_profile_response(request):
    if request.method == 'POST':
        userid = request.POST['user_id']
        username = request.POST['user_name']
        useremail = request.POST['user_email']
        userphone = request.POST['user_phone']
        userregisterfor = request.POST['user_register_for']
        useroldpassword = request.POST['user_password']
        usernewpassword = request.POST['user_new_password']
        usernewconfirmpassword = request.POST['user_new_confirm_password']

        if usernewpassword != "0" and usernewconfirmpassword != "0":

            if(usernewpassword == usernewconfirmpassword): # check new password and new confirm password
                encrypt_old_Password = hashlib.md5(useroldpassword.encode("utf-8")).hexdigest()
                encrypt_new_Password = hashlib.md5(usernewpassword.encode("utf-8")).hexdigest()
                getuser = models.User.objects.get(user_id=userid)
                user_old_password = getuser.user_pass

                if(encrypt_old_Password == user_old_password): # check old password

                    if (encrypt_old_Password != encrypt_new_Password):  # check old password and new password
                        upd_user = models.User(user_id=userid)
                        upd_user.user_name = username
                        upd_user.user_email = useremail
                        upd_user.user_pass = encrypt_new_Password
                        upd_user.user_phone = userphone
                        upd_user.user_mode = userregisterfor
                        upd_user.save()
                        messages.success(request, "Password Change Successfull")
                        return redirect('/EditProfile')
                    else:
                        messages.error(request, "Old password and new password are same...")
                        return redirect('/EditProfile')
                else:
                    messages.error(request, "Old password was Incorrect...")
                    return redirect('/EditProfile')
            else:
                messages.error(request, "Confirm password not matched...")
                return redirect('/EditProfile')

        elif usernewpassword == "0" and usernewconfirmpassword == "0":
            usercountry = request.POST['user_country']
            usercity = request.POST['user_city']
            # update user data
            upd_user = models.User(user_id= userid)
            upd_user.user_name = username
            upd_user.user_email = useremail
            upd_user.user_pass = useroldpassword
            upd_user.user_phone = userphone
            upd_user.user_mode = userregisterfor
            upd_user.save()
            request.session['UserName'] = username
            request.session['UserEmail'] = useremail

            fk_getuser = models.User.objects.get(user_email=useremail)
            fk_getcountry = models.Country.objects.get(country_name=usercountry)
            fk_getcity = models.City.objects.get(city_name=usercity)

            add_user_city = models.User_City.objects.get(fk_user= userid)
            add_user_city.fk_user = fk_getuser
            add_user_city.fk_country = fk_getcountry
            add_user_city.fk_city = fk_getcity
            add_user_city.save()

            messages.success(request, "Changes Successfull")
            return redirect('/EditProfile')
        else:
            messages.error(request, "Error")
            return redirect('/EditProfile')
    else:
        messages.error(request, "Invalid Request ...")
        return redirect('/EditProfile')

# ============= Add sell
def sell_add(request):
    if request.session.get('UserId') != None:
        category_data = models.Category.objects.all()
        city_data = models.City.objects.all().order_by('city_name')
        user_data = models.User.objects.get(user_id= request.session.get('UserId'))
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'category_data': category_data,
            'user_data': user_data,
            'city_data': city_data
        }
        return render(request, 'user/add_sell.html', context)
    else:
        return redirect('/')

def sell_add_response(request):
    if request.session.get('UserId') != None:
        if request.method == 'POST':
            itemtitle = request.POST['item_title']
            itemprice = request.POST['item_price']
            itemcondition = request.POST['item_condition']
            itemdescription = request.POST['item_description']
            itemcategory = request.POST['item_category']
            itemimages = request.FILES.getlist('item_images')
            contactcity = request.POST['item_city']
            contactaddress = request.POST['item_address']
            contactnumber = request.POST['item_contact_number']

            # get category
            get_category = models.Category.objects.get(category_name= itemcategory)
            # get user
            user_id = request.session.get('UserId')
            get_user = models.User.objects.get(user_id = user_id)
            #get_city
            get_city = models.City.objects.get(city_id= contactcity)
            #random code
            randdate = datetime.now().strftime("%m%d%M%S")
            code =str(random.randint(1, 9)) + randdate + str(random.randint(1, 9))
            # add item
            add_item = models.Item()
            add_item.item_title = itemtitle
            add_item.item_code = code
            add_item.item_desp = itemdescription
            add_item.item_price = itemprice
            add_item.item_condition = itemcondition
            add_item.item_location = contactaddress
            add_item.item_status = 'Active'
            add_item.item_user_contact = contactnumber
            add_item.fk_user = get_user
            add_item.fk_category = get_category
            add_item.fk_city = get_city
            add_item.save()

            # get item
            get_item = models.Item.objects.get(item_title= itemtitle, item_price= itemprice, item_user_contact= contactnumber)

            #add item image
            for item_image in itemimages:
                models.Item_Images.objects.create(item_img_name=item_image, fk_item=get_item)
            messages.success(request, 'POST ADDED SUCCESSFULLY...')
            return redirect('/Dashboard')
        else:
            messages.error(request, 'INVALID REQUEST...');
            return redirect('/AddSell')
    else:
        return redirect('/')

# ============= Sell List
def sell_list(request):
    if request.session.get('UserId') != None:
        category_data = models.Category.objects.all()
        item_data = models.Item.objects.filter(item_status='Active').order_by('-item_id')
        city_data = models.City.objects.filter().order_by('city_name')
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'category_data': category_data,
            'item_data': item_data,
            'city_data': city_data,
        }
        return render(request, 'user/list_sell.html', context)
    else:
        category_data = models.Category.objects.all()
        item_data = models.Item.objects.filter(item_status='Active').order_by('-item_id')
        context = {
            'category_data': category_data,
            'item_data': item_data
        }
        return render(request, 'user/list_sell.html', context)

# =========== Dashbard
def dashboard(request):
    if request.session.get('UserId') != None:
        logged_user_id= request.session.get('UserId')
        if logged_user_id:
            logged_user_data = models.User.objects.get(user_id= logged_user_id)
            item_data = models.Item.objects.filter(fk_user= logged_user_data).order_by('-item_id')
            active_item_count = models.Item.objects.filter(item_status='Active').count()
            inactive_item_count = models.Item.objects.filter(item_status='Inactive').count()
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'user_data': logged_user_data,
            'item_data': item_data,
            'active_item_count': active_item_count,
            'inactive_item_count': inactive_item_count,

        }
        return render(request, 'user/my_all_sell.html', context)
    else:
        messages.error(request, 'First need to be login...')
        return render(request, 'user/login.html')

#=========== User Active sell
def user_active_sell(request):
    if request.session.get('UserId') != None:
        logged_user_id= request.session.get('UserId')
        if logged_user_id:
            logged_user_data = models.User.objects.get(user_id= logged_user_id)
            item_data = models.Item.objects.filter(fk_user= logged_user_data, item_status='Active').order_by('-item_id')
            active_item_count = models.Item.objects.filter(item_status='Active').count()
            inactive_item_count = models.Item.objects.filter(item_status='Inactive').count()

        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'user_data': logged_user_data,
            'item_data': item_data,
            'active_item_count': active_item_count,
            'inactive_item_count': inactive_item_count,

        }
        return render(request, 'user/my_all_sell.html', context)
    else:
        messages.error(request, 'First need to be login...')
        return render(request, 'user/login.html')

#=========== User Inactive sell
def user_inactive_sell(request):
    if request.session.get('UserId') != None:
        logged_user_id= request.session.get('UserId')
        if logged_user_id:
            logged_user_data = models.User.objects.get(user_id= logged_user_id)
            item_data = models.Item.objects.filter(fk_user= logged_user_data, item_status='Inactive').order_by('-item_id')
            active_item_count = models.Item.objects.filter(item_status='Active').count()
            inactive_item_count = models.Item.objects.filter(item_status='Inactive').count()

        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'user_data': logged_user_data,
            'item_data': item_data,
            'active_item_count': active_item_count,
            'inactive_item_count': inactive_item_count,

        }
        return render(request, 'user/my_all_sell.html', context)
    else:
        messages.error(request, 'First need to be login...')
        return render(request, 'user/login.html')

#=========== Item Status Change =====
def item_change_status(request, item_id):
    if request.session.get('UserId') != None:
        get_item = models.Item.objects.get(item_id= item_id)
        get_status= get_item.item_status
        if get_status == 'Active':
            get_item.item_status= 'Inactive'
            get_item.save()
            messages.success(request, 'Ad Inactive Successfully')
            return redirect('/Dashboard')
        elif get_status == 'Inactive':
            get_item.item_status= 'Active'
            get_item.save()
            messages.success(request, 'Ad Active Successfully')
            return redirect('/Dashboard')
        else:
            messages.error(request, 'Error')
            return redirect('/Dashboard')
    else:
        messages.error(request, 'First need to be login...')
        return render(request, 'user/login.html')

#=========== User Edit sell
def user_edit_sell(request, item_code):
    if request.session.get('UserId') != None:
        category_data = models.Category.objects.all()
        city_data = models.City.objects.all().order_by('city_name')
        item_data = models.Item.objects.get(item_code= item_code)
        user_data = models.User.objects.filter(user_id=request.session.get('UserId'))
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'category_data': category_data,
            'user_data': user_data,
            'city_data': city_data,
            'item_data': item_data
        }
        return render(request, 'user/edit_sell.html', context)
    else:
        return redirect('/')

#=========== User Edit Sell Response
def user_edit_sell_response(request):
    if request.session.get('UserId') != None:
        if request.method == 'POST':
            item_id = request.POST['item_id']
            item_code = request.POST['item_code']
            item_status = request.POST['item_status']
            itemtitle = request.POST['item_title']
            itemprice = request.POST['item_price']
            itemcondition = request.POST['item_condition']
            itemdescription = request.POST['item_description']
            itemcategory = request.POST['item_category']
            itemimages = request.FILES.getlist('item_images')
            contactcity = request.POST['item_city']
            contactaddress = request.POST['item_address']
            contactnumber = request.POST['item_contact_number']

            if not itemimages:
                get_category = models.Category.objects.get(category_name=itemcategory)
                # get user
                user_id = request.session.get('UserId')
                get_user = models.User.objects.get(user_id=user_id)
                # get_city
                get_city = models.City.objects.get(city_id=contactcity)
                # add item
                add_item = models.Item(item_id= item_id)
                add_item.item_code = item_code
                add_item.item_title = itemtitle
                add_item.item_desp = itemdescription
                add_item.item_price = itemprice
                add_item.item_condition = itemcondition
                add_item.item_location = contactaddress
                add_item.item_status = item_status
                add_item.item_user_contact = contactnumber
                add_item.fk_user = get_user
                add_item.fk_category = get_category
                add_item.fk_city = get_city
                add_item.save()

                messages.success(request, 'Changes Successfully...')
                return redirect('/AdEdit/'+item_code)

            else:
                # get category
                get_category = models.Category.objects.get(category_name= itemcategory)
                # get user
                user_id = request.session.get('UserId')
                get_user = models.User.objects.get(user_id = user_id)
                #get_city
                get_city = models.City.objects.get(city_id= contactcity)
                # add item
                add_item = models.Item(item_id= item_id)
                add_item.item_code = item_code
                add_item.item_title = itemtitle
                add_item.item_desp = itemdescription
                add_item.item_price = itemprice
                add_item.item_condition = itemcondition
                add_item.item_location = contactaddress
                add_item.item_status = item_status
                add_item.item_user_contact = contactnumber
                add_item.fk_user = get_user
                add_item.fk_category = get_category
                add_item.fk_city = get_city
                add_item.save()

                # get item
                get_item = models.Item.objects.get(item_code= item_code)

                #add item image
                for item_image in itemimages:
                    models.Item_Images.objects.create(item_img_name=item_image, fk_item=get_item)
                messages.success(request, 'Changes Successfully...')
                return redirect('/AdEdit/'+item_code)
        else:
            messages.error(request, 'INVALID REQUEST...')
            return redirect('/ListSell')
    else:
        return redirect('/')

# ============= Delete Items images(in item edit)
def delete_item_images(request, item_image_id, item_id):
    if request.session.get('UserId') != None:
        image = models.Item_Images.objects.get(item_img_id= item_image_id)
        image.delete()
        #get item code
        item_data = models.Item.objects.get(item_id= item_id)
        item_code = item_data.item_code
        messages.success(request, 'Image Remove Successfully')
        return redirect('/AdEdit/'+str(item_code))
    else:
        return redirect('/')

# ============= Delete Item
def delete_item(request, item_code):
    if request.session.get('UserId') != None:
        #get item from code
        item = models.Item.objects.get(item_code = item_code)
        item_id = item.item_id
        # delete images
        item_image = models.Item_Images.objects.filter(fk_item= item)
        item_image.delete()
        # delete item
        item = models.Item.objects.get(item_id= item_id)
        item.delete()
        messages.success(request, 'Ad Delete Successfully')
        return redirect('/Dashboard')
    else:
        return redirect('/')

#============== Single Item
def single_item(request, item_code):
    if request.session.get('AdminName') != None:
        city_data = models.City.objects.filter().order_by('city_name')  # location dropdown search
        item_data = models.Item.objects.get(item_code=item_code)
        context = {
            'AdminName': request.session.get('AdminName'),
            'item_data': item_data,
            'city_data': city_data,
        }
        return render(request, 'user/single_sell.html', context)
    elif request.session.get('UserId') != None:
        city_data = models.City.objects.filter().order_by('city_name')  # location dropdown search
        item_data = models.Item.objects.get(item_code= item_code)
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'item_data': item_data,
            'city_data': city_data,
        }
        return render(request,'user/single_sell.html', context)
    else:
        city_data = models.City.objects.filter().order_by('city_name')  # location dropdown search
        item_data = models.Item.objects.get(item_code=item_code)
        context = {
            'item_data': item_data,
            'city_data': city_data,
        }
        return render(request, 'user/single_sell.html', context)

# ============= Item Reviews
def comment_item(request):
    if request.session.get('UserId') != None:
        if request.method == 'POST':
            user_review = request.POST['review']
            item_code = request.POST['item_code']
            # get user
            get_user = models.User.objects.get(user_id= request.session.get('UserId'))
            # get item
            get_item = models.Item.objects.get(item_code= item_code)
            # add review
            review = models.Comment()
            review.comment_body = user_review
            review.fk_user = get_user
            review.fk_item = get_item
            review.save()
            return redirect('/Ad/'+str(item_code))
    else:
        return redirect('/')

# =========== Comment Delete (ONLY BY ADMIN)
def comment_del(request):
    if request.session.get('AdminId') != None:
        if request.method == 'POST':
            comment_id = request.POST['comment_id']
            item_code = request.POST['item_code']
            # delete review
            review = models.Comment.objects.filter(comment_id= comment_id)
            review.delete()
            return redirect('/Ad/'+str(item_code))
    else:
        return redirect('/')

# ============ Item Search
def item_search(request):
    if request.method == 'GET':
        search_item = request.GET['search_item']
        search_category = request.GET['search_category']
        search_city = request.GET['search_city']
        # get category
        if search_category != 'Category':
            get_category= models.Category.objects.get(category_id= search_category)
        else:
            get_category = 0
        # get city
        if search_city != 'Location':
            get_city = models.City.objects.get(city_id=search_city)
        else:
            get_city = 0
        if request.session.get('UserId') != None:
            item_data = models.Item.objects.filter(item_status= 'Active').filter(Q(item_title__icontains= search_item) | Q(fk_category= get_category)| Q(fk_city= get_city)).order_by('-item_id')
            search_count = item_data.count()
            search_date= date.today()
            category_data = models.Category.objects.filter().order_by('category_name') # category dropdown search
            city_data = models.City.objects.filter().order_by('city_name')  # location dropdown search
            context = {
                'UserName': request.session.get('UserName'),
                'UserEmail': request.session.get('UserEmail'),
                'category_data': category_data,
                'city_data': city_data,
                'item_data': item_data,
                'search_item': search_item,
                'search_date': search_date,
                'search_count': search_count
            }
            return render(request, 'user/list_sell.html', context)
        else:
            item_data = models.Item.objects.filter(item_status='Active').filter(Q(item_title__icontains=search_item) | Q(fk_category=get_category) | Q(fk_city=get_city)).order_by('-item_id')
            search_count = item_data.count()
            search_date = date.today()
            category_data = models.Category.objects.filter().order_by('category_name')  # category dropdown search
            city_data = models.City.objects.filter().order_by('city_name')  # location dropdown search
            context = {
                'UserName': request.session.get('UserName'),
                'UserEmail': request.session.get('UserEmail'),
                'category_data': category_data,
                'city_data': city_data,
                'item_data': item_data,
                'search_item': search_item,
                'search_date': search_date,
                'search_count': search_count
            }
            return render(request, 'user/list_sell.html', context)

# ============ About us
def aboutus(request):
    if request.session.get('UserId') != None:
        admin_data = models.Admin.objects.only('admin_name').filter()
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
            'admin_data': admin_data
        }
        return render(request, 'user/about-us.html', context)
    else:
        admin_data = models.Admin.objects.only('admin_name').filter()
        return render(request, 'user/about-us.html', {'admin_data': admin_data})

# ============ Contact us
def contactus(request):
    if request.session.get('UserId') != None:
        context = {
            'UserName': request.session.get('UserName'),
            'UserEmail': request.session.get('UserEmail'),
        }
        return render(request, 'user/contact-us.html', context)
    else:
        return render(request, 'user/contact-us.html')

def contactus_resp(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        user_email = request.POST['useremail']
        user_message = request.POST['message']
        contact = models.Contact()
        contact.contact_uname= user_name
        contact.contact_uemail= user_email
        contact.contact_umessage= user_message
        contact.save()
        messages.success(request, 'Your Request has been submitted...')
        return redirect('/Contact-us')
    else:
        messages.error(request, 'Something went wrong...')
        return redirect('/Contact-us')

# ============= user account delete
def user_account_deactive(request):
    if request.session.get('UserId') != None:
        if request.method == 'POST':
            user_email = request.POST['user_email']
            # get user
            user_data = models.User.objects.get(user_email= user_email)
            # delete user profile photo
            user_photo = models.User_Images.objects.filter(fk_user=user_data)
            user_photo.delete()
            # delete user city data
            user_city = models.User_City.objects.filter(fk_user=user_data)
            user_city.delete()
            # delete user account status
            user_account = models.Account_status.objects.filter(fk_user=user_data)
            user_account.delete()
            # delete user items comment
            user_comment = models.Comment.objects.filter(fk_user=user_data)
            user_comment.delete()
            # get user item data
            user_item = models.Item.objects.filter(fk_user=user_data)
            # delete single item and their images
            for user_item in user_item:
                print(user_item.item_id)
                # delete item images
                item_images = models.Item_Images.objects.filter(fk_item= user_item.item_id)
                item_images.delete()
                # delete item
                item_data = models.Item.objects.filter(item_id= user_item.item_id)
                item_data.delete()
            # now delete user
            user_data.delete()
            request.session.clear()
            messages.success(request, 'Account deleted successfully...')
            return redirect('/login')
        else:
            messages.error(request, 'Invalid request...')
            return redirect('/Dashboard')
    else:
        messages.error(request, 'Error...')
        return redirect('/Dashboard')

# ============= logout
def logout(request):
    request.session.clear()
    return redirect('/login')
