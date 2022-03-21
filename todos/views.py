from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'todos/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todos/signup.html', {'forms':UserCreationForm()})
    else:
        #Create a new User
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save() #To save the user information from above line into database
                login(request, user)
                return redirect('currenttodos') #viewname parameter
            except IntegrityError:
                return render(request, 'todos/signup.html', {'forms':UserCreationForm(), 'error':"This username is already taken, please use a different username"})


        else:
            #Tell the user that passwords didn't match
            return render(request, 'todos/signup.html', {'forms':UserCreationForm(), 'error':"Passwords didn't match"})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todos/login.html', {'forms':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todos/login.html', {'forms':AuthenticationForm(), 'error':'Username & Password did not match, try again'})
        else:
            login(request, user)
            return redirect('currenttodos')   

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todos/createtodo.html', {'todoform':TodoForm()} ) 
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False) #.save saves the stuff to database and we dont want to save yet as these todo details should belong to the logged in user.
        newtodo.user = request.user
        newtodo.save()
        return redirect('currenttodos')  

@login_required
def currenttodos(request):
    todoss = Todo.objects.filter(user=request.user, datecompleted__isnull=True)#user=request.user is for only displaying info for that user.
    return render(request, 'todos/currenttodos.html', {'todos': todoss})

@login_required
def completedtodos(request):
    todoss = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('datecompleted')# Use order by for ordering how you want to see on webpage.
                                                                                                           #Use -datecompleted with 'minus' order in descending
    return render(request, 'todos/completedtodos.html', {'todos': todoss})

@login_required
def viewtodo(request, todo_pk):
    todos = get_object_or_404(Todo, pk = todo_pk, user=request.user) #Takes (model class, primary key AS ARGUEMENT), 
                                                                     #taking user=request.user bcoz the logged in user can see only his todos
    if request.method == 'GET':
        form = TodoForm(instance=todos) 
        #we can pass in our model 'instance' into this form if we want to display and update the
        #associated already filled details for that todo.
        return render(request, "todos/viewtodo.html", {'todo':todos, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todos)#instance parameter has to be put here as coz of this the form will know
                                                          #we are trying to edit an already existing user.
            form.save()
            return redirect('currenttodos') 
        except ValueError:
            return render(request, "todos/viewtodo.html", {'todo':todos, 'form':form, 'error':'Bad data'})            

@login_required
def completetodo(request, todo_pk):
    todos = get_object_or_404(Todo, pk = todo_pk, user=request.user)
    if request.method=='POST':
        todos.datecompleted = timezone.now()
        todos.save()
        return redirect('currenttodos') 

@login_required
def deletetodo(request, todo_pk):
    todos = get_object_or_404(Todo, pk = todo_pk, user=request.user)
    if request.method=='POST':
        todos.delete()
        return redirect('currenttodos') 


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')