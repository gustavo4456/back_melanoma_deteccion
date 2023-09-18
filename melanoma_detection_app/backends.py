from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomEmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        
        try:
            user = User.objects.get(email=email)
            print("Se encontro al usuario con el correo electronico:", user)
        except User.DoesNotExist:
            print("No se encontró ningún usuario con el correo electrónico:", email)
            return None
        
        if user.password == password:  # Compara la contraseña en texto plano
            print("Contraseña correcta: ", password)
            return user
        else:
            print("Contraseña incorrecta")
            return None
        
        
    
    def authenticate_header(self, request):
        return 'CustomEmailBackend'
