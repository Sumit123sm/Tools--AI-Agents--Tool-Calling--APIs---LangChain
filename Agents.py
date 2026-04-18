# from dotenv import load_dotenv
# import os
# import requests

# load_dotenv()

# from langchain_mistralai import ChatMistralAI
# from langchain.tools import tool
# from langchain_core.messages import HumanMessage, ToolMessage
# from tavily import TavilyClient
# from rich import print
# from langchain.agents import create_agent 
# from langchain.agents.middleware import wrap_tool_call

# # =========================
# # 🌦️ Weather Tool
# # =========================

# @tool
# def get_weather(city: str) -> str:
#     """Get current weather of a city"""
    
#     api_key = os.getenv("OPENWEATHER_API_KEY")
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    
#     response = requests.get(url)
#     data = response.json()
    
#     if str(data.get("cod")) != "200":
#         return f"Error: {data.get('message', 'Could not fetch weather')}"
    
#     temp = data["main"]["temp"]
#     desc = data["weather"][0]["description"]
    
#     return f"Weather in {city}: {desc}, {temp}°C"


# # =========================
# # 📰 News Tool (Tavily)
# # =========================

# tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# @tool
# def get_news(city: str) -> str:
#     """Get latest news about a city"""
    
#     response = tavily_client.search(
#         query=f"latest news in {city}",
#         search_depth="basic",
#         max_results=3
#     )
    
#     results = response.get("results", [])
    
#     if not results:
#         return f"No news found for {city}"
    
#     news_list = []
    
#     for r in results:
#         title = r.get("title", "No title")
#         url = r.get("url", "")
#         snippet = r.get("content", "")
        
#         news_list.append(
#             f"- {title}\n  🔗 {url}\n  📝 {snippet[:100]}..."
#         )
    
#     return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)
# # =========================
# # 🧠 LLM Setup
# # =========================

# llm = ChatMistralAI(model="mistral-small-2506")


# @wrap_tool_call
# def human_approval(request, handler):
#     """Ask for human approval before every tool call."""
#     tool_name = request.tool_call["name"]
#     confirm = input(f"Agent wants to call '{tool_name}'. Approve? (yes/no): ")

#     if confirm.lower() != "yes":
#         return ToolMessage(
#             content="Tool call denied by user.",
#             tool_call_id=request.tool_call["id"]
#         )

#     return handler(request)  

# agent = create_agent(
#     llm,
#     tools = [get_weather,get_news],
#     system_prompt= "you are a helpful city assistant.",
#     middleware= [human_approval]
# )

# print("City Agent | type exit to quit")

# while True:
#     user_input = input("You : ")
#     if user_input.lower() == "exit":
#         break 
#     result = agent.invoke({
#         "messages": [{"role": "user", "content": user_input}]
#     })

#     print("bot : ", result['messages'][-1].content )

import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv()

# LangChain imports
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call

# Tavily
from tavily import TavilyClient

# =========================
# 🌦️ Weather Tool
# =========================
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"🌤 Weather in {city}: {desc}, {temp}°C"


# =========================
# 📰 News Tool
# =========================
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool

def get_news(city: str) -> str:
    """Get latest news about a city"""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"""
### 📰 {title}
👉 [Read full article]({url})

{snippet[:150]}...
"""
        )

    return "\n\n".join(news_list)


# =========================
# 🧠 LLM Setup
# =========================
llm = ChatMistralAI(model="mistral-small-2506")


# =========================
# 👤 Human Approval Middleware (UI version)
# =========================
@wrap_tool_call
def human_approval(request, handler):
    tool_name = request.tool_call["name"]

    # Show approval UI
    with st.sidebar:
        st.warning(f"⚠️ Tool Request: {tool_name}")
        approve = st.radio(
            "Approve tool call?",
            ("Yes", "No"),
            key=request.tool_call["id"]
        )

    if approve != "Yes":
        return ToolMessage(
            content="❌ Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request)


# =========================
# 🤖 Agent
# =========================
agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="""
You are a helpful city assistant.

STRICT RULES:
- Do NOT rewrite tool outputs
- Do NOT remove links
- Always keep links clickable in markdown format
- If tool provides news, show it exactly as it is
""",
    middleware=[human_approval]
)


# =========================
# 🎨 Streamlit UI
# =========================
st.set_page_config(page_title="City Assistant AI", layout="wide")

st.title("🌍 City Assistant AI")
st.markdown("Get **weather 🌦️** and **latest news 📰** for any city")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("This agent uses:")
    st.markdown("- 🌦️ Weather API")
    st.markdown("- 📰 Tavily News")
    st.markdown("- 🤖 Mistral LLM")

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# User input
user_input = st.chat_input("Ask about a city...")

if user_input:
    # Add user message
    st.session_state.messages.append(HumanMessage(content=user_input))

    with st.chat_message("user"):
        st.markdown(user_input)

    # Invoke agent
    result = agent.invoke({
        "messages": st.session_state.messages
    })

    response = result["messages"][-1].content

    # Add AI response
    st.session_state.messages.append(AIMessage(content=response))

    with st.chat_message("assistant"):
        st.markdown(response, unsafe_allow_html=True)