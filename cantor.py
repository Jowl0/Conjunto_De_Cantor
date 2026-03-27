import os
import sys
import time
import subprocess
import shutil
import importlib.util
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

if os.path.exists("CantorLib/Cargo.toml"):
    try:
        subprocess.check_call(
            ["cargo", "build", "--release"], 
            cwd="CantorLib", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
        )
        shutil.copy("CantorLib/target/release/libCantorLib.so", "CantorLib.so")
    except Exception as e:
        if not os.path.exists("CantorLib.so"): sys.exit(1)

ruta_so = os.path.abspath("CantorLib.so")
spec = importlib.util.spec_from_file_location("CantorLib", ruta_so)
CantorLib = importlib.util.module_from_spec(spec)
sys.modules["CantorLib"] = CantorLib
spec.loader.exec_module(CantorLib)

ITERACIONES = int(input('Elige el numero de iteraciones: \n'))

t0 = time.time()
segs_por_nivel = []
for i in range(ITERACIONES + 1):
    inter = CantorLib.conjunto_de_cantor(i)
    segs_por_nivel.append(np.array(inter, dtype=np.float64))

print(f"Calculados {2**(ITERACIONES+1)-1:,} elementos en {time.time() - t0:.3f}s")

fig, ax = plt.subplots(figsize=(12, 8))
coleccion = LineCollection([], colors='black', linewidths=8.0, antialiased=False)
coleccion.set_capstyle('butt')
ax.add_collection(coleccion)

def actualizar_escena(event_ax=None):
    for txt in list(ax.texts):
        txt.remove()

    xlim = ax.get_xlim()
    ancho_vista = xlim[1] - xlim[0]
    
    if ancho_vista <= 0: return
    
    min_dx = ancho_vista / 1920.0 
    
    try:
        j_max = int(math.log(1.0 / min_dx) / math.log(3.0)) + 1
    except ValueError:
        j_max = ITERACIONES

    segs_a_dibujar = []

    for i in range(ITERACIONES + 1):
        k = min(i, j_max, ITERACIONES)
        segs_k = segs_por_nivel[k]
        
        mask = (segs_k[:, 1] >= xlim[0]) & (segs_k[:, 0] <= xlim[1])
        visibles = segs_k[mask]
        
        if len(visibles) > 0:
            n_vis = len(visibles)
            y_val = -i
            
            bloque = np.empty((n_vis, 2, 2))
            bloque[:, 0, 0] = visibles[:, 0]
            bloque[:, 0, 1] = y_val
            bloque[:, 1, 0] = visibles[:, 1]
            bloque[:, 1, 1] = y_val
            
            segs_a_dibujar.append(bloque)
            
            if i <= j_max:
                for x0, x1 in visibles:
                    dx_real = x1 - x0
                    if dx_real > (ancho_vista * 0.15):
                        caja_inicio = dict(boxstyle="round,pad=0.2", facecolor="#f4f8fa", edgecolor="#0055aa", alpha=0.9)
                        caja_fin = dict(boxstyle="round,pad=0.2", facecolor="#faf4f4", edgecolor="#aa0000", alpha=0.9)
                        
                        ax.annotate(f"{x0:.16g}", xy=(x0, y_val), xytext=(5, 18),
                                    textcoords="offset points", ha='left', va='bottom',
                                    fontsize=9, family='monospace', color='#003366',
                                    bbox=caja_inicio, arrowprops=dict(arrowstyle="->", color="#0055aa", shrinkB=4))
                        
                        ax.annotate(f"{x1:.16g}", xy=(x1, y_val), xytext=(-5, -18),
                                    textcoords="offset points", ha='right', va='top',
                                    fontsize=9, family='monospace', color='#660000',
                                    bbox=caja_fin, arrowprops=dict(arrowstyle="->", color="#aa0000", shrinkB=4))
            
    if segs_a_dibujar:
        coleccion.set_segments(np.vstack(segs_a_dibujar))
    else:
        coleccion.set_segments([])

    if event_ax:
        ax.figure.canvas.draw_idle()

ax.callbacks.connect('xlim_changed', actualizar_escena)

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-ITERACIONES - 1, 1)
ax.axis('off')
plt.title(f"Conjunto de Cantor - {ITERACIONES} Iteraciones\n", fontsize=14)
plt.tight_layout()

actualizar_escena()

plt.show()