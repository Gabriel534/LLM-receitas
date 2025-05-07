from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models.huggingface import ChatHuggingFace
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(repo_id="deepseek-ai/DeepSeek-Prover-V2-671B") #task="conversational")
chat = ChatHuggingFace(llm=llm)

# Definindo as mensagens anteriores
mensagens = [
    HumanMessage(content='Hello World'),
    AIMessage(content='2'),
    HumanMessage(content='Quanto é 10 * 5?'),
    AIMessage(content='50'),
    HumanMessage(content='Qual o seu nome?'),
]

# Invocando o modelo
resposta = chat.invoke(mensagens).text()
print(resposta)