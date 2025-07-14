import uvicorn

import app

from environment import EnvironmentVariables

backend = app.create_app()


if __name__ == "__main__":
    uvicorn.run(
        "main:backend",
        host=EnvironmentVariables.HOST,
        port=EnvironmentVariables.PORT,
        reload=True,
        timeout_keep_alive=5 * 60,
    )
