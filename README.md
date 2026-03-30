# 📁 Organizador de Arquivos

Script em Python para organizar arquivos de uma pasta por tipo (extensão), renomeando automaticamente e gerando um relatório.

---

## 🚀 Como usar

```bash
python main.py --origem CAMINHO_ORIGEM --destino CAMINHO_DESTINO
```

### Exemplo

```bash
python main.py --origem ./entrada --destino ./saida
```

---

## 📂 O que o programa faz

* Lê arquivos (incluindo subpastas)
* Organiza por extensão (txt, pdf, jpg, etc.)
* Renomeia arquivos (ex: `txt_001.txt`)
* Cria pastas automaticamente
* Gera um arquivo `relatorio.txt`

---

## 📄 Relatório

O relatório contém:

* Total de arquivos processados
* Quantidade por tipo
* Lista de arquivos organizados
* Erros (se houver)

---

## ⚙️ Requisitos

* Python 3
