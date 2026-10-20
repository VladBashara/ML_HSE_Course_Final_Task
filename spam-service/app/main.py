from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.model import SpamCascade
from app.eml_parser import parse_eml_bytes

app = FastAPI(title="Spam Cascade API (2-layer)", version="1.0")
clf = SpamCascade()

class TextIn(BaseModel):
    text: str
    sender_domain: str = ""

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/predict")
def predict(p: TextIn):
    meta = {"sender_domain":p.sender_domain,"n_urls":0,"has_url":0,
            "n_digits":sum(c.isdigit() for c in p.text),
            "n_excl":p.text.count("!"),"n_upper":sum(c.isupper() for c in p.text),
            "len":len(p.text)}
    s,l,src = clf.predict([p.text],[meta])
    return {"score":float(s[0]),"label":int(l[0]),"is_spam":bool(l[0]),"source":src[0]}

@app.post("/predict_eml")
async def predict_eml(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".eml"): raise HTTPException(400,"need .eml")
    text, meta = parse_eml_bytes(await file.read())
    if not text: raise HTTPException(400,"empty email")
    s,l,src = clf.predict([text],[meta])
    return {"score":float(s[0]),"label":int(l[0]),"is_spam":bool(l[0]),"source":src[0],"sender_domain":meta["sender_domain"]}
