import math

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

print("=" * 60)
print("SOLUCION: OPERACION ESPEJO ROJO")
print("=" * 60)

# ===== CAPA 1: RSA con ataque de Fermat =====
print("\n[CAPA 1] RSA - Ataque de Fermat (primos cercanos)")
print("-" * 60)
n = 1000000000000000000000000000310000000000000000000000000020889
e = 65537
c = 124362460198726234541394411860289841086379638401675728329293

p, q = fermat_factor(n)
print(f"  Factorizacion de n:")
print(f"  p = {p}")
print(f"  q = {q}")
print(f"  Verificacion: p*q == n -> {p*q == n}")

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)
m = pow(c, d, n)
plaintext1 = m.to_bytes(14, 'big').decode()
print(f"\n  Descifrado RSA: {plaintext1}")

# ===== CAPA 3: Transposicion (primero para obtener Hill cipher) =====
print("\n[CAPA 3] Transposicion Columnar - Clave: QUANTUM")
print("-" * 60)
final_cipher = "BZPNANBTKXYXTJNFMKCXDKPCNEDQHLXVPKX"
hill_cipher = columnar_decrypt(final_cipher, "QUANTUM")
print(f"  Ciphertext final: {final_cipher}")
print(f"  Descifrado:       {hill_cipher}")

# ===== CAPA 2: Hill =====
print("\n[CAPA 2] Cifrado Hill 3x3 - Matriz inversa mod 26")
print("-" * 60)
M = [[2, 1, 3], [5, 7, 4], [9, 2, 6]]
det = mat_det3(M)
print(f"  Matriz M = {M}")
print(f"  det(M) mod 26 = {det}")
print(f"  gcd(det, 26) = {math.gcd(det, 26)}")

M_inv = mat_inverse_mod26(M)
print(f"  M_inv = {M_inv}")

cipher_nums = [ord(ch) - 65 for ch in hill_cipher]
plaintext_nums = []
for i in range(0, len(cipher_nums), 3):
    block = [[cipher_nums[i]], [cipher_nums[i+1]], [cipher_nums[i+2]]]
    result = mat_mul(M_inv, block)
    for row in result:
        plaintext_nums.append(row[0])

plaintext2 = ''.join([chr(n + 65) for n in plaintext_nums])
print(f"\n  Hill cipher: {hill_cipher}")
print(f"  Descifrado:  {plaintext2}")

# ===== FLAG =====
flag = plaintext2.rstrip('A')
print("\n" + "=" * 60)
print(f"  FLAG: {{{flag}}}")
print("=" * 60)
