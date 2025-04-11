import json
import shutil
import os
import sys
import time
import logging


def main() -> None:
    timestr: str = time.strftime("%d.%m.%Y %H.%M.%S")  # formatação da datahora
    logger: logging.Logger = logging.getLogger("main")  # inicializa o arquivo de Log
    logging.basicConfig(
        filename=f"Log - {timestr}.log",
        encoding="utf-8",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%d/%m/%Y %H:%M:%S",
    )  # configura o formato de hora/data nas mensagens e a encodificação
    logger.info("Inicializando")

    with (
        open("config.json") as config
    ):  # extraindo as informações de whitelist e destino do arquivo config.json da pasta do programa
        config_from_JSON = json.load(config)
        logger.info("Carregando informações do JSON")

        logger.info("Validando Caminho da Pasta a ser deletada")
        if os.path.exists(
            config_from_JSON["destino"]
        ):  # Verifica se o endereço de destino dentro do JSON é um caminho válido no Sistema
            destino: str = config_from_JSON["destino"]
            logger.info(f"Endereço {destino} válido")
        else:
            logger.warning(
                "Endereço Inválido. Por favor, verifique o arquivo config.json"
            )
            logger.error(
                "Um erro foi encontrado durante a execução do programa, por favor verifique o Log"
            )
            sys.exit(0)

        logger.info("Verificando Whitelist")
        if isinstance(
            config_from_JSON["whitelist"], list
        ):  # Verifica se a Whitelist é uma Lista Python válida (arrays são resolvidos como Listas quando são importados)
            whitelist: list[str] = config_from_JSON["whitelist"]
            if not whitelist:  # Checa se a Whitelist está vazia
                logger.warning(
                    "Whitelist Vazia, isto removerá todos os arquivos da pasta de destino"
                )
            else:
                logger.info(f"{whitelist = }")
        else:
            logger.warning(
                "Whitelist Inválida. Por favor verifique o arquivo config.json"
            )
            logger.error(
                "Um erro foi encontrado durante a execução do programa, por favor verifique o Log"
            )
            sys.exit(0)
        config.close()

    logger.info("Informações carregadas com Sucesso")

    arquivos: list[str] = [
        item for item in os.listdir(destino) if item not in whitelist
    ]

    if not arquivos:
        logger.warning("Não há arquivos a serem removidos")
        sys.exit(0)

    logger.info("Removendo arquivos")
    for nome_do_arquivo in arquivos:
        caminho_do_arquivo: str = os.path.join(destino, nome_do_arquivo)
        try:
            if os.path.isfile(
                caminho_do_arquivo
            ):  # Verifica se o arquivo atual é um arquivo
                os.remove(caminho_do_arquivo)  # remove se for um arquivo
                logger.info(f"Arquivo {nome_do_arquivo} removido")
            elif os.path.isdir(
                caminho_do_arquivo
            ):  # se não for um arquivo, verifica se é uma pasta
                shutil.rmtree(
                    caminho_do_arquivo
                )  # remove a pasta (e todos os arquivos de dentr)
                logger.info(f"Pasta {nome_do_arquivo} removida")
        except OSError as e:
            logger.error(
                f"Falha ao remover {caminho_do_arquivo}. Erro: {e}"
            )  # Lança o erro no log, caso tenha algum erro


if __name__ == "__main__":
    main()
