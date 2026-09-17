# OPERACIÓN ESPEJO ROJO

**Nivel:** Alto | **Categoría:** Criptografía | **Puntos:** 500

---

## Contexto

Una célula de inteligencia ha sido interceptada utilizando un protocolo de comunicación cifrado de tres capas. Cada capa utiliza un algoritmo criptográfico diferente, y la salida de cada capa alimenta la siguiente.

Nuestros analistas han recuperado los siguientes datos interceptados, junto con algunas pistas crípticas dejadas por un informante interno.

---

## Datos Interceptados

### CAPA 1 - Comunicaciones RSA

Se interceptó el siguiente cifrado RSA:

```
n = 1000000000000000000000000000310000000000000000000000000020889
e = 65537
c = 124362460198726234541394411860289841086379638401675728329293
```

**Pista del informante:** *"Los gemelos guardan el secreto. La diferencia entre los factores es menor que 200."*

### CAPA 2 - Cifrado Matricial

El plaintext resultante de la Capa 1 contiene la clave para descifrar este cifrado matricial (Hill) de bloque 3x3.

**Ciphertext interceptado:**
```
FEBYDXNMDZXKVBKQPTPPTCHNJCKKXLANN
```

**Pista del informante:** *"La matriz clave fue encontrada en las notas del sospechoso. Es una matriz 3x3 con valores enteros positivos menores que 10. El determinante de la matriz es coprimo con 26. La matriz es: M = [[2, 1, 3], [5, 7, 4], [9, 2, 6]]."*

### CAPA 3 - Transposición Columnar

El resultado de la Capa 2 fue cifrado usando una transposición columnar con una palabra clave.

**Ciphertext final:**
```
BZPNANBTKXYXTJNFMKCXDKPCNEDQHLXVPKX
```

**Pista del informante:** *"La clave de transposición es una palabra de 7 letras relacionada con la física cuántica. El orden de las columnas se determina alfabéticamente por las letras de la clave."*

---

## Objetivo

Recuperar el mensaje original (flag) que fue cifrado en la Capa 2.

**Formato de flag:** `FLAG{mensaje_en_mayusculas_con_guiones_bajos}`

---

## Restricciones

- No se permite el uso de herramientas automatizadas de cracking
- Debe documentar cada paso del proceso de descifrado
- La solución debe incluir el código utilizado para cada capa

---

## Archivos Adjuntos

- `datos_interceptados.txt` - Contiene todos los datos numéricos del reto
- `pistas.txt` - Contiene las pistas del informante

---

## Notas Técnicas

- Todos los textos están en inglés y en mayúsculas
- El alfabeto usado es el inglés estándar de 26 letras (A-Z)
- Para el cifrado Hill, se usa aritmética modular mod 26
- Para la transposición columnar, las columnas se ordenan alfabéticamente según las letras de la clave
- Si el texto no llena completamente la matriz, se rellena con 'X' al final

---

**Buena suerte, agente. El tiempo es esencial.**
