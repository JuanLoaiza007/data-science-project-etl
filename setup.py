import os
import sys

env_name = "venv"
requirements_file = "requirements.txt"


def main():
    print("\nIniciando instalación y configuración del proyecto.\nEspere por favor...")

    check_requirements_file()
    create_virtual_env()
    install_dependencies()
    init_postgres_config()

    print(
        "\n\nProceso completado."
        + "\n\nSiguientes pasos:"
        + "\n   1. Complete los datos de conexión de las bases de datos en `config/`."
        + "\n   2. Active el entorno virtual desde su editor de código."
        + "\n   3. Ejecute el archivo 'main.py' para iniciar el proceso ETL."
    )


def check_requirements_file():
    if not os.path.exists(requirements_file):
        print(f"\nEl archivo {requirements_file} no existe.")
        sys.exit(1)


def create_virtual_env():
    print("\nCreando entorno virtual...")
    os.system(f"{sys.executable} -m venv {env_name}")


def install_dependencies():
    python_executable = generate_python_executable()
    print(
        f"\nUsando: {python_executable}"
        + f"\nInstalando dependencias de Python desde {requirements_file}...\n"
    )
    # Actualización de pip y setuptools
    os.system(f"{python_executable} -m pip install --upgrade pip setuptools")
    # Instalación de requerimientos
    os.system(f"{python_executable} -m pip install -r {requirements_file}")


def generate_python_executable():
    return (
        os.path.join(env_name, "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "python")
    )


def init_postgres_config():
    repo_url = "https://github.com/JuanLoaiza007/config-postgres-yaml-template.git"
    target_dir = "config"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if os.system(f"git clone {repo_url} {target_dir}") == 0:

        # Eliminar el directorio .git para que no sea reconocido como repositorio
        git_dir = os.path.join(target_dir, ".git")

        # Elimina el rastro de git para hacer la carpeta independiente
        if os.path.exists(git_dir):
            if os.name == "nt":
                os.system(f"rmdir /S /Q {git_dir}")
            else:
                os.system(f"rm -rf {git_dir}")
        print(
            f"\nEl archivo de configuración se ha creado en: {os.path.abspath(target_dir)}"
        )
    else:
        print(
            f"\nError al clonar el archivo de configuración. Asegúrate de tener 'git' instalado."
        )


if __name__ == "__main__":
    main()
