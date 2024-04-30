from app.core.application import create_api, create_mock_api
import os
import uvicorn

is_mock = os.getenv("MOCK_API", False)

if is_mock:
    api = create_mock_api()
else:
    api = create_api()


if __name__ == "__main__":
    uvicorn.run("main:api")
