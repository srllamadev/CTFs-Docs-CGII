# PROTOCOLO CERBERUS
## Protocolo de Comunicación Cuádruple

**Nivel:** Experto | **Categoría:** Criptografía Avanzada | **Puntos:** 1000

---

## Contexto

Una organización de inteligencia ha interceptado un protocolo de comunicación de cuatro capas utilizado por una célula criptográfica de élite. El protocolo, denominado "CERBERUS", utiliza una cascada de algoritmos donde cada capa alimenta a la siguiente.

Nuestros criptoanalistas han logrado extraer los datos interceptados, pero se enfrentan a un desafío sin precedentes: cada capa requiere un ataque especializado diferente, y la salida de cada capa es esencial para descifrar la siguiente.

---

## Arquitectura del Protocolo

```
[FLAG] → [CAPA 4: SPN] → [CAPA 3: ECC] → [CAPA 2: LFSR] → [CAPA 1: RSA] → [DATOS PÚBLICOS]
```

El cifrado se aplica en orden: Capa 1 → Capa 2 → Capa 3 → Capa 4
El descifrado debe hacerse en orden inverso: Capa 4 → Capa 3 → Capa 2 → Capa 1

---

## Datos Interceptados

### CAPA 1 - RSA de Clave Pública Múltiple

Se interceptaron dos cifrados RSA del **mismo mensaje** usando la **misma clave pública n** pero diferentes exponentes públicos:

```
n  = 100000000006712542916867339521688560103987169326142141852927546739722177792723343
e1 = 17
e2 = 23

c1 = 76182663331704153302610677079307837417643545552339609114238076443558029344088636
c2 = 71999570678755885643091057320450206963414272066733379576310185038729015804289977
```

**Nota del analista:** "El mismo mensaje fue cifrado dos veces con el mismo módulo pero diferentes exponentes. Esto debería ser explotable..."

### CAPA 2 - Cifrado de Flujo

El plaintext de la Capa 1 revela que se utilizó un LFSR (Registro de Retroalimentación con Desplazamiento Lineal) para generar un keystream que cifró el mensaje de la Capa 3 mediante XOR.

**Keystream interceptado (80 bits):**
```
62324cd47c98929241ee
```

**Ciphertext de la Capa 3:**
```
277e009d2cccdbd11eaddf8fb71c97b69dd1
```

**Nota del analista:** "El LFSR tiene longitud 16. Con suficiente keystream, deberíamos poder recuperar el polinomio de retroalimentación y el estado inicial..."

### CAPA 3 - Criptografía de Curva Elíptica

El plaintext de la Capa 2 indica que se utilizó una curva elíptica sobre un campo primo para el intercambio de claves.

**Parámetros de la curva:**
```
E: y² = x³ + 2x + 3 (mod p)
p = 33554467

Punto base G = (1, 30337350)
Clave pública P = (30117005, 2695286)
Orden del subgrupo = 1009
```

**Nota del analista:** "La clave privada es un entero k tal que P = k*G. El orden del subgrupo es pequeño, lo que podría hacer factible un ataque de logaritmo discreto..."

### CAPA 4 - Cifrado de Bloque SPN

El plaintext de la Capa 3 (la clave privada de la curva) se utiliza como clave para un cifrado de bloque SPN (Substitution-Permutation Network) de 16 bits.

**Parámetros del SPN:**
```
S-Box (4 bits): [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
Permutación:    [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
Rondas: 4
```

**Ciphertext del flag:**
```
cc5248654cc0179fe9441ca694e458a19b04
```

**Nota del analista:** "El SPN usa bloques de 16 bits. La clave se deriva de la clave privada de la Capa 3 tomando los 16 bits menos significativos..."

---

## Objetivo

Recuperar el flag original cifrado en la Capa 4.

**Formato de flag:** `FLAG{mensaje_en_mayusculas_con_guiones_bajos}`

---

## Restricciones

- No se permite el uso de herramientas automatizadas de cracking
- Debe documentar cada paso del proceso de descifrado
- La solución debe incluir el código utilizado para cada capa
- El uso de IA está permitido, pero el problema está diseñado para resistir soluciones automatizadas

---

## Notas Técnicas

- **Capa 1:** Investiga el "Common Modulus Attack" para RSA
- **Capa 2:** El algoritmo de Berlekamp-Massey puede recuperar el polinomio del LFSR
- **Capa 3:** El problema del logaritmo discreto en curvas elípticas (ECDLP) puede ser vulnerable cuando el orden del subgrupo es pequeño
- **Capa 4:** El SPN es un cifrado de bloque simple; la clave es pequeña (16 bits)

---

**Buena suerte, criptoanalista. El tiempo es esencial.**
