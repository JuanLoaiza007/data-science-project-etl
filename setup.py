import os
import sys

env_name = "venv"
requirements_file = "requirements.txt"


def main():
    print("\nIniciando instalación y configuración del proyecto.\nEspere por favor...")

    if not check_requirements_file():
        return
    if not create_virtual_env():
        return
    if not update_pip_and_setuptools():
        return
    if not install_dependencies():
        return
    if not init_postgres_config():
        return

    print(
        "\n\n[FIN] Proceso completado."
        + "\n\nSiguientes pasos:"
        + "\n1. Complete los datos de conexión de las bases de datos en 'config/'"
        + "\n2. Active el entorno virtual desde su editor de código."
        + "\n3. Ejecute el archivo 'main.py' para iniciar el proceso ETL."
    )


def check_requirements_file():
    if not os.path.exists(requirements_file):
        print(f"\n[ERROR] El archivo {requirements_file} no existe.")
        return False
    return True


def create_virtual_env():
    print("\nCreando entorno virtual...")
    if os.system(f"{sys.executable} -m venv {env_name}") != 0:
        print("\n[ERROR] Falló la creación del entorno virtual.")
        return False
    return True


def generate_python_executable():
    return (
        os.path.join(env_name, "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "python")
    )


def update_pip_and_setuptools():
    python_executable = generate_python_executable()
    print(f"\nActualizando pip y setuptools en el entorno virtual...")
    if (
        os.system(f"{python_executable} -m ensurepip --upgrade") != 0
        or os.system(f"{python_executable} -m pip install --upgrade setuptools") != 0
    ):
        print("\n[ERROR] Falló la actualización de pip y setuptools.")
        return False
    return True


def install_dependencies():
    # Flags
    use_cache = True
    use_binary = True

    cache = "--no-cache-dir" if not use_cache else ""
    binary = "--only-binary :all:" if use_binary else ""

    python_executable = generate_python_executable()
    print(
        f"\nUsando: {python_executable}"
        + f"\nInstalando dependencias de Python desde {requirements_file}...\n"
    )

    if (
        os.system(
            f"{python_executable} -m pip install {cache} {binary} -r {requirements_file}"
        )
        != 0
    ):
        print("\n[ERROR] Falló la instalación de dependencias.")
        return False
    return True


def init_postgres_config():
    repo_url = "https://github.com/JuanLoaiza007/config-postgres-yaml-template.git"
    target_dir = "config"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if os.system(f"git clone {repo_url} {target_dir}") != 0:
        print(
            "\n[ERROR] Falló la clonación del archivo de configuración. Asegúrate de tener 'git' instalado."
        )
        return False

    git_dir = os.path.join(target_dir, ".git")
    if os.path.exists(git_dir):
        if os.name == "nt":
            os.system(f"rmdir /S /Q {git_dir}")
        else:
            os.system(f"rm -rf {git_dir}")
    print(
        f"\nEl archivo de configuración se ha creado en: {os.path.abspath(target_dir)}"
    )
    return True


if __name__ == "__main__":
    main()
