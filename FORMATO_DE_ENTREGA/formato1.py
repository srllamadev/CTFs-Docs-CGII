import hashlib

texto = input("Ingrese el texto: ")

primera = hashlib.md5(texto.encode()).hexdigest()
segunda = hashlib.md5(texto.replace(" ", "").encode()).hexdigest()
tercera = hashlib.md5(texto.lower().encode()).hexdigest()
cuarta = hashlib.md5(texto.replace(" ", "").lower().encode()).hexdigest()

print(f"\nprimera entrega:\n{primera}")
print(f"\nsegunda entrega:\n{segunda}")
print(f"\ntercera entrega:\n{tercera}")
print(f"\ncuarta entrega:\n{cuarta}")
