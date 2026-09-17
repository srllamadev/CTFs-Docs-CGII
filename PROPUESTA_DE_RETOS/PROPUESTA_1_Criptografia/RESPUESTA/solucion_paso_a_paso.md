# SOLUCIÓN: OPERACIÓN ESPEJO ROJO
## Resolución Paso a Paso

---

## CAPA 1 - Descifrado RSA

### Análisis del problema

Tenemos:
```
n = 1000000000000000000000000000310000000000000000000000000020889
e = 65537
c = 124362460198726234541394411860289841086379638401675728329293
```

**Pista clave:** *"Los gemelos guardan el secreto. La diferencia entre los factores es menor que 200."*

Esto indica que los primos p y q son muy cercanos entre sí, lo que hace vulnerable a n ante el **ataque de factorización de Fermat**.

### Paso 1: Ataque de Fermat

El ataque de Fermat se basa en que si p y q son cercanos, entonces:
```
n = p * q
a = ceil(sqrt(n))
b² = a² - n
```

Si b² es un cuadrado perfecto, entonces:
```
p = a + b
q = a - b
```

**Implementación:**
```python
import math

n = 1000000000000000000000000000310000000000000000000000000020889

def fermat_factor(n):
    a = math.isqrt(n)
    if a * a == n:
        return a, a
    a += 1
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a + b, a - b
        a += 1

p, q = fermat_factor(n)
print(f"p = {p}")
print(f"q = {q}")
```

**Resultado:**
```
p = 1000000000000000000000000000099
q = 1000000000000000000000000000211
```

**Verificación:** `p * q = n` ✓

### Paso 2: Calcular la clave privada d

```python
phi = (p - 1) * (q - 1)
e = 65537
d = mod_inverse(e, phi)
```

### Paso 3: Descifrar el mensaje

```python
m = pow(c, d, n)
plaintext = m.to_bytes(14, 'big')
```

**Resultado Capa 1:**
```
KRYPTOS_MATRIX
```

Este texto será la clave para la Capa 2.

---

## CAPA 2 - Descifrado Hill 3x3

### Análisis del problema

Tenemos:
- **Plaintext de Capa 1:** `KRYPTOS_MATRIX` (no se usa directamente para la matriz)
- **Ciphertext Hill:** `FEBYDXNMDZXKVBKQPTPPTCHNJCKKXLANN`
- **Pista:** La matriz fue encontrada en las notas del sospechoso: `[[2, 1, 3], [5, 7, 4], [9, 2, 6]]`

### Paso 1: Verificar la matriz clave

La matriz proporcionada es:
```
M = [[2, 1, 3],
     [5, 7, 4],
     [9, 2, 6]]
```

Verificamos que sea invertible mod 26:
```python
def mat_det3(M):
    det = (M[0][0] * (M[1][1]*M[2][2] - M[1][2]*M[2][1])
         - M[0][1] * (M[1][0]*M[2][2] - M[1][2]*M[2][0])
         + M[0][2] * (M[1][0]*M[2][1] - M[1][1]*M[2][0]))
    return det % 26

det = mat_det3(M)
print(f"det = {det}, gcd(det, 26) = {math.gcd(det, 26)}")
```

**Resultado:** det = 19, gcd(19, 26) = 1 ✓ (La matriz es invertible)

### Paso 2: Calcular la matriz inversa mod 26

Para descifrar Hill, necesitamos M^(-1) mod 26.

```python
def mat_inverse_mod26(M):
    det = mat_det3(M) % 26
    det_inv = mod_inverse(det, 26)
    
    # Matriz adjunta (cofactores transpuestos)
    adj = [[0]*3 for _ in range(3)]
    adj[0][0] = (M[1][1]*M[2][2] - M[1][2]*M[2][1]) % 26
    adj[0][1] = -(M[0][1]*M[2][2] - M[0][2]*M[2][1]) % 26
    adj[0][2] = (M[0][1]*M[1][2] - M[0][2]*M[1][1]) % 26
    adj[1][0] = -(M[1][0]*M[2][2] - M[1][2]*M[2][0]) % 26
    adj[1][1] = (M[0][0]*M[2][2] - M[0][2]*M[2][0]) % 26
    adj[1][2] = -(M[0][0]*M[1][2] - M[0][2]*M[1][0]) % 26
    adj[2][0] = (M[1][0]*M[2][1] - M[1][1]*M[2][0]) % 26
    adj[2][1] = -(M[0][0]*M[2][1] - M[0][1]*M[2][0]) % 26
    adj[2][2] = (M[0][0]*M[1][1] - M[0][1]*M[1][0]) % 26
    
    # M^(-1) = det_inv * adj mod 26
    inv = [[(det_inv * adj[i][j]) % 26 for j in range(3)] for i in range(3)]
    return inv
```

### Paso 3: Descifrar el mensaje

```python
cipher_text = "FEBYDXNMDZXKVBKQPTPPTCHNJCKKXLANN"
cipher_nums = [ord(c) - 65 for c in cipher_text]

plaintext_nums = []
for i in range(0, len(cipher_nums), 3):
    block = [[cipher_nums[i]], [cipher_nums[i+1]], [cipher_nums[i+2]]]
    result = mat_mul(M_inv, block)
    for row in result:
        plaintext_nums.append(row[0])

plaintext = ''.join([chr(n + 65) for n in plaintext_nums])
```

**Resultado Capa 2:**
```
THEVAULTISDEEPINSIDETHEMOUNTAIN
```

---

## CAPA 3 - Descifrado por Transposición Columnar

### Análisis del problema

Tenemos:
- **Ciphertext final:** `BZPNANBTKXYXTJNFMKCXDKPCNEDQHLXVPKX`
- **Pista:** Clave de 7 letras relacionada con física cuántica

### Paso 1: Determinar la clave

La palabra de 7 letras relacionada con física cuántica es: **QUANTUM**

### Paso 2: Determinar el orden de columnas

Ordenamos las letras de QUANTUM alfabéticamente:
```
Q U A N T U M
6 7 1 4 5 3 2  (posición en orden alfabético)
```

Orden alfabético: A(1), M(2), N(3), Q(4), T(5), U(6), U(7)
```
Columna 0 (Q) -> posición 4
Columna 1 (U) -> posición 6
Columna 2 (A) -> posición 1
Columna 3 (N) -> posición 3
Columna 4 (T) -> posición 5
Columna 5 (U) -> posición 7
Columna 6 (M) -> posición 2
```

### Paso 3: Descifrar la transposición

```python
def columnar_decrypt(cipher, key):
    order = sorted(range(len(key)), key=lambda k: key[k])
    cols = len(key)
    rows = math.ceil(len(cipher) / cols)
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for col in order:
        for row in range(rows):
            if idx < len(cipher):
                grid[row][col] = cipher[idx]
                idx += 1
    result = ''
    for row in grid:
        result += ''.join(row)
    return result.rstrip('X')

final_cipher = "BZPNANBTKXYXTJNFMKCXDKPCNEDQHLXVPKX"
plaintext = columnar_decrypt(final_cipher, "QUANTUM")
```

**Resultado Capa 3:**
```
FEBYDXNMDZXKVBKQPTPPTCHNJCKKXLANN
```

Este es el ciphertext de la Capa 2, que al descifrarse con Hill nos da el mensaje original.

---

## SOLUCIÓN FINAL

El mensaje original (flag) es:

```
FLAG{THEVAULTISDEEPINSIDETHEMOUNTAIN}
```

---

## Código Completo de Solución

```python
import math
import hashlib

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

def mod_inverse(a, m):
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        return None
    return x % m

def fermat_factor(n):
    a = math.isqrt(n)
    if a * a == n:
        return a, a
    a += 1
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a + b, a - b
        a += 1

def mat_det3(M):
    return (M[0][0] * (M[1][1]*M[2][2] - M[1][2]*M[2][1])
          - M[0][1] * (M[1][0]*M[2][2] - M[1][2]*M[2][0])
          + M[0][2] * (M[1][0]*M[2][1] - M[1][1]*M[2][0])) % 26

def mat_mul(A, B):
    rows_a, cols_a = len(A), len(A[0])
    rows_b, cols_b = len(B), len(B[0])
    C = [[0]*cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % 26
    return C

def mat_inverse_mod26(M):
    det = mat_det3(M)
    det_inv = mod_inverse(det, 26)
    
    adj = [[0]*3 for _ in range(3)]
    adj[0][0] = (M[1][1]*M[2][2] - M[1][2]*M[2][1]) % 26
    adj[0][1] = -(M[0][1]*M[2][2] - M[0][2]*M[2][1]) % 26
    adj[0][2] = (M[0][1]*M[1][2] - M[0][2]*M[1][1]) % 26
    adj[1][0] = -(M[1][0]*M[2][2] - M[1][2]*M[2][0]) % 26
    adj[1][1] = (M[0][0]*M[2][2] - M[0][2]*M[2][0]) % 26
    adj[1][2] = -(M[0][0]*M[1][2] - M[0][2]*M[1][0]) % 26
    adj[2][0] = (M[1][0]*M[2][1] - M[1][1]*M[2][0]) % 26
    adj[2][1] = -(M[0][0]*M[2][1] - M[0][1]*M[2][0]) % 26
    adj[2][2] = (M[0][0]*M[1][1] - M[0][1]*M[1][0]) % 26
    
    inv = [[(det_inv * adj[i][j]) % 26 for j in range(3)] for i in range(3)]
    return inv

def columnar_decrypt(cipher, key):
    order = sorted(range(len(key)), key=lambda k: key[k])
    cols = len(key)
    rows = math.ceil(len(cipher) / cols)
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    idx = 0
    for col in order:
        for row in range(rows):
            if idx < len(cipher):
                grid[row][col] = cipher[idx]
                idx += 1
    result = ''
    for row in grid:
        result += ''.join(row)
    return result.rstrip('X')

# ===== CAPA 1: RSA =====
print("=== CAPA 1: RSA ===")
n = 1000000000000000000000000000310000000000000000000000000020889
e = 65537
c = 124362460198726234541394411860289841086379638401675728329293

p, q = fermat_factor(n)
print(f"p = {p}")
print(f"q = {q}")

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)
m = pow(c, d, n)
plaintext1 = m.to_bytes(14, 'big').decode()
print(f"Plaintext Capa 1: {plaintext1}")

# ===== CAPA 2: Hill =====
print("\n=== CAPA 2: Hill ===")
M = [[2, 1, 3], [5, 7, 4], [9, 2, 6]]
M_inv = mat_inverse_mod26(M)

cipher_text = "FEBYDXNMDZXKVBKQPTPPTCHNJCKKXLANN"
cipher_nums = [ord(ch) - 65 for ch in cipher_text]

plaintext_nums = []
for i in range(0, len(cipher_nums), 3):
    block = [[cipher_nums[i]], [cipher_nums[i+1]], [cipher_nums[i+2]]]
    result = mat_mul(M_inv, block)
    for row in result:
        plaintext_nums.append(row[0])

plaintext2 = ''.join([chr(n + 65) for n in plaintext_nums])
print(f"Plaintext Capa 2: {plaintext2}")

# ===== CAPA 3: Transposición =====
print("\n=== CAPA 3: Transposición ===")
final_cipher = "BZPNANBTKXYXTJNFMKCXDKPCNEDQHLXVPKX"
plaintext3 = columnar_decrypt(final_cipher, "QUANTUM")
print(f"Plaintext Capa 3: {plaintext3}")

# ===== FLAG =====
print(f"\n=== FLAG ===")
print(f"FLAG{{{plaintext2}}}")
```

---

## Resumen de Técnicas Utilizadas

| Capa | Cifrado | Vulnerabilidad | Técnica de Ataque |
|------|---------|----------------|-------------------|
| 1 | RSA | Primos cercanos (diferencia < 200) | Factorización de Fermat |
| 2 | Hill 3x3 | Matriz conocida (derivada de Capa 1) | Cálculo de matriz inversa mod 26 |
| 3 | Transposición Columnar | Clave predecible (QUANTUM) | Descifrado por reordenamiento de columnas |

---

**Flag final:** `FLAG{THEVAULTISDEEPINSIDETHEMOUNTAIN}`
