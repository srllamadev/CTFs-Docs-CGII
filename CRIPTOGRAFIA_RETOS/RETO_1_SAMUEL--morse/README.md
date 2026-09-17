# Documentación de Solución: Reto de Criptografía "Samuel"

## 1. Información General del Reto
* **Nombre del Reto:** Samuel
* **Puntos:** 50
* **Descripción:** "Nuestro amigo nos dejo este mensaje al parecer trabaja ahí."
* **Mensaje cifrado:** `-.-. . -. - .-. --- / -.. . / --. . ... - .. --- -. / -.. . / .. -. -.-. .. -.. . -. - . ... / .. -. ..-. --- .-. -- .- - .. -.-. --- ...`
* **Formato de la Flag:** `cidsi{Tu_flag_en_MD5}`

## 2. Análisis Inicial
El reto presenta un mensaje cifrado mediante código Morse, evidenciado por el uso de puntos (`.`), guiones (`-`) y barras (`/`) que actúan como separadores de palabras.

## 3. Paso 1: Decodificación del Código Morse
Para descifrar el mensaje inicial, se utilizó un script en Python:

- Define un diccionario para mapear los caracteres del código Morse al alfabeto tradicional. 

Al ejecutar la función `morse_a_texto` con el código proporcionado:

```python
codigo_entrada = "-.-. . -. - .-. --- / -.. . / --. . ... - .. --- -. / -.. . / .. -. -.-. .. -.. . -. - . ... / .. -. ..-. --- .-. -- .- - .. -.-. --- ..."
texto_traducido = morse_a_texto(codigo_entrada)
print(texto_traducido)
```

**Texto descifrado resultante:** `CENTRO DE GESTION DE INCIDENTES INFORMATICOS`

## 4. Paso 2: Generación del Hash MD5
Convertir el texto obtenido a un hash MD5 utilizando la librería `hashlib` de Python. Se diseñó un segundo script para calcular cuatro posibles variantes del hash:

1. El texto original con espacios y mayúsculas.
2. El texto sin espacios (`texto.replace(" ", "")`).
3. El texto en minúsculas (`texto.lower()`).
4. El texto en minúsculas y sin espacios.

Código utilizado para las variantes:
```python
import hashlib

texto = "CENTRO DE GESTION DE INCIDENTES INFORMATICOS"
primera = hashlib.md5(texto.encode()).hexdigest()
segunda = hashlib.md5(texto.replace(" ", "").encode()).hexdigest()
tercera = hashlib.md5(texto.lower().encode()).hexdigest()
cuarta = hashlib.md5(texto.replace(" ", "").lower().encode()).hexdigest()
```

Al probar las opciones generadas contra la plataforma del reto, se determinó que la **segunda entrega** (el hash del texto en mayúsculas pero sin espacios) era la correcta.

* **Texto utilizado para el hash correcto:** `CENTRODEGESTIONDEINCIDENTESINFORMATICOS`
* **Hash MD5 generado (Segunda entrega):** `942fb4e8d4a076e1c38e446ad94cc378`

## 5. Solución Final


**Flag:** `cidsi{942fb4e8d4a076e1c38e446ad94cc378}`