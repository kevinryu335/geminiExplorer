import google.cloud.aiplatform as vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

project = 'confident-abode-424118-v9'
vertexai.init(project = project)
config = generative_models.GenerationConfig(
    temperature = 0.4
)

model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)
chat = model.start_chat()

def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message('model'):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role" : "user",
            "content" : query
        }
    
    )
    st.session_state.messages.append(
        {
            "role" : "model",
            "content" :output
        }
    )

st.title("Gemini Explorer")

if "messages" not in st.session_state:
    st.session_state.messages=[]

for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message['role'],
        parts = [ Part.from_text(message['content'])]
    )
    if index !=0:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    chat.history.append(content)

query = st.chat_input("Gemini Explorer")

if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive. Use genz speak"
    llm_function(chat, initial_prompt)

if query:
    with st.chat_message('user'):
        st.markdown(query)
    llm_function(chat,query)
 
def generate_greetin(name):
    return f"👋 Hello, {name}! I'm ReX, your assistant powered by Google Gemini. How can I help you today? 🚀"

user_name = st.text_input("Please Enter your name")
if user_name:
    personalized_greeting = generate_greetin(user_name)
    st.write(personalized_greeting)