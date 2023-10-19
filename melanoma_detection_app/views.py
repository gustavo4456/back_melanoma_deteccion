from django.shortcuts import render

import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from .models import Usuarios, Etiquetas, UsuariosDetecciones, ConfiguracionUsuario, Notificaciones
from .serializers import UsuarioSerializer, EtiquetaSerializer, UsuariosDeteccionesSerializer, ConfiguracionUsuarioSerializer, NotificacionSerializer
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
@permission_classes([AllowAny])
def registrar_usuario(request):
    # Serializa los datos del usuario a registrar
    usuario_serializer = UsuarioSerializer(data=request.data)
    if usuario_serializer.is_valid():
        usuario = usuario_serializer.save()

        # Crea una configuración de usuario para el usuario registrado
        configuracion_usuario = ConfiguracionUsuario(usuario=usuario)
        configuracion_usuario.save()  # Guarda la configuración de usuario

        return Response({'mensaje': 'Usuario registrado con éxito'}, status=201)
    return Response(usuario_serializer.errors, status=400)



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


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_usuarios_detecciones(request):
    try:
        # Obtén una lista de IDs de detecciones a eliminar del cuerpo de la solicitud
        deteccion_ids = request.data.get('deteccion_ids', [])

        # Verifica que al menos un ID haya sido proporcionado
        if not deteccion_ids:
            return Response({'message': 'Debes proporcionar al menos un ID de detección para eliminar.'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtra los registros de UsuariosDetecciones que pertenecen al usuario autenticado y tienen IDs en la lista
        usuarios_detecciones = UsuariosDetecciones.objects.filter(usuario=request.user, id__in=deteccion_ids)

        # Verifica si se encontraron registros para eliminar
        if not usuarios_detecciones:
            return Response({'message': 'No se encontraron detecciones para eliminar o no tienes permiso para eliminarlas.'}, status=status.HTTP_404_NOT_FOUND)

        # Itera a través de los registros de UsuariosDetecciones y elimina tanto la detección como el registro en UsuariosDetecciones.
        for usuarios_deteccion in usuarios_detecciones:
            # Obtén la instancia de Detecciones a la que está relacionada este UsuariosDetecciones.
            deteccion = usuarios_deteccion.deteccion
            # Obtén la ruta del archivo de imagen asociado a la detección.
            imagen_path = os.path.join(settings.MEDIA_ROOT, str(deteccion.imagen))
            # Elimina tanto la instancia de UsuariosDetecciones como la de Detecciones.
            usuarios_deteccion.delete()
            deteccion.delete()
            # Elimina el archivo físico de la imagen.
            if os.path.exists(imagen_path):
                os.remove(imagen_path)

        return Response({'message': 'Las detecciones y los registros de UsuariosDetecciones han sido eliminados correctamente.'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_usuario(request, pk):
    try:
        usuario = Usuarios.objects.get(pk=pk)

        # Verifica que el usuario que realiza la solicitud sea el propietario del perfil o un administrador
        if request.user == usuario or request.user.is_staff:
            serializer = UsuarioSerializer(usuario, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No tienes permiso para actualizar este usuario.'}, status=status.HTTP_403_FORBIDDEN)
    except Usuarios.DoesNotExist:
        return Response({'message': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notificaciones(request):
    # Obtén todas las notificaciones
    notificaciones = Notificaciones.objects.all()
    
    # Serializa las notificaciones
    serializer = NotificacionSerializer(notificaciones, many=True)
    
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def configuracion_usuario(request):
    try:
        usuario = request.user  # Obtén el usuario autenticado

        # Verifica si ya existe una configuración de usuario para este usuario
        configuracion_usuario, created = ConfiguracionUsuario.objects.get_or_create(usuario=usuario)

        if request.method == 'GET':
            # Si la solicitud es una GET, simplemente se serializa y devuelve la configuración del usuario
            serializer = ConfiguracionUsuarioSerializer(configuracion_usuario)
            return Response(serializer.data)

        elif request.method == 'PUT':
            # Si la solicitud es una PUT, actualiza la configuración del usuario con los datos proporcionados
            serializer = ConfiguracionUsuarioSerializer(configuracion_usuario, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except ConfiguracionUsuario.DoesNotExist:
        return Response({'message': 'La configuración de usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notificaciones(request):
    # Obtén todas las notificaciones
    notificaciones = Notificaciones.objects.all()
    
    # Serializa las notificaciones
    serializer = NotificacionSerializer(notificaciones, many=True)
    
    return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def crear_notificacion(request):
#     if request.method == 'POST':
#         serializer = NotificacionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def eliminar_notificacion(request, notificacion_id):
#     try:
#         notificacion = Notificaciones.objects.get(id=notificacion_id)
#     except Notificaciones.DoesNotExist:
#         return Response({'message': 'La notificación no existe.'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'DELETE':
#         notificacion.delete()
#         return Response({'message': 'Notificación eliminada correctamente.'})
    
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def actualizar_notificacion(request, notificacion_id):
#     try:
#         notificacion = Notificaciones.objects.get(id=notificacion_id)
#     except Notificaciones.DoesNotExist:
#         return Response({'message': 'La notificación no existe.'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = NotificacionSerializer(notificacion, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

