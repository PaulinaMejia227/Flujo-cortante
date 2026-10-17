"""
=============================================================
ESTRUCTURAS AEROESPACIALES — UNII  |  Clase 3  |  09 Julio 2026
ACTIVIDAD PARA ENTREGA (sube tu solución a NEOLMS)
Tema: Flujo de cortante — booms asimétricos, corte alterno y sección I
=============================================================
INSTRUCCIONES GENERALES
  1. Completa CADA sección marcada con TODO:
  2. No borres los comentarios de orientación.
  3. Guarda el archivo como:  actividad3_TuNombre.py
  4. Súbelo a NEOLMS en la tarea "Actividad 3".

LIBRERÍAS NECESARIAS:  numpy
=============================================================
"""

import numpy as np

# ─────────────────────────────────────────────
# DATOS BASE — NO MODIFICAR
# Sección C idealizada de la práctica
# ─────────────────────────────────────────────
Vy   = 15000.0      # cortante vertical [N]
b, h = 120.0, 240.0 # dimensiones [mm]


# ─────────────────────────────────────────────
# EJERCICIO 1 — Simetría alterada: A3 = A4 = 300 mm^2
# Los booms inferiores duplican su área. La sección deja de ser
# simétrica: primero encuentra el nuevo eje neutro (centroide).
# ─────────────────────────────────────────────
A_arr = np.array([150.0, 150.0, 300.0, 300.0])   # booms 1..4 [mm^2]
y0    = np.array([h/2, h/2, -h/2, -h/2])         # coords y [mm]

# TODO 1a: Centroide  ybar = sum(A*y)/sum(A)
ybar = np.sum(A_arr * y0) / np.sum(A_arr)

# TODO 1b: Coordenadas respecto al nuevo eje neutro y nueva inercia
#          y_rel = y0 - ybar ;  Ix = sum(A * y_rel^2)
y_rel = y0 - ybar
Ix    = np.sum(A_arr * y_rel**2)
print(f"Centroide: ybar = {ybar:.2f} mm")
print(f"Momento de inercia: Ix = {Ix:,.0f} mm^4")
# TODO 1c: Flujos de cortante abiertos (bucle de la práctica):
#          q_i = q_{i-1} - (Vy/Ix) * A_i * y_rel_i   para i = 0,1,2
q_b = np.zeros(3)
# ... tu bucle aquí ...
for i in range(3):
    q_b[i] = (q_b[i-1] if i > 0 else 0) - (Vy / Ix) * A_arr[i] * y_rel[i]
print("Flujos de cortante:", q_b)

print("--- EJERCICIO 1: Booms asimetricos ---")
print(f"  ybar = {ybar:.1f} mm  (esperado: hacia abajo, negativo)")
print(f"  Ix   = {Ix:,.0f} mm^4")
print(f"  q12={q_b[0]:.2f}, q23={q_b[1]:.2f}, q34={q_b[2]:.2f} N/mm")

# TODO 1d: Calcula la posición horizontal del centro de cortadura
#          igual que en la práctica: e = |q12|*b*h / Vy ; x_sc = -e
x_sc = -(abs(q_b[0]) *b * h)/ Vy
print(f"  x_sc = {x_sc:.1f} mm")

# TODO 1e: Responde en un comentario:
#   Los flujos ¿cambiaron respecto al caso simétrico? ¿Por qué el
#   eje neutro se movió hacia los booms más pesados?
#RESPUESTA: Si, los flujos cambiaron porque al aumentar el area de los
# booms inferiores se modifica la distribucion de la seccion.
# El eje neutro se desplaza hacia abajo porque los booms inferiores
# tienen mayor area y aportan mas al calculo del centroide.


# ─────────────────────────────────────────────
# EJERCICIO 2 — Corte en el centro del alma (sección cerrada)
# En la práctica el corte base se hizo en el panel 4-1. Repite el
# cálculo cerrado (sección simétrica original, A = 150 mm^2 todos)
# pero iniciando el corte en el CENTRO del alma (x = 0).
# Debes demostrar que los flujos finales q_s son LOS MISMOS.
# ─────────────────────────────────────────────
print("\n--- EJERCICIO 2: Corte en el alma ---")
A_sim = 150.0
y_sim = np.array([h/2, h/2, -h/2, -h/2])
Ix_s  = np.sum(A_sim * y_sim**2)

# Pista: si el corte está en medio del alma, el recorrido de s
# empieza ahí; el alma queda dividida en dos tramos de h/2.
# Los paneles del recorrido serían: alma_sup(h/2) -> ala_sup(b)
# -> alma_derecha(h)... según tu numeración.
#
# TODO 2a: Calcula los flujos base q_b con tu nuevo recorrido.
q_b2 = np.zeros(5)
ds2 = np.array([h/2, b, h, b, h/2])
q_actual = 0.0
orden_booms = [1, 0, 3, 2]
for i in range(5):
    if i > 0:
        boom_index = orden_booms[i-1]
        y_i = y_sim[boom_index]
        q_actual -= (Vy / Ix_s) * A_sim * y_i
    q_b2[i] = q_actual
print("Longitudes de los tramos:", ds2)
# TODO 2b: Aplica el flujo de cierre  q_0 = -sum(q_b*ds)/sum(ds)
q_02 = -np.sum(q_b2 * ds2) / np.sum(ds2)
q_s2 = q_b2 + q_02
print("Flujos base:", q_b2)
print("Flujo de cierre:", q_02)
print("Flujos finales:", q_s2)
# TODO 2c: Imprime los flujos finales y compáralos con:
q12 = q_s2[1]
q23 = -q_s2[4]
q34 = q_s2[3]
q41 = -q_s2[2]
print(f"q12={q12:.2f}, q23={q23:.2f}, q34={q34:.2f}, q41={q41:.2f} N/mm")
#          q12=0.00, q23=-31.25, q34=0.00, q41=+31.25  (práctica)
# ... tus prints aquí ...

# TODO 2d: Responde en un comentario:
#   ¿Por qué el resultado cerrado NO depende de dónde se hace
#   el corte base?
# RESPUESTA: El resultado final no depende de donde se haga el corte
# base porque el flujo de cierre compensa los cambios que aparecen
# al modificar el punto de inicio. Aunque los flujos base sean
# diferentes, al sumar q_0 obtenemos la misma distribucion final
# de cortante en la seccion cerrada.


# ─────────────────────────────────────────────
# EJERCICIO 3 — Sección en I idealizada
print("\n--- EJERCICIO 3: Seccion I ---")
# 2 alas de ancho b (booms en sus extremos) y un alma central de
# altura h. Por doble simetría, el centro de cortadura debe caer
# EXACTAMENTE en el centroide.
#
#      1 •───────• 2        y = +h/2   (ala superior, booms 1 y 2)
#            │
#            │              (alma central en x = 0)
#      3 •───────• 4        y = -h/2   (ala inferior, booms 3 y 4)
# ─────────────────────────────────────────────
# TODO 3a: Define los booms (área 150 mm^2, x = ±b/2, y = ±h/2),
A_I = 150.0
x_I = np.array([-b/2, b/2, -b/2, b/2])
y_I = np.array([h/2, h/2, -h/2, -h/2])
Ix_I = np.sum(A_I * y_I**2)
print(f"Inercia de la seccion I: {Ix_I:,.0f} mm^4")
#          calcula Ix y los flujos abiertos con un corte en un
#          borde libre del ala superior.
q_I = np.zeros(4)
q_I[0] = -(Vy / Ix_I) * A_I * y_I[0]
print(f"Primer flujo superior: {q_I[0]:.2f} N/mm")
q_I[1] = -(Vy / Ix_I) * A_I * y_I[1]
print(f"Segundo flujo superior: {q_I[1]:.2f} N/mm")
q_alma = q_I[0] + q_I[1]
print(f"Flujo del alma central: {q_alma:.2f} N/mm")
# TODO 3b: Toma momentos respecto al alma y verifica que la
#          resultante pasa por x = 0 (centro de cortadura en el
#          centroide). Imprime x_sc.

q_I[2] = -(Vy / Ix_I) * A_I * y_I[2]
q_I[3] = -(Vy / Ix_I) * A_I * y_I[3]
print(f"Primer flujo inferior: {q_I[2]:.2f} N/mm")
print(f"Segundo flujo inferior: {q_I[3]:.2f} N/mm")
# ... tus prints aquí ...
M_izq = abs(q_I[0]) * (b/2) * (h/2) + abs(q_I[2]) * (b/2) * (h/2)
M_der = abs(q_I[1]) * (b/2) * (h/2) + abs(q_I[3]) * (b/2) * (h/2)
M_total = M_der - M_izq
x_sc_I = M_total / Vy
print(f"Centro de cortadura de la seccion I: {x_sc_I:.2f} mm")
# TODO 3c: Responde en un comentario:
#   ¿Qué propiedad de la sección I hace que el S.C. coincida con
#   el centroide, a diferencia del perfil C?
# RESPUESTA: En la seccion I, la simetria respecto al alma central
# permite que los momentos generados por los flujos de cortante
# de ambos lados se compensen. Por eso el centro de cortadura
# coincide con el centroide, a diferencia del perfil C.
