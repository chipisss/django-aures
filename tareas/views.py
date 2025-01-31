from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form_ulario import TareaForm
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "home.html")


def registro(request):
    if request.method == "GET":
        return render(
            request,
            "registro.html",
            {
                "form": UserCreationForm,
            },
        )
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("crear_tarea")
            except IntegrityError:
                return render(
                    request,
                    "registro.html",
                    {"form": UserCreationForm, "error": "Ya existe"},
                )

        return render(
            request,
            "registro.html",
            {"form": UserCreationForm, "error": "No coinciden las claves"},
        )


@login_required
def tareas(request):
    task = Tarea.objects.filter(usuario=request.user, completado__isnull=True)
    return render(request, "tareas.html", {"tareas": task})


@login_required
def todas(request):
    task = Tarea.objects.filter(usuario=request.user)
    return render(request, "tareas-todas.html", {"tareas": task})


@login_required
def crear_tarea(request):
    if request.method == "GET":
        return render(
            request,
            "crear-tarea.html",
            {
                "form": TareaForm,
            },
        )
    else:
        try:
            form = TareaForm(request.POST)
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
            return redirect("tareas")
        except ValueError:
            return render(
                request,
                "crear-tarea.html",
                {"form": TareaForm},
            )


@login_required
def editar_tarea(request, tarea_id):
    if request.method == "GET":
        task = get_object_or_404(Tarea, pk=tarea_id)
        form = TareaForm(instance=task)
        print(form)
        return render(request, "editar-tarea.html", {"tarea": task, "form": form})
    else:

        try:
            task = get_object_or_404(Tarea, pk=tarea_id)
            form = TareaForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                task.usuario = request.user
                task.save()

            return redirect("tareas")
        except ValueError:
            print("que esta pasando?")
            return render(
                request,
                "editar-tarea.html",
                {
                    "error": "no encuentro el error",
                    "tarea": task,
                    "form": form,
                },
            )


@login_required
def finalizar(request, tarea_id):
    task = get_object_or_404(Tarea, pk=tarea_id)
    if request.method == "POST":
        task = get_object_or_404(Tarea, pk=tarea_id)
        task.completado = timezone.now()
        task.save()
        print("terminado")
    return redirect("tareas")


@login_required
def eliminar(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)
    print("o que la")
    if request.method == "POST":
        print("probando")
        tarea.delete()
        return redirect("tareas")


def autenticar(request):
    if request.method == "GET":
        return render(
            request,
            "autenticar.html",
            {
                "form": AuthenticationForm,
            },
        )
    else:
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        # print(user)
        if user is None:
            return render(
                request,
                "autenticar.html",
                {
                    "form": AuthenticationForm,
                },
            )
        else:
            login(request, user)
        return redirect("tareas")

    # return render(request, "autenticar.html", {"form": AuthenticationForm})


def outlog(request):
    logout(request)
    return render(request, "home.html")
