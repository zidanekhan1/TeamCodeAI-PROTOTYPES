from langchain_groq import ChatGroq
import subprocess
import streamlit as st
import os
from scenario import scenarios

if "problem_generated" not in st.session_state:
    st.session_state.problem_generated = False

if "game_started" not in st.session_state:
    st.session_state.game_started = False

os.makedirs(
    "temp_project",
    exist_ok=True
)



st.set_page_config("TeamCodeAI v4")

st.sidebar.subheader("Options")
st.sidebar.write("Paste your api key below:")
api = st.sidebar.text_input("",type="password")

selected_problem = st.sidebar.selectbox(
    "choose the problem",
    scenarios,
    format_func=lambda x: x["title"]
)


frontend_prompt = """
You are a frontend engineer working in a software team.

Your task:
Generate ONLY the frontend code file based on the provided project requirements.

IMPORTANT:
- Output ONLY raw code.
- No explanations.
- No markdown.
- No ``` blocks.

Rules:
- Generate HTML + JavaScript only.
- Use fetch() for API communication.
- Keep code clean and realistic.
- Include:
    - UI elements
    - API requests
    - result handling
- Frontend MUST strictly follow the provided project specification.
- Expected request/response fields MUST match the specification exactly.
"""

auth_prompt = """
You are an authentication engineer working in a software team.

Your task:
Generate ONLY the auth.py helper module.

IMPORTANT:
- Output ONLY raw Python code.
- No explanations.
- No markdown.
- No ``` blocks.

Rules:
- This file is NOT the main FastAPI app.
- Another developer will later create main.py.
- Your auth.py must be importable and reusable.
- Generate helper logic that can be connected
  to both frontend requirements and backend routes.

Include:
- request/response models if needed
- fake database
- reusable authentication functions
- helper utilities

DO NOT:
- create FastAPI app instance
- create API routes
- create @app.post decorators

Your job is ONLY to generate reusable
authentication/business logic.

The generated code should help another
developer easily build the final backend.
"""

if not "frontend_code" in st.session_state:
    st.session_state.frontend_code = None

if not "auth_code" in st.session_state:
    st.session_state.auth_code = None

generator = st.button("generate a problem")

if generator:
    if not api:
        st.error("NO API KEY")
        st.stop()
    model_frontend = ChatGroq(model="llama-3.3-70b-versatile",api_key=api)
    message_front = [
        ("system",frontend_prompt),
        ("human",f"""generate frontend for this project:\n
         {selected_problem["prompt"]}
         
         """)
    ]
    frontend_generation = model_frontend.invoke(message_front)
    st.session_state.frontend_code = frontend_generation.content

    with open(
        "temp_project/frontend.html",
        "w"
    ) as f:
        f.write(st.session_state.frontend_code)

    model_auth = ChatGroq(model="openai/gpt-oss-20b",api_key=api)
    messages_auth = [
        ("system",auth_prompt),
        ("human",f"""generate auth for this project:\n
         {selected_problem["prompt"]}
         
         """)
    ]
    auth_gen = model_auth.invoke(messages_auth)
    st.session_state.auth_code = auth_gen.content

    with open(
        "temp_project/auth.py",
        "w"
    ) as f:
        f.write(st.session_state.auth_code)
    st.session_state.problem_generated = True

if st.button("start game"):
    st.session_state.game_started = True

if st.session_state.game_started:

    default_code = '''print("hello world")'''

    user_code = st.text_area(
        "write code",
        height=300,
        value=default_code
    )

    if st.button("submit"):

        with open(
            "temp_project/backend.py",
            "w"
        ) as f:

            f.write(user_code)

        result = subprocess.run(
    ["../venv/Scripts/python.exe", "backend.py"],
    capture_output=True,
    text=True,
    cwd="temp_project",
    timeout=5
)

        st.subheader("OUTPUT")

        if result.stdout:
            st.code(result.stdout)

        if result.stderr:
            st.error("ERRORS:")
            st.code(result.stderr)


st.sidebar.subheader("project folders")
project_files = os.listdir("temp_project")
selected_file = st.sidebar.selectbox(
    "Open File",
    project_files
)



if selected_file:
    with open(
        f"temp_project/{selected_file}",
        "r",
        encoding="utf-8"
    ) as f:
        file_content = f.read()

    st.subheader(selected_file)
    st.code(file_content)



