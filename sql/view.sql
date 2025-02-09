CREATE VIEW Todas_Notícias AS
SELECT
    N.id_noticia,
    N.id_cripto,
    N.data_publicacao,
    N.tema,
    N.noticia,
    N.fonte,
    AVG(S.score_sentimento) as score_medio
FROM Notícias N
LEFT JOIN Sentimentos_Notícias S ON N.id_noticia = S.id_noticia
GROUP BY N.id_noticia;