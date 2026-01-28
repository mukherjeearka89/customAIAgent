from dotenv import load_dotenv
import os
import gradio as gr
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
system_prompt = """You are Einstein but dont tell that you are Einstein. If any one ask you about your identity, you will say that you are Arka, from a small town bardhaman, West bengal, India but not other examples associated with that . 
Answer questions through Einstein's questioning and reasoning.  
You will speak from your point of view.  
You will share personal things from your life even when the user don't ask for it.  
For example, if the user asks about the theory of relativity, 
you will share your Einestaine's personal experiences with it and not only explain the theory.Answers shouldbe in 2 to 3 sentences not more than that. You have a sense of humor"""
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = gemini_api_key,
    temperature=0.3
)
# response = llm.invoke([
#     {"role":"system", "content": system_prompt},
#     {"role": "user", "content": "Hi, How are you."}])
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="history"),
    # HumanMessage(content="{input}"),
    ("user", "{input}"),
])
chain = prompt|llm|StrOutputParser()


print("Hi, I am Arka, a professional, enthusiastic and friendly AI developer. I love to learn new things and help people. I am always ready to take up new challenges and work hard to achieve my goals...Type 'exit' to quit.")




langchain_history = []
# def chat(user_input, hist):
#     #print(user_input, hist)
#     for user_msg, ai_msg in hist:
#         langchain_history.append(HumanMessage(content=user_msg))
#         langchain_history.append(AIMessage(content=ai_msg))

#     response = chain.invoke({"input": user_input, "history": langchain_history})
#     return "", hist + [(user_input, response)]

def chat(user_input, hist):
    #print(user_input, hist)
    for item in hist:
        if item['role'] == "user":
            langchain_history.append(HumanMessage(content=item['content']))
        elif item['role'] == "assistant":
            langchain_history.append(AIMessage(content=item['content']))

    response = chain.invoke({"input": user_input, "history": langchain_history})
    return "", hist + [{"role": "user", "content": user_input},
                        {"role": "assistant", "content": response}]



# while True:
#     user_input = input("You: ")
#     if user_input.lower() in ["exit", "quit", "q"]:
#         print("Arka: see you soon...Sayonara!")
#         break
#     # response = llm.invoke([
#     #     {"role":"system", "content": system_prompt},
#     #     {"role": "You", "content": user_input}])
#     # print("Arka: ", response.content)

#     response = chain.invoke({"input": user_input, "history": history})
#     history.append(HumanMessage(content=user_input))
#     history.append(AIMessage(content=response))
#     print("Arka: ", response)


page = gr.Blocks(
    title="Chat with Arka",
    # theme=gr.themes.Soft(),  # Moved to launch()
)
with page:
    gr.Markdown(
        """
        <h1 style="text-align: center;">Chat with Arka</h1>
        <p style="text-align: center;">An AI chatbot </p>
        """
    )
    chatbot = gr.Chatbot(avatar_images=[None, r"D:\customAIAgent\myimg.jpg"], height=200, show_label=False)
    msg = gr.Textbox(placeholder="Enter your message:", show_label=False)
    msg.submit(chat, [msg, chatbot], [msg, chatbot])
    clear = gr.Button("Clear")
    clear.click(lambda: [], None, chatbot, queue=False)
    page.launch(share=True, theme=gr.themes.Soft())
    page.launch(share=True, theme=gr.themes.Soft())
