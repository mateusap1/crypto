import psycopg2
import datetime
import dotenv
import os
from typing import List, Tuple, Union


class Database:
    def __init__(self, database_url: str):
        self.conn = psycopg2.connect(database_url)

    def query(self, query: str, args: Tuple = ()) -> List[tuple]:
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, args)
                result = cursor.fetchall()
                return result
            except Exception as e:
                self.conn.rollback()
                raise e

    def execute(
        self, query: str, args: Tuple = (), fetch: bool = False
    ) -> Union[List[tuple], None]:
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, args)
                self.conn.commit()
                if fetch:
                    return cursor.fetchall()
            except Exception as e:
                self.conn.rollback()
                raise e

    def enforce_only(self, value: List[tuple]):
        if len(value) != 1:
            raise ValueError("Enforce only validation failure.")
        return value[0][0]

    def close(self):
        if self.conn:
            self.conn.close()

    # --- CRUD Notícias and Sentimentos ---

    def insert_noticia(
        self,
        id_cripto: int,
        data_publicacao: datetime.date,
        tema: str,
        noticia: str,
        fonte: str,
    ) -> int:
        query = """
            INSERT INTO Notícias (id_cripto, data_publicacao, tema, noticia, fonte)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_noticia;
        """
        result = self.execute(
            query, (id_cripto, data_publicacao, tema, noticia, fonte), fetch=True
        )
        return self.enforce_only(result)

    def atualizar_noticia(
        self,
        id_noticia: int,
        id_cripto: int,
        data_publicacao: datetime.date,
        tema: str,
        noticia: str,
        fonte: str,
    ):
        query = """
            UPDATE Notícias
            SET id_cripto = %s, data_publicacao = %s, tema = %s, noticia = %s, fonte = %s
            WHERE id_noticia = %s;
        """
        self.execute(
            query, (id_cripto, data_publicacao, tema, noticia, fonte, id_noticia)
        )

    def inserir_sentimento(
        self, id_noticia: int, id_usuario: int, sentimento: str, score_sentimento: float
    ) -> int:
        query = """
            INSERT INTO Sentimentos_Notícias (id_noticia, id_usuario, sentimento, score_sentimento)
            VALUES (%s, %s, %s, %s)
            RETURNING id_sentimento;
        """
        result = self.execute(
            query, (id_noticia, id_usuario, sentimento, score_sentimento), fetch=True
        )
        return self.enforce_only(result)

    def excluir_sentimento(self, id_sentimento: int):
        # Excluir sentimentos relacionados
        query_sentimentos = "DELETE FROM Sentimentos_Notícias WHERE id_sentimento = %s;"
        self.execute(query_sentimentos, (id_sentimento,))

    def listar_noticias_por_criptomoeda(self, id_cripto: int) -> List[dict]:
        query = """
            SELECT N.id_noticia, N.data_publicacao, N.tema, N.noticia, N.fonte,
                   U.nome AS usuario, S.sentimento, S.score_sentimento
            FROM Notícias N
            JOIN Sentimentos_Notícias S ON N.id_noticia = S.id_noticia
            JOIN Usuarios U ON S.id_usuario = U.id_usuario
            WHERE N.id_cripto = %s;
        """
        result = self.query(query, (id_cripto,))
        noticias = []
        for row in result:
            (
                id_noticia,
                data_publicacao,
                tema,
                noticia,
                fonte,
                usuario,
                sentimento,
                score,
            ) = row
            noticias.append(
                {
                    "id_noticia": id_noticia,
                    "data_publicacao": data_publicacao,
                    "tema": tema,
                    "noticia": noticia,
                    "fonte": fonte,
                    "usuario": usuario,
                    "sentimento": sentimento,
                    "score_sentimento": score,
                }
            )
        return noticias

    def atualizar_sentimento(
        self,
        id_sentimento: int,
        id_usuario: int,
        novo_sentimento: str,
        novo_score: float,
    ):
        query = """
            UPDATE Sentimentos_Notícias
            SET id_usuario = %s, sentimento = %s, score_sentimento = %s
            WHERE id_sentimento = %s;
        """
        self.execute(query, (id_usuario, novo_sentimento, novo_score, id_sentimento))

    def excluir_noticia(self, id_noticia: int):
        # Excluir sentimentos relacionados
        query_sentimentos = "DELETE FROM Sentimentos_Notícias WHERE id_noticia = %s;"
        self.execute(query_sentimentos, (id_noticia,))
        # Excluir notícia
        query_noticia = "DELETE FROM Notícias WHERE id_noticia = %s;"
        self.execute(query_noticia, (id_noticia,))

    def listar_noticias(self) -> List[dict]:
        """
        List all news records with an aggregation of the sentiments.
        Returns a list of dictionaries with the news details,
        an array of associated sentiments, and the average sentiment score.
        """
        query = "SELECT * FROM Todas_Notícias ORDER BY data_publicacao DESC;"
        result = self.query(query)
        noticias = []
        for row in result:
            (
                id_noticia,
                id_cripto,
                data_publicacao,
                tema,
                noticia,
                fonte,
                score_medio,
            ) = row
            noticias.append(
                {
                    "id_noticia": id_noticia,
                    "id_cripto": id_cripto,
                    "data_publicacao": data_publicacao,
                    "tema": tema,
                    "noticia": noticia,
                    "fonte": fonte,
                    "score_medio": score_medio,
                }
            )
        return noticias

    def listar_sentimentos_por_noticia(self, id_noticia: int) -> List[dict]:
        """
        List all sentiment entries (with user information) for a given news item.
        """
        query = """
            SELECT S.id_sentimento, U.id_usuario, U.nome AS usuario, S.sentimento, S.score_sentimento
            FROM Sentimentos_Notícias S
            JOIN Usuarios U ON S.id_usuario = U.id_usuario
            WHERE S.id_noticia = %s;
        """
        result = self.query(query, (id_noticia,))
        sentimentos = []
        for row in result:
            id_sentimento, id_usuario, usuario, sentimento, score_sentimento = row
            sentimentos.append(
                {
                    "id_sentimento": id_sentimento,
                    "id_usuario": id_usuario,
                    "usuario": usuario,
                    "sentimento": sentimento,
                    "score_sentimento": score_sentimento,
                }
            )
        return sentimentos

    # --- CRUD for Criptomoedas ---

    def inserir_criptomoeda(
        self, nome: str, simbolo: str, descricao: str, mercado: str
    ) -> int:
        query = """
            INSERT INTO Criptomoedas (nome, simbolo, descricao, mercado)
            VALUES (%s, %s, %s, %s)
            RETURNING id_cripto;
        """
        result = self.execute(query, (nome, simbolo, descricao, mercado), fetch=True)
        return self.enforce_only(result)

    def listar_criptomoedas(self) -> List[dict]:
        query = "SELECT id_cripto, nome, simbolo, descricao, mercado FROM Criptomoedas ORDER BY nome;"
        result = self.query(query)
        cryptos = []
        for row in result:
            id_cripto, nome, simbolo, descricao, mercado = row
            cryptos.append(
                {
                    "id_cripto": id_cripto,
                    "nome": nome,
                    "simbolo": simbolo,
                    "descricao": descricao,
                    "mercado": mercado,
                }
            )
        return cryptos

    def atualizar_criptomoeda(
        self, id_cripto: int, nome: str, simbolo: str, descricao: str, mercado: str
    ):
        query = """
            UPDATE Criptomoedas
            SET nome = %s, simbolo = %s, descricao = %s, mercado = %s
            WHERE id_cripto = %s;
        """
        self.execute(query, (nome, simbolo, descricao, mercado, id_cripto))

    def excluir_criptomoeda(self, id_cripto: int):
        query = "DELETE FROM Criptomoedas WHERE id_cripto = %s;"
        self.execute(query, (id_cripto,))

    # --- CRUD for Cotações ---

    def inserir_cotacao(
        self,
        id_cripto: int,
        data_hora: datetime.datetime,
        preco: float,
        volume: float,
        market_cap: float,
        variacao: float,
    ) -> int:
        query = """
            INSERT INTO Cotações (id_cripto, data_hora, preco, volume, market_cap, variacao)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_cotacao;
        """
        result = self.execute(
            query,
            (id_cripto, data_hora, preco, volume, market_cap, variacao),
            fetch=True,
        )
        return self.enforce_only(result)

    def listar_cotacoes(self, id_cripto: int) -> List[dict]:
        query = """
            SELECT id_cotacao, data_hora, preco, volume, market_cap, variacao
            FROM Cotações
            WHERE id_cripto = %s
            ORDER BY data_hora DESC;
        """
        result = self.query(query, (id_cripto,))
        cotacoes = []
        for row in result:
            id_cotacao, data_hora, preco, volume, market_cap, variacao = row
            cotacoes.append(
                {
                    "id_cotacao": id_cotacao,
                    "data_hora": data_hora,
                    "preco": preco,
                    "volume": volume,
                    "market_cap": market_cap,
                    "variacao": variacao,
                }
            )
        return cotacoes

    # --- CRUD for Transações de Mercado ---

    def inserir_transacao(
        self,
        id_cripto: int,
        data_hora: datetime.datetime,
        tipo: str,
        quantidade: float,
        preco_unitario: float,
    ) -> int:
        query = """
            INSERT INTO Transações_Mercado (id_cripto, data_hora, tipo, quantidade, preco_unitario)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_transacao;
        """
        result = self.execute(
            query, (id_cripto, data_hora, tipo, quantidade, preco_unitario), fetch=True
        )
        return self.enforce_only(result)

    def listar_transacoes(self, id_cripto: int) -> List[dict]:
        query = """
            SELECT id_transacao, data_hora, tipo, quantidade, preco_unitario
            FROM Transações_Mercado
            WHERE id_cripto = %s
            ORDER BY data_hora DESC;
        """
        result = self.query(query, (id_cripto,))
        transacoes = []
        for row in result:
            id_transacao, data_hora, tipo, quantidade, preco_unitario = row
            transacoes.append(
                {
                    "id_transacao": id_transacao,
                    "data_hora": data_hora,
                    "tipo": tipo,
                    "quantidade": quantidade,
                    "preco_unitario": preco_unitario,
                }
            )
        return transacoes

    # --- CRUD for Ordens ---

    def inserir_ordem(
        self, id_cripto: int, tipo: str, quantidade: float, preco_limite: float
    ) -> int:
        query = """
            INSERT INTO Ordens (id_cripto, tipo, quantidade, preco_limite)
            VALUES (%s, %s, %s, %s)
            RETURNING id_ordem;
        """
        result = self.execute(
            query, (id_cripto, tipo, quantidade, preco_limite), fetch=True
        )
        return self.enforce_only(result)

    def listar_ordens(self, id_cripto: int) -> List[dict]:
        query = """
            SELECT id_ordem, tipo, quantidade, preco_limite
            FROM Ordens
            WHERE id_cripto = %s
            ORDER BY id_ordem DESC;
        """
        result = self.query(query, (id_cripto,))
        ordens = []
        for row in result:
            id_ordem, tipo, quantidade, preco_limite = row
            ordens.append(
                {
                    "id_ordem": id_ordem,
                    "tipo": tipo,
                    "quantidade": quantidade,
                    "preco_limite": preco_limite,
                }
            )
        return ordens

    # --- CRUD for Tendências de Preço ---

    def inserir_tendencia(
        self, id_cripto: int, periodo: str, variacao_preco: float, tendencia: str
    ) -> int:
        query = """
            INSERT INTO Tendências_Preço (id_cripto, periodo, variacao_preco, tendencia)
            VALUES (%s, %s, %s, %s)
            RETURNING id_tendencia;
        """
        result = self.execute(
            query, (id_cripto, periodo, variacao_preco, tendencia), fetch=True
        )
        return self.enforce_only(result)

    def listar_tendencias(self, id_cripto: int) -> List[dict]:
        query = """
            SELECT id_tendencia, periodo, variacao_preco, tendencia
            FROM Tendências_Preço
            WHERE id_cripto = %s
            ORDER BY periodo DESC;
        """
        result = self.query(query, (id_cripto,))
        tendencias = []
        for row in result:
            id_tendencia, periodo, variacao_preco, tendencia = row
            tendencias.append(
                {
                    "id_tendencia": id_tendencia,
                    "periodo": periodo,
                    "variacao_preco": variacao_preco,
                    "tendencia": tendencia,
                }
            )
        return tendencias

    # --- CRUD for Dados Externos ---

    def inserir_dado_externo(
        self, descricao: str, data_hora: datetime.datetime, valor: float
    ) -> int:
        query = """
            INSERT INTO Dados_Externos (descricao, data_hora, valor)
            VALUES (%s, %s, %s)
            RETURNING id_dado;
        """
        result = self.execute(query, (descricao, data_hora, valor), fetch=True)
        return self.enforce_only(result)

    def listar_dados_externos(self) -> List[dict]:
        query = """
            SELECT id_dado, descricao, data_hora, valor
            FROM Dados_Externos
            ORDER BY data_hora DESC;
        """
        result = self.query(query)
        dados = []
        for row in result:
            id_dado, descricao, data_hora, valor = row
            dados.append(
                {
                    "id_dado": id_dado,
                    "descricao": descricao,
                    "data_hora": data_hora,
                    "valor": valor,
                }
            )
        return dados

    # --- CRUD for Imagens de Criptomoedas ---

    def inserir_imagem_criptomoeda(
        self, id_cripto: int, tipo: str, conteudo: bytes, data_upload: datetime.datetime
    ) -> int:
        query = """
            INSERT INTO Imagens_Criptomoedas (id_cripto, tipo, conteudo, data_upload)
            VALUES (%s, %s, %s, %s)
            RETURNING id_imagem;
        """
        result = self.execute(
            query, (id_cripto, tipo, conteudo, data_upload), fetch=True
        )
        return self.enforce_only(result)

    def listar_imagens_criptomoedas(self, id_cripto: int) -> List[dict]:
        query = """
            SELECT id_imagem, tipo, data_upload
            FROM Imagens_Criptomoedas
            WHERE id_cripto = %s
            ORDER BY data_upload DESC;
        """
        result = self.query(query, (id_cripto,))
        imagens = []
        for row in result:
            id_imagem, tipo, data_upload = row
            imagens.append(
                {
                    "id_imagem": id_imagem,
                    "tipo": tipo,
                    "data_upload": data_upload,
                }
            )
        return imagens

    # --- CRUD for Usuários ---

    def inserir_usuario(
        self, nome: str, email: str, senha: str, admin_flag: bool = False
    ) -> int:
        query = """
            INSERT INTO Usuarios (nome, email, senha, admin_flag)
            VALUES (%s, %s, %s, %s)
            RETURNING id_usuario;
        """
        result = self.execute(query, (nome, email, senha, admin_flag), fetch=True)
        return self.enforce_only(result)

    def listar_usuarios(self) -> List[dict]:
        query = (
            "SELECT id_usuario, nome, email, admin_flag FROM Usuarios ORDER BY nome;"
        )
        result = self.query(query)
        usuarios = []
        for row in result:
            id_usuario, nome, email, admin_flag = row
            usuarios.append(
                {
                    "id_usuario": id_usuario,
                    "nome": nome,
                    "email": email,
                    "admin_flag": admin_flag,
                }
            )
        return usuarios

    def atualizar_usuario(
        self, id_usuario: int, nome: str, email: str, senha: str, admin_flag: bool
    ):
        query = """
            UPDATE Usuarios
            SET nome = %s, email = %s, senha = %s, admin_flag = %s
            WHERE id_usuario = %s;
        """
        self.execute(query, (nome, email, senha, admin_flag, id_usuario))

    def excluir_usuario(self, id_usuario: int):
        query = "DELETE FROM Usuarios WHERE id_usuario = %s;"
        self.execute(query, (id_usuario,))

    @staticmethod
    def load():
        dotenv.load_dotenv()
        database_url = os.environ.get("DB_URL")
        if database_url is None:
            raise ValueError("Could not load database: DB_URL not found.")
        return Database(database_url)
