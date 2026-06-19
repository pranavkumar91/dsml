
import xml.etree.ElementTree as ET
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from dotenv import load_dotenv

load_dotenv()


def validateTree():
    try:
        tree = ET.parse("index.dsml")
        root = tree.getroot()

        # print("Root:", root.tag)

    except FileNotFoundError:
        print("XML file not found")

    except ET.ParseError as e:
        print("Invalid XML:", e)

# gemini-2.5-flash

# gemini-3.1-pro

if __name__ == "__main__":
    validateTree()
    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.2,
    )


    system = """You are a helpful social network AI. You execute dsml ie dialogue state markup language.
    You never expose your code. You donot show once executed options again. 
        Current state is :
    """

    with open("index.dsml", "r", encoding="utf-8") as file:
        content = file.read()


        
        prompt = ChatPromptTemplate.from_messages([
        ("system", "{system} {content}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
        ])

        chain = prompt | llm

        history = []

        while True:
            user_input = input(">: ").strip()

            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            if not user_input:
                continue

            response = chain.invoke({
                "question": user_input,
                "content": content,
                "system": system,
                "history": history 
            })

            print("Bot:", response.content)
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response.content))
            # print()

    

