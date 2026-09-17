# Documentación de Solución: Reto de Criptografía "PASE PERDIDO =') POR LA TÓXICA XD"

## 1. Información General del Reto
* **Nombre del Reto:** PASE PERDIDO =') POR LA TÓXICA XD
* **Puntos:** 80
* **Descripción:** "Pablito faltó a clases y quiere participar en la 4 Competencia de Seguridad Informática CIDSI, uno de sus docentes le dejo una pista, será que Pablito participa de la Competencia???"
* **Mensaje cifrado:** `494a55574b3354574d565847535a44504c354255535243544a465054454d425347493d3d3d3d3d3d`

## 2. Análisis Inicial
El mensaje es una cadena de caracteres en el rango numérico (0-9) y letras de la "a" a la "f". Indicador de que la primera capa de ofuscación es una codificación **Hexadecimal**.

## 3. Fase de Decodificación a base32

El relleno (padding) extenso al final: El bloque de seis signos iguales **======** Mientras en Base64 utilizan como máximo dos signos igual **==**, Base32 estructura los datos en bloques que frecuentemente requieren 1, 3, 4 o hasta 6 signos igual al final de la cadena para completar la secuencia.

Base32 utiliza un alfabeto compuesto por letras mayúsculas (A-Z) y los números del 2 al 7. 

La cadena no contiene letras minúsculas, símbolos especiales (como + o / que sí usa Base64), ni los números 0, 1, 8 o 9 (excluidos intencionalmente en Base32 para evitar confusiones de lectura con las letras O, I, B y g).

Decodificar de Hexadecimal y luego decodificar de **Base32**.

### Método 1: Uso de CyberChef

1. **From Hex:** Toma la cadena hexadecimal de entrada y la convierte a texto (ASCII). El resultado intermedio obtenido fue una cadena en Base32 (`IJUWK3TWMVXGSZDPL5BUSRCTJFPTEMBSGI======`).
2. **From Base32:** Toma la cadena intermedia y la decodifica utilizando el alfabeto estándar (A-Z2-7=).

**Resultado obtenido:** `Bienvenido_CIDSI_2022`

### Método 2: Uso de herramientas online (dCode)
Se replicó el proceso utilizando la suite de herramientas de dCode:
1. Primero se ingresó la cadena original en el decodificador de código ASCII/Hexadecimal (`https://www.dcode.fr/codigo-ascii`).
2. La salida obtenida se procesó posteriormente en el decodificador de Base32 (`https://www.dcode.fr/base-32-encoding`).
3. El resultado fue idéntico al método anterior: `Bienvenido_CIDSI_2022`.

## 4. Solución Final
* **Texto plano descubierto:** `Bienvenido_CIDSI_2022`
* **Hash MD5 generado (Primera entrega):** `28e043ef6109375dafe8d541f2896bed`

**Flag Final (Formato asumido CIDSI):** `cidsi{28e043ef6109375dafe8d541f2896bed}`