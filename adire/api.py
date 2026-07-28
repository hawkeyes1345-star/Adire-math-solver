from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import UploadFile, File
from adire.ocr import image_to_latex
import shutil, tempfile, os
from fastapi.responses import StreamingResponse
from adire.normalize import parse, make_key
from adire.solver import solve
from adire.steps import build_steps
from adire.llm import explain_stream
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

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    # save the uploaded image to a temp file, OCR it, delete it
    suffix = os.path.splitext(file.filename)[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        result = image_to_latex(tmp_path)
    finally:
        os.remove(tmp_path)
    return result

@app.post("/explain_stream")
def explain_stream_endpoint(body: Problem):
    """Stream the explanation token-by-token."""
    info = make_key(body.latex)
    obj = parse(body.latex)
    answer = solve(obj, info["task"])
    steps = build_steps(obj, info["task"], answer)

    def generate():
        for chunk in explain_stream(body.latex, answer, steps):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")