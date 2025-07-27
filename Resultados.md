
# Resultados – Tarea 3: Comunicación Colectiva y Medición de Latencia

**Curso:** Computación Paralela  
**Profesor:** Johansell Villalobos Cubillo  
**Estudiante:** [Tu nombre]  
**Fecha:** [Fecha actual]

---

## 🧩 Parte A – Operaciones Colectivas con MPI

### 🖥️ Ejecución

```bash
mpiexec -n 4 python MPI_stats.py 1000000
```

### 📸 Evidencia de ejecución

![Resultados Parte A](ecdd1d55-2183-4167-bfa6-125a10a506fb.png)

### 📊 Análisis

- El mínimo fue 0.00 y el máximo 100.00, como se espera en una distribución uniforme [0, 100].
- El promedio de 50.02 también confirma la correcta agregación global con `MPI_Reduce`.

---

## ⏱ Parte B – Medición de Latencia Punto a Punto

### 🖥️ Ejecución

```bash
mpiexec -n 2 python latency_MPI.py 1000000
```

### 📸 Evidencia de ejecución

![Resultados Parte B](d0d02136-6518-4248-8cb3-8d8435376d94.png)

### 📊 Análisis

- La latencia de ida y vuelta fue de 2.05 µs, estimando una latencia de ida de 1.02 µs.
- Esto indica una comunicación extremadamente rápida en entorno local.

---

## 💡 Reflexión Final

- Las operaciones colectivas permiten simplificar el análisis paralelo.
- La latencia punto a punto es muy baja en entornos locales, pero su medición es clave para aplicaciones distribuidas.
- La implementación orientada a objetos con `logging` facilita la escalabilidad y depuración del código.
