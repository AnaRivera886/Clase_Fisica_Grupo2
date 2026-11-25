"""
modelo_termico.py — Modelo térmico de primer orden de un procesador. ¡SIMULACIÓN!

Modelo (ley de enfriamiento de Newton + balance de energía):

    C · dT/dt = P(t) - (T - T_amb) / R

    T      temperatura del chip                       [°C] (o K: solo importan diferencias)
    T_amb  temperatura ambiente                       [°C]
    P(t)   potencia disipada por el chip              [W]
    R      resistencia térmica chip -> ambiente       [K/W]  (disipador + ventilador)
    C      capacidad térmica (masa · calor específico) [J/K]
    τ = R·C  constante de tiempo                      [s]

Estado estacionario: T_final = T_amb + P · R
Respuesta a un escalón de potencia: T(t) = T_final + (T_0 - T_final)·e^(-t/τ)

Los parámetros por defecto son ILUSTRATIVOS (orden de magnitud de un portátil),
no medidos. No use esta curva como si fuera un resultado experimental.

Uso:
    python modelo_termico.py                              # escalón 5 W -> 25 W -> 5 W
    python modelo_termico.py --R 1.2 --C 30 --p_alta 35   # explorar parámetros
"""
import argparse

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

p = argparse.ArgumentParser()
p.add_argument("--t_amb", type=float, default=25.0, help="°C")
p.add_argument("--R", type=float, default=2.0, help="resistencia térmica K/W")
p.add_argument("--C", type=float, default=15.0, help="capacidad térmica J/K")
p.add_argument("--p_baja", type=float, default=5.0, help="potencia en reposo W")
p.add_argument("--p_alta", type=float, default=25.0, help="potencia bajo carga W")
p.add_argument("--inicio", type=float, default=30.0, help="s en que inicia la carga")
p.add_argument("--fin", type=float, default=150.0, help="s en que termina la carga")
p.add_argument("--total", type=float, default=300.0, help="s simulados")
p.add_argument("--salida", default="modelo_termico_SIMULADO.png")
a = p.parse_args()

dt = 0.1
T = a.t_amb + a.p_baja * a.R  # se parte del equilibrio en reposo
tiempos, temps, potencias = [], [], []
energia = 0.0
t = 0.0
while t <= a.total:
    P = a.p_alta if a.inicio <= t < a.fin else a.p_baja
    T += dt * (P - (T - a.t_amb) / a.R) / a.C   # método de Euler
    energia += P * dt
    tiempos.append(t); temps.append(T); potencias.append(P)
    t += dt

tau = a.R * a.C
print("SIMULACIÓN (parámetros ilustrativos, no medidos)")
print(f"τ = R·C = {a.R} K/W · {a.C} J/K = {tau:.1f} s   -> ~63 % del cambio en τ, ~95 % en 3τ = {3*tau:.0f} s")
print(f"Equilibrio en reposo: {a.t_amb + a.p_baja * a.R:.1f} °C · bajo carga: {a.t_amb + a.p_alta * a.R:.1f} °C")
print(f"Temperatura máxima alcanzada: {max(temps):.1f} °C")
print(f"Energía total disipada: {energia:.0f} J = {energia / 3600:.3f} Wh")

if plt:
    # Dos paneles con eje de tiempo compartido (nunca doble eje y)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5.5), sharex=True, height_ratios=[2, 1])
    ax1.plot(tiempos, temps, color="#eb6834", lw=2)
    ax1.set_ylabel("Temperatura θ [°C]")
    ax1.set_title(f"Modelo térmico de primer orden (τ = {tau:.0f} s) — DATOS SIMULADOS")
    ax2.step(tiempos, potencias, where="post", color="#2a78d6", lw=2)
    ax2.set_ylabel("Potencia P [W]"); ax2.set_xlabel("Tiempo t [s]")
    for ax in (ax1, ax2):
        ax.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(a.salida, dpi=150)
    print(f"Gráfico: {a.salida}")
