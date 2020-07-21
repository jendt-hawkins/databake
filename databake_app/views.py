from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def form(request):
    return render(request, 'login.html')

def homepage(request): 
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_recipes": Recipe.objects.all(),
        "all_categories" : Category.objects.all(),
    }
    return render(request, 'homepage.html', context)

def registered(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)

        request.session['user_id'] = user.id

        return redirect("/homepage")

def logout(request):
    request.session.flush()
    return redirect('/')

def login(request):

    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)

    if len(user) == 0:
        messages.error(request,"User not recognized")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode()) ):
            request.session['user_id'] = user[0].id
            return redirect('/homepage')
        else:
            messages.error(request,'Invalid password.')
            return redirect('/')

def profile(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "all_recipes": Recipe.objects.all(),
    }
    return render(request, 'profile.html', context)

def my_recipes(request):
    return render(request, 'my_recipes.html')

def categories(request):
    return redirect('/homepage')

def recipe_info(request, recipe_id):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "recipe": Recipe.objects.get(id=recipe_id),
    }
    return render (request, 'recipe_info.html', context)

def edit_profile(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        # "profile": Profile.objects.get(id=request.session['profile_id']),
    }
    return render (request, 'edit_profile.html', context)

def create_recipe(request):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
    }
    return render (request, 'create_recipe.html', context)


def add_recipe(request):
    errors = Recipe.objects.recipe_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/create')
    
    else:
        user = User.objects.get(id=request.session['user_id'])
        new_recipe = Recipe.objects.create(
            recipe_title=request.POST['recipe_title'], 
            recipe_directions = request.POST['recipe_directions'],
            prep_time = request.POST['prep_time'],
            uploaded_by = user,
            cook_time = request.POST['cook_time'], 
        )
        request.session['recipe_id'] = new_recipe.id
        new_recipe.save()
        user.added_recipes.add(new_recipe)
        
        this_recipe = Recipe.objects.get(id=new_recipe.id)
        new_category = Category.objects.create(
            category_name=request.POST['category_name'],
            categories = this_recipe,
        )
        new_category.save()
        
        new_ingredient = Ingredient.objects.create(
            ingredient_name = request.POST['ingredient_name'],
            ingredient_quantity = request.POST['ingredient_quantity'],
            ingredient_measurement = request.POST['ingredient_measurement'],
            ingredients_for = this_recipe,
        )
        new_ingredient.save()
        
        return redirect('/homepage')    

# def metric(request):
    

# def imperial(request):


# def percent (request):


# def add_ingredient(request):

def update_profile(request):
    errors = Profile.objects.profile_validator(request.POST)

    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/update_profile')
    
    else:
        user = User.objects.get(id=request.session['user_id'])
        profile_info = Profile.objects.create(
            title=request.POST['title'], 
            location = request.POST['location'],
            bio = request.POST['bio'],
            users = user,
        )
        request.session['profile_id'] = profile_info.id
        profile_info.save()

        return redirect('/profile')

def delete_recipe(request, recipe_id):
    Recipe.objects.get(id=recipe_id).delete()
    return redirect('/homepage')

def add_recipe(request, recipe_id):
    user=User.objects.get(id=request.session['user_id'])
    this_recipe = Recipe.objects.get(id=recipe_id)
    user.added_recipes.add(this_recipe)

    return redirect('/my_recipes')

def remove_recipe(request, recipe_id):
    user=User.objects.get(id=request.session['user_id'])
    this_recipe = Recipe.objects.get(id=recipe_id)
    user.added_recipes.remove(this_recipe)

    return redirect('/my_recipes')



def edit_recipe(request, trip_id):
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "trip": Trip.objects.get(id=trip_id),
        "start_date": str(Trip.objects.get(id=trip_id).start_date),
        "end_date": str(Trip.objects.get(id=trip_id).end_date),
    }
    return render (request, 'edit_trip.html', context)


def update(request, trip_id):
    errors = Profile.objects.profile_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/trips/{trip_id}/edit")
    else:
        updated = Trip.objects.get(id=trip_id)
        if request.method == "POST":
            updated.destination = request.POST.get('destination')
            updated.start_date = request.POST.get('start_date')
            updated.end_date = request.POST.get('end_date')
            updated.plan = request.POST.get('plan')
        updated.save()
        return redirect(f"/trips/{trip_id}")