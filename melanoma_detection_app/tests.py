from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Usuarios  # Asegúrate de que esta importación sea correcta

import os

# Create your tests here.

class RegistroLoginObtenerDatosTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.file_path = os.path.join("/home/gustavo/Imágenes/user_img.jpg") 

    def test_registro_login_obtener_datos(self):
        # Paso 1: Registro de un nuevo usuario
        registro_url = reverse('registro_usuario')
        nuevo_usuario_data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password': '123456789',
            'fecha_nacimiento': '1991-01-01',
            'sexo': 'Masculino',
            'foto_perfil': open(self.file_path, 'rb'),  # Abre el archivo en modo binario
            'first_name': 'adminNNN',
            'last_name': 'adminAA',
            'is_active': True,
        }

        response = self.client.post(registro_url, nuevo_usuario_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Paso 2: Inicio de sesión con el nuevo usuario
        login_url = reverse('user_login')
        credenciales = {
            'email': 'test@gmail.com',
            'password': '123456789',
        }
        response = self.client.post(login_url, credenciales, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Paso 3: Obtener los datos del usaurio autenticado, se usa url de check_authentication
        datos_usuario_url = reverse('check_authentication')
        response = self.client.get(datos_usuario_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ahora, puedes acceder al contenido JSON de la respuesta
        etiquetas_data = response.json()

        # Muestra las etiquetas en la terminal
        print("Datos del usaurio autenticado:")
        print(etiquetas_data)


class ActualizarDatosUsuarioTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Usuarios.objects.create(username='testuser', email='test@gmail.com', password='123456789')  # Crea un usuario

    def test_actualizar_datos_usuario(self):
        # Iniciar sesión con el usuario
        login_url = reverse('user_login')
        credenciales = {
            'email': 'test@gmail.com',
            'password': '123456789',
        }
        response = self.client.post(login_url, credenciales, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Actualizar los datos del usuario
        update_url = reverse('update_usuario', args=[self.user.id])
        nuevos_datos = {
            'first_name': 'NuevoNombre',
            'last_name': 'NuevoApellido',
            # Aca se pueden agregar otros campos que desees actualizar
        }
        response = self.client.put(update_url, nuevos_datos, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que los datos se hayan actualizado correctamente
        print("Nombre antes de actualziar: " + self.user.first_name)
        self.user.refresh_from_db()
        print("Nombre despues de actualizar: " + self.user.first_name)
        self.assertEqual(self.user.first_name, 'NuevoNombre')
        self.assertEqual(self.user.last_name, 'NuevoApellido')
        # Aca se puede agregar otras verificaciones para otros campos si es necesario



class ActualizarDatosUsuarioSinSesionTestCase(TestCase):
    def setUp(self):
        # Crea un cliente de API para simular las solicitudes
        self.client = APIClient()

        # Crea un usuario de ejemplo en la base de datos
        self.user = Usuarios.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

    def test_actualizar_datos_usuario_sin_sesion(self):
        # Obtiene la URL de la vista de actualización de usuario
        update_url = reverse('update_usuario', args=[self.user.id])

        # Datos de actualización
        nuevos_datos = {
            'first_name': 'NuevoNombre',
            'last_name': 'NuevoApellido',
            # Añade otros campos si es necesario
        }

        # Realiza una solicitud PUT a la vista de actualización sin autenticación
        response = self.client.put(update_url, nuevos_datos, format='json')

        # Verifica que la respuesta tenga un código de estado HTTP 401 (No autorizado)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



