from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from crypto import Database

app = FastAPI(title="Crypto Wallet/Watcher API")

# Pydantic models for incoming request bodies

class CriptomoedaIn(BaseModel):
    nome: str
    simbolo: str
    descricao: str

class NoticiaIn(BaseModel):
    id_cripto: int
    data_publicacao: datetime  # Use a datetime object (or date, if you prefer)
    tema: str
    noticia: str
    fonte: str

class SentimentoIn(BaseModel):
    id_noticia: int
    id_usuario: int
    sentimento: str
    score_sentimento: float

class SentimentoUpdate(BaseModel):
    id_noticia: int
    id_usuario: int
    novo_sentimento: str
    novo_score: float

# Endpoint to create a new notícia (news item)
@app.post("/noticias/", summary="Create a new notícia")
def create_noticia(noticia: NoticiaIn):
    try:
        db = Database.load()
        id_noticia = db.insert_noticia(
            noticia.id_cripto,
            noticia.data_publicacao,
            noticia.tema,
            noticia.noticia,
            noticia.fonte,
        )
        return {"id": id_noticia}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to create a new sentimento (sentiment) on a notícia
@app.post("/sentimentos/", summary="Create a new sentimento for a notícia")
def create_sentimento(sentimento: SentimentoIn):
    try:
        db = Database.load()
        id_sentimento = db.inserir_sentimento(
            sentimento.id_noticia,
            sentimento.id_usuario,
            sentimento.sentimento,
            sentimento.score_sentimento,
        )
        return {"id": id_sentimento}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to update an existing sentimento (sentiment) for a notícia
@app.put("/sentimentos/", summary="Update a sentimento for a notícia")
def update_sentimento(sent_update: SentimentoUpdate):
    try:
        db = Database.load()
        db.atualizar_sentimento(
            sent_update.id_noticia,
            sent_update.id_usuario,
            sent_update.novo_sentimento,
            sent_update.novo_score,
        )
        return {"message": "Sentimento updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to list notícias for a given criptomoeda
@app.get("/noticias/criptomoeda/{id_cripto}", summary="List notícias for a criptomoeda")
def list_noticias(id_cripto: int):
    try:
        db = Database.load()
        noticias = db.listar_noticias_por_criptomoeda(id_cripto)
        return noticias
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete a notícia (and its related sentimentos)
@app.delete("/noticias/{id_noticia}", summary="Delete a notícia")
def delete_noticia(id_noticia: int):
    try:
        db = Database.load()
        db.excluir_noticia(id_noticia)
        return {"message": "Notícia excluída com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
