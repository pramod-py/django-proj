from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import Users
from django.db.models import Q
from pathlib import Path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def manageuser(request):
    if 'query' in request.GET:
        query = request.GET['query']
        search_user = Q(Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(email__icontains=query)|Q(phone_number__icontains=query))
        user_obj = Users.objects.filter(search_user)
        if not user_obj.count():
            messages.error(request, f'No records found for the {query} query.')
        else:
            if query != '':
                messages.success(request, f'{user_obj.count()} Record Found For:{query}')
    else:
        user_obj = Users.objects.all()
    context = {'user_obj': user_obj}
    return render(request, 'users/manageuser.html', context)


def manageuser_pagination(request):
    query = request.GET.get('query')
    if query:
        search_user = Q(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(phone_number__icontains=query))
        user_obj = Users.objects.filter(search_user)
        if not user_obj.exists():
            messages.error(request, f'No records found for the "{query}" query.')
        else:
            messages.success(request, f'{user_obj.count()} Record(s) Found For: "{query}"')
    else:
        user_obj = Users.objects.all()

    # Configure pagination
    paginator = Paginator(user_obj, 2)  # Show 5 users per page
    page = request.GET.get('page')

    try:
        user_obj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        user_obj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        user_obj = paginator.page(paginator.num_pages)

    context = {'user_obj': user_obj, 'query': query}
    return render(request, 'users/manageuser.html', context)



def adduser(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if Users.objects.filter(email=email).exists():
            messages.error(request, f'Email already used. Please use a different email address.')
            return redirect('/users/manageuser')
        elif Users.objects.filter(phone_number=phone_number).exists():
            messages.error(request, f'Phone Number already used. Please use a different Phone Number.')
            return redirect('/users/manageuser')
        else:
            user_obj = Users(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, address=address)
            user_obj.save()
            messages.success(request, f'{first_name}\'s record added successfully!')
            return redirect('/users/manageuser')


def edituser(request):
    user_obj = Users.objects.all()
    context = {'user_obj': user_obj}
    return redirect(request, '/users/manageuser', context)


def updateuser(request, id):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
       
        # Find the user object to update
        user_obj = Users.objects.get(id=id)

        # qr_code_url = request.POST.get('qr_code')  # Get the image URL
 
        user_obj = Users.objects.get(id=id)
        
        # Update the user data
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.email = email
        user_obj.address = address
        user_obj.phone_number = phone_number
        # file_path = 'C:\\Users\\admin\\Downloads\\lmsys\\' + qr_code_url
        # file_path = Path(file_path)
        #
        # if file_path.exists():
        #     file_path.unlink()

        user_obj.save()
        messages.success(request, 'User record Updated successfully!')
        return redirect('/users/manageuser')


def deleteuser(request, id):
    if request.method == 'POST':
        user_obj = Users.objects.filter(id=id)
        user_obj.delete()
        messages.success(request, 'User record deleted successfully!')
        context = {'USER_OBJ': user_obj}
        return redirect('/users/manageuser')


def viewuser(request):
    user_obj = Users.objects.all()
    context = {'user_obj': user_obj}
    return redirect(request, '/users/manageuser', context)


# viewuserqrcode
def viewuserqrcode(request):
    user_obj = Users.objects.all()
    context = {'user_obj': user_obj}
    return redirect(request, '/users/manageuser', context)


def searchuser(request):
    user_obj = Users.objects.all()

    search_contains = request.GET.get('search_contains')
    
    if search_contains != '' and search_contains is not None:
        user_obj = user_obj.filter(first_name__icontains=search_contains) 

    context = {'user_obj': user_obj}
    return redirect(request, '/users/manageuser', context)
