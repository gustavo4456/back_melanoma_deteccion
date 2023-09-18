from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def suma(request, num1, num2):
    resultado = num1 + num2
    return HttpResponse(f"La suma de {num1} y {num2} es {resultado}")

def hola_mundo(request):
    return HttpResponse("Hola Mundo")

