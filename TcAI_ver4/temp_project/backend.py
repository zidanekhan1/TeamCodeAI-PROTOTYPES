from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from auth import (
    LoginRequest,
    LoginResponse,
    login_user,
    get_current_user
)

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):

    try:
        response = login_user(request)

        return response

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )


@app.get("/dashboard")
async def dashboard(token: str):

    user = get_current_user(token)

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return {
        "message": f"Welcome {user['name']}"
    }


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )