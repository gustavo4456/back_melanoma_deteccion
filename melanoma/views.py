from django.shortcuts import render


# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from melanoma_detection_app.models import Etiquetas, UsuariosDetecciones, Detecciones
from datetime import datetime

import cv2
import numpy as np
from tensorflow import keras

# Función para aplicar la segmentación utilizando la magnitud del gradiente
def apply_image_enhancements(image):
    # Extraer el canal azul de la imagen
    blue_channel = image[:, :, 0]  # El canal azul está en la posición 0 del eje RGB
    
    # Aplicar un ajuste de contraste al canal azul para realzar el color
    alpha = 1.5  # Factor de ajuste de contraste
    beta = 20    # Factor de ajuste de brillo
    enhanced_blue_channel = np.clip(alpha * blue_channel + beta, 0, 255).astype(np.uint8)
    
    # Crear una copia de la imagen original y reemplazar el canal azul con el canal realzado
    enhanced_image = image.copy()
    enhanced_image[:, :, 0] = enhanced_blue_channel
    
    # Convertir la imagen realzada a escala de grises
    gray_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2GRAY)
    
    # Mezclar la imagen en escala de grises con el canal azul realzado
    weighted_gray_image = cv2.addWeighted(gray_image, 0.5, enhanced_blue_channel, 0.5, 0)
    
    return weighted_gray_image

# cargar el modelo entrenado
model = keras.models.load_model('models/best_model.h5')

# definir las etiquetas
labels = {0: 'non_melanoma', 1: 'melanoma'}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def detect_melanoma(request):
    # leer la imagen del request
    file = request.FILES['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # aplicar la segmentación a la imagen de prueba
    segmented_img = apply_image_enhancements(image)

    # redimensionar la imagen a 128x128 píxeles
    resized_image = cv2.resize(segmented_img, (100, 100))

    # normalizar la imagen
    normalized_image = resized_image / 255.0

    # agregar una dimensión a la imagen para que tenga la forma (1, 128, 128, 3)
    input_image = np.expand_dims(normalized_image, axis=0)

    # Obtener la predicción del modelo
    predictions = model.predict(input_image)
    predicted_class = np.argmax(predictions[0])  # Índice de la clase con mayor probabilidad
    class_names = ['No Melanoma', 'Melanoma']  # Nombre de las clases



# Guardar la imagen en la tabla Detecciones
    deteccion = Detecciones()
    deteccion.imagen.save(file.name, file, save=True)
    # deteccion.fecha_creacion = datetime.now()
    deteccion.resultado = class_names[predicted_class]
    deteccion.save()

    # Obtener la ID y el nombre de la etiqueta desde la solicitud
    etiqueta_id = request.data.get('etiqueta_id')
    etiqueta_nombre = request.data.get('etiqueta_nombre')

    # Buscar la etiqueta existente por ID
    try:
        etiqueta = Etiquetas.objects.get(id=etiqueta_id)
    except Etiquetas.DoesNotExist:
        # Si la etiqueta no existe, créala
        etiqueta = Etiquetas(nombre=etiqueta_nombre)
        etiqueta.save()

    # Crear una instancia de UsuariosDetecciones y establecer la etiqueta
    usuarios_detecciones = UsuariosDetecciones()
    usuarios_detecciones.etiqueta = etiqueta

    # Asociar la detección, el usuario y otros datos
    usuarios_detecciones.deteccion = deteccion
    usuarios_detecciones.usuario = request.user
    usuarios_detecciones.save()




    # devolver la respuesta
    response = {
        'result': class_names[predicted_class]
    }
    return Response(response)






