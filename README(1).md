# Analizador Léxico con Autómatas Finitos Deterministas (AFD)

Este proyecto implementa un **analizador léxico** para un lenguaje tipo *Python*, usando **Autómatas Finitos Deterministas (DFA)** diseñados y codificados manualmente en **Python**.  
El enfoque es **POO (Programación Orientada a Objetos)**: cada tipo de token tiene su propio AFD implementado como una clase independiente.  
Finalmente, un **Lexer** central utiliza estos AFD para recorrer el código fuente y generar la lista de tokens.

---

## ✅ ¿Qué hace este analizador?
- Lee un archivo de código fuente (ej. `ejemplo.py`).
- Reconoce y emite tokens en el formato solicitado:
  - **Palabras reservadas:** `<palabra,fila,columna>`
  - **Identificadores:** `<id,lexema,fila,columna>`
  - **Enteros:** `<tk_entero,valor,fila,columna>`
  - **Cadenas:** `<tk_cadena,"texto",fila,columna>`
  - **Operadores y símbolos:** `<tk_nombre,fila,columna>`
- Ignora **espacios** y **comentarios**.
- Aplica el **principio de subcadena más larga** (ej. `!=` antes que `!`).
- Muestra un **error léxico** y detiene el análisis al primer caracter inválido:
  ```
  >>> Error léxico(linea:X,posicion:Y)
  ```

---

## ✅ Características principales
✔ **AFDs implementados como clases**:
- `AFDIdentificador` → Identificadores y palabras reservadas.
- `AFDEntero` → Números enteros (con signo opcional).
- `AFDCadena` → Literales de cadena (`"` o `'`).
- `AFDOperador` → Operadores simples y dobles (`==`, `!=`, `<=`, `>=`, `->`, etc.).

✔ **Lexer modular**:
- Tiene una lista de AFDs y los ejecuta en orden de prioridad.
- Si un AFD reconoce el token, lo emite y avanza.
- Si ninguno lo reconoce, genera error léxico.

✔ **Soporte para casos especiales**:
- Punto `.` tokenizado aparte (ej. `90.00.50` → `90`, `.`, `00`, `.`, `50`).
- Comentarios con `#` ignorados.
- Cadenas con `"` o `'`, soporta escapes simples (`\"` y `\'`).

---

## ✅ Requisitos
- **Python 3.x** (probado en 3.8+)
- No requiere librerías externas.

---

## ✅ Estructura del proyecto
```
📂 proyecto-lexer
 ├── lexer_clases.py       # Analizador léxico implementado con POO
 ├── README.md             # Este archivo
 ├── ejemplo.py            # Ejemplo de código para probar el lexer
```

---

## ✅ Cómo ejecutar
1. Clona el repositorio o descarga los archivos.
2. Crea un archivo de prueba (ej. `ejemplo.py`):
   ```python
   class Animal:
       def __init__(self, nombre):
           self.nombre = nombre
   ```
3. Ejecuta el analizador:
   ```bash
   python3 lexer_clases.py ejemplo.py
   ```
4. Salida esperada:
   ```
   <class,1,1>
   <id,Animal,1,7>
   <tk_dos_puntos,1,13>
   <def,2,5>
   ...
   ```

---

## ✅ Ejemplo con error léxico
Archivo:
```
2.5598055while3!=88¬56.a
```
Salida:
```
<tk_entero,2,1,1>
<tk_punto,1,2>
<tk_entero,5598055,1,3>
<id,while3,1,10>
<tk_distinto,1,16>
<tk_entero,88,1,18>
>>> Error léxico(linea:1,posicion:20)
```

---

## ✅ ¿Por qué usamos AFD?
Porque un **analizador léxico** es básicamente un conjunto de **autómatas deterministas** que reconocen patrones de tokens.  
Cada token (identificador, número, cadena, etc.) tiene su **propio AFD**, y todos están implementados de forma manual siguiendo la lógica de la función de transición δ.

---

## ✅ Mejoras posibles
- Soporte para **floats** (números con punto decimal como un solo token).
- Soporte para **cadenas multilínea** y triple comillas.
- Validación más avanzada de escapes en cadenas.
- Generación de **archivo de salida** automático en vez de imprimir en consola.

---

## ✅ Autor
Proyecto desarrollado como parte de la materia **Teoría de la Computación** / **Compiladores** (5° semestre).  
**Autor:** *[Tu Nombre]*  
**Lenguaje:** Python  
**Tema:** Análisis léxico con Autómatas Finitos Deterministas.
