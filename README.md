# Conjunto de Cantor

Un proyecto que combina Python y Rust para calcular y visualizar el Conjunto de Cantor de forma eficiente. 
El núcleo del cálculo matemático está escrito en Rust usando `pyo3` para integrarse con Python como una biblioteca compartida (`CantorLib`), lo cual mejora el rendimiento cuando se realiza un número muy grande de iteraciones.

> **📖 Nota:** Hay un documento **PDF** (generado a partir de los archivos en la carpeta `Latex/`) que puedes leer para entender a profundidad la teoría matemática y los detalles técnicos del proyecto.

## Requisitos Previos

- **Python 3.8+**
- **Rust / Cargo**: Necesitas la cadena de herramientas de Rust para compilar la biblioteca. Puedes instalarlo usando `rustup` desde [rustup.rs](https://rustup.rs/).

## Instalación

1. Es recomendable crear un entorno virtual de Python:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # En Windows usa: venv\Scripts\activate
   ```

2. Instala las dependencias de Python necesarias:

   ```bash
   pip install -r requirements.txt
   ```

*(Nota: no necesitas compilar manualmente el código de Rust. El script de Python se encargará de ello la primera vez que lo ejecutes).*

## Ejecución

Para iniciar el programa, simplemente ejecuta el archivo principal:

```bash
python cantor.py
```

### ¿Qué ocurre al ejecutarlo?

1. En la **primera ejecución** o si el archivo `CantorLib.so` (o `.pyd`) no existe aún, el archivo `cantor.py` invocará a Cargo internamente (`cargo build --release`) para compilar la biblioteca de Rust a partir del código en la carpeta `CantorLib`.
2. Te pedirá introducir por la terminal el **número de iteraciones** del conjunto de Cantor que deseas calcular. *(Se recomienda probar números pequeños primero, ya que el número de segmentos crece de forma exponencial)*.
3. Se abrirá una ventana interactiva de `matplotlib` mostrando la representación visual de todos los segmentos generados. Puedes hacer zoom y desplazarte por ella dinámicamente.

## Estructura del código

- **`cantor.py`**: Interfaz visual y script de ejecución. Realiza la conexión y carga dinámica de la librería compilada en Rust, a la vez de encargarse de la vista ("View") utilizando `matplotlib` e incorporando interactividad.
- **`CantorLib/`**: Proxecto de librería con Rust.
  - **`Cargo.toml`**: Configuración y dependencias de Rust, que actualmente usa `pyo3` para crear la interfaz C-Python.
  - **`src/lib.rs`**: Es el código base. Exporta la función de cálculo del conjunto (`conjunto_de_cantor`), diseñada para ejecutarse a un bajo nivel con altísimo rendimiento.
- **`requirements.txt`**: Listado de paquetes de Python (`numpy`, `matplotlib`, `maturin`).
