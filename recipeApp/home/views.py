from django.shortcuts import render,redirect
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.messages import add_message, WARNING, SUCCESS
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    user = request.user
    return render(request , "home.html" , {"user":user})

@login_required(login_url="/login/")
def recipes(request):
    recipe = Recipe.objects.all()
    paginator = Paginator(recipe, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request , "recipes.html", {"data" : page_obj})

@login_required(login_url="/login/")
def upload(request):
    if request.method=="POST" :
        data = request.POST
        recipeNew = Recipe(
            user = request.user,
            title = data.get('title'),
            description = data.get('description'),
            link = data.get('link'),
            image = request.FILES.get('image'),
        )
        recipeNew.save()
        add_message(request,SUCCESS, message="Recipe Uploaded Sucessfully")
        return redirect("/upload/")


    return render(request , "upload.html")

@login_required(login_url="/login/")
def detail(request):
    try:
        recipe = Recipe.objects.get(id=request.GET.get('id'))
    except Recipe.DoesNotExist:
        add_message(request, WARNING, message="Recipe not found")
        return redirect("/recipes/")
    
    context = {'data': recipe, 'page': request.GET.get('page')}
    return render(request, "detail.html", context=context)


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
        
        user = authenticate(request, username = data.get("username") , password = data.get("password"))

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

@login_required(login_url="/login/")
def user(request):
    user = request.user
    return render(request , "user.html", {"user_data" : user})