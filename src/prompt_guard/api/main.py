from fastapi import FastAPI

app = FastAPI(title="PromptGuard API")


@app.get("/")
def read_root():
    return {"message": "Welcome to the PromptGuard API"}
