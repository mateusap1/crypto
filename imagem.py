import sys
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        print(
            f"Usage: {sys.argv[0]} <caminho_para_imagem1> [<caminho_para_imagem2> ... <caminho_para_imagemN>]"
        )
        sys.exit(1)

    id_cripto = 1  # Exemplo: ID da criptomoeda associada
    tipo = "logo"  # Exemplo: tipo da imagem (pode ser 'logo', 'icone', etc.)
    data_upload = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for caminho_imagem in sys.argv[1:]:
        try:
            with open(caminho_imagem, "rb") as file:
                conteudo_bytes = file.read()
        except Exception as e:
            print(f"Erro ao abrir a imagem '{caminho_imagem}': {e}")
            continue

        query = (
            "INSERT INTO Imagens_Criptomoedas (id_cripto, tipo, conteudo, data_upload) "
            f"VALUES ({id_cripto}, '{tipo}', decode('{conteudo_bytes.hex()}', 'hex'), '{data_upload}');"
        )

        print(query)


if __name__ == "__main__":
    main()
