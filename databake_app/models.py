from django.db import models
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):

        errors = {}

        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be at least 2 characters"

        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be at least 2 characters"

        if len(postData['email'])<1:
            errors['email'] = "Email cannot be blank"
        elif not EMAIL_REGEX.match(postData['email']):               
            errors['email'] = "Invalid email address"

        if len(postData['password'])<8:
            errors['password'] = "Password must be at least 8 characters"

        if postData['password'] != postData['confirm']:
            errors['passwords'] = "Passwords must match"

        user = User.objects.filter(email=postData['email'])
        if len(user) != 0:
            errors['login_email']="This email has already been registered"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()


class RecipeManager(models.Manager):

    def recipe_validator(self, postData):

        errors = {}

        if len(postData['recipe_title'])<2:
            errors['recipe_title'] = "Title must be at least 2 characters" 

        if len(postData["recipe_directions"]) <10:
            errors["recipe_directions"] = "Directions must be at least 10 characters"

        if len(postData['prep_time']) < 1:
            errors['prep_time'] = "Prep time cannot be left blank"

        if len(postData['cook_time'])<1:
            errors['cook_time'] = "Cook time cannot be left blank"

        return errors

class Recipe(models.Model):
    recipe_title = models.CharField(max_length=255)
    recipe_directions = models.TextField()
    prep_time = models.CharField(max_length = 20)
    cook_time = models.CharField(max_length = 20)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    uploaded_by = models.ForeignKey(User, related_name="recipes_uploaded", on_delete = models.CASCADE)
    added_by = models.ManyToManyField(User, related_name="added_recipes")

    objects = RecipeManager()


class Image(models.Model):
    recipe_image = models.ImageField(upload_to='images/')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    images = models.ForeignKey(Recipe, related_name="for_recipe", on_delete = models.CASCADE)

class CategoryManager(models.Manager):

    def category_validator(self, postData):

        errors = {}

        if len(postData['category_name'])<1:
            errors['category_name'] = "Category name cannot be blank" 

        return errors

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    categories = models.ForeignKey(Recipe, related_name="recipe_categories", on_delete = models.CASCADE, null=True)

    objects = CategoryManager()


class IngredientManager(models.Manager):

    def ingredient_validator(self, postData):

        errors = {}

        if len(postData['ingredient_name'])<1:
            errors['ingredient_name'] = "Ingredients cannot be blank" 

        if len(postData['ingredient_quantity'])<1:
            errors['ingredient_quantity'] = "Quantity cannot be blank" 

        if len(postData['ingredient_measurement'])<1:
            errors['ingredient_measurement'] = "Quantities cannot be blank"   

        return errors


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)
    ingredient_quantity = models.FloatField(null=True)
    ingredient_measurement = models.CharField(max_length=15, null=True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    ingredients_for = models.ForeignKey(Recipe, related_name="recipe_ingredients",on_delete=models.CASCADE)

    objects = IngredientManager()



class Tag(models.Model):
    tag_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    tags = models.ManyToManyField(Recipe, related_name="recipe_tags")


class Survey(models.Model):
    overall = models.IntegerField()
    flavor = models.IntegerField()
    difficulty = models.IntegerField()
    accessibility = models.IntegerField()
    survey_text = models.TextField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    surveys = models.ForeignKey(Recipe, related_name="recipe_surveys", on_delete=models.CASCADE)


class ProfileManager(models.Manager):
    def profile_validator(self, postData):

        errors = {}

        if len(postData['title'])<1:
            errors['title'] = "Title cannot be blank" 

        if len(postData['location'])<1:
            errors['location'] = "Location cannot be blank" 

        if len(postData['bio'])<1:
            errors['bio'] = "Bio cannot be blank"   

        return errors

class Profile(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    bio = models.TextField()

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    users = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)

    objects = ProfileManager()