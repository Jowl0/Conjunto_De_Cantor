import CantorLib
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np

# --- CONFIGURACIÓN ---
ITERACIONES = 17
print(f"Calculando {2**ITERACIONES:,} segmentos en Rust...")

# Traemos los datos una sola vez
datos_crudos = []
for i in range(ITERACIONES + 1):
    inter = CantorLib.conjunto_de_cantor(i)
    y = -i
    # Guardamos como [(x0, x1, y), ...] para filtrar rápido
    datos_crudos.extend([(inicio, fin, y) for inicio, fin in inter])

datos_np = np.array(datos_crudos)

fig, ax = plt.subplots(figsize=(12, 8))
coleccion = LineCollection([], colors='black', antialiased=False)
ax.add_collection(coleccion)

def actualizar_escena(event_ax):
    # 1. Obtener los límites actuales de la "cámara" (zoom)
    xlim = event_ax.get_xlim()
    
    # 2. FILTRADO DINÁMICO: Solo lo que está en escena
    # Filtramos segmentos que tengan alguna parte dentro del rango visible
    mask = (datos_np[:, 1] >= xlim[0]) & (datos_np[:, 0] <= xlim[1])
    visibles = datos_np[mask]
    
    # 3. Re-empaquetar para LineCollection
    nuevos_segs = [[(row[0], row[2]), (row[1], row[2])] for row in visibles]
    
    coleccion.set_segments(nuevos_segs)
    
    # Ajustar grosores dinámicos (opcional, para que no desaparezcan al hacer zoom)
    ax.figure.canvas.draw_idle()

# Conectamos el evento de zoom/pan a nuestra función de optimización
ax.callbacks.connect('xlim_changed', actualizar_escena)

# Estado inicial
ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-ITERACIONES - 1, 1)
ax.axis('off')
plt.title("Conjunto de Cantor - Zoom Optimizado (Clipping Dinámico)")

print("Cámara lista. Prueba la lupa ahora.")
plt.show()