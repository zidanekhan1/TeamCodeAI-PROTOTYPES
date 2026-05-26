scenarios = [

    {
        "title": "Basic Login System",

        "prompt": """
Build a login system.

Project Structure:
- frontend.html will be generated separately
- auth.py will contain reusable auth logic
- user will create main.py

Requirements:
- Route: POST /login

Request JSON:
{
    "username": str,
    "password": str
}

Success Response JSON:
{
    "name": str,
    "token": str
}

Behavior:
- frontend should send login request
- auth.py should contain reusable authentication logic
- main.py should connect frontend and auth.py together

Use JSON requests and responses.
"""
    },

    {
        "title": "User Profile Fetch",

        "prompt": """
Build a user profile system.

Project Structure:
- frontend.html will be generated separately
- auth.py may contain helper/user logic
- user will create main.py

Requirements:
- Route: GET /profile

Response JSON:
{
    "username": str,
    "email": str,
    "age": int
}

Behavior:
- frontend fetches profile data
- auth.py contains reusable helper logic
- main.py handles FastAPI routes and integration
"""
    }

]