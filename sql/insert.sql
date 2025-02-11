-- Criptomoedas
INSERT INTO Criptomoedas (id_cripto, nome, simbolo, descricao, mercado)
VALUES 
(1, 'Bitcoin', 'BTC', 'Primeira criptomoeda descentralizada', 'Binance'),
(2, 'Ethereum', 'ETH', 'Plataforma de contratos inteligentes', 'Coinbase'),
(3, 'Cardano', 'ADA', 'Criptomoeda de terceira geração focada em escalabilidade', 'Kraken'),
(4, 'Solana', 'SOL', 'Plataforma blockchain para aplicativos descentralizados', 'Binance'),
(5, 'Ripple', 'XRP', 'Criptomoeda para pagamentos digitais', 'Bitstamp');

-- Cotações
INSERT INTO Cotações (id_cripto, data_hora, preco, volume, market_cap, variacao)
VALUES 
(1, '2025-01-01 12:00:00', 27000.50, 1000000.00, 500000000.00, 2.5),
(2, '2025-01-01 12:00:00', 1900.75, 500000.00, 250000000.00, -1.8),
(3, '2025-01-01 12:00:00', 0.40, 200000.00, 12000000.00, 5.2),
(4, '2025-01-01 12:00:00', 23.70, 300000.00, 70000000.00, -0.5),
(5, '2025-01-01 12:00:00', 0.50, 150000.00, 20000000.00, 1.2);

-- Transações
INSERT INTO Transações_Mercado (id_cripto, data_hora, tipo, quantidade, preco_unitario)
VALUES 
(1, '2025-01-01 12:30:00', 'Compra', 0.1, 27000.50),
(2, '2025-01-01 13:00:00', 'Venda', 0.2, 1900.75),
(3, '2025-01-01 13:30:00', 'Compra', 100, 0.40),
(4, '2025-01-01 14:00:00', 'Venda', 50, 23.70),
(5, '2025-01-01 14:30:00', 'Compra', 200, 0.50);

-- Ordens
INSERT INTO Ordens (id_cripto, tipo, quantidade, preco_limite)
VALUES 
(1, 'Compra', 0.05, 25000.00),
(2, 'Venda', 0.10, 2000.00),
(3, 'Compra', 200, 0.35),
(4, 'Venda', 50, 25.00),
(5, 'Compra', 100, 0.45);

-- Tendências
INSERT INTO Tendências_Preço (id_cripto, periodo, variacao_preco, tendencia)
VALUES 
(1, '24h', 2.5, 'Alta'),
(2, '24h', -1.8, 'Baixa'),
(3, '24h', 5.2, 'Alta'),
(4, '24h', -0.5, 'Estável'),
(5, '24h', 1.2, 'Alta');

-- Dados Externos
INSERT INTO Dados_Externos (descricao, data_hora, valor)
VALUES 
('Taxa de juros dos EUA', '2025-01-01 09:00:00', 0.05),
('Índice de inflação global', '2025-01-01 09:00:00', 3.2),
('Preço do ouro', '2025-01-01 09:00:00', 1850.00),
('Preço do barril de petróleo', '2025-01-01 09:00:00', 75.50),
('Taxa de câmbio USD/EUR', '2025-01-01 09:00:00', 1.10);

-- Notícias
INSERT INTO Notícias (id_cripto, data_publicacao, tema, noticia, fonte)
VALUES 
(1, '2025-01-01', 'Regulação', 'Bitcoin será regulamentado em breve.', 'CoinDesk'),
(2, '2025-01-01', 'Adoção', 'Ethereum será aceito como pagamento em grandes varejistas.', 'Bloomberg'),
(3, '2025-01-01', 'Tecnologia', 'Cardano anuncia atualização para maior escalabilidade.', 'CryptoNews'),
(4, '2025-01-01', 'Desempenho', 'Solana apresenta alta no volume de transações.', 'Kraken Blog'),
(5, '2025-01-01', 'Parceria', 'Ripple firma parceria com bancos europeus.', 'Bitstamp Insights');

-- Usuários
INSERT INTO Usuarios (nome, email, senha, admin_flag)
VALUES 
('João Silva', 'joao@gmail.com', 'senha123', TRUE),
('Maria Oliveira', 'maria@gmail.com', 'senha123', FALSE),
('Carlos Santos', 'carlos@gmail.com', 'senha123', FALSE),
('Ana Costa', 'ana@gmail.com', 'senha123', FALSE),
('Pedro Almeida', 'pedro@gmail.com', 'senha123', TRUE);

-- Sentimentos
INSERT INTO Sentimentos_Notícias (id_noticia, id_usuario, sentimento, score_sentimento)
VALUES 
(1, 1, 'Positivo', 0.8),
(2, 2, 'Neutro', 0.0),
(3, 3, 'Positivo', 0.6),
(4, 4, 'Negativo', -0.4),
(5, 5, 'Positivo', 0.9);
