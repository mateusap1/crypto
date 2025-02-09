from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, date
from crypto import Database  # Assumes the updated Database class is in crypto.py

app = FastAPI(title="Crypto Wallet/Watcher API")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic models for incoming request bodies ---


class CriptomoedaIn(BaseModel):
    nome: str
    simbolo: str
    descricao: str
    mercado: str


class NoticiaIn(BaseModel):
    id_cripto: int
    data_publicacao: date  # Use date (or datetime, if preferred)
    tema: str
    noticia: str
    fonte: str


class SentimentoIn(BaseModel):
    id_noticia: int
    id_usuario: int
    sentimento: str
    score_sentimento: float


class SentimentoUpdate(BaseModel):
    id_sentimento: int
    id_usuario: int
    novo_sentimento: str
    novo_score: float


class CotacaoIn(BaseModel):
    id_cripto: int
    data_hora: datetime
    preco: float
    volume: float
    market_cap: float
    variacao: float


class TransacaoIn(BaseModel):
    id_cripto: int
    data_hora: datetime
    tipo: str
    quantidade: float
    preco_unitario: float


class OrdemIn(BaseModel):
    id_cripto: int
    tipo: str
    quantidade: float
    preco_limite: float


class TendenciaIn(BaseModel):
    id_cripto: int
    periodo: str
    variacao_preco: float
    tendencia: str


class DadoExternoIn(BaseModel):
    descricao: str
    data_hora: datetime
    valor: float


class UsuarioIn(BaseModel):
    nome: str
    email: str
    senha: str
    admin_flag: bool = False


# --- Endpoints for Notícias and Sentimentos ---


@app.post("/noticias/", summary="Create a new notícia")
def create_noticia(noticia: NoticiaIn):
    db = Database.load()
    try:
        id_noticia = db.insert_noticia(
            noticia.id_cripto,
            noticia.data_publicacao,
            noticia.tema,
            noticia.noticia,
            noticia.fonte,
        )
        return {"id": id_noticia}
    finally:
        db.close()


@app.put("/noticias/{id_noticia}", summary="Update a notícia")
def update_noticia(id_noticia: int, noticia: NoticiaIn):
    db = Database.load()
    try:
        db.atualizar_noticia(
            id_noticia,
            noticia.id_cripto,
            noticia.data_publicacao,
            noticia.tema,
            noticia.noticia,
            noticia.fonte,
        )
        return {"message": "Notícia updated successfully"}
    finally:
        db.close()


@app.post("/sentimentos/", summary="Create a new sentimento for a notícia")
def create_sentimento(sentimento: SentimentoIn):
    db = Database.load()
    try:
        id_sentimento = db.inserir_sentimento(
            sentimento.id_noticia,
            sentimento.id_usuario,
            sentimento.sentimento,
            sentimento.score_sentimento,
        )
        return {"id": id_sentimento}
    finally:
        db.close()


@app.put("/sentimentos/", summary="Update a sentimento for a notícia")
def update_sentimento(sent_update: SentimentoUpdate):
    db = Database.load()
    try:
        db.atualizar_sentimento(
            sent_update.id_sentimento,
            sent_update.id_usuario,
            sent_update.novo_sentimento,
            sent_update.novo_score,
        )
        return {"message": "Sentimento updated successfully"}
    finally:
        db.close()


@app.delete("/sentimentos/{id_noticia}/{id_sentimento}", summary="Delete a sentimento for a notícia")
def delete_sentimento(id_noticia: int, id_sentimento: int):
    db = Database.load()
    try:
        # Make sure you implement this method in your Database class (crypto.py)
        db.excluir_sentimento(id_sentimento)
        return {"message": "Sentimento deleted successfully"}
    finally:
        db.close()


@app.get("/noticias/criptomoeda/{id_cripto}", summary="List notícias for a criptomoeda")
def list_noticias_por_criptomoeda(id_cripto: int):
    db = Database.load()
    try:
        noticias = db.listar_noticias_por_criptomoeda(id_cripto)
        return noticias
    finally:
        db.close()


@app.get("/noticias/", summary="List all notícias with aggregated sentiments")
def list_all_noticias():
    db = Database.load()
    try:
        noticias = db.listar_noticias()
        return noticias
    finally:
        db.close()


@app.get(
    "/noticias/{id_noticia}/sentimentos", summary="List all sentimentos for a notícia"
)
def list_sentimentos_for_noticia(id_noticia: int):
    db = Database.load()
    try:
        sentimentos = db.listar_sentimentos_por_noticia(id_noticia)
        return sentimentos
    finally:
        db.close()


@app.delete("/noticias/{id_noticia}", summary="Delete a notícia")
def delete_noticia(id_noticia: int):
    db = Database.load()
    try:
        db.excluir_noticia(id_noticia)
        return {"message": "Notícia excluída com sucesso"}
    finally:
        db.close()


# --- Endpoints for Criptomoedas ---


@app.post("/criptomoedas/", summary="Create a new criptomoeda")
def create_criptomoeda(cripto: CriptomoedaIn):
    db = Database.load()
    try:
        id_cripto = db.inserir_criptomoeda(
            cripto.nome, cripto.simbolo, cripto.descricao, cripto.mercado
        )
        return {"id": id_cripto}
    finally:
        db.close()


@app.get("/criptomoedas/", summary="List all criptomoedas")
def list_criptomoedas():
    db = Database.load()
    try:
        cryptos = db.listar_criptomoedas()
        return cryptos
    finally:
        db.close()


@app.put("/criptomoedas/{id_cripto}", summary="Update a criptomoeda")
def update_criptomoeda(id_cripto: int, cripto: CriptomoedaIn):
    db = Database.load()
    try:
        db.atualizar_criptomoeda(
            id_cripto, cripto.nome, cripto.simbolo, cripto.descricao, cripto.mercado
        )
        return {"message": "Criptomoeda updated successfully"}
    finally:
        db.close()


@app.delete("/criptomoedas/{id_cripto}", summary="Delete a criptomoeda")
def delete_criptomoeda(id_cripto: int):
    db = Database.load()
    try:
        db.excluir_criptomoeda(id_cripto)
        return {"message": "Criptomoeda deleted successfully"}
    finally:
        db.close()


# --- Endpoints for Cotações ---


@app.post("/cotacoes/", summary="Create a new cotação")
def create_cotacao(cotacao: CotacaoIn):
    db = Database.load()
    try:
        id_cotacao = db.inserir_cotacao(
            cotacao.id_cripto,
            cotacao.data_hora,
            cotacao.preco,
            cotacao.volume,
            cotacao.market_cap,
            cotacao.variacao,
        )
        return {"id": id_cotacao}
    finally:
        db.close()


@app.get("/cotacoes/criptomoeda/{id_cripto}", summary="List cotacoes for a criptomoeda")
def list_cotacoes(id_cripto: int):
    db = Database.load()
    try:
        cotacoes = db.listar_cotacoes(id_cripto)
        return cotacoes
    finally:
        db.close()


# --- Endpoints for Transações de Mercado ---


@app.post("/transacoes/", summary="Create a new transação")
def create_transacao(transacao: TransacaoIn):
    db = Database.load()
    try:
        id_transacao = db.inserir_transacao(
            transacao.id_cripto,
            transacao.data_hora,
            transacao.tipo,
            transacao.quantidade,
            transacao.preco_unitario,
        )
        return {"id": id_transacao}
    finally:
        db.close()


@app.get(
    "/transacoes/criptomoeda/{id_cripto}", summary="List transações for a criptomoeda"
)
def list_transacoes(id_cripto: int):
    db = Database.load()
    try:
        transacoes = db.listar_transacoes(id_cripto)
        return transacoes
    finally:
        db.close()


# --- Endpoints for Ordens ---


@app.post("/ordens/", summary="Create a new ordem")
def create_ordem(ordem: OrdemIn):
    db = Database.load()
    try:
        id_ordem = db.inserir_ordem(
            ordem.id_cripto, ordem.tipo, ordem.quantidade, ordem.preco_limite
        )
        return {"id": id_ordem}
    finally:
        db.close()


@app.get("/ordens/criptomoeda/{id_cripto}", summary="List ordens for a criptomoeda")
def list_ordens(id_cripto: int):
    db = Database.load()
    try:
        ordens = db.listar_ordens(id_cripto)
        return ordens
    finally:
        db.close()


# --- Endpoints for Tendências de Preço ---


@app.post("/tendencias/", summary="Create a new tendência")
def create_tendencia(tendencia: TendenciaIn):
    db = Database.load()
    try:
        id_tendencia = db.inserir_tendencia(
            tendencia.id_cripto,
            tendencia.periodo,
            tendencia.variacao_preco,
            tendencia.tendencia,
        )
        return {"id": id_tendencia}
    finally:
        db.close()


@app.get(
    "/tendencias/criptomoeda/{id_cripto}", summary="List tendências for a criptomoeda"
)
def list_tendencias(id_cripto: int):
    db = Database.load()
    try:
        tendencias = db.listar_tendencias(id_cripto)
        return tendencias
    finally:
        db.close()


# --- Endpoints for Dados Externos ---


@app.post("/dados_externos/", summary="Create a new dado externo")
def create_dado_externo(dado: DadoExternoIn):
    db = Database.load()
    try:
        id_dado = db.inserir_dado_externo(dado.descricao, dado.data_hora, dado.valor)
        return {"id": id_dado}
    finally:
        db.close()


@app.get("/dados_externos/", summary="List all dados externos")
def list_dados_externos():
    db = Database.load()
    try:
        dados = db.listar_dados_externos()
        return dados
    finally:
        db.close()


# --- Endpoints for Imagens de Criptomoedas ---


@app.post("/imagens/criptomoedas/", summary="Upload an image for a criptomoeda")
async def upload_imagem(
    id_cripto: int, tipo: str, data_upload: datetime, file: UploadFile = File(...)
):
    content = await file.read()
    db = Database.load()
    try:
        id_imagem = db.inserir_imagem_criptomoeda(id_cripto, tipo, content, data_upload)
        return {"id": id_imagem}
    finally:
        db.close()


@app.get("/imagens/criptomoedas/{id_cripto}", summary="List images for a criptomoeda")
def list_imagens_criptomoedas(id_cripto: int):
    db = Database.load()
    try:
        imagens = db.listar_imagens_criptomoedas(id_cripto)
        return imagens
    finally:
        db.close()


# --- Endpoints for Usuários ---


@app.post("/usuarios/", summary="Create a new usuário")
def create_usuario(usuario: UsuarioIn):
    db = Database.load()
    try:
        id_usuario = db.inserir_usuario(
            usuario.nome, usuario.email, usuario.senha, usuario.admin_flag
        )
        return {"id": id_usuario}
    finally:
        db.close()


@app.get("/usuarios/", summary="List all usuários")
def list_usuarios():
    db = Database.load()
    try:
        usuarios = db.listar_usuarios()
        return usuarios
    finally:
        db.close()


@app.put("/usuarios/{id_usuario}", summary="Update a usuário")
def update_usuario(id_usuario: int, usuario: UsuarioIn):
    db = Database.load()
    try:
        db.atualizar_usuario(
            id_usuario, usuario.nome, usuario.email, usuario.senha, usuario.admin_flag
        )
        return {"message": "Usuário updated successfully"}
    finally:
        db.close()


@app.delete("/usuarios/{id_usuario}", summary="Delete a usuário")
def delete_usuario(id_usuario: int):
    db = Database.load()
    try:
        db.excluir_usuario(id_usuario)
        return {"message": "Usuário deleted successfully"}
    finally:
        db.close()
