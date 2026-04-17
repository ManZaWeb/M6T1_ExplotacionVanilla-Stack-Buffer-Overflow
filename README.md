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









