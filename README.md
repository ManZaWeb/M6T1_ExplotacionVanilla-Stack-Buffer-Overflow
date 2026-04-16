# M6T1_ExplotacionVanilla-Stack-Buffer-Overflow
En esta tarea explotaremos una vulnerabilidad tipo Vanilla Stack Buffer Overflow, para continuar con la actividad se debe haber configurado un entorno de laboratiorio, podeis seguir la guia incluida en este repositorio.

## Ejecución Vulnserver

Nos posicionamos en el directorio indicado y ejecutamos:

````bash
vulnserver.exe
````

<img width="1479" height="417" alt="image" src="https://github.com/user-attachments/assets/21ccfd29-e783-47cc-9dea-05c3019d231e" />

Si todo esta correcto aparecera el siguiente mensaje en la consola:

<img width="1304" height="248" alt="image" src="https://github.com/user-attachments/assets/8050c03a-878f-4a3d-a83d-aaedcbb6fa67" />


## Comprobación de conexión

### Comprobación de conexión

Desde nuestra máquina Kali, comprobaremos la conectividad con el servicio **VulnServer** utilizando Netcat.

#### Obtención de la dirección IP

En primer lugar, necesitamos conocer la dirección IP de la máquina Windows 10. Para ello, ejecutamos el siguiente comando:

```bash
ipconfig
````

<img width="1169" height="395" alt="image" src="https://github.com/user-attachments/assets/4522f50c-26b3-4fb0-9942-f55597c5a056" />

En este caso, la dirección IP asignada es: 192.168.1.136

####Conexión al servicio

Desde Kali Linux, establecemos una conexión con VulnServer mediante Netcat:

```bash
nc 192.168.1.136 9999
````

<img width="1718" height="225" alt="image" src="https://github.com/user-attachments/assets/a741cb07-eff7-44b3-b055-510cf7b6d2a1" />






