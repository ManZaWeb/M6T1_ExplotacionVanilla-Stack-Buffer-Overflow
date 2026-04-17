# M6T1_ExplotacionVanilla-Stack-Buffer-Overflow
En esta tarea explotaremos una vulnerabilidad tipo Vanilla Stack Buffer Overflow, para continuar con la actividad se debe haber configurado un entorno de laboratiorio, podeis seguir la guia incluida en este repositorio.

## Ejecución Vulnserver

Nos posicionamos en el directorio indicado y ejecutamos:

````bash
vulnserver.exe
````

<img width="1479" height="417" alt="image" src="https://github.com/user-attachments/assets/21ccfd29-e783-47cc-9dea-05c3019d231e" />

Si todo es correcto, aparecerá un mensaje en la consola indicando que el servidor está en ejecución.

<img width="1304" height="248" alt="image" src="https://github.com/user-attachments/assets/8050c03a-878f-4a3d-a83d-aaedcbb6fa67" />


## Comprobación de la conexión

Desde nuestra máquina Kali, comprobaremos la conectividad con el servicio **VulnServer** utilizando Netcat.

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

### Preparación del entorno

Para llevar a cabo el fuzzing, se prepara el siguiente entorno:

### Máquina víctima (Windows 10)

1. Levantar **Vulnserver**.
2. Abrir **Immunity Debugger** con privilegios de administrador.
3. Cargar el ejecutable:
```File → Attach → vulnserver.exe```
4. Clickar en el botón de play

De esta forma, VulnServer queda en ejecución y monitorizado por el debugger.

<img width="1919" height="1028" alt="image" src="https://github.com/user-attachments/assets/f0d496ca-36f1-43a4-b54f-0f969083727f" />


### Máquina atacante (Kali Linux)

Se verifica la conectividad con el servicio:

```bash
nc 192.168.1.136 9999
```
Si el servidor responde con un banner, la conexión es correcta.

### Procedimiento

Vamos a utilizar el script Python3Fuzzing.py, proporcionado por TheMalwareGuardian, este envía peticiones al comando TRUN incrementando progresivamente el tamaño del buffer.

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


Position found at offset 2006

Esto confirma que:

El desbordamiento de buffer alcanza el registro EIP en el byte 2006.










