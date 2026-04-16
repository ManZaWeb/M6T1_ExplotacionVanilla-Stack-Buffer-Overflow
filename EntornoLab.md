# Entorno de laboratorio

Con el objetivo de llevar a cabo la explotación de la vulnerabilidad de forma controlada, es necesario desplegar un entorno de laboratorio.  
En esta sección se describen los pasos necesarios para su instalación y correcta configuración:
## Instalación de máquinas virtuales

Para la creación del entorno de laboratorio, se utilizarán dos máquinas virtuales:

- **Kali Linux**: utilizada como máquina atacante.
- **Windows 10**: utilizada como máquina víctima.

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
