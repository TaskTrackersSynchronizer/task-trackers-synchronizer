from app.core.application import create_api, create_mock_api
import os
import uvicorn

is_mock = os.getenv("MOCK_API", False)

if is_mock:
    api = create_mock_api()
else:
    api = create_api()


# # if __name__ == "__main__":
# def start():
#     """Launched with `poetry run start` at root level"""
#     uvicorn.run("app:main", host="0.0.0.0", port=8000, reload=True)


# if __name__ == "main":
#     uvicorn.run("main:app")
