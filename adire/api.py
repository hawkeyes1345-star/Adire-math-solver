from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from adire.pipeline import solve_problem

app = FastAPI(title="Adire")

# lets the web page (opened as a file) talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Problem(BaseModel):
    latex: str


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/solve")
def solve(body: Problem):
    return solve_problem(body.latex)