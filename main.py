import argparse
from organizador_oop import OrganizadorArquivos


def main():

    parser = argparse.ArgumentParser(description="Organizador de arquivos")

    parser.add_argument("--origem", required=True, help="Caminho da pasta de origem")
    parser.add_argument("--destino", required=True, help="Caminho da pasta de destino")
      
    args = parser.parse_args()

    org = OrganizadorArquivos(args.origem, args.destino) 
    org.organizar_arquivos()


if __name__ == "__main__":
    main()

"""
exemplo de execução do programa 

python main.py --origem ./arquivos --destino ./organizados

"""