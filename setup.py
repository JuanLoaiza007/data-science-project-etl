import os
import subprocess
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
        + "\n\nADVERTENCIAS:"
        + "\n1. Recuerde completar los datos de conexión de las bases de datos en config."
        + "\n2. Recuerde activar el entorno virtual desde su editor de código."
    )


def check_requirements_file():
    if not os.path.exists(requirements_file):
        print(f"\nEl archivo {requirements_file} no existe.")
        sys.exit(1)


def create_virtual_env():
    print("\nCreando entorno virtual...")
    subprocess.check_call([sys.executable, "-m", "venv", env_name])


def generate_python_executable():
    return (
        os.path.join(env_name, "Scripts", "python.exe")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "python")
    )


def install_dependencies():
    python_executable = generate_python_executable()
    python_path = (
        subprocess.check_output(
            [python_executable, "-c", "import sys; print(sys.executable)"]
        )
        .decode()
        .strip()
    )

    print(
        f"\nUsando: {python_executable}"
        + "\nRuta completa: {python_path}"
        + "\nInstalando dependencias de Python desde {requirements_file}...\n"
    )
    subprocess.check_call(
        [
            python_executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "setuptools",
        ],
        stderr=subprocess.STDOUT,
    )
    subprocess.check_call(
        [python_executable, "-m", "pip", "install", "-r", requirements_file],
        stderr=subprocess.STDOUT,
    )


def init_postgres_config():
    repo_url = "https://github.com/JuanLoaiza007/config-postgres-yaml-template.git"
    target_dir = "config"

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    try:
        subprocess.check_call(["git", "clone", repo_url, target_dir])
        print(
            f"\nEl archivo de configuración se ha creado en: {os.path.abspath(target_dir)}"
        )
    except subprocess.CalledProcessError as e:
        print(f"\nError al clonar el archivo de configuración: {e}")


if __name__ == "__main__":
    main()
