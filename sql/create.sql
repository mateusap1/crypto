-- Tabela Criptomoedas
CREATE TABLE Criptomoedas (
    id_cripto SERIAL PRIMARY KEY, -- Identificador único da criptomoeda
    nome VARCHAR(50) NOT NULL, -- Nome da criptomoeda
    simbolo VARCHAR(10) NOT NULL, -- Símbolo da criptomoeda (ex.: BTC, ETH)
    descricao TEXT, -- Descrição da criptomoeda
    mercado VARCHAR(50) -- Nome do mercado onde a criptomoeda é negociada
);

COMMENT ON TABLE Criptomoedas IS 'Tabela que armazena informações sobre criptomoedas, incluindo nome, símbolo e mercado de negociação.';
COMMENT ON COLUMN Criptomoedas.id_cripto IS 'Identificador único da criptomoeda';
COMMENT ON COLUMN Criptomoedas.nome IS 'Nome da criptomoeda';
COMMENT ON COLUMN Criptomoedas.simbolo IS 'Símbolo da criptomoeda (ex.: BTC, ETH)';
COMMENT ON COLUMN Criptomoedas.descricao IS 'Descrição da criptomoeda';
COMMENT ON COLUMN Criptomoedas.mercado IS 'Nome do mercado onde a criptomoeda é negociada';

-- Tabela Cotações
CREATE TABLE Cotações (
    id_cotacao SERIAL PRIMARY KEY, -- Identificador único da cotação
    id_cripto INT REFERENCES Criptomoedas (id_cripto), -- Referência à criptomoeda
    data_hora TIMESTAMP NOT NULL, -- Data e hora da cotação
    preco DECIMAL(18, 8) NOT NULL, -- Preço da criptomoeda
    volume DECIMAL(18, 2), -- Volume negociado
    market_cap DECIMAL(18, 2), -- Capitalização de mercado
    variacao DECIMAL(5, 2) -- Variação percentual do preço
);

COMMENT ON TABLE Cotações IS 'Tabela que armazena informações sobre cotações das criptomoedas, incluindo preço, volume e market cap.';
COMMENT ON COLUMN Cotações.id_cotacao IS 'Identificador único da cotação';
COMMENT ON COLUMN Cotações.id_cripto IS 'Referência à criptomoeda';
COMMENT ON COLUMN Cotações.data_hora IS 'Data e hora da cotação';
COMMENT ON COLUMN Cotações.preco IS 'Preço da criptomoeda';
COMMENT ON COLUMN Cotações.volume IS 'Volume negociado';
COMMENT ON COLUMN Cotações.market_cap IS 'Capitalização de mercado';
COMMENT ON COLUMN Cotações.variacao IS 'Variação percentual do preço';

-- Tabela Notícias
CREATE TABLE Notícias (
    id_noticia SERIAL PRIMARY KEY, -- Identificador único da notícia
    id_cripto INT REFERENCES Criptomoedas (id_cripto), -- Referência à criptomoeda
    data_publicacao DATE NOT NULL, -- Data de publicação da notícia
    tema VARCHAR(50), -- Tema principal da notícia
    noticia TEXT NOT NULL, -- Texto completo da notícia
    fonte VARCHAR(100) -- Fonte da notícia (ex.: Bloomberg, CoinDesk)
);

COMMENT ON TABLE Notícias IS 'Tabela que armazena notícias relacionadas às criptomoedas.';
COMMENT ON COLUMN Notícias.id_noticia IS 'Identificador único da notícia';
COMMENT ON COLUMN Notícias.id_cripto IS 'Referência à criptomoeda';
COMMENT ON COLUMN Notícias.data_publicacao IS 'Data de publicação da notícia';
COMMENT ON COLUMN Notícias.tema IS 'Tema principal da notícia';
COMMENT ON COLUMN Notícias.noticia IS 'Texto completo da notícia';
COMMENT ON COLUMN Notícias.fonte IS 'Fonte da notícia (ex.: Bloomberg, CoinDesk)';

-- Tabela Usuários
CREATE TABLE Usuarios (
    id_usuario SERIAL PRIMARY KEY, -- Identificador único do usuário
    nome VARCHAR(100) NOT NULL, -- Nome do usuário
    email VARCHAR(100) UNIQUE NOT NULL, -- Email do usuário (deve ser único)
    senha VARCHAR(255) NOT NULL, -- Senha do usuário (criptografada)
    admin_flag BOOLEAN DEFAULT FALSE -- Indica se o usuário é administrador
);

COMMENT ON TABLE Usuarios IS 'Tabela que registra os usuários do sistema, incluindo permissões administrativas.';
COMMENT ON COLUMN Usuarios.id_usuario IS 'Identificador único do usuário';
COMMENT ON COLUMN Usuarios.nome IS 'Nome do usuário';
COMMENT ON COLUMN Usuarios.email IS 'Email do usuário (deve ser único)';
COMMENT ON COLUMN Usuarios.senha IS 'Senha do usuário (criptografada)';
COMMENT ON COLUMN Usuarios.admin_flag IS 'Indica se o usuário é administrador';


-- Tabela Sentimentos de Notícias
CREATE TABLE Sentimentos_Notícias (
    id_sentimento SERIAL PRIMARY KEY, -- Identificador único do sentimento
    id_noticia INT REFERENCES Notícias (id_noticia), -- Referência à notícia
    id_usuario INT REFERENCES Usuarios (id_usuario), -- Referência ao usuário
    sentimento VARCHAR(20), -- Classificação do sentimento (positivo, neutro, negativo)
    score_sentimento DECIMAL(5, 2) -- Escore numérico do sentimento (-1 a 1)
);

COMMENT ON TABLE Sentimentos_Notícias IS 'Tabela que armazena os sentimentos associados às notícias sobre criptomoedas, incluindo quem atribuiu o sentimento.';
COMMENT ON COLUMN Sentimentos_Notícias.id_sentimento IS 'Identificador único do sentimento';
COMMENT ON COLUMN Sentimentos_Notícias.id_noticia IS 'Referência à notícia';
COMMENT ON COLUMN Sentimentos_Notícias.id_usuario IS 'Referência ao usuário que atribuiu o sentimento';
COMMENT ON COLUMN Sentimentos_Notícias.sentimento IS 'Classificação do sentimento (positivo, neutro, negativo)';
COMMENT ON COLUMN Sentimentos_Notícias.score_sentimento IS 'Escore numérico do sentimento (-1 a 1)';

-- Tabela Transações de Mercado
CREATE TABLE Transações_Mercado (
    id_transacao SERIAL PRIMARY KEY, -- Identificador único da transação
    id_cripto INT REFERENCES Criptomoedas (id_cripto), -- Referência à criptomoeda
    data_hora TIMESTAMP NOT NULL, -- Data e hora da transação
    tipo VARCHAR(20) NOT NULL, -- Tipo da transação (compra, venda)
    quantidade DECIMAL(18, 8) NOT NULL, -- Quantidade negociada
    preco_unitario DECIMAL(18, 8) NOT NULL -- Preço unitário da criptomoeda
);

COMMENT ON TABLE Transações_Mercado IS 'Tabela que registra as transações realizadas no mercado de criptomoedas.';
COMMENT ON COLUMN Transações_Mercado.id_transacao IS 'Identificador único da transação';
COMMENT ON COLUMN Transações_Mercado.id_cripto IS 'Referência à criptomoeda';
COMMENT ON COLUMN Transações_Mercado.data_hora IS 'Data e hora da transação';
COMMENT ON COLUMN Transações_Mercado.tipo IS 'Tipo da transação (compra, venda)';
COMMENT ON COLUMN Transações_Mercado.quantidade IS 'Quantidade negociada';
COMMENT ON COLUMN Transações_Mercado.preco_unitario IS 'Preço unitário da criptomoeda';

-- Tabela Ordens de Compra/Venda
CREATE TABLE Ordens (
    id_ordem SERIAL PRIMARY KEY, -- Identificador único da ordem
    id_cripto INT REFERENCES Criptomoedas (id_cripto), -- Referência à criptomoeda
    tipo VARCHAR(20) NOT NULL, -- Tipo da ordem (compra, venda)
    quantidade DECIMAL(18, 8) NOT NULL, -- Quantidade desejada
    preco_limite DECIMAL(18, 8) NOT NULL -- Preço limite da ordem
);

COMMENT ON TABLE Ordens IS 'Tabela que registra as ordens de compra ou venda de criptomoedas.';
COMMENT ON COLUMN Ordens.id_ordem IS 'Identificador único da ordem';
COMMENT ON COLUMN Ordens.id_cripto IS 'Referência à criptomoeda';
COMMENT ON COLUMN Ordens.tipo IS 'Tipo da ordem (compra, venda)';
COMMENT ON COLUMN Ordens.quantidade IS 'Quantidade desejada';
COMMENT ON COLUMN Ordens.preco_limite IS 'Preço limite da ordem';

-- Tabela Tendências de Preço
CREATE TABLE Tendências_Preço (
    id_tendencia SERIAL PRIMARY KEY, -- Identificador único da tendência
    id_cripto INT REFERENCES Criptomoedas (id_cripto), -- Referência à criptomoeda
    periodo VARCHAR(20), -- Período analisado (ex.: 24h, 7d)
    variacao_preco DECIMAL(5, 2), -- Variação percentual do preço
    tendencia VARCHAR(20) -- Classificação da tendência (alta, baixa, estável)
);

COMMENT ON TABLE Tendências_Preço IS 'Tabela que armazena informações sobre tendências de preços de criptomoedas.';
COMMENT ON COLUMN Tendências_Preço.id_tendencia IS 'Identificador único da tendência';
COMMENT ON COLUMN Tendências_Preço.id_cripto IS 'Referência à criptomoeda';
COMMENT ON COLUMN Tendências_Preço.periodo IS 'Período analisado (ex.: 24h, 7d)';
COMMENT ON COLUMN Tendências_Preço.variacao_preco IS 'Variação percentual do preço';
COMMENT ON COLUMN Tendências_Preço.tendencia IS 'Classificação da tendência (alta, baixa, estável)';

-- Tabela Dados Externos
CREATE TABLE Dados_Externos (
    id_dado SERIAL PRIMARY KEY, -- Identificador único do dado externo
    descricao TEXT, -- Descrição do fator externo (ex.: taxa de juros)
    data_hora TIMESTAMP NOT NULL, -- Data e hora da coleta
    valor DECIMAL(18, 8) -- Valor do fator externo
);

COMMENT ON TABLE Dados_Externos IS 'Tabela que armazena dados externos que podem impactar o mercado de criptomoedas.';
COMMENT ON COLUMN Dados_Externos.id_dado IS 'Identificador único do dado externo';
COMMENT ON COLUMN Dados_Externos.descricao IS 'Descrição do fator externo (ex.: taxa de juros)';
COMMENT ON COLUMN Dados_Externos.data_hora IS 'Data e hora da coleta';
COMMENT ON COLUMN Dados_Externos.valor IS 'Valor do fator externo';

-- Tabela Imagens de Criptomoedas
CREATE TABLE Imagens_Criptomoedas (
    id_imagem SERIAL PRIMARY KEY, -- Identificador único da imagem
    id_cripto INT REFERENCES Criptomoedas (id_cripto), -- Referência à criptomoeda correspondente
    tipo VARCHAR(50) NOT NULL, -- Tipo da imagem (ex.: logo, ícone)
    conteudo BYTEA NOT NULL, -- Conteúdo da imagem armazenado como binário
    data_upload TIMESTAMP NOT NULL -- Data de upload da imagem
);

COMMENT ON TABLE Imagens_Criptomoedas IS 'Tabela que armazena imagens relacionadas às criptomoedas, como logos ou ícones.';
COMMENT ON COLUMN Imagens_Criptomoedas.id_imagem IS 'Identificador único da imagem';
COMMENT ON COLUMN Imagens_Criptomoedas.id_cripto IS 'Referência à criptomoeda correspondente';
COMMENT ON COLUMN Imagens_Criptomoedas.tipo IS 'Tipo da imagem (ex.: logo, ícone)';
COMMENT ON COLUMN Imagens_Criptomoedas.conteudo IS 'Conteúdo da imagem armazenado como binário';
COMMENT ON COLUMN Imagens_Criptomoedas.data_upload IS 'Data de upload da imagem';