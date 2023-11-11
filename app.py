import json  # biblioteca para trabajar con datos en formato JSON
import random  # biblioteca para generar números aleatorios
import nltk  # Natural Language Toolkit para procesamiento de lenguaje natural
from nltk.tokenize import word_tokenize  # para tokenizar palabras
from nltk.metrics.distance import edit_distance # para calcular distancias entre cadenas de texto
from unidecode import unidecode # para para quitar diacríticos de caracteres Unicode
import re  # para realizar operaciones de expresiones regulares
from flask import Flask, request, render_template # para construir una aplicación web

nltk.download('punkt')  # modelo punkt para tokenizar palabras

# se crea la instancia de Flask, y se especifica un directorio donde se almacenan CSS, JS, imágenes, etc.
app = Flask(__name__, static_folder='static')

# Cargar el corpus desde el archivo JSON (corpus.json, r en modo lectura, utf-8 para caracteres especiales)
with open('corpus.json', 'r', encoding='utf-8') as file:
    corpus = json.load(file)  # cargar el archivo JSON en la variable corpus

# Obtener la lista de conversaciones del corpus
conversaciones = corpus["conversaciones"]

# Tokenización
def tokenize(text):
    normalized_text = unidecode(text) # quitar diacríticos de caracteres Unicode (á -> a, é -> e, etc.)
    text_without_punctuation = re.sub(r'[¿?¡!]', '', normalized_text) # sub para reemplazar caracteres de puntuación por una cadena vacía
    return word_tokenize(text_without_punctuation)

# Función para calcular la similitud entre dos listas de tokens
def calculate_similarity(tokens1, tokens2):
    distance = edit_distance(" ".join(tokens1), " ".join(tokens2)) # edit_distance para calcular la distancia entre dos cadenas de texto
    similarity = 1 - (distance / max(len(tokens1), len(tokens2))) # se calcula la similitud entre tokens, dando valores entre 0 (nada similar) y 1 (muy similar
    return similarity

# Crear un modelo simple basado en NLTK
def train_nltk_model(conversaciones): # se pasa como parámetro la lista de conversaciones
    training_data = [] # lista vacía para almacenar los datos de entrenamiento

    for conversacion in conversaciones: # se recorre la lista de conversaciones
        usuario = conversacion["usuario"] # se obtiene el usuario
        bot = conversacion["bot"] # se obtiene el bot

        tokens_usuario = tokenize(" ".join(usuario)) # se tokeniza el usuario
        tokens_bot = tokenize(" ".join(bot)) # se tokeniza las respuestas del bot el bot

        training_data.append((tokens_usuario, tokens_bot)) # se añade a la lista de datos de entrenamiento

    return training_data


# Entrenar el modelo: se llama a la función train_nltk_model y se pasa como parámetro la lista de conversaciones
training_data = train_nltk_model(conversaciones)

# Modificar la función select_response
# se pasa como parámetro el texto de entrada, los datos de entrenamiento y el umbral de similitud (70%)
def select_response(input_text, training_data, similarity_threshold=0.7):
    input_tokens = tokenize(unidecode(input_text.lower())) # se tokeniza, se quitan diacríticos y se pasa el texto a minúsculas
    best_similarity = 0.0 # se inicializa la mejor similitud a 0
    best_response = "Lo siento, aun no estoy lo suficientemente entrenado para responder a ello."

    for pattern, response in training_data: # se recorre la lista de datos de entrenamiento (patrón, respuesta)
         # se tokeniza el patrón, se quitan diacríticos y se pasa el texto a minúsculas
        pattern_tokens = tokenize(" ".join([unidecode(token.lower()) for token in pattern]))
        similarity = calculate_similarity(input_tokens, pattern_tokens) # se calcula la similitud entre el texto de entrada y el patrón
         # si la similitud es mayor que la mejor similitud y mayor o igual que el umbral de similitud (0.7)
        if similarity > best_similarity and similarity >= similarity_threshold:
            best_similarity = similarity # se actualiza la mejor similitud
            best_response = " ".join(response) # se actualiza la mejor respuesta (se pasa a cadena de texto) con la respuesta del bot

    if best_similarity > similarity_threshold: # si la mejor similitud es mayor que el umbral de similitud (0.7)
        return best_response
    else:
        return "Lo siento, aun no estoy lo suficientemente entrenado para poderte dar una respuesta a ello."


@app.route('/') # ruta raíz
def chat():
    return render_template('chat.html') # se renderiza la plantilla chat.html


@app.route('/send_message', methods=['POST']) # ruta para enviar el mensaje
def send_message():
    user_input = request.form['user_input'] # se obtiene el texto de entrada
    # se llama a la función select_response y se pasa como parámetro el texto de entrada y los datos de entrenamiento
    response = select_response(user_input, training_data)
    return response


if __name__ == '__main__': # si se ejecuta el script directamente
    app.run(debug=True) # se ejecuta la aplicación en modo debug (para desarrollo)
