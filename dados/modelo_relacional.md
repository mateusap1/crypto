# BD - Criptos

## 1. Criptomoedas

**Descrição:** Representa as moedas digitais disponíveis no sistema.

### Atributos:
- **id_cripto (PK):** Identificador único.
- **nome:** Nome da criptomoeda.
- **simbolo:** Símbolo (ex.: BTC, ETH).
- **descricao:** Descrição breve.
- **mercado:** Nome do mercado (ex.: Binance).

---

## 2. Cotações

**Descrição:** Armazena o histórico de preços das criptomoedas.

### Atributos:
- **id_cotacao (PK):** Identificador único.
- **id_cripto (FK):** Referência à criptomoeda.
- **data_hora:** Data e hora da cotação.
- **preco:** Preço atual da criptomoeda.
- **volume:** Volume negociado.
- **market_cap:** Capitalização de mercado.
- **variacao:** Variação percentual em relação à cotação anterior.

---

## 3. Notícias

**Descrição:** Contém informações sobre eventos relacionados ao mercado de criptomoedas.

### Atributos:
- **id_noticia (PK):** Identificador único.
- **id_cripto (FK):** Referência à criptomoeda.
- **data_publicacao:** Data da publicação.
- **tema:** Tema principal (ex.: regulação, adoção, tecnologia).
- **noticia:** Texto completo.
- **fonte:** Fonte da notícia (ex.: Bloomberg, CoinDesk).

---

## 4. Sentimentos de Notícias

**Descrição:** Armazena a análise de sentimento das notícias.

### Atributos:
- **id_sentimento (PK):** Identificador único.
- **id_noticia (FK):** Referência à notícia.
- **id_usuario (FK):** Referência ao usuário.
- **sentimento:** Classificação (positivo, neutro, negativo).
- **score_sentimento:** Escore numérico do sentimento (-1 a 1).

---

## 5. Transações de Mercado

**Descrição:** Representa compras, vendas e transferências de criptomoedas.

### Atributos:
- **id_transacao (PK):** Identificador único.
- **id_cripto (FK):** Referência à criptomoeda.
- **data_hora:** Data e hora da transação.
- **tipo:** Tipo da transação (compra, venda).
- **quantidade:** Quantidade negociada.
- **preco_unitario:** Preço unitário.

---

## 6. Usuários

**Descrição:** Usuários da plataforma.

### Atributos:
- **id_usuario (PK):** Identificador único.
- **nome:** Nome completo.
- **email:** Email do usuário.
- **senha:** Hash da senha do usuário.
- **admin_flag:** Flag indicando se usuário é admin ou não.

---

## 7. Ordens de Compra/Venda

**Descrição:** Ordens criadas por usuários para compra ou venda de criptomoedas.

### Atributos:
- **id_ordem (PK):** Identificador único.
- **id_cripto (FK):** Referência à criptomoeda.
- **tipo:** Tipo da ordem (compra, venda).
- **quantidade:** Quantidade desejada.
- **preco_limite:** Preço máximo/mínimo para executar a ordem.

---

## 8. Tendências de Preço

**Descrição:** Captura dados agregados sobre preços e variações temporais.

### Atributos:
- **id_tendencia (PK):** Identificador único.
- **id_cripto (FK):** Referência à criptomoeda.
- **periodo:** Período analisado (ex.: 24h, 7d).
- **variacao_preco:** Variação percentual no período.
- **tendencia:** Classificação (alta, baixa, estável).

---

## 9. Dados Externos

**Descrição:** Armazena informações de fatores externos que podem impactar o mercado.

### Atributos:
- **id_dado (PK):** Identificador único.
- **descricao:** Breve descrição do fator externo (ex.: taxa de juros).
- **data_hora:** Data e hora da coleta.
- **valor:** Valor associado ao fator.

---

## 10. Imagens de Criptomoedas

**Descrição:** Armazena imagens relacionadas às criptomoedas cadastradas.

### Atributos:
- **id_imagem (PK):** Identificador único.
- **id_cripto (FK):** Referência à criptomoeda correspondente.
- **tipo:** Tipo da imagem (ex.: logo, ícone).
- **conteudo:** Arquivo binário (BLOB).
- **data_upload:** Data de upload da imagem.
