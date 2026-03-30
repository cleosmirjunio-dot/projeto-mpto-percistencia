from pathlib import Path
import shutil
from collections import defaultdict


def organizar_arquivos(pasta_origem, pasta_destino):
    origem = Path(pasta_origem)
    destino = Path(pasta_destino)

    # 🔹 pasta inexistente
    if not origem.exists():
        print("❌ Pasta de origem não existe")
        return

    try:
        arquivos = [arq for arq in origem.iterdir() if arq.is_file()]
    except PermissionError:
        print("❌ Sem permissão para acessar a pasta de origem")
        return

    if not arquivos:
        print("⚠️ Nenhum arquivo encontrado")
        return

    try:
        destino.mkdir(exist_ok=True)
    except PermissionError:
        print("❌ Sem permissão para criar pasta de destino")
        return

    contadores = defaultdict(int)
    relatorio = []

    for arquivo in arquivos:
        try:
            extensao = arquivo.suffix[1:].lower()

            if extensao == "":
                extensao = "outros"

            pasta_destino = destino / extensao
            pasta_destino.mkdir(exist_ok=True)

            # 🔥 contador
            contadores[extensao] += 1
            numero = contadores[extensao]

            # 🔥 nome padronizado
            if arquivo.suffix == "":
                novo_nome = f"{extensao}_{numero:03d}"
            else:
                novo_nome = f"{extensao}_{numero:03d}.{extensao}"

            arquivo_destino = pasta_destino / novo_nome

            # 🔹 conflito de nome
            while arquivo_destino.exists():
                contadores[extensao] += 1
                numero = contadores[extensao]

                if arquivo.suffix == "":
                    novo_nome = f"{extensao}_{numero:03d}"
                else:
                    novo_nome = f"{extensao}_{numero:03d}.{extensao}"

                arquivo_destino = pasta_destino / novo_nome

            # 🔹 mover arquivo
            shutil.move(str(arquivo), str(arquivo_destino))

            #print(f"✅ {arquivo.name} → {novo_nome}")
            relatorio.append(f"{arquivo.name} → {novo_nome}")

        except PermissionError:
            print(f"❌ Sem permissão: {arquivo.name}")

        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado (pode ter sido movido): {arquivo.name}")

        except Exception as e:
            print(f"⚠️ Erro inesperado com {arquivo.name}: {e}")

    gerar_relatorio(destino, contadores, relatorio)


def gerar_relatorio(destino, contadores, relatorio):
    caminho = destino / "relatorio.txt"

    try:
        with caminho.open("w", encoding="utf-8") as f:
            f.write("📊 RELATÓRIO DE ORGANIZAÇÃO\n")
            f.write("=" * 40 + "\n\n")

            total = sum(contadores.values())
            f.write(f"Total de arquivos movidos: {total}\n\n")

            f.write("Arquivos por tipo:\n")
            for ext, qtd in contadores.items():
                f.write(f"- {ext}: {qtd}\n")

            f.write("\nDetalhes:\n")
            for item in relatorio:
                f.write(f"- {item}\n")

        print(f"\n📄 Relatório criado em: {caminho}")

    except PermissionError:
        print("❌ Sem permissão para criar o relatório")

    except Exception as e:
        print(f"⚠️ Erro ao gerar relatório: {e}")