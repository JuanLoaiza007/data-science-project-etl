import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import sys

debug = False

NOTEBOOKS_DIR = "notebooks"
notebooks = [
    "dim_fecha.ipynb",
    "dim_hora.ipynb",
    "dim_cliente.ipynb",
    "dim_mensajero.ipynb",
    "dim_novedad.ipynb",
    "dim_ubicacion.ipynb",
    "hecho_servicio_accumulating_snap.ipynb",
    "hecho_novedad_servicio.ipynb",
    "hecho_realizacion_servicio_dia.ipynb",
    "hecho_realizacion_servicio_hora.ipynb",
]

env_name = "venv"  # Nombre del entorno virtual
success_file = (
    "setup_success"  # Nombre del archivo que indica que setup.py fue ejecutado
)


def main():

    check_success_file()

    print("\nIniciado ejecución de notebooks...")

    # Crea un preprocesador para ejecutar los notebooks
    ep = ExecutePreprocessor(timeout=900, kernel_name="python3")

    # Llama a la función 'process' para ejecutar cada notebook en la lista
    process(notebooks, ep)

    print("\n\n[FIN] Proceso completado, todos los notebooks ejecutados correctamente.")


def process(notebooks, ep):
    for notebook in notebooks:
        notebook_path = os.path.join(NOTEBOOKS_DIR, notebook)
        try:
            print(f"\nEjecutando {notebook_path}...")

            # Abre y lee el notebook actual
            with open(notebook_path) as f:
                nb = nbformat.read(f, as_version=4)

                # Ejecuta el notebook en el directorio para usarlo como contexto de modulos y archivos
                ep.preprocess(nb, {"metadata": {"path": NOTEBOOKS_DIR}})

                if debug:
                    # Sobreescribe el notebook con la salida de los resultados
                    with open(notebook_path, "w", encoding="utf-8") as f_out:
                        nbformat.write(nb, f_out)

                    print(f"{notebook_path} ejecutado y actualizado.")
                    continue

                print(f"{notebook_path} ejecutado.")

        except Exception as e:
            print(
                f"\n[ERROR] {notebook_path}: {e}"
                + "\n[CAUTION] Ha ocurrido un error, hay algunas cosas que podria intentar:"
                + "\n   * Verifique la configuracion de conexion en la carpeta 'config/' de este proyecto."
                + "\n      (!) Verifique sus credenciales de autenticacion y el servidor."
                + "\n      (!) Use una base de datos limpia para el warehouse."
                + "\n   * Verifique que su entorno virtual este activo."
            )
            sys.exit(1)


def check_success_file():
    success_file_path = os.path.join(env_name, success_file)
    if not os.path.exists(success_file_path):
        print(
            "\n[ERROR] Falló la verificacion, no se ha ejecutado previamente 'setup.py'."
            + "\n   * Ejecute 'setup.py' para completar la configuración."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
