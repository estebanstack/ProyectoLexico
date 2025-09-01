# Analizador Léxico de Python usando Autómatas Finitos Deterministas (AFD)

Este proyecto implementa un analizador léxico para un lenguaje tipo *Python*, usando Autómatas Finitos Deterministas diseñados y codificados manualmente en **Python**.  
El enfoque es **POO (Programación Orientada a Objetos)**: cada tipo de token tiene su propio AFD implementado como una clase independiente.  
Finalmente, un Lexer central utiliza estos AFD para recorrer el código fuente y generar la lista de tokens.

---

## ¿Qué hace este analizador?
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

## Características principales
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
- Cadenas con `"` o `'`, soporta escapes simples (`\"` y `\'`)

---

## Cómo ejecutar
1. Crea un archivo de prueba (ej. `ejemplo.py`) en este caso se usó el ejemplo del PDF, ademas se implementan los casos extremos presentados al final:
   ```python
    class Animal(object):
	  makes_noise:bool = False
	
	    def make_noise(self: "Animal") -> object:
		    if(self.makes_noise):
			    print(self.sound())
	
	    def sound(self: "Animal") -> str:
		    return "???"
	
    class Cow(Animal):
	    def __init__(self: "Cow"):
		  
		  self.makes_noise = True
	
	    def sound(self: "Cow") -> str:
		    return "moo"
		
		
    c:Animal = None
    c = Cow()
    c.make_noise()              # Prints "moo"
                    
    numero=80.00.50
    print(numero)

    2.5598055while3!=88¬56.a

2. Ejecuta el analizador:
   ```bash
   python3 lexer_clases.py ejemplo.py
   ```
4. Salida esperada:
   ```
    <class,1,1>
    <id,Animal,1,7>
    <tk_par_izq,1,13>
    <id,object,1,14>
    <tk_par_der,1,20>
    <tk_dos_puntos,1,21>
    <id,makes_noise,2,2>
    <tk_dos_puntos,2,13>
    <id,bool,2,14>
    <tk_asig,2,19>
    <False,2,21>
    <def,4,2>
    <id,make_noise,4,6>
    <tk_par_izq,4,16>
    <id,self,4,17>
    <tk_dos_puntos,4,21>
    <tk_cadena,"Animal",4,23>
    <tk_par_der,4,31>
    <tk_flecha,4,33>
    <id,object,4,36>
    <tk_dos_puntos,4,42>
    <if,5,3>
    <tk_par_izq,5,5>
    <id,self,5,6>
    <tk_punto,5,10>
    <id,makes_noise,5,11>
    <tk_par_der,5,22>
    <tk_dos_puntos,5,23>
    <print,6,4>
    <tk_par_izq,6,9>
    <id,self,6,10>
    <tk_punto,6,14>
    <id,sound,6,15>
    <tk_par_izq,6,20>
    <tk_par_der,6,21>
    <tk_par_der,6,22>
    <def,8,2>
    <id,sound,8,6>
    <tk_par_izq,8,11>
    <id,self,8,12>
    <tk_dos_puntos,8,16>
    <tk_cadena,"Animal",8,18>
    <tk_par_der,8,26>
    <tk_flecha,8,28>
    <id,str,8,31>
    <tk_dos_puntos,8,34>
    <return,9,3>
    <tk_cadena,"???",9,10>
    <class,12,1>
    <id,Cow,12,7>
    <tk_par_izq,12,10>
    <id,Animal,12,11>
    <tk_par_der,12,17>
    <tk_dos_puntos,12,18>
    <def,13,2>
    <id,__init__,13,6>
    <tk_par_izq,13,14>
    <id,self,13,15>
    <tk_dos_puntos,13,19>
    <tk_cadena,"Cow",13,21>
    <tk_par_der,13,26>
    <tk_dos_puntos,13,27>
    <id,self,15,3>
    <tk_punto,15,7>
    <id,makes_noise,15,8>
    <tk_asig,15,20>
    <True,15,22>
    <def,17,2>
    <id,sound,17,6>
    <tk_par_izq,17,11>
    <id,self,17,12>
    <tk_dos_puntos,17,16>
    <tk_cadena,"Cow",17,18>
    <tk_par_der,17,23>
    <tk_flecha,17,25>
    <id,str,17,28>
   <tk_dos_puntos,17,31>
    <return,18,3>
    <tk_cadena,"moo",18,10>
    <id,c,21,1>
    <tk_dos_puntos,21,2>
    <id,Animal,21,3>
    <tk_asig,21,10>
    <None,21,12>
    <id,c,22,1>
    <tk_asig,22,3>
    <id,Cow,22,5>
    <tk_par_izq,22,8>
    <tk_par_der,22,9>
    <id,c,23,1>
    <tk_punto,23,2>
    <id,make_noise,23,3>
    <tk_par_izq,23,13>
    <tk_par_der,23,14>
    <id,numero,24,1>
    <tk_asig,24,7>
    <tk_entero,80,24,8>
    <tk_punto,24,10>
    <tk_entero,00,24,11>
    <tk_punto,24,13>
    <tk_entero,50,24,14>
    <print,25,1>
    <tk_par_izq,25,6>
    <id,numero,25,7>
    <tk_par_der,25,13>
    <tk_entero,2,27,1>
    <tk_punto,27,2>
    <tk_entero,5598055,27,3>
    <id,while3,27,10>
    <tk_distinto,27,16>
    <tk_entero,88,27,18>
    >>> Error léxico(linea:27,posicion:20)

   
   ```

---


---

## ¿Por qué usamos AFD?
Porque un analizador léxico es básicamente un conjunto de autómatas deterministas que reconocen patrones de tokens.  
Cada token (identificador, número, cadena, etc.) tiene su propio AFD, y todos están implementados de forma manual siguiendo la lógica de la función de transición δ.

---

