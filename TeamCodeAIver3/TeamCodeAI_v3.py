import streamlit as st
import subprocess
from langchain_groq import ChatGroq

st.set_page_config(page_title="TeamCodeAI v3")

st.title("TeamCodeAI v3")
st.subheader("Python Code Runner")

st.sidebar.text("API KEYS")
api = st.sidebar.text_input("enter api key",type="password")
st.sidebar.info("STILL A TEST VERSION!!")

frontend_prompt = """
You are a frontend engineer.

Generate ONLY a simple HTML + JavaScript frontend snippet that can be 
connected by the backend code.

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

if st.button("Generate test code"):
    if not api:
        st.error("ENTER THE FUCKING API KEY YOU WORTHLESS WIMP GODDAMN FREELOADER")
        st.stop()
    model = ChatGroq(model="llama-3.3-70b-versatile",api_key=api)
    messages = [
        ("system",frontend_prompt),
        ("human","Generate a login frontend")
    ]
    result = model.invoke(messages)
    result_code = result.content

    if result_code:
        with open("frontend.py","w") as file:
            file.write(result_code)
    st.subheader("frontend code")
    st.write(result_code)


default_code = """print("hello world)"""

user_code=st.text_area("write the goddamn code",height=300,value=default_code)

if st.button("Run Code"):
    with open("main.py","w") as file:
        file.write(user_code)

    result = subprocess.run(
        ["python","main.py"],
        capture_output=True,
        text=True
    )

    st.subheader("OutPut")

    if result.stdout:
        st.code(result.stdout)
    if result.stderr:
        st.subheader("Errors")
        st.code(result.stderr)

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

Frontend may conditionally access fields.

Do NOT require response fields that are only
used inside conditional branches unless the
backend path can actually trigger that branch.

Analyze frontend logic carefully before deciding FAIL.

Output format:

STATUS: PASS or FAIL

ISSUES:
- ...

HINTS:
- ...
"""

if st.button("check your answer romeo"):
    if not api:
        st.error("ENTER THE FUCKING API KEY YOU WORTHLESS WIMP GODDAMN FREELOADER")
        st.stop()
    checker_model = ChatGroq(model="openai/gpt-oss-20b",api_key=api)
    messages = [
        ("system",checker_prompt),
        ("human",f"""
FRONTEND:
{result_code}

BACKEND:
{user_code}
""")
    ]
    feedback = checker_model.invoke(messages)
    st.write(feedback.content)

