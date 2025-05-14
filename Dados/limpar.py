import json
import csv

# Caminho para o arquivo JSON original
caminho_arquivo = 'Dados\DadosBrutos.json'
dadosLimpos = []

# Abrindo e carregando o conteúdo do JSON
with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

cont = 0
# Coletando os dicionários internos
for usuario, informacoes in dados.items():
    if cont == 200:
        break
    cont += 1
    dadosLimpos.append(informacoes)

# Obtemos os nomes das colunas com base nas chaves do primeiro dicionário
colunas = dadosLimpos[0].keys()

# Salvando em formato CSV
with open('Dados\DadosLimpos.csv', 'w', encoding='utf-8', newline='') as arquivo_csv:
    writer = csv.DictWriter(arquivo_csv, fieldnames=colunas)
    writer.writeheader()  # Escreve o cabeçalho
    writer.writerows(dadosLimpos)  # Escreve os dados
