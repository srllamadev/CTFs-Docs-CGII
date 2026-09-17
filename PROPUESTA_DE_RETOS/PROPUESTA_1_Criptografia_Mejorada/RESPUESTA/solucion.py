import math
import random

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

# ================================================================
# CAPA 1: Common Modulus Attack
# ================================================================
print("=" * 70)
print("CAPA 1: Common Modulus Attack")
print("=" * 70)

n = 100000000006712542916867339521688560103987169326142141852927546739722177792723343
e1, e2 = 17, 23
c1 = 76182663331704153302610677079307837417643545552339609114238076443558029344088636
c2 = 71999570678755885643091057320450206963414272066733379576310185038729015804289977

print(f"\nDatos:")
print(f"n = {n}")
print(f"e1 = {e1}, e2 = {e2}")
print(f"c1 = {c1}")
print(f"c2 = {c2}")

# Paso 1: Verificar que gcd(e1, e2) = 1
g, a, b = extended_gcd(e1, e2)
print(f"\nAlgoritmo de Euclides Extendido:")
print(f"gcd({e1}, {e2}) = {g}")
print(f"Coeficientes de Bezout: a = {a}, b = {b}")
print(f"Verificacion: {a}*{e1} + {b}*{e2} = {a*e1 + b*e2}")

# Paso 2: Calcular el mensaje
if a < 0:
    c1_inv = mod_inverse(c1, n)
    m = (pow(c1_inv, -a, n) * pow(c2, b, n)) % n
else:
    m = (pow(c1, a, n) * pow(c2, b, n)) % n

plaintext1 = m.to_bytes(15, 'big').decode()
print(f"\nMensaje recuperado: {plaintext1}")
print(f"[+] CAPA 1 RESUELTA: {plaintext1}")

# ================================================================
# CAPA 2: LFSR + Berlekamp-Massey
# ================================================================
print("\n" + "=" * 70)
print("CAPA 2: LFSR + Berlekamp-Massey")
print("=" * 70)

keystream_hex = "62324cd47c98929241ee"
cipher_hex = "277e009d2cccdbd11eaddf8fb71c97b69dd1"

# Convertir hex a bits
keystream_bits = []
for h in keystream_hex:
    val = int(h, 16)
    for i in range(3, -1, -1):
        keystream_bits.append((val >> i) & 1)

cipher_bits = []
for h in cipher_hex:
    val = int(h, 16)
    for i in range(3, -1, -1):
        cipher_bits.append((val >> i) & 1)

print(f"\nKeystream ({len(keystream_bits)} bits): {''.join(map(str, keystream_bits[:32]))}...")
print(f"Ciphertext ({len(cipher_bits)} bits): {''.join(map(str, cipher_bits[:32]))}...")

# Paso 1: Berlekamp-Massey para recuperar el polinomio
def berlekamp_massey(bits):
    n = len(bits)
    c = [0] * (n + 1)
    b = [0] * (n + 1)
    c[0] = 1
    b[0] = 1
    l = 0
    m = -1
    
    for i in range(n):
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

L, poly_coeffs = berlekamp_massey(keystream_bits)
print(f"\nBerlekamp-Massey:")
print(f"Longitud del LFSR: {L}")
print(f"Coeficientes del polinomio: {poly_coeffs}")

# Reconstruir taps
LFSR_LEN = L
recovered_taps = []
for i in range(1, len(poly_coeffs)):
    if poly_coeffs[i] == 1:
        recovered_taps.append(LFSR_LEN - i)
print(f"Taps recuperados: {sorted(recovered_taps)}")

# Paso 2: Encontrar seed por fuerza bruta
def lfsr_generate(seed, taps, length):
    state = seed
    keystream = []
    for _ in range(length):
        out = state & 1
        keystream.append(out)
        feedback = 0
        for tap in taps:
            feedback ^= (state >> tap) & 1
        state = (state >> 1) | (feedback << (LFSR_LEN - 1))
    return keystream

print(f"\nBuscando seed (fuerza bruta 2^{LFSR_LEN} = {2**LFSR_LEN} posibilidades)...")
found_seed = None
for seed_candidate in range(2**LFSR_LEN):
    ks = lfsr_generate(seed_candidate, recovered_taps, len(keystream_bits))
    if ks == keystream_bits:
        found_seed = seed_candidate
        break

print(f"Seed encontrado: 0x{found_seed:04X}")

# Paso 3: Generar keystream completo y descifrar
keystream_full = lfsr_generate(found_seed, recovered_taps, len(cipher_bits))
msg_bits = [(c ^ k) for c, k in zip(cipher_bits, keystream_full)]

msg_bytes = []
for i in range(0, len(msg_bits), 8):
    byte = 0
    for j in range(8):
        if i + j < len(msg_bits):
            byte = (byte << 1) | msg_bits[i + j]
    if byte > 0:
        msg_bytes.append(byte)

plaintext2 = bytes(msg_bytes).decode('ascii', errors='ignore')
print(f"\nMensaje descifrado: {plaintext2}")
print(f"[+] CAPA 2 RESUELTA: {plaintext2}")

# ================================================================
# CAPA 3: ECDLP con Baby-step Giant-step
# ================================================================
print("\n" + "=" * 70)
print("CAPA 3: ECDLP (Baby-step Giant-step)")
print("=" * 70)

p_ec = 33554467
a_ec = 2
b_ec = 3
G = (1, 30337350)
P = (30117005, 2695286)
order = 1009

print(f"\nParametros de la curva:")
print(f"E: y^2 = x^3 + {a_ec}x + {b_ec} (mod {p_ec})")
print(f"G = {G}")
print(f"P = {P}")
print(f"Orden = {order}")

# Operaciones de punto
def point_add(P, Q, a, p):
    if P is None: return Q
    if Q is None: return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if P != Q:
        lam = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    else:
        lam = ((3 * x1 * x1 + a) * mod_inverse(2 * y1, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def point_mul(k, P, a, p):
    result = None
    addend = P
    while k:
        if k & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return result

# Paso 1: Baby-step Giant-step
m = math.ceil(math.sqrt(order))
print(f"\nBaby-step Giant-step:")
print(f"m = ceil(sqrt({order})) = {m}")

# Baby steps: i*G para i = 0..m-1
print(f"Calculando {m} baby steps...")
baby_steps = {}
temp = None
for i in range(m):
    baby_steps[temp] = i
    temp = point_add(temp, G, a_ec, p_ec)

# Giant step: m*G
mG = point_mul(m, G, a_ec, p_ec)
print(f"m*G = {mG}")

# Giant steps: P - j*m*G para j = 0..m-1
print(f"Buscando colision en {m} giant steps...")
found_k = None
for j in range(m):
    jmG = point_mul(j, mG, a_ec, p_ec)
    neg_jmG = (jmG[0], (-jmG[1]) % p_ec) if jmG else None
    target = point_add(P, neg_jmG, a_ec, p_ec)
    
    if target in baby_steps:
        i = baby_steps[target]
        found_k = i + j * m
        print(f"\nColision encontrada!")
        print(f"i = {i}, j = {j}")
        print(f"k = i + j*m = {i} + {j}*{m} = {found_k}")
        break

# Verificar
P_check = point_mul(found_k, G, a_ec, p_ec)
print(f"\nVerificacion: {found_k}*G = {P_check}")
print(f"Match: {P_check == P}")

plaintext3 = found_k
print(f"\nClave privada: {plaintext3}")
print(f"[+] CAPA 3 RESUELTA: {plaintext3}")

# ================================================================
# CAPA 4: SPN Cipher
# ================================================================
print("\n" + "=" * 70)
print("CAPA 4: SPN Cipher")
print("=" * 70)

SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
SBOX_INV = [0] * 16
for i in range(16):
    SBOX_INV[SBOX[i]] = i

PERM = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
PERM_INV = [0] * 16
for i in range(16):
    PERM_INV[PERM[i]] = i

print(f"\nS-Box: {SBOX}")
print(f"S-Box inversa: {SBOX_INV}")
print(f"Permutacion: {PERM}")

def spn_decrypt(ciphertext, key, rounds=4):
    state = ciphertext
    # Key mixing final
    round_key = (key >> (rounds * 4)) & 0xFFFF
    state ^= round_key
    
    for r in range(rounds - 1, -1, -1):
        # Key mixing
        round_key = (key >> (r * 4)) & 0xFFFF
        state ^= round_key
        
        # Inverse permutation (excepto ultima ronda inversa)
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

cipher_spn_hex = "cc5248654cc0179fe9441ca694e458a19b04"
cipher_blocks = []
for i in range(0, len(cipher_spn_hex), 4):
    cipher_blocks.append(int(cipher_spn_hex[i:i+4], 16))

print(f"\nCipher blocks: {[f'0x{c:04x}' for c in cipher_blocks]}")

# La clave SPN es priv_key & 0xFFFF
spn_key = plaintext3 & 0xFFFF
print(f"Clave SPN: 0x{spn_key:04X} (derivada de la clave privada de la Capa 3)")

# Descifrar
decrypted_blocks = [spn_decrypt(c, spn_key) for c in cipher_blocks]
decrypted_msg = b''
for block in decrypted_blocks:
    decrypted_msg += bytes([(block >> 8) & 0xFF, block & 0xFF])

flag = decrypted_msg.decode('ascii', errors='ignore').rstrip('\x00')
print(f"\nMensaje descifrado: {flag}")
print(f"[+] CAPA 4 RESUELTA: {flag}")

# ================================================================
# RESULTADO FINAL
# ================================================================
print("\n" + "=" * 70)
print("RESULTADO FINAL")
print("=" * 70)
print(f"\nCapa 1: {plaintext1}")
print(f"Capa 2: {plaintext2}")
print(f"Capa 3: {plaintext3}")
print(f"Capa 4: {flag}")
print(f"\nFLAG: FLAG{{{flag}}}")
print("=" * 70)
