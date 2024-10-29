import os
import subprocess
import sys

env_name = "venv"
requirements_file = "requirements.txt"


def main():
    print(
        "\nIniciando instalación y configuración del proyecto.\nEspere por favor...\n"
    )

    check_requirements_file()
    create_virtual_env()
    install_dependencies()

    print(
        "\n\nProceso completado.\n\nADVERTENCIA: Recuerde activar el entorno virtual desde su editor de código.\n"
    )


def check_requirements_file():
    if not os.path.exists(requirements_file):
        print(f"El archivo {requirements_file} no existe.\n")
        sys.exit(1)


def create_virtual_env():
    print("Creando entorno virtual...\n")
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
        f"Usando: {python_executable}\nRuta completa: {python_path}\nInstalando dependencias de Python desde {requirements_file}...\n"
    )
    subprocess.check_call(
        [python_executable, "-m", "pip", "install", "-r", requirements_file],
        stderr=subprocess.STDOUT,
    )


if __name__ == "__main__":
    main()
