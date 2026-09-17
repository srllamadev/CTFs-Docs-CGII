# SOLUCIÓN: PROTOCOLO CERBERUS
## Resolución Paso a Paso

---

## Visión General

El protocolo CERBERUS consiste en 4 capas de cifrado en cascada:

```
[FLAG] → SPN → ECC → LFSR → RSA → [DATOS]
```

El descifrado se realiza en orden inverso: RSA → LFSR → ECC → SPN

---

## CAPA 1: Common Modulus Attack (RSA)

### Análisis del Problema

Tenemos dos cifrados RSA del **mismo mensaje** con el **mismo módulo n** pero diferentes exponentes públicos:

```
n  = 100000000006712542916867339521688560103987169326142141852927546739722177792723343
e1 = 17, e2 = 23
c1 = 76182663331704153302610677079307837417643545552339609114238076443558029344088636
c2 = 71999570678755885643091057320450206963414272066733379576310185038729015804289977
```

### Fundamento Matemático

Si gcd(e1, e2) = 1, entonces por el **Algoritmo de Euclides Extendido** existen a, b tales que:

```
a*e1 + b*e2 = 1
```

Dado que:
- c1 = m^e1 mod n
- c2 = m^e2 mod n

Podemos calcular:
```
c1^a * c2^b = m^(a*e1) * m^(b*e2) = m^(a*e1 + b*e2) = m^1 = m (mod n)
```

### Paso 1: Algoritmo de Euclides Extendido

```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x

g, a, b = extended_gcd(17, 23)
# Resultado: g=1, a=-4, b=3
# Verificación: -4*17 + 3*23 = -68 + 69 = 1 ✓
```

### Paso 2: Recuperar el Mensaje

```python
# Como a = -4 < 0, necesitamos el inverso modular de c1
c1_inv = mod_inverse(c1, n)
m = (pow(c1_inv, 4, n) * pow(c2, 3, n)) % n
plaintext = m.to_bytes(15, 'big').decode()
```

**Resultado:** `LFSR_POLYNOMIAL`

### ¿Por qué esto funciona?

El ataque de Common Modulus explota que cuando el mismo mensaje se cifra con el mismo módulo pero diferentes exponentes coprimos, la relación de Bezout permite recuperar el mensaje sin necesidad de factorizar n.

---

## CAPA 2: LFSR + Berlekamp-Massey

### Análisis del Problema

Tenemos:
- **Keystream** (80 bits): `62324cd47c98929241ee`
- **Ciphertext**: `277e009d2cccdbd11eaddf8fb71c97b69dd1`
- **Longitud del LFSR**: 16 bits

### Fundamento Matemático

El **algoritmo de Berlekamp-Massey** encuentra el LFSR de mínima longitud que genera una secuencia binaria dada. Con 2L bits de keystream, podemos recuperar completamente un LFSR de longitud L.

### Paso 1: Berlekamp-Massey

```python
def berlekamp_massey(bits):
    n = len(bits)
    c = [0] * (n + 1)  # Polinomio de conexión
    b = [0] * (n + 1)  # Polinomio anterior
    c[0] = b[0] = 1
    l = 0  # Longitud actual
    m = -1  # Última actualización
    
    for i in range(n):
        # Calcular discrepancia
        d = bits[i]
        for j in range(1, l + 1):
            d ^= c[j] * bits[i - j]
        
        if d == 1:
            t = c[:]
            for j in range(n + 1):
                if j - (i - m) >= 0 and b[j - (i - m)] == 1:
                    c[j] ^= 1
            if l <= i // 2:
                l = i + 1 - l
                m = i
                b = t[:]
    
    return l, c[:l+1]

L, poly = berlekamp_massey(keystream_bits)
# Resultado: L=16, poly=[1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0]
```

### Paso 2: Recuperar Taps

Del polinomio de conexión extraemos los taps:
```
Polinomio: x^16 + x^12 + x^3 + x + 1
Taps: [4, 13, 15] (posiciones 0-indexed)
```

### Paso 3: Encontrar Seed

Con el polinomio conocido, buscamos el seed por fuerza bruta (2^16 = 65536 posibilidades):

```python
for seed in range(65536):
    ks = lfsr_generate(seed, taps, 80)
    if ks == keystream_bits:
        found_seed = seed
        break
# Resultado: seed = 0x4C46
```

### Paso 4: Descifrar

Generamos el keystream completo y XOR con el ciphertext:

```python
keystream_full = lfsr_generate(seed, taps, len(cipher_bits))
msg_bits = [c ^ k for c, k in zip(cipher_bits, keystream_full)]
```

**Resultado:** `ELLIPTIC_CURVE_KEY`

---

## CAPA 3: ECDLP (Baby-step Giant-step)

### Análisis del Problema

Tenemos una curva elíptica:
```
E: y² = x³ + 2x + 3 (mod 33554467)
G = (1, 30337350)
P = (30117005, 2695286)
Orden = 1009
```

Necesitamos encontrar k tal que P = k*G (problema del logaritmo discreto en curvas elípticas).

### Fundamento Matemático

El algoritmo **Baby-step Giant-step** de Shanks resuelve ECDLP con complejidad O(√n):

1. **Baby steps**: Calcular i*G para i = 0, 1, ..., m-1 donde m = ⌈√n⌉
2. **Giant step**: Calcular m*G
3. **Giant steps**: Para j = 0, 1, ..., m-1, calcular P - j*m*G y buscar colisión en baby steps

Si P - j*m*G = i*G, entonces P = (i + j*m)*G, así k = i + j*m.

### Paso 1: Configuración

```python
m = math.ceil(math.sqrt(1009))  # m = 32
```

### Paso 2: Baby Steps

```python
baby_steps = {}
temp = None  # Punto en el infinito
for i in range(m):
    baby_steps[temp] = i
    temp = point_add(temp, G, a, p)
```

### Paso 3: Giant Steps

```python
mG = point_mul(m, G, a, p)

for j in range(m):
    jmG = point_mul(j, mG, a, p)
    neg_jmG = (jmG[0], (-jmG[1]) % p)
    target = point_add(P, neg_jmG, a, p)
    
    if target in baby_steps:
        i = baby_steps[target]
        k = i + j * m
        break
```

**Resultado:** i=5, j=13, k = 5 + 13*32 = 421

### Paso 4: Verificación

```python
P_check = point_mul(421, G, a, p)
assert P_check == P  # ✓
```

**Resultado:** `421`

---

## CAPA 4: SPN Cipher

### Análisis del Problema

Tenemos un cifrado SPN de 16 bits con:
- **S-Box**: [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
- **Permutación**: [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
- **Rondas**: 4
- **Clave**: 0x01A5 (derivada de la clave privada de Capa 3: 421 & 0xFFFF)
- **Ciphertext**: `cc5248654cc0179fe9441ca694e458a19b04`

### Estructura del SPN

Cada ronda consiste en:
1. **SubBytes**: Sustitución usando S-Box (4 bits por nibble)
2. **Permutation**: Reordenamiento de bits (excepto en la última ronda)
3. **Key Mixing**: XOR con la round key

### Paso 1: Construir S-Box Inversa

```python
SBOX_INV = [0] * 16
for i in range(16):
    SBOX_INV[SBOX[i]] = i
# SBOX_INV = [14, 3, 4, 8, 1, 12, 10, 15, 7, 13, 9, 6, 11, 2, 5, 0]
```

### Paso 2: Construir Permutación Inversa

```python
PERM_INV = [0] * 16
for i in range(16):
    PERM_INV[PERM[i]] = i
# PERM_INV = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
```

### Paso 3: Descifrado SPN

El descifrado aplica las operaciones en orden inverso:

```python
def spn_decrypt(ciphertext, key, rounds=4):
    state = ciphertext
    
    # Key mixing final
    round_key = (key >> (rounds * 4)) & 0xFFFF
    state ^= round_key
    
    for r in range(rounds - 1, -1, -1):
        # Key mixing
        round_key = (key >> (r * 4)) & 0xFFFF
        state ^= round_key
        
        # Inverse permutation
        if r < rounds - 1:
            new_state = 0
            for i in range(16):
                if state & (1 << (15 - i)):
                    new_state |= 1 << (15 - PERM_INV[i])
            state = new_state
        
        # Inverse SubBytes
        new_state = 0
        for i in range(4):
            nibble = (state >> (12 - 4*i)) & 0xF
            new_state |= SBOX_INV[nibble] << (12 - 4*i)
        state = new_state
    
    return state
```

### Paso 4: Descifrar Bloques

```python
cipher_blocks = [0xcc52, 0x4865, 0x4cc0, 0x179f, 0xe944, 0x1ca6, 0x94e4, 0x58a1, 0x9b04]
decrypted = [spn_decrypt(c, 0x01A5) for c in cipher_blocks]
```

**Resultado:** `PRIME_FIELD_GALOIS`

---

## Resultado Final

```
Capa 1: LFSR_POLYNOMIAL
Capa 2: ELLIPTIC_CURVE_KEY
Capa 3: 421
Capa 4: PRIME_FIELD_GALOIS

FLAG: FLAG{PRIME_FIELD_GALOIS}
```

---

## Resumen de Técnicas

| Capa | Cifrado | Vulnerabilidad | Ataque |
|------|---------|----------------|--------|
| 1 | RSA | Mismo módulo, exponentes coprimos | Common Modulus Attack (Bezout) |
| 2 | LFSR | Complejidad lineal baja | Berlekamp-Massey + fuerza bruta |
| 3 | ECC | Orden del subgrupo pequeño | Baby-step Giant-step (Shanks) |
| 4 | SPN | Clave pequeña (16 bits) | Descifrado directo con clave conocida |

---

## ¿Por qué este reto es resistente a IA?

1. **Requiere conocimiento de dominio**: Cada capa requiere conocer algoritmos específicos (Bezout, Berlekamp-Massey, BSGS, SPN)

2. **Dependencias entre capas**: El output de cada capa es necesario para la siguiente, lo que dificulta el razonamiento automatizado

3. **Implementación desde cero**: No hay librerías estándar para todos estos algoritmos, requiere implementación manual

4. **Matemáticas avanzadas**: Aritmética modular, curvas elípticas, álgebra lineal sobre GF(2)

5. **Múltiples pasos de razonamiento**: No es un problema de "una sola llamada" a IA, requiere descomposición y composición

---

**Flag final:** `FLAG{PRIME_FIELD_GALOIS}`
