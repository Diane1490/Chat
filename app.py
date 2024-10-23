import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI  
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Set up the page configuration
st.set_page_config(page_title="Chat Page", page_icon="book", layout="wide")
st.title("Chat Page")

# Function to retrieve the response from the AI
def retrieve_response(user_input, chat_history):
    template = """
    You are a helpful assistant. Answer the following questions considering
    the history of the conversation:
    Chat history: {chat_history}
    User question: {user_input}
    """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI()  # Initialize the language model
    chain = prompt | llm | StrOutputParser()  # Create the chain with the LLM
    return chain.run({
        "chat_history": chat_history,
        "user_input": user_input
    })

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hey! This is FTA. How can I help you?"),
    ]

# Display the conversation history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# Handle user input
user_query = st.chat_input("How Can I Help You?")
if user_query and user_query != "":
    # Append user query to chat history
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    # Display the user message
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    # Retrieve AI response
    response = retrieve_response(user_query, st.session_state.chat_history)
    
    # Append AI response to chat history
    st.session_state.chat_history.append(AIMessage(content=response))
    
    # Display the AI response
    with st.chat_message("AI"):
        st.markdown(response)
