import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

## IMPORTANTE: Este archivo NO DEBE ser ejecutado sin haber ejecutado setup.py.

# Ruta de la carpeta que contiene los notebooks
NOTEBOOKS_DIR = "notebooks"

def main():
    # Lista de notebooks a ejecutar. 
    # Especifica la ruta de cada notebook dentro de la carpeta "notebooks"
    notebooks = [
        #Aqui van los notebooks a ejecutar
        # Ejemplo "dim_fecha.ipynb",
    ]

    # Crea un preprocesador para ejecutar los notebooks
    # Establece un tiempo de espera de 600 segundos y usa el kernel de Python 3
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    
    # Llama a la función 'process' para ejecutar cada notebook en la lista
    process(notebooks, ep)

def process(notebooks, ep):
    # Itera sobre la lista de notebooks
    for notebook in notebooks:
        notebook_path = os.path.join(NOTEBOOKS_DIR, notebook)
        try:
            print(f"Ejecutando {notebook_path}...")

            # Abre y lee el notebook actual
            with open(notebook_path) as f:
                nb = nbformat.read(f, as_version=4)

                # Ejecuta el notebook con el directorio de trabajo configurado como "notebooks"
                # Esto permite que el notebook encuentre módulos y archivos en esta carpeta
                ep.preprocess(nb, {'metadata': {'path': NOTEBOOKS_DIR}})

                # Sobrescribe el notebook con los resultados de la ejecución, conservando el mismo archivo
                with open(notebook_path, "w", encoding="utf-8") as f_out:
                    nbformat.write(nb, f_out)

                print(f"{notebook_path} ejecutado y actualizado.")  # Indica que la ejecución fue exitosa

        except Exception as e:
            # En caso de error, muestra el mensaje de error específico
            print(f"Error al ejecutar {notebook_path}: {e}")

if __name__ == "__main__":
    main()
