from fastapi import FastAPI
import uvicorn
from api import main_router
# C:\\Users\\Lenovo\\Desktop\\texts\\Весна.txt
app = FastAPI()
app.include_router(main_router)
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True,
    )