from pathlib import Path

def criar_arquivos():
    pasta = Path("teste_arquivos")
    pasta.mkdir(exist_ok=True)

    extensoes = ["pdf", "docx", "xlsx", "jpg", "png", "txt", "csv", "pptx", "zip", "mp4"]

    for ext in extensoes:
        for i in range(1, 4):  # 3 arquivos de cada
            arquivo = pasta / f"Arquivo_{ext}_{i}.{ext}"
            arquivo.write_text("conteúdo de teste")

    print("Arquivos criados!")
