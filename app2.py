import json
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.metrics.distance import edit_distance
from unidecode import unidecode
import re
import tkinter as tk

nltk.download('punkt')

# Cargar el corpus desde el archivo JSON
with open('corpus.json', 'r', encoding='utf-8') as file:
    corpus = json.load(file)

# Obtener la lista de conversaciones
conversaciones = corpus["conversaciones"]

# Tokenización
def tokenize(text):
    normalized_text = unidecode(text)
    text_without_punctuation = re.sub(r'[¿?¡!]', '', normalized_text)
    return word_tokenize(text_without_punctuation)

# Función para calcular la similitud entre dos listas de tokens
def calculate_similarity(tokens1, tokens2):
    distance = edit_distance(" ".join(tokens1), " ".join(tokens2))
    similarity = 1 - (distance / max(len(tokens1), len(tokens2)))
    return similarity

# Crear un modelo simple basado en NLTK
def train_nltk_model(conversaciones):
    training_data = []

    for conversacion in conversaciones:
        usuario = conversacion["usuario"]
        bot = conversacion["bot"]

        tokens_usuario = tokenize(" ".join(usuario))
        tokens_bot = tokenize(" ".join(bot))

        training_data.append((tokens_usuario, tokens_bot))

    return training_data

# Entrenar el modelo
training_data = train_nltk_model(conversaciones)

# Modificar la función select_response
def select_response(input_text, training_data, similarity_threshold=0.7):
    input_tokens = tokenize(unidecode(input_text.lower()))
    best_similarity = 0.0
    best_response = "Lo siento, aun no estoy lo suficientemente entrenado para responder a ello."

    for pattern, response in training_data:
        pattern_tokens = tokenize(" ".join([unidecode(token.lower()) for token in pattern]))
        similarity = calculate_similarity(input_tokens, pattern_tokens)
        if similarity > best_similarity and similarity >= similarity_threshold:
            best_similarity = similarity
            best_response = " ".join(response)

    if best_similarity > similarity_threshold:
        return best_response
    else:
        return "Lo siento, aun no estoy lo suficientemente entrenado para poderte dar una respuesta a ello."

# Función para manejar la entrada del usuario desde la interfaz gráfica
def handle_user_input():
    usuario_input = entry.get()
    if usuario_input.lower() == 'salir':
        root.quit()
    respuesta_bot = select_response(usuario_input, training_data)
    conversation_text.config(state=tk.NORMAL)
    conversation_text.insert(tk.END, "Tú: " + usuario_input + "\n")
    conversation_text.insert(tk.END, "Bot: " + respuesta_bot + "\n")
    conversation_text.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

# Crear la ventana principal
root = tk.Tk()
root.title("MusiTomo Chatbot")

# Crear un campo de texto para mostrar la conversación
conversation_text = tk.Text(root, state=tk.DISABLED)
conversation_text.pack()

# Crear un campo de entrada para que el usuario escriba
entry = tk.Entry(root)
entry.pack()

# Crear un botón para enviar el mensaje del usuario
send_button = tk.Button(root, text="Enviar", command=handle_user_input)
send_button.pack()

# Iniciar el chat
conversation_text.config(state=tk.NORMAL)
conversation_text.insert(tk.END, "Bot: ¡Hola! Soy MusiTomo.\n")
conversation_text.config(state=tk.DISABLED)

root.mainloop()