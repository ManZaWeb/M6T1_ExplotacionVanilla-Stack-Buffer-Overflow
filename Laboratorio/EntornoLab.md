# Entorno de laboratorio

Con el objetivo de llevar a cabo la explotación de la vulnerabilidad de forma controlada, es necesario desplegar un entorno de laboratorio.  
En esta sección se describen los pasos necesarios para su instalación y correcta configuración:
## Instalación de máquinas virtuales

Para la creación del entorno de laboratorio, se utilizarán dos máquinas virtuales:

- **Kali Linux**
- **Windows 10**

### Requisitos previos

- Software de virtualización (por ejemplo, VirtualBox o VMware).
- Imagen ISO de Kali Linux.
- Imagen ISO de Windows 10.

### Creación de las máquinas virtuales

1. Crear una nueva máquina virtual para Kali Linux:
   - Tipo: Linux
   - Versión: Debian (64-bit)
   - Asignar al menos 2 GB de RAM y 2 CPUs.
   - Crear un disco duro virtual (mínimo 20 GB).
   - Montar la ISO de Kali Linux e iniciar la instalación.

2. Crear una nueva máquina virtual para Windows 10:
   - Tipo: Microsoft Windows
   - Versión: Windows 10 (64-bit)
   - Asignar al menos 4 GB de RAM.
   - Crear un disco duro virtual (mínimo 40 GB).
   - Montar la ISO de Windows 10 e iniciar la instalación.

### Configuración de red

Para permitir la comunicación entre ambas máquinas:

- Configurar ambas máquinas en la misma red (por ejemplo, **Red interna** o **Adaptador puente**).
- Verificar la conectividad mediante `ping` entre ambas máquinas.

## Despliegue de VulnServer en Windows 10

Con el objetivo de disponer de un servicio vulnerable sobre el que realizar pruebas de explotación, se procederá al despliegue de **VulnServer** en la máquina Windows 10.

### Descarga de VulnServer

1. Descargar VulnServer desde su repositorio https://github.com/stephenbradshaw/vulnserver
2. Copiar el archivo descargado en la máquina virtual Windows 10.

### Ejecución del servidor

1. Abrir una terminal (Símbolo del sistema) con permisos de usuario.
2. Navegar hasta el directorio donde se encuentra VulnServer:
   ```bash
   cd C:\ruta\al\directorio\vulnserver
3.Ejecuar vulnerserver
  vulnserver.exe

## Instalación de Python 3 en Windows 10

Python 3 es una herramienta esencial para el desarrollo de scripts de explotación y automatización durante el laboratorio.

### Descarga

1. Acceder a la página oficial de Python: https://www.python.org/downloads/windows/
2. Descargar el instalador de **Python 3 (Windows x86-64 executable installer)**.

### Instalación

1. Ejecutar el instalador descargado.
2. **IMPORTANTE**: Marcar la casilla:
   - `Add Python to PATH`
3. Seleccionar la opción **Install Now**.
4. Esperar a que finalice el proceso de instalación.

### Verificación

1. Abrir el **Símbolo del sistema (cmd)**.
2. Ejecutar:
   ```bash
   python --version

## Instalación de herramientas en Windows 10

### Immunity Debugger

**Immunity Debugger** es una herramienta fundamental para el análisis de vulnerabilidades en aplicaciones Windows, especialmente en la explotación de desbordamientos de memoria (buffer overflow).

### Descarga

1. Acceder a la página oficial de Immunity Debugger.
2. Descargar la última versión disponible.

### Instalación

1. Ejecutar el instalador (`.exe`) en la máquina Windows 10.
2. Seguir los pasos del asistente de instalación.
3. Mantener la configuración por defecto.

### Configuración inicial

1. Ejecutar Immunity Debugger como administrador.
2. (Opcional) Instalar el plugin **mona.py**:
   - Descargar `mona.py`.
   - Copiar el archivo en la ruta:
     ```
     C:\Program Files (x86)\Immunity Inc\Immunity Debugger\PyCommands\
     ```
3. Configurar el directorio de trabajo de mona:
   - Abrir Immunity Debugger.
   - En la consola inferior, ejecutar:
     ```
     !mona config -set workingfolder c:\mona\%p
     ```

### Verificación

1. Abrir Immunity Debugger.
2. Cargar el ejecutable `vulnserver.exe`:
   - `File -> Open`
3. Comprobar que el programa se carga correctamente y queda en estado de pausa (paused).

### Instalación de IDA Free en Windows 10

**IDA Free** es una herramienta de ingeniería inversa que permite analizar binarios y comprender su funcionamiento interno, siendo especialmente útil en el estudio de vulnerabilidades.

### Descarga

1. Acceder a la página oficial de IDA Free: https://hex-rays.com/ida-free/
2. Descargar la versión gratuita (**IDA Freeware**) para Windows.

### Instalación

1. Ejecutar el instalador descargado.
2. Aceptar los términos de licencia.
3. Seleccionar la ruta de instalación (se puede dejar por defecto).
4. Completar el asistente de instalación.

### Ejecución

1. Ejecutar **IDA Free** desde el acceso directo o el menú de inicio.
2. Abrir un archivo ejecutable:
   - `File -> Open`
   - Seleccionar `vulnserver.exe`
