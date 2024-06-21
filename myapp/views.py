from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Adjust the import based on your user model
from .db import *



# Create your views here.
# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    confirmation_message = None

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Save the user
            form.save()
            add_user(username, password)
            # Set the confirmation message
            confirmation_message = f"Signup successful! Username: {username}"

            # Redirect to the login page or any other page as needed
            return redirect('login')
        else:
            # Display an alert for invalid username or password
            messages.error(request, 'Invalid username or password. Please try again.')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form, 'confirmation_message': confirmation_message})



def user_profile(request, username):
    # Assuming your user model has a field 'username' and 'email'
    user_info = User.objects.get(username=username)

    context = {
        'user_info': user_info,
    }

    return render(request, 'profile.html', context)

def profile(request, user_name):
    if request.method == 'POST':
        # If the form is submitted, get the username from the form
        user_name = request.POST.get('username')

        # You can save the username to the database or perform any other actions here

    return render(request, 'profile.html', {'user_name': user_name})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Assuming you have a function to check the user's credentials
            if check_user_name_pwd(username, password):
                # Set a session variable to indicate that the user is logged in
                #return render(request, 'index.html') 
                if isadmin(username):
                    return render(request, 'profile_admin.html', {'user_name': username})
                elif ishr(username):
                    return render(request, 'profile_hr.html', {'user_name': username})
                else:    
                    return render(request, 'profile.html', {'user_name': username})
            else:
                messages.error(request, 'Invalid username or password. Please try again.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def profile_data(request, user_name):
    # Your view logic for the profile_data page
    if request.method == 'POST':
        # Retrieve form data from the POST request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        gender = request.POST.get('gender')
        education = request.POST.get('education')
        job =  request.POST.get('job')
        income =  request.POST.get('income')
        nationality = request.POST.get('nationality')
        residence = request.POST.get('residence')
        religion = request.POST.get('religion')
        fashion_style = request.POST.get('fashion_style')
        hijab_type = request.POST.get('hijab_type')
        marriages_count = request.POST.get('marriages_count')
        divorces_count = request.POST.get('divorces_count')
        no_siblings = request.POST.get('no_siblings')
        order_siblings = request.POST.get('order_siblings')
        social_class = request.POST.get('social_class')
        bank_balance = request.POST.get('bank_balance')
        car_type_model = request.POST.get('car_type') + request.POST.get('car_model')

        user_values = {
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': birth_date,
            'gender': gender,
            'education': education,
            'job': job,
            'income': int(income),
            'nationality': nationality,
            'residence': residence,
            'religion': int(religion),
            'fashion_style': fashion_style,
            'hijab_type': hijab_type,
            'marriages_count':int(marriages_count),
            'divorces_count':int(divorces_count)
        }
        add_social_class(user_name, social_class, bank_balance, car_type_model)
        add_family_status(user_name, no_siblings, order_siblings)
        add_fashion_hijab(user_name, fashion_style, hijab_type)
        add_user_profile(user_name, user_values)
    return render(request, 'profile_data.html', {'user_name': user_name})

def hobbies(request, user_name):
    if request.method == 'POST':
        # Retrieve form data from the POST request
        hobbies = request.POST.getlist('hobbies')
        print(hobbies)

        if len(hobbies) > 0:
            add_hobby(user_name, hobbies)
    return render(request, 'hobbies.html', {'user_name': user_name})

def home_skills(request, user_name):
    if request.method == 'POST':
        # Retrieve form data from the POST request
        home_skills = request.POST.getlist('home_skills')
        print(home_skills)

        if len(home_skills) > 0:
            add_home_skills(user_name, home_skills)
    return render(request, 'home_skills.html', {'user_name': user_name})

def character(request, user_name):
    if request.method == 'POST':
        skin_color = request.POST.get('SKIN_COLOR')
        height = int(request.POST.get('HEIGHT'))
        weight = int(request.POST.get('WEIGHT'))
        eye_color = request.POST.get('EYE_COLOR')
        hair_color = request.POST.get('HAIR_COLOR')
        hair_length = request.POST.get('HAIR_LENGTH')
        hair_type = request.POST.get('HAIR_TYPE')
        mustache = request.POST.get('Mustache')
        beard = request.POST.get('Beard')
        eye_glasses = request.POST.get('Eye_Glasses')

        user_character_list = {
            'skin_color' :skin_color,
            'height': height,
            'weight': weight,
            'eye_color': eye_color,
            'hair_color': hair_color,
            'hair_length':hair_length,
            'hair_type': hair_type,
            'mustache': mustache,
            'beard': beard,
            'eye_glasses':eye_glasses
        }
        print(user_character_list)
        add_character(user_name, user_character_list)
    return render(request, 'character.html', {'user_name': user_name})

def find_partner(request, user_name):
    if request.method == 'POST':
        print("hello")
        skin_color = request.POST.get('SKIN_COLOR')
        height = int(request.POST.get('HEIGHT'))
        weight = int(request.POST.get('WEIGHT'))
        eye_color = request.POST.get('EYE_COLOR')
        hair_color = request.POST.get('HAIR_COLOR')
        hair_length = request.POST.get('HAIR_LENGTH')
        hair_type = request.POST.get('HAIR_TYPE')
        mustache = request.POST.get('Mustache')
        beard = request.POST.get('Beard')
        eye_glasses = request.POST.get('Eye_Glasses')
        hijab_type  = request.POST.get('hijab_type')
        fashion_style  = request.POST.get('fashion_style')
        min_income  = int(request.POST.get('min_income'))
        gender  = request.POST.get('gender')
        religion  = request.POST.get('religion')

        partner_character_list = {
            'skin_color' :skin_color,
            'height': height,
            'weight': weight,
            'eye_color': eye_color,
            'hair_color': hair_color,
            'hair_length':hair_length,
            'hair_type': hair_type,
            'mustache': mustache,
            'beard': beard,
            'eye_glasses':eye_glasses,
            'hijab_type': hijab_type,
            'fashion_style':fashion_style,
            'min_income':min_income,
            'gender': gender,
            'religion':religion

        }
        partner_list = get_partner(user_name, partner_character_list)
        return render(request, 'find_partner.html', {'user_name': user_name, 'partner_list': partner_list})
    return render(request, 'find_partner.html', {'user_name': user_name})

def add_user_admin(request, user_name):
    if request.method == 'POST':
        new_user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        role = request.POST.get('role')
        add_user_admin_db(new_user_name, pwd, role)
    return render(request, 'add_user_admin.html', {'user_name': user_name})

def profile_admin(request, user_name):
    return render(request, 'profile_admin.html', {'user_name': user_name})

def profile_hr(request, user_name):
    return render(request, 'profile_hr.html', {'user_name': user_name})

def delete_user(request, user_name):
    if request.method == 'POST':
        new_user_name = request.POST.get('user_name')
        delete_user_db(new_user_name)
    return render(request, 'delete_user.html', {'user_name': user_name})

def edit_user_data(request, user_name):
    if request.method == 'POST':
        # Retrieve form data from the POST request
        input_user_name = request.POST.get('input_user_name')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        education = request.POST.get('education')
        job =  request.POST.get('job')
        income =  int(request.POST.get('income'))
        nationality = request.POST.get('nationality')
        residence = request.POST.get('residence')
        role = request.POST.get('role')

        user_values = {
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': birth_date,
            'education': education,
            'job': job,
            'income': int(income),
            'nationality': nationality,
            'residence': residence,
            'role':role
        }
        edit_user_profile_db(input_user_name, user_values)
    return render(request, 'edit_user_data.html', {'user_name': user_name})

def view_profilies_hr(request, user_name):
    # Call the function to retrieve profiles from the database
    profiles = query_profiles_from_hr_db()

    # Pass the profiles and user_name to the template
    return render(request, 'view_profilies_hr.html', {'profiles': profiles, 'user_name': user_name})


def view_profilies_admin(request, user_name):
    # Call the function to retrieve profiles from the database
    profiles = query_profiles_from_admin_db()

    # Pass the profiles and user_name to the template
    return render(request, 'view_profiles_admin.html', {'profiles': profiles, 'user_name': user_name})


def profile_data_hr(request, user_name):
    return render(request, 'profile_data_hr.html', {'user_name': user_name})

def profile_data_admin(request, user_name):
    return render(request, 'profile_data_admin.html', {'user_name': user_name})

def hobbies_admin(request, user_name):
    return render(request, 'hobbies_admin.html', {'user_name': user_name})

def hobbies_hr(request, user_name):
    return render(request, 'hobbies_hr.html', {'user_name': user_name})

def home_skills_admin(request, user_name):
    return render(request, 'home_skills_admin.html', {'user_name': user_name})

def home_skills_hr(request, user_name):
    return render(request, 'home_skills_hr.html', {'user_name': user_name})

def character_admin(request, user_name):
    return render(request, 'character_admin.html', {'user_name': user_name})

def character_hr(request, user_name):
    return render(request, 'character_hr.html', {'user_name': user_name})

def find_partner_admin(request, user_name):
    return render(request, 'find_partner_admin.html', {'user_name': user_name})

def find_partner_hr(request, user_name):
    return render(request, 'find_partner_hr.html', {'user_name': user_name})



# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

