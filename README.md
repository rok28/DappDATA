# Resumen de DApp para Mitigación de Ataques DoS, DDoS y Censura de Internet

## Descripción
La DApp propuesta tiene como objetivo mitigar los ataques de denegación de servicio (DoS), denegación de servicio distribuida (DDoS) y la censura de Internet mediante el uso de tecnologías descentralizadas y bibliotecas Python.

## Características principales
1. **Arquitectura descentralizada**: La DApp se basará en una arquitectura descentralizada utilizando tecnologías como blockchain (Ethereum - Ganache, entorno de pruebas para desplegar contratos) para garantizar la resistencia a la censura y la disponibilidad continua de los servicios.

2. **Almacenamiento descentralizado**: La DApp utiliza IPFS como sistema de almacenamiento descentralizado, se establecerá computadora como un nodo de ipfs y se aprovechará dicha conexion para carga y descarga de ficheros.

3. **Filtrado y detección de ataques**: Se implementarán algoritmos y bibliotecas Python especializadas en la detección y filtrado de tráfico malicioso. Estas bibliotecas analizarán los patrones de tráfico para identificar posibles ataques DoS y DDoS.

4. **Red de nodos**: Se establece el pc como un nodo publico en la red publica de IPFS.Los nodos estarán interconectados y utilizarán técnicas criptográficas para proteger la privacidad y la integridad de los datos.

6. **Bibliotecas Python**: Para implementar las medidas de mitigación, se utilizarán las siguientes bibliotecas Python:
   - `Flask`  para el desarrollo del backend de la aplicación y la gestión de solicitudes HTTP.
   - `limiter` para limitar la velocidad de las solicitudes entrantes y prevenir la sobrecarga del servidor.

## Beneficios esperados
- Mayor resistencia a los ataques DoS y DDoS, lo que garantizará una mayor disponibilidad y rendimiento de la aplicación.
- Mayor resiliencia frente a la censura de Internet, permitiendo el acceso a la información incluso en entornos restringidos.
- Mantenimiento de la integridad y la privacidad de los datos mediante técnicas criptográficas y la descentralización de la red de nodos.
