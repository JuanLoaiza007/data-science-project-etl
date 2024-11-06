import os
import sys

env_name = "venv"
requirements_file = "requirements.txt"

py_min = [3, 10]
py_max = [3, 12]


def main():

    check_python_version()

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
    if not create_success_file():
        return

    print(
        "\n\n[FIN] Proceso completado."
        + "\n\nSiguientes pasos:"
        + "\n1. Complete los datos de conexión de las bases de datos en 'config/'"
        + "\n2. Active el entorno virtual desde su editor de código."
        + "\n3. Ejecute el archivo 'main.py' para iniciar el proceso ETL."
    )


def check_python_version():
    python_version = sys.version_info
    python_version_str = f"{python_version.major}.{python_version.minor}"

    if python_version < (py_min[0], py_min[1]) or python_version > (
        py_max[0],
        py_max[1],
    ):
        print(
            f"\n[WARNING] Se recomienda una versión de Python entre {py_min[0]}.{py_min[1]} y {py_max[0]}.{py_max[1]}."
        )
        user_input = input(
            f"\n¿Desea continuar con usando {python_version_str}? (y/n): "
        )

        if user_input.strip().lower() != "y":
            print(
                f"\n[INFO] Proceso abortado. Por favor, usa una versión de Python entre {py_min[0]}.{py_min[1]} y {py_max[0]}.{py_max[1]}."
            )
            sys.exit(1)


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


def create_success_file():
    success_file_path = os.path.join(env_name, "setup_success")
    try:
        with open(success_file_path, "w") as file:
            pass
    except Exception as e:
        print(f"\n[ERROR] Falló la creación del archivo de confirmación: {e}")
        return False
    return True


if __name__ == "__main__":
    main()
