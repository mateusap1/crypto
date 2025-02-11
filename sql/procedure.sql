CREATE OR REPLACE PROCEDURE atualizar_sentimentos ()
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Sentimentos_Notícias
    SET sentimento = CASE
        WHEN score_sentimento > 0.5 THEN 'Positivo'
        WHEN score_sentimento < -0.5 THEN 'Negativo'
        ELSE 'Neutro'
    END;
END;
$$;

-- CALL atualizar_sentimentos();