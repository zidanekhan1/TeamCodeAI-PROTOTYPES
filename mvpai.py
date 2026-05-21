from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import streamlit as st

api_key = st.sidebar.text_input("enter api:",type="password")

frontend_model = ChatGroq(model="llama-3.3-70b-versatile",api_key=api_key)
checker_model = ChatGroq(model="llama-3.3-70b-versatile",api_key=api_key)

st.sidebar.info("TEST MODEL !! ONLY BACKEND PRACTICE SUPPORT FOR NOW !!")

frontend_prompt = """
You are a frontend engineer.

Generate ONLY a simple HTML + JavaScript frontend snippet.

Requirements:
- Use fetch() for API calls
- Keep code under 30 lines
- Require a FastAPI backend
- Clearly include:
    - endpoint route
    - HTTP method
    - expected JSON fields
- Do NOT explain anything
- Output code only
"""

checker_prompt = """
You are a senior QA engineer reviewing frontend/backend compatibility.

Your job:
- ONLY analyze compatibility issues.
- Ignore future hypothetical problems.
- Ignore code quality discussions unless they break compatibility.

You MUST:
1. Decide PASS or FAIL.
2. Explain ONLY real compatibility issues.
3. Give concise hints.
4. Do NOT rewrite the code.

Output format:

STATUS: PASS or FAIL

ISSUES:
- ...

HINTS:
- ...
"""

message_for_frontend = [
    ("system",frontend_prompt),
    ("human", "Generate a snippet for a basic user login form check.")
]

frontend_code = frontend_model.invoke(message_for_frontend)

st.write(frontend_code.content)

user_code = st.text_area("write code according to the frontend code provided to connect to the frontend with the least possible bugs")

message_for_checkermdl = [
    ("system", checker_prompt),
    ("human", f"""
FRONTEND CODE:
{frontend_code.content}

BACKEND CODE:
{user_code}
""")
]

if user_code:
    checker_feedback = checker_model.invoke(message_for_checkermdl)
    st.write(checker_feedback.content)