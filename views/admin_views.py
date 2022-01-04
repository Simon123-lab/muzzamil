import hashlib
from django.contrib import messages
from django.shortcuts import redirect, render
from admin_app.models import *
from django.db.models import Q

# Create your views here.


# ============= admin index
def admin_index(request):
     if request.session.get('AdminId') != None:
          context = {
               'AdminName': request.session.get('AdminName')
          }
          return render(request, 'admin/index.html', context)
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= admin register
def admin_register(request):
     if request.session.get('AdminId') != None:
          admin_data = Admin.objects.all().order_by('-admin_id')
          context = {
               'AdminName': request.session.get('AdminName'),
               'admin_data': admin_data
          }
          return render(request, 'admin/register.html', context)
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

def admin_register_response(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               admin_email = request.POST['admin_email']
               check_email = Admin.objects.filter(admin_email=admin_email).count()
               if check_email == 0:
                    admin_register = Admin()
                    admin_register.admin_name = request.POST['admin_name']
                    admin_register.admin_email = request.POST['admin_email']
                    admin_register.admin_pass = hashlib.md5(request.POST['admin_password'].encode("utf-8")).hexdigest()
                    admin_register.admin_phone = request.POST['admin_phone']
                    admin_register.save()
                    messages.success(request, "ADMIN REGISTER SUCCESSFULLY...")
                    return redirect('/admin/register')
               else:
                    messages.error(request, "Email Already registered")
                    return redirect('/admin/register')
          else:
               messages.error(request, "INVALID FIELDS...")
               return redirect('/admin/register')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= admin delete
def admin_delete(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               admin_id = str(request.POST['admin_id'])
               logged_admin_id = str(request.session.get('AdminId'))
               if logged_admin_id == admin_id:
                    messages.warning(request, 'ADMIN LOGGED...')
                    return redirect('/admin/register')
               else:
                    admin_del = Admin(admin_id=admin_id)
                    admin_del.delete()
                    messages.info(request, 'ADMIN DELETED...')
                    return redirect('/admin/register')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= admin update
def admin_update(request):
     if request.session.get('AdminId') != None:
          admin_id = request.POST['admin_id']
          update_data = Admin.objects.get(admin_id=admin_id)
          admin_data = Admin.objects.all().order_by('-admin_id')
          context = {
               'AdminName': request.session.get('AdminName'),
               'admin_data': admin_data,
               'update_data': update_data,
          }
          return render(request, 'admin/update.html', context)
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

def admin_update_response(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               admin_id = request.POST['admin_id']
               admin_register = Admin(admin_id= admin_id)
               admin_register.admin_name = request.POST['admin_name']
               admin_register.admin_email = request.POST['admin_email']
               admin_register.admin_pass = hashlib.md5(request.POST['admin_password'].encode("utf-8")).hexdigest()
               admin_register.admin_phone = request.POST['admin_phone']
               admin_register.save()
               request.session['AdminName'] = request.POST['admin_name']
               messages.info(request, "ADMIN UPDATED SUCCESSFULLY...")
               return redirect('/admin/register')
          else:
               messages.warning(request, "INVALID FIELDS...")
               return redirect('/admin/register')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= region
def admin_region(request):
     if request.session.get('AdminId') != None:
          country_data = Country.objects.all().order_by('country_name')
          context = {
               'AdminName': request.session.get('AdminName'),
               'country_data': country_data
          }
          return render(request, 'admin/region.html', context)
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= Add Country
def country_add(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               country_name = request.POST['country_name']
               check_country = Country.objects.filter(country_name=country_name).count()
               if check_country == 0:
                    country = Country()
                    country.country_name = country_name
                    country.save()
                    messages.success(request, "COUNTRY ADD SUCCESSFULLY...")
                    return redirect('/admin/region')
               else:
                    messages.error(request, "Country Already Add..")
                    return redirect('/admin/region')
          else:
               messages.error(request, "INVALID FIELDS...")
               return redirect('/admin/region')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= Add City
def city_add(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               city_name = request.POST['city_name']
               fk_city_name = request.POST['country_city_name']
               get_country = Country.objects.get(country_name=fk_city_name)
               check_city = City.objects.filter(city_name=city_name).filter(fk_country=get_country).count()
               print(check_city)
               if check_city == 0:
                    city = City()
                    city.city_name = city_name
                    city.fk_country = get_country
                    city.save()
                    messages.info(request, "CITY ADD SUCCESSFULLY...")
                    return redirect('/admin/region')
               else:
                    messages.warning(request, "CITY Already Add..")
                    return redirect('/admin/region')
          else:
               messages.warning(request, "INVALID FIELDS...")
               return redirect('/admin/region')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

def city_delete(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               city_id = request.POST['city_id']
               city = City(city_id= city_id)
               city.delete()
               return redirect('/admin/region')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

def country_delete(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               country_id = request.POST['country_id']
               fk_city = City.objects.filter(fk_country=country_id)
               fk_city.delete()
               country = Country(country_id= country_id)
               country.delete()
               return redirect('/admin/region')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= Category
def category_add(request):
     if request.session.get('AdminId') != None:
          category_data = Category.objects.all()
          context = {
               'AdminName': request.session.get('AdminName'),
               'category_data': category_data
          }
          return render(request, 'admin/category.html', context)
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

def category_add_response(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               category = request.POST['category']
               check_category = Category.objects.filter(category_name=category).count()
               if check_category == 0:
                    add_category = Category()
                    add_category.category_name = category
                    add_category.save()
                    messages.success(request, "CATEGORY ADDED SUCCESSFULLY...")
                    return redirect('/admin/category')
               else:
                    messages.error(request, "CATEGORY ALREADY EXIST...")
                    return redirect('/admin/category')
          else:
               messages.error(request, "INVALID FIELDS...")
               return redirect('/admin/category')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

def category_del(request):
     if request.session.get('AdminId') != None:
          if request.method == 'POST':
               category_id = request.POST['category_id']
               get_category = Category(category_id = category_id)
               get_category.delete()
               messages.info(request, "CATEGORY REMOVE SUCCESSFULLY...")
               return redirect('/admin/category')
          else:
               messages.warning(request, "INVALID REQUEST...")
               return redirect('/admin/category')
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# ============= User List
def user_list(request):
     if request.session.get('AdminId') != None:
          user_data = User.objects.all().order_by('-user_id')
          city_data = City.objects.all().order_by('city_name')
          context = {
               'AdminName': request.session.get('AdminName'),
               'user_data': user_data,
               'city_data': city_data,
          }
          return render(request, 'admin/user_list.html', context)
     else:
          messages.error(request, "First needs to be login...")
          return redirect('/login')

# =========== Edit User
def user_edit(request):
    if request.session.get('AdminId') != None:
        if request.method == 'POST':
            user_id = request.POST['user_id']
            user_data = User.objects.get(user_id= user_id)
            country_data = Country.objects.all().order_by('-country_id')
            context = {
                'AdminName': request.session.get('AdminName'),
                'country_data': country_data,
                'user_data': user_data
            }
            return render(request, 'admin/user_edit.html', context)
        else:
            context = {
                'AdminName': request.session.get('AdminName'),
            }
            messages.warning(request, "INVALID REQUEST...")
            return render(request, 'admin/user_edit.html', context)
    else:
        messages.error(request, "First needs to be login...")
        return redirect('/login')

def user_edit_response(request):
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
                encrypt_new_Password = hashlib.md5(usernewpassword.encode("utf-8")).hexdigest()
                getuser = User.objects.get(user_id=userid)
                user_old_password = getuser.user_pass

                if(useroldpassword == user_old_password): # check old password

                    if (useroldpassword != encrypt_new_Password):  # check old password and new password
                        upd_user = User(user_id=userid)
                        upd_user.user_name = username
                        upd_user.user_email = useremail
                        upd_user.user_pass = encrypt_new_Password
                        upd_user.user_phone = userphone
                        upd_user.user_mode = userregisterfor
                        upd_user.save()
                        messages.info(request, "Password Change Successfull")
                        return redirect('/admin/user')
                    else:
                        messages.warning(request, "Old password and new password are same...")
                        return redirect('/admin/user')
                else:
                    messages.warning(request, "Old password was Incorrect...")
                    return redirect('/admin/user')
            else:
                messages.warning(request, "Confirm password not matched...")
                return redirect('/admin/user')

        elif usernewpassword == "0" and usernewconfirmpassword == "0":
            usercountry = request.POST['user_country']
            usercity = request.POST['user_city']
            # update user data
            upd_user = User(user_id= userid)
            upd_user.user_name = username
            upd_user.user_email = useremail
            upd_user.user_pass = useroldpassword
            upd_user.user_phone = userphone
            upd_user.user_mode = userregisterfor
            upd_user.save()

            fk_getuser = User.objects.get(user_email=useremail)
            fk_getcountry = Country.objects.get(country_name=usercountry)
            fk_getcity = City.objects.get(city_name=usercity)

            add_user_city = User_City.objects.get(fk_user= userid)
            add_user_city.fk_user = fk_getuser
            add_user_city.fk_country = fk_getcountry
            add_user_city.fk_city = fk_getcity
            add_user_city.save()

            messages.info(request, "Changes Successfull")
            return redirect('/admin/user')
        else:
            messages.warning(request, "Error")
            return redirect('/admin/user')
    else:
        messages.warning(request, "Invalid Request ...")
        return redirect('/admin/user')

#============ Ads List
def ad_list(request):
    if request.session.get('AdminId') != None:
        item_data = Item.objects.all().order_by('-item_id')
        context = {
            'AdminName': request.session.get('AdminName'),
            'item_data': item_data
        }
        return render(request, 'admin/ads_list.html', context)
    else:
        messages.error(request, "First needs to be login...")
        return redirect('/login')

#============ Ads Delete
def ad_delete(request):
    if request.session.get('AdminId') != None:
        if request.method == 'POST':
            item_id = request.POST['item_id']
            item_data = Item.objects.get(item_id= item_id)
            item_data.delete()
            context = {
                'AdminName': request.session.get('AdminName'),
            }
            messages.info(request, 'Data deleted...')
            return redirect('/admin/Ad', context)
        else:
            context = {
                'AdminName': request.session.get('AdminName'),
            }
            messages.warning(request, 'Invalid Request...')
            return redirect('/admin/Ad', context)
    else:
        messages.error(request, "First needs to be login...")
        return redirect('/login')

# ============ Contact list
def contact_list(request):
    if request.session.get('AdminId') != None:
        contact_data = Contact.objects.all().order_by('-contact_id')
        context = {
            'AdminName': request.session.get('AdminName'),
            'contact_data': contact_data
        }
        return render(request, 'admin/contact_list.html', context)
    else:
        messages.error(request, "First needs to be login...")
        return redirect('/login')

# ============= Contact delete
def contact_delete(request):
    if request.session.get('AdminId') != None:
        if request.method == 'POST':
            contact_id = request.POST['contact_id']
            contact_data = Contact.objects.filter(contact_id= contact_id)
            contact_data.delete()
            messages.info(request, 'Data Deleted...')
            return redirect('/admin/Contact_list')
        else:
            messages.warning(request, 'Invalid request...')
            return redirect('/admin/Contact_list')
    else:
        messages.error(request, "First needs to be login...")
        return redirect('/login')

# =========== ADMIN PANEL SEARCH

# ------- Admin search
def admin_search(request):
     if request.session.get('AdminId') != None:
         if request.method == 'GET':
             admin_email = request.GET['email']
             admin_data = Admin.objects.filter(admin_email=admin_email)
             context = {
               'AdminName': request.session.get('AdminName'),
               'admin_data': admin_data
             }
             return render(request, 'admin/register.html', context)
         else:
             messages.warning(request, 'Error')
             return redirect('/admin/register')
     else:
          return redirect('/login')

# -------- User Search
def user_search(request):
    if request.session.get('AdminId') != None:
        if request.method =='GET':
            user_email = request.GET['email']
            user_data = User.objects.filter(user_email=user_email)
            city_data = City.objects.all().order_by('city_name')
            context = {
                'AdminName': request.session.get('AdminName'),
                'user_data': user_data,
                'city_data': city_data,
            }
            return render(request, 'admin/user_list.html', context)
        else:
            messages.warning(request, 'Error')
            return render('/admin/user')
    else:
        return redirect('/login')

# -------- Country Search -----
def country_search(request):
    if request.session.get('AdminId') != None:
        if request.method == 'GET':
            country = request.GET['country']
            country_data = Country.objects.filter(country_name= country)
            context = {
                'AdminName': request.session.get('AdminName'),
                'country_data': country_data
            }
            return render(request, 'admin/region.html', context)
        else:
            return redirect('/admin/region')
    else:
        messages.error(request, "First needs to be login...")
        return redirect('/login')

# -------- Ad Search -----
def ad_search(request):
    if request.session.get('AdminId') != None:
        if request.method == 'GET':
            code = request.GET['code']
            item_data = Item.objects.filter(item_code = code)
            context = {
                'AdminName': request.session.get('AdminName'),
                'item_data': item_data
            }
            return render(request, 'admin/ads_list.html', context)
        else:
            messages.warning(request, 'Error')
            return redirect('/admin/Ad')
    else:
        messages.error(request, "First needs to be login...")
        return redirect('/login')
