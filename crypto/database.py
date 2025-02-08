from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any

import psycopg2
import datetime
import dotenv
import os


class Database:
    def __init__(self, database_url: str):
        self.conn = psycopg2.connect(database_url)

    def query(self, query: str, args: tuple) -> list[tuple]:
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, args)
                result = cursor.fetchall()

                return result
            except Exception as e:
                self.conn.rollback()
                raise e
            finally:
                cursor.close()
                self.conn.close()

    def execute(self, query: str, args: tuple) -> list[tuple]:
        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query, args)
                result = cursor.fetchall()
                self.conn.commit()

                return result
            except Exception as e:
                self.conn.rollback()
                raise e
            finally:
                cursor.close()
                self.conn.close()

    def enforce_only(self, value: list[tuple]):
        if not len(value) == 1:
            raise ValueError("Enforce only validation failure.")

        return value[0][0]

    def insert_criptomoeda(self, nome: str, simbolo: str, descricao: str) -> int:
        result = self.execute(
            "INSERT INTO criptomoedas (nome, simbolo, descricao) VALUES (%s, %s, %s) RETURNING id;",
            (nome, simbolo, descricao),
        )

        return self.enforce_only(result)

    def insert_noticia(
        self,
        id_cripto: int,
        data_publicacao: datetime.datetime,
        tema: str,
        noticia: str,
        fonte: str,
    ) -> int:
        query = "INSERT INTO Notícias (id_cripto, data_publicacao, tema, noticia, fonte) VALUES (%s, %s, %s, %s, %s) RETURNING id_noticia;"
        result = self.execute(query, (id_cripto, data_publicacao, tema, noticia, fonte))

        return self.enforce_only(result)

    def inserir_sentimento(
        self, id_noticia: int, id_usuario: int, sentimento: str, score_sentimento: float
    ) -> int:
        query = "INSERT INTO sentimentos_noticias (noticia_id, usuario_id, sentimento, score_sentimento) VALUES (%s, %s, %s, %s) RETURNING id;"
        result = self.execute(
            query, (id_noticia, id_usuario, sentimento, score_sentimento)
        )

        return self.enforce_only(result)

    def listar_noticias_por_criptomoeda(self, id_cripto: int) -> int:
        query = "SELECT N.id_noticia, N.tema, N.noticia, U.nome AS usuario, S.sentimento, S.score_sentimento FROM Notícias N JOIN Sentimentos_Notícias S ON N.id_noticia = S.id_noticia JOIN Usuarios U ON S.id_usuario = U.id_usuario WHERE N.id_cripto = %s;"
        result = self.query(query, tuple(id_cripto))

        noticias = []
        for linha in result:
            id_noticia, tema, noticia, usuario, sentimento, score = linha
            noticias.append(
                {
                    "id_noticia": id_noticia,
                    "tema": tema,
                    "noticia": noticia,
                    "usuario": usuario,
                    "sentimento": sentimento,
                    "score_sentimento": score,
                }
            )

        return noticias

    def atualizar_sentimento(
        self, id_noticia: int, id_usuario: int, novo_sentimento: str, novo_score: float
    ):
        query = "UPDATE Sentimentos_Notícias SET sentimento = %s, score_sentimento = %s WHERE id_noticia = %s AND id_usuario = %s;"
        self.execute(query, (novo_sentimento, novo_score, id_noticia, id_usuario))

    def excluir_noticia(self, id_noticia: int):
        # Excluir sentimentos relacionados
        query_sentimentos = "DELETE FROM Sentimentos_Notícias WHERE id_noticia = %s;"
        self.execute(query_sentimentos, tuple(id_noticia))

        # Excluir notícia
        query_noticia = "DELETE FROM Notícias WHERE id_noticia = %s;"
        self.execute(query_noticia, tuple(id_noticia))

    @staticmethod
    def load():
        dotenv.load_dotenv()
        database_url = os.environ.get("DB_URL")
        if database_url is None:
            raise ValueError("Could not load database: DB_URL not found.")

        return Database(database_url)