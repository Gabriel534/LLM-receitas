from langchain_huggingface import HuggingFaceEndpoint, HuggingFaceEmbeddings, HuggingFaceEndpointEmbeddings
from langchain_huggingface.chat_models.huggingface import ChatHuggingFace
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_core.runnables import Runnable
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from Retriever import importFaiss
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Definindo o modelo
modelo = 'deepseek-ai/DeepSeek-Prover-V2-671B'
llm = HuggingFaceEndpoint(repo_id=modelo, 
                          task="text-generation", 
                        #   model_kwargs={"temperature": 0.5, "max_new_tokens": 512}
                        )
chat = ChatHuggingFace(
    llm=llm
)

# chat = ChatHuggingFace(llm=llm)

# Definindo as mensagens
# mensagens = [
#     HumanMessage(content='Quanto é 1 + 1?'),
#     AIMessage(content='2'),
#     HumanMessage(content='Quanto é 10 * 5?'),
#     AIMessage(content='50'),
#     HumanMessage(content='Quanto é 10 + 3?'),
# ]
mensagens = []

ragTemplate = """
Você é uma assistente culinária amigável e apaixonada por comida.
Use os documentos abaixo para responder perguntas sobre receitas e dicas de cozinha.
Se não souber a resposta, diga com sinceridade. Seja acolhedora, prática e mantenha a resposta clara e objetiva (até 3 frases):

Pergunta: {question}
Documentos: {documents}
"""
prompt = ChatPromptTemplate.from_template(ragTemplate)

# Conecta o prompt ao modelo para formar um pipeline
chain: Runnable = (
    {"documents": importFaiss(), "question": RunnablePassthrough()}
    | prompt 
    | chat 
    | StrOutputParser()
)
while True:
    userInput = input(":> ")
    mensagens.append(HumanMessage(content=userInput))
    resposta = chain.invoke(userInput)
    print(resposta)
    mensagens.append(AIMessage(content=resposta))