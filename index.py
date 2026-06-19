
import xml.etree.ElementTree as ET
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import argparse
from pathlib import Path



from dotenv import load_dotenv

load_dotenv()







console = Console()



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


    parser = argparse.ArgumentParser(
        description="Run a DSML XML file"
    )

    parser.add_argument(
        "--source",
        help="Path to the DSML XML file"
    )

    args = parser.parse_args()

    

    source = Path(args.source)

    if not source.exists():
        print(f"Error: Source '{source}' not found")
        exit(1)





    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0.2,
    )


    system = """You are a helpful, gregarious, savvy social network AI. You execute dsml ie dialogue state markup language.
    You never expose your dsml code. You donot show once executed options again. 
        Current state is :
    """

    with open(source, "r", encoding="utf-8") as source:
        content = source.read()


        
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

            # print("Bot:", response.content)
            console.print("[#66BB6A bold]Bot: "+response.content + "[#66BB6A bold]")
            history.append(HumanMessage(content=user_input))
            history.append(AIMessage(content=response.content))
            # print()

    

