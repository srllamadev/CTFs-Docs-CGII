# Diccionario con el alfabeto, números y algunos signos en código Morse
MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--', ' ': '/'
}

# Invertir el diccionario para traducir de Morse a Texto
REVERSE_MORSE_DICT = {value: key for key, value in MORSE_DICT.items()}

def texto_a_morse(texto):
    """Convierte una cadena de texto a código Morse."""
    morse = []
    # Convertir a mayúsculas para que coincida con el diccionario
    for caracter in texto.upper():
        if caracter in MORSE_DICT:
            morse.append(MORSE_DICT[caracter])
    # Unir los caracteres con un espacio
    return ' '.join(morse)

def morse_a_texto(codigo_morse):
    """Convierte código Morse a una cadena de texto."""
    texto = []
    # Separar el código por espacios (cada letra en Morse está separada por un espacio)
    caracteres = codigo_morse.split(' ')
    for caracter in caracteres:
        if caracter in REVERSE_MORSE_DICT:
            texto.append(REVERSE_MORSE_DICT[caracter])
    return ''.join(texto).replace('/', ' ') # Reemplazar la barra por espacio real

# --- Ejemplos de uso ---
texto_original = "HOLA MUNDO"
morse_traducido = texto_a_morse(texto_original)
print(f"Texto original: {texto_original}")
print(f"En Morse: {morse_traducido}")

print("-" * 30)

codigo_entrada = "-.-. . -. - .-. --- / -.. . / --. . ... - .. --- -. / -.. . / .. -. -.-. .. -.. . -. - . ... / .. -. ..-. --- .-. -- .- - .. -.-. --- ..."
texto_traducido = morse_a_texto(codigo_entrada)
print(f"Código Morse: {codigo_entrada}")
print(f"En Texto: {texto_traducido}")