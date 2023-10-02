from django.shortcuts import render

import os
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .models import Usuarios, Etiquetas, UsuariosDetecciones
from .serializers import UsuarioSerializer, EtiquetaSerializer, UsuariosDeteccionesSerializer
from rest_framework import status

from django.http import JsonResponse

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_usuarios(request):
    usuarios = Usuarios.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_etiquetas(request):
    etiquetas = Etiquetas.objects.all()
    serializer = EtiquetaSerializer(etiquetas, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'})
    else:
        return Response({'message': 'Invalid credentials'}, status=400)



@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logout successful'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    user = request.user
    if user.is_authenticated:
        # Obtén todos los datos del usuario utilizando el serializador
        serializer = UsuarioSerializer(user)
        user_data = serializer.data
        return Response({'message': 'Usuario autenticado', 'user_data': user_data})
    else:
        return Response({'message': 'Usuario no autenticado'}, status=401)

@api_view(['POST'])
@permission_classes([AllowAny])  # Esto permite el acceso sin autenticación
def registrar_usuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Usuario registrado con éxito'})
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_detecciones(request):
    # Obtener parámetros de consulta (etiqueta_id y orden)
    etiqueta_id = request.GET.get('etiqueta_id')
    orden = request.GET.get('orden')

    # Obtener todas las detecciones del usuario autenticado
    detecciones = UsuariosDetecciones.objects.filter(usuario=request.user)

    # Filtrar por etiqueta si se proporciona etiqueta_id
    if etiqueta_id and etiqueta_id != 'todo':
        etiqueta = Etiquetas.objects.filter(id=etiqueta_id).first()
        if etiqueta:
            detecciones = detecciones.filter(etiqueta=etiqueta)

    # Ordenar por fecha de carga más reciente si se proporciona 'orden=desc'
    if orden == 'asc':
        detecciones = detecciones.order_by('deteccion__fecha_creacion')
    elif orden == 'desc':
        detecciones = detecciones.order_by('-deteccion__fecha_creacion')

    # Serializar las detecciones utilizando el serializador adecuado
    serializer = UsuariosDeteccionesSerializer(detecciones, many=True, context={'request': request})  # Usa el serializador correcto aquí
    # print(serializer.data)
    return Response({'detecciones': serializer.data})