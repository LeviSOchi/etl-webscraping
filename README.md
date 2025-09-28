<img width="953" alt="Image" src="https://github.com/user-attachments/assets/58da9cc5-a91a-4727-b6f7-f1f897b3baba" />

---

# 📘 Coleta de Dados com Scrapy — Mercado Livre Notebooks

Este guia documenta o passo a passo completo de um projeto real de scraping de produtos (notebooks) no site do Mercado Livre, utilizando **Scrapy**, uma das ferramentas mais poderosas de coleta de dados com Python.

---

## 🔧 Etapa 1 — Instalar o Scrapy

```bash
pip install scrapy
```

Instalamos o Scrapy, que é um framework robusto para criação de spiders (robôs de coleta de dados). Ele permite navegar por páginas HTML, extrair dados com seletores CSS ou XPath, lidar com paginação, entre outros.

---

## 🏗️ Etapa 2 — Criar o Projeto

```bash
scrapy startproject mercadolivre
```

Esse comando cria a estrutura inicial do projeto, com os diretórios:
- `spiders/`: onde ficam os crawlers
- `settings.py`: onde configuramos o comportamento do bot
- `items.py`: (opcional) definição da estrutura de dados
- `middlewares.py`: interceptadores de requisição/resposta

---

## 📂 Etapa 3 — Entrar no Projeto

```bash
cd mercadolivre
```

---

## 🧬 Etapa 4 — Criar a Spider

```bash
scrapy genspider notebook mercadolivre.com.br
```

Criamos uma spider chamada `notebook` voltada para o domínio do Mercado Livre. A spider será criada dentro de `mercadolivre/spiders/notebook.py`.

---

## 🐚 Etapa 5 — Testar no Shell do Scrapy

```bash
scrapy shell
```

Esse modo nos dá um ambiente interativo para testar seletores, verificar HTML da página e debugar.

---

## 🔍 Etapa 6 — Tentar fazer um `fetch()`

```python
fetch("https://lista.mercadolivre.com.br/notebook?sb=rb#D[A:notebook]")
```

Esse comando busca a página desejada. Se o retorno for `403 Forbidden`, significa que o site está bloqueando o acesso automatizado.

---

## 🕵️ Etapa 7 — Adicionar o User-Agent

### O que é `User-Agent`?

É uma string que identifica o tipo de cliente que está acessando o site (navegador, sistema, etc). Sites como o Mercado Livre bloqueiam robôs, mas permitem navegadores comuns.

```python
# settings.py
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
```

Com isso, nosso bot finge ser um navegador legítimo.

---

## 🧠 Etapa 8 — Revisar Middlewares (opcional)

```python
# settings.py (mantido padrão nesse projeto)
DOWNLOADER_MIDDLEWARES = {
   # pode ser customizado caso precise alterar headers, usar proxy, etc.
}
```

---

## 🧪 Etapa 9 — Retestando com `scrapy shell`

```python
fetch("https://lista.mercadolivre.com.br/notebook?sb=rb#D[A:notebook]")
response
response.text
```

Verificamos se conseguimos acessar o HTML corretamente e começamos a testar os seletores.

---

## 🔎 Etapa 10 — Testar seletores

```python
response.css('div.ui-search-result__wrapper')
```

```python
len(response.css('div.ui-search-result__wrapper'))
```

```python
products = response.css('div.ui-search-result__wrapper')
products[0].css('span.poly-component__brand::text').get()
```

Encontramos os dados e validamos que conseguimos extrair marca, nome, preço, avaliações, etc.

---

## 🧱 Etapa 11 — Transformar os testes em código

Criamos o crawler programático com os seletores testados, salvando os dados como JSON.

```bash
scrapy crawl notebook -o data.json
```

---

## 💸 Etapa 12 — Coletar os preços corretamente

```python
prices = products[0].css('span.andes-money-amount__fraction::text').getall()
```

Isso retorna todos os valores de preços (antigo, novo, desconto, etc). Precisamos selecionar corretamente:

```python
old_price = prices[0] if len(prices) > 0 else None
new_price = prices[1] if len(prices) > 1 else None
```

---

## 📁 Etapa 13 — Salvar os dados fora da pasta do projeto

```bash
scrapy crawl notebook -o ../data/data.json
```

Organizamos os dados coletados na pasta `data/`, fora do diretório `mercadolivre`.

---

## 📦 Etapa 14 — Organizar o projeto em camadas

Criamos subpastas para manter a estrutura do pipeline mais clara e modular:

```
src/
│
├── coleta/          <- spiders, dados brutos
├── transformacao/   <- tratamento dos dados
├── dashboard/       <- visualizações e relatórios
```

---

## 🔁 Etapa 15 — Paginação

Adicionamos suporte para múltiplas páginas, buscando o botão “Próxima Página”:

```python
next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
yield scrapy.Request(url=next_page, callback=self.parse)
```

- `url` = link para a próxima página
- `callback` = função que será chamada ao carregar a nova página

---

## 🔐 Etapa 16 — Evitar bloqueio

Limitamos a quantidade de páginas para não abusar do site:

```python
page_count = 1
max_pages = 10
```

---

## 🤖 Etapa 17 — Respeitar `robots.txt`?

Por padrão:

```python
ROBOTSTXT_OBEY = True
```

Isso impede que o scraper acesse URLs proibidas no `robots.txt` do site. No Mercado Livre, várias URLs são bloqueadas por padrão. Podemos **desabilitar** isso em projetos internos:

```python
ROBOTSTXT_OBEY = False
```

---

## ✅ Etapa 18 — Rodar a coleta final

```bash
scrapy crawl notebook -o ../data/data.json
```

Agora, a spider coleta notebooks com nome, marca, preço, avaliações e vendedor, navegando por até 10 páginas.

---

## 🏁 Finalizamos a coleta

O próximo passo é criar transformações (por exemplo, limpeza de preços e normalização dos nomes) e visualizações (como dashboards com Streamlit, Dash ou Power BI).
