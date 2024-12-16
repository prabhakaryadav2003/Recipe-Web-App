from django.shortcuts import render,redirect
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.messages import add_message, WARNING, SUCCESS
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request , "home.html")

@login_required(login_url="/login/")
def recipes(request):
    context = {'data' : Recipe.objects.all()}
    return render(request , "recipes.html", context=context)

@login_required(login_url="/login/")
def upload(request):
    if request.method=="POST" :
        data = request.POST
        recipieNew = Recipe(
            title = data.get('title'),
            description = data.get('description'),
            image = request.FILES.get('image'),
        )
        recipieNew.save()
        add_message(request,SUCCESS, message="Recipe Uploaded Sucessfully")
        return redirect("/upload/")


    return render(request , "upload.html")

@login_required(login_url="/login/")
def detail(request, id):
    context = {'data' : Recipe.objects.get(id=id)}
    return render(request , "detail.html", context=context)


def register(request):
    
    if request.method=="POST":
        data = request.POST

        if User.objects.filter(username = data.get("username")).exists():
            add_message(request,WARNING, message="Username already taken")
            return redirect("/register/")
        
        user = User(
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            username = data.get("username")
        )

        user.set_password(data.get("password"))
        user.save()
        add_message(request,SUCCESS, message="Username registered sucessfully")
        return redirect("/login/")

    return render(request , "register.html")


def login_page(request):

    if request.method =="POST":
        data = request.POST
        if not User.objects.filter(username = data.get("username") ).exists():
            add_message(request,WARNING, message="Invalid Username")
            return redirect("/login/")
        
        user = authenticate(username = data.get("username") , password = data.get("password"))

        if user is None :
            add_message(request,WARNING , message="Invalid Password")
            return redirect("/login/")
        else:
            login(request,user)
            return redirect("/recipes/")

    return render(request , "login.html")

@login_required(login_url="/login/")
def logout_page(request):
    logout(request)
    return redirect("/login/")