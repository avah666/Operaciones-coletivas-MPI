# Operaciones-coletivas-MPI
[Profesor: Johansell Villalobos Cubillo]
Estudiantes: 
Andrea Arias
Axel Alvarado## 

### Objetivos

- Aplicar operaciones colectivas de MPI (`Bcast`, `Scatter`, `Reduce`).
- Calcular estadísticas globales a partir de datos distribuidos.
- Utilizar buenas prácticas de programación paralela en Python.
- Registrar resultados usando el módulo `logging`.

Estructura del proyecto
.
├── MPI_stats.py           # Código principal con operaciones colectivas
├── latency_MPI.py         # Codigo principal para datos de latencia
├── requirements.txt       # Dependencias Python
└── README.md              # Este documento


Para ejecutar Mpi Stars:
1. Asegurarse de tener MPI instalado en la pc y agregar el path a variables del sistema.
-- Para instalarlo seguir las instrucciones de: https://www.microsoft.com/en-us/download/details.aspx?id=105289
--- Abrir system variables en Windows y agregar a "path"  C:\Program Files\Microsoft MPI\Bin ***ESTO SI ES WINDOWS***
3. En CMD, ejecutar un ejemplo como el siguiente: & "C:\Program Files\Microsoft MPI\Bin\mpiexec.exe" -n 4 python MPI_stats.py 1000000 == para stats
 y & "C:\Program Files\Microsoft MPI\Bin\mpiexec.exe" -n 2 python latency_MPI.py 1000000 == para latencia




