import os
import shutil
from PIL import Image
from webbrowser import get
from textwrap import dedent
from datetime import datetime


# Função para buscar e validar existencia da pasta inserida pelo usuário
def get_path(path: str) -> str:
    while not os.path.exists(path):
        print(f"❌ Não foi possível encontrar a pasta: '{path}'")

        verify_create_path = input("Deseja criar a pasta? (s/n): ").strip().lower()
        if verify_create_path == "s":
            os.makedirs(path, exist_ok=True)
            print(f"📁 Pasta criada com sucesso: '{path}'")
            break  # Sai do loop

        verify_new_get = input("Deseja tentar novamente? (s/n): ").strip().lower()
        if verify_new_get != "s":
            print("⚠️ Nenhuma pasta válida informada. Operação cancelada.")
            return ""  # Retorna string vazia encerrar programa

        path = input("Insira a pasta novamente: ").strip()

    print(f"✅ Pasta encontrada com sucesso: '{path}'")
    return path


# Função para copiar arquivos de uma pasta para outra
def copy_files(path_origin: str, path_destiny: str):
    if not path_origin or not path_destiny:
        print(
            f"\n⚠️ As pastas inseridas são invalidas: path_origin='{path_origin}' e path_destiny='{path_destiny}'"
        )

    if not os.path.exists(path_origin):
        print(f"❌ Não foi possível encontrar a pasta de origem: '{path_origin}'")
        return ""

    if not os.path.exists(path_destiny):
        print(f"❌ Não foi possível encontrar a pasta de destino: '{path_destiny}'")
        return ""

    shutil.copytree(path_origin, path_destiny, dirs_exist_ok=True)
    print("✅ Arquivo movido com sucesso!")


# Função para conver arquivos para .png, .webp ou tiff
def convert_files(source_path: str, file_type: str):
    os.makedirs(source_path, exist_ok=True)

    for filename in os.listdir(source_path):
        if filename.lower().endswith((".webp", ".jpeg", ".jpg", ".tiff", ".png")):
            file_path = os.path.join(source_path, filename)
            img = Image.open(file_path)  # Abre a imagem

            new_filename = os.path.splitext(filename)[0] + f".{file_type.lower()}"
            new_path = os.path.join(source_path, new_filename)

            img.save(new_path, file_type.upper())
            img.close()
            print(f"✅ Convertido: {filename} ➝ {new_filename}")

            os.remove(file_path)
            print("✅ Arquivo convertido com sucesso!")
        else:
            print(f"⚠️ Arquivo não pode ser convertido: '{filename}'")


# Função para renomear os arquivos no padrão
def rename_files(source_path: str, name_file: str):
    os.makedirs(source_path, exist_ok=True)

    counter = 1
    for filename in os.listdir(source_path):
        if filename.endswith((".webp", ".jpeg", ".jpg", ".tiff", ".png")):
            old_name_file = os.path.join(source_path, filename)

            timestamp_modification = os.path.getmtime(old_name_file)
            date_modification = datetime.fromtimestamp(timestamp_modification).strftime(
                "%Y.%m.%d-%H.%M"
            )

            new_name_file = f"{name_file}_{date_modification}_{counter}{os.path.splitext(filename)[1]}"
            new_name_file_path = os.path.join(source_path, new_name_file)

            if os.path.exists(new_name_file_path):
                print(f"⚠️ Arquivo já tem o nome informado: '{new_name_file}'")
                continue

            os.rename(old_name_file, new_name_file_path)

            os.utime(
                new_name_file_path, (timestamp_modification, timestamp_modification)
            )

            print(f"✅ Arquivo renomeado: {filename} -> {new_name_file}")

            counter += 1


def run():
    try:
        while True:
            option: str = input(
                dedent(
                    """
                    Qual operação você quer realizar:
                    1 Copiar arquivos para outra pasta
                    2 Converter arquivos para .webp, .tiff ou .png
                    3 Renomear arquivos nome_data_contador.tipo

                    :"""
                )
            )

            if option == "1":
                path_origin: str = get_path(input("\nPasta de origem das imagens: "))
                path_destiny: str = get_path(input("\nPasta de destino das imagens: "))

                if path_origin == path_destiny:
                    print("🚨 As pasta de origem e destino são as mesmas!")
                    continue  # Retorna ao início do loop

                copy_files(path_origin, path_destiny)

            elif option == "2":
                source_path: str = get_path(input("\nPasta de origem dos arquivos: "))

                files_types: dict = {"1": "png", "2": "webp", "3": "tiff"}
                file_type = input(
                    f"Tipo do arquivo ({', '.join([f'{key}:{value}' for key, value in files_types.items()])}): "
                )

                if file_type not in files_types:
                    print("🚨 Tipo de arquivo inválido!")
                    continue  # Retorna ao início do loop

                convert_files(source_path, files_types[file_type])

            elif option == "3":
                source_path: str = get_path(input("\nPasta dos arquivos: "))
                name_file: str = input("Nome do arquivo: ")

                rename_files(source_path, name_file)

            else:
                print("🚨 Insira um valor válido.")

    except Exception as e:
        print(f"\n🚨 Ocorreu um erro: {e}")
        print("O programa será encerrado.")


run()