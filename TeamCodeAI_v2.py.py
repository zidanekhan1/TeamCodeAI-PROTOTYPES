from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import streamlit as st
from scenario import scenarios

api_key = st.sidebar.text_input("enter api:",type="password")

st.title("AI BACKEND SIM v2")

if "frontend_code" not in st.session_state:
    st.session_state.frontend_code = None

if "feedback" not in st.session_state:
    st.session_state.feedback = None

st.sidebar.info("TEST MODEL !! ONLY BACKEND PRACTICE SUPPORT FOR NOW !!")

difficulty = st.sidebar.selectbox(
    "Choose difficulty",
    ["Easy","Medium","Hard","All"]
)

if difficulty == "All":
    filtered_scenarios = scenarios

else:
    filtered_scenarios = [
        scenario
        for scenario in scenarios
        if scenario["difficulty"]==difficulty
    ] 

selected_scenario = st.selectbox(
    "Choose Scenario",
    filtered_scenarios,
    format_func=lambda x: x["title"]
)

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

You must verify:
- ALL frontend-accessed response fields exist
- response structure matches exactly
- successful frontend execution is possible

If any required field may be undefined:
return FAIL

Output format:

STATUS: PASS or FAIL

ISSUES:
- ...

HINTS:
- ...
"""

if st.button("generate session"):
    if not api_key:
        st.warning("Please enter API key")
        st.stop()
    frontend_model = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key
    )
    messages = [
        ("system",frontend_prompt),
        ("human","Generate a login frontend")
    ]

    response = frontend_model.invoke(messages)

    st.session_state.frontend_code = response.content

if st.session_state.frontend_code:
    st.subheader("FrontEnd Code")
    if not api_key:
        st.warning("Please enter API key")
        st.stop()
    st.code(
        st.session_state.frontend_code,
        language="html"
    )

    user_code = st.text_area(
        "write backed code",
        height=300
    )

    if st.button("submit your code"):
        checker_model = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=api_key
        )

        checker_messages = [
            ("system", checker_prompt),
            ("human", f"""
FRONTEND:
{st.session_state.frontend_code}

BACKEND:
{user_code}
""")
        ]

        feedback = checker_model.invoke(checker_messages)
        st.session_state.feedback = feedback.content

if st.session_state.feedback:
    st.subheader("tester feedback :-")
    st.write(st.session_state.feedback)