from pathlib import Path
import shutil
from collections import defaultdict
class Organizador:
    def organizar_arquivos(pasta_origem, pasta_destino):
        origem = Path(pasta_origem)
        destino = Path(pasta_destino)
        destino.mkdir(exist_ok=True)

        if not origem.exists():
            print("A pasta de origem não existe.")
            return
    
        contadores = defaultdict(int)
        relatorio = [] 

        for arquivo in origem.rglob("*"):
            if arquivo.is_file():
                extensao = identificar_extensao(arquivo)
                contadores[extensao] += 1

    def identificar_extensao(arquivo):
        ext = arquivo.suffix.lower().replace(".", "")
        if not ext:
            ext = "outros"
        print (ext)





