"""
Práctica de laboratorio: Análisis y visualización de calificaciones
con Pandas y Matplotlib.
Asignatura: Tópicos Avanzados de Programación
Nombre: ______________________   Número de control: ____________
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================================
# EJERCICIO 1. Carga y revisión
# =====================================================================
print("=" * 60)
print("EJERCICIO 1. Carga y revisión")
print("=" * 60)

df = pd.read_csv("calificaciones_isc.csv")

print("\nPrimeras 5 filas:")
print(df.head())

print("\nFilas y columnas:", df.shape)
print(f"Número de filas: {df.shape[0]}  |  Número de columnas: {df.shape[1]}")

print("\nTipo de dato de cada columna:")
print(df.dtypes)

print("\nResumen estadístico de calificacion y asistencias:")
print(df[["calificacion", "asistencias"]].describe())

# El archivo tiene 288 registros y no 24 porque cada alumno aparece en
# varias filas: una por cada materia y por cada unidad.
# Son 24 alumnos x 4 materias x 3 unidades = 288 filas.

# =====================================================================
# EJERCICIO 2. Filtros (sin modificar df)
# =====================================================================
print("\n" + "=" * 60)
print("EJERCICIO 2. Filtros")
print("=" * 60)

solo_grupo_a = df[df["grupo"] == "A"]
menores_70 = df[df["calificacion"] < 70]
bd_grupo_b_80 = df[
    (df["materia"] == "Bases de datos")
    & (df["grupo"] == "B")
    & (df["calificacion"] >= 80)
]

print("Filas del grupo A:", len(solo_grupo_a))
print("Filas con calificación menor a 70:", len(menores_70))
print("Filas de Bases de datos, grupo B, calificación >= 80:", len(bd_grupo_b_80))

# =====================================================================
# EJERCICIO 3. Columna calculada
# =====================================================================
print("\n" + "=" * 60)
print("EJERCICIO 3. Columna situacion")
print("=" * 60)

df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")
print(df[["matricula", "materia", "unidad", "calificacion", "situacion"]].head(10))

# =====================================================================
# EJERCICIO 4. Resúmenes
# =====================================================================
print("\n" + "=" * 60)
print("EJERCICIO 4. Resúmenes")
print("=" * 60)

# a) Promedio por materia
prom_materia = df.groupby("materia")["calificacion"].mean()
print("\nPromedio de calificación por materia:")
print(prom_materia.round(2))

# b) Promedio por grupo y materia
prom_grupo_materia = df.groupby(["grupo", "materia"])["calificacion"].mean()
print("\nPromedio por grupo y materia:")
print(prom_grupo_materia.round(2))

# c) Promedio general de cada alumno, de mayor a menor
#    Se agrupa por matricula y nombre para conservar ambos datos.
prom_alumno = (
    df.groupby(["matricula", "nombre"])["calificacion"]
    .mean()
    .sort_values(ascending=False)
    .reset_index(name="promedio")
)
print("\nPromedio general por alumno (mayor a menor):")
print(prom_alumno.round(2))

# d) Promedio general por unidad (todas las materias juntas)
prom_unidad = df.groupby("unidad")["calificacion"].mean()
print("\nPromedio general por unidad:")
print(prom_unidad.round(2))

# e) Unidades aprobadas y reprobadas
conteo_situacion = df["situacion"].value_counts()
print("\nUnidades aprobadas y reprobadas:")
print(conteo_situacion)

# Exportar promedios por alumno (con matrícula y nombre, sin índice)
prom_alumno.to_csv("promedios_alumnos.csv", index=False)
print("\nArchivo promedios_alumnos.csv generado.")

# =====================================================================
# EJERCICIO 5. Gráficas (primero savefig, después show)
# =====================================================================
print("\n" + "=" * 60)
print("EJERCICIO 5. Gráficas")
print("=" * 60)

# --- Gráfica 1: barras del promedio por materia ---
plt.figure(figsize=(8, 5))
plt.bar(prom_materia.index, prom_materia.values, color="steelblue")
plt.title("Promedio de calificación por materia")
plt.xlabel("Materia")
plt.ylabel("Promedio de calificación")
plt.ylim(0, 100)
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("promedio_materias.png", dpi=150)
plt.show()

# --- Gráfica 2: histograma de calificaciones con línea en 70 ---
plt.figure(figsize=(8, 5))
plt.hist(df["calificacion"], bins=10, color="seagreen", edgecolor="black")
plt.axvline(70, color="red", linestyle="--", linewidth=2, label="Mínimo aprobatorio (70)")
plt.title("Distribución de todas las calificaciones")
plt.xlabel("Calificación")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig("histograma.png", dpi=150)
plt.show()

# --- Gráfica 3: líneas del promedio por unidad, una línea por materia ---
tendencia = df.groupby(["unidad", "materia"])["calificacion"].mean().unstack()

plt.figure(figsize=(8, 5))
for materia in tendencia.columns:
    plt.plot(tendencia.index, tendencia[materia], marker="o", label=materia)
plt.title("Tendencia del promedio por unidad y materia")
plt.xlabel("Unidad")
plt.ylabel("Promedio de calificación")
plt.xticks([1, 2, 3])
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("tendencia_unidades.png", dpi=150)
plt.show()

# =====================================================================
# EJERCICIO 6. Lectura de resultados
# =====================================================================
print("\n" + "=" * 60)
print("EJERCICIO 6. Lectura de resultados")
print("=" * 60)


# La materia con el promedio más bajo fue Matematicas discretas con un promedio de 62.56.
# El promedio general de la unidad 3 (70.50) no es menor que el de la
# unidad 1 (68.52) y la unidad 2 (69.34).
# En total, 11 alumnos quedan con promedio general menor a 70.