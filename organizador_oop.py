from pathlib import Path
import shutil
from collections import defaultdict


class OrganizadorArquivos:
    """
    Classe responsável por organizar arquivos de uma pasta de origem
    em uma pasta de destino, separando por extensão, renomeando
    e gerando um relatório final.
    """

    def __init__(self, pasta_origem, pasta_destino):
        """
        Inicializa o organizador com os caminhos de origem e destino.

        Args:
            pasta_origem (str): Caminho da pasta de entrada.
            pasta_destino (str): Caminho da pasta de saída.
        """
        self.origem = Path(pasta_origem)
        self.destino = Path(pasta_destino)
        self.contadores = defaultdict(int)
        self.relatorio = []
        self.arquivos = []
        self.erros = []

    def validar_pastas(self):
        """
        Valida a existência da pasta de origem, coleta os arquivos
        (incluindo subpastas) e garante que a pasta de destino exista.

        Raises:
            FileNotFoundError: Se a pasta de origem não existir.
            ValueError: Se não houver arquivos para processar.
        """
        if not self.origem.exists():
            raise FileNotFoundError("❌ Pasta de origem não existe")
        self.arquivos = [arq for arq in self.origem.rglob("*") if arq.is_file()]

        if not self.arquivos:
            raise ValueError("⚠️ Nenhum arquivo encontrado")
        self.destino.mkdir(exist_ok=True)

    def organizar_arquivos(self):
        """
        Método principal que executa o processo de organização dos arquivos.

        Percorre todos os arquivos encontrados e tenta processá-los
        individualmente. Em caso de erro, registra e continua o processamento.
        """
        self.validar_pastas()
        for arquivo in self.arquivos:
            try:
                self.processar_arquivo(arquivo)
            except Exception as e:
                self.erros.append(f"{arquivo} -> ERRO: {e}")
        self._gerar_relatorio()

    def processar_arquivo(self, arquivo):
        """
        Processa um único arquivo: identifica extensão, cria pasta destino,
        gera novo nome, move o arquivo e registra no relatório.

        Args:
            arquivo (Path): Arquivo a ser processado.
        """

        if self.destino in arquivo.parents:
            return
        extensao = arquivo.suffix[1:].lower()

        if extensao == "":
            extensao = "outros"

        destino = self.criar_pasta(extensao)

        novo_nome = self.gerar_nome(arquivo, extensao, destino)

        self._mover_arquivo(arquivo, destino / novo_nome)

        self.registrar(arquivo.name, novo_nome)

    def criar_pasta(self, extensao):
        """
        Cria (se necessário) e retorna a pasta de destino para uma extensão.

        Args:
            extensao (str): Tipo/extensão do arquivo.

        Returns:
            Path: Caminho da pasta criada ou existente.
        """

        pasta_destino = self.destino / extensao
        pasta_destino.mkdir(exist_ok=True)
        return pasta_destino

    def gerar_nome(self, arquivo, extensao, pasta_destino):
        """
        Gera um nome único padronizado para o arquivo, evitando sobrescrita.

        Args:
            arquivo (Path): Arquivo original.
            extensao (str): Extensão do arquivo.
            pasta_destino (Path): Pasta onde o arquivo será salvo.

        Returns:
            str: Nome gerado para o arquivo.
        """
        while True:
            self.contadores[extensao] += 1
            numero = self.contadores[extensao]

            if arquivo.suffix == "":
                nome = f"{extensao}_{numero:03d}"
            else:
                nome = f"{extensao}_{numero:03d}.{extensao}"
            if not (pasta_destino / nome).exists():
                return nome

    def _mover_arquivo(self, arquivo, destino):
        """
        Move o arquivo para o destino especificado.

        Args:
            arquivo (Path): Arquivo original.
            destino (Path): Caminho final do arquivo.
        """

        shutil.move(str(arquivo), str(destino))
        print(f"✅ {arquivo.name} → {destino.name}")

    def registrar(self, nome_original, nome_novo):
        """
        Registra a movimentação do arquivo para o relatório.

        Args:
            nome_original (str): Nome original do arquivo.
            nome_novo (str): Nome após organização.
        """
        self.relatorio.append(f"{nome_original} → {nome_novo}")

    def _gerar_relatorio(self):
        """
        Gera o arquivo relatorio.txt com o resumo da execução.

        Inclui:
        - Total de arquivos processados
        - Quantidade por tipo
        - Lista de arquivos organizados
        - Lista de erros (se houver)
        """

        caminho = self.destino / "relatorio.txt"

        with caminho.open("w", encoding="utf-8") as f:
            total = sum(self.contadores.values())

            f.write("📊 RELATÓRIO\n\n")
            f.write(f"Total: {total}\n\n")

            for ext, qtd in self.contadores.items():
                f.write(f"{ext}: {qtd}\n")

            f.write("\nDetalhes:\n")
            for item in self.relatorio:
                f.write(f"{item}\n")

            f.write("\nErros:\n")
            for erro in self.erros:
                f.write(f"{erro}\n")

        print(f"\n📄 Relatório criado: {caminho}")
