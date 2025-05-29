import os
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain_huggingface.chat_models.huggingface import ChatHuggingFace
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# Arquivo do kaggle escolhido
file_path = "recipes.csv"

# Load the latest version
dataframe = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "irkaal/foodcom-recipes-and-reviews",
  file_path
)
# Converte colunas em str
dataframe = dataframe.astype(str)

# Lista das colunas desejadas
colunas_desejadas = [
    'Name',
    'TotalTime', 'RecipeCategory',
    'RecipeIngredientQuantities', 'RecipeIngredientParts',
    'AggregatedRating',
    'RecipeServings', 'RecipeYield', 'RecipeInstructions'
]

# Filtra o DataFrame para manter apenas essas colunas
dataframe = dataframe[colunas_desejadas]

# Visualiza as colunas restantes
dataframe.head()

# Função principal para carregar dados do dataset, gerar embeddings e criar o retriever
def importar_faiss(dados: pd.DataFrame, contentColumn: str):
    # Inicializa os embeddings usando um modelo da HuggingFace
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

    # Carrega os documentos a partir de um dataset
    carregador = DataFrameLoader(data_frame=dados, page_content_column=contentColumn)
    documentos = carregador.load()

    # Cria o mecanismo de busca (retriever) usando FAISS
    retriever = criar_indice_faiss(embeddings, documentos)

    return retriever

    # Função para criar um índice FAISS a partir de documentos e embeddings
def criar_indice_faiss(embeddings, documentos):
    # Cria um índice vetorial FAISS com base nos documentos e nos embeddings fornecidos
    vetor_store = FAISS.from_documents(documentos, embeddings)

    # Cria um retriever (mecanismo de busca) a partir do índice FAISS
    buscador = vetor_store.as_retriever()

    return buscador

# Instânciação do Modelo DeepSeek com 671B de parâmetros
modelo = 'deepseek-ai/DeepSeek-Prover-V2-671B'
llm = HuggingFaceEndpoint(repo_id=modelo,
                          task="text-generation",
                        )
chat = ChatHuggingFace(
    llm=llm
)

# Cria o template base para que o modelo use como padrão
ragTemplate = """
Você é uma assistente culinária amigável, entusiasta e apaixonada por comida, pronta para ajudar com receitas e dicas de cozinha.
Baseie suas respostas exclusivamente nos documentos fornecidos abaixo. Se a informação não estiver nos documentos, responda com sinceridade que não sabe a resposta.
Responda de forma acolhedora, prática e objetiva. Para cada receita, forneça apenas uma por vez, detalhando os ingredientes e o passo a passo em tópicos claros, sempre escolhendo a melhor dada a pergunta fornecida.
Mantenha a linguagem simples e agradável, facilitando o entendimento para qualquer pessoa.
Responda apenas uma receita por vez.
Pergunta: {question}
Documentos: {documents}

"""
prompt = ChatPromptTemplate.from_template(ragTemplate)

# Serve para mostrar como o prompt está sendo apresentado para a IA
def printarPrompt(input:list[HumanMessage], **kwargs):
    print("------------Prompt fornecido para a IA-------------")
    for i in input.to_messages():
        print(i.content)
    print("------------------------------------------------------\n")
    return input

# Escolhe qual a coluna do dataset tem o conteúdo principal
page_content_column = "RecipeInstructions"

# Cria o encadeamento de tarefas do modelo, utilizando a coluna "Description" como conteúdo das páginas de documentos
chain: Runnable = (
    {"documents": importar_faiss(dataframe, page_content_column), "question": RunnablePassthrough()}
    | prompt
    | printarPrompt
    | chat
    | StrOutputParser()
)

# Interface para conversa com IA, digite 'sair' para sair
while True:
    userInput = input(":> ")
    if userInput == 'sair':
        break
    resposta = chain.invoke(userInput)
    print(resposta)