# 🐍 Battlesnake Python Template

Template de [Battlesnake](https://play.battlesnake.com) em **Python**, com
**FastAPI** rodando em **AWS Lambda** com **API Gateway**. O deploy é
automático: você programa, dá push, e o GitHub Actions devolve a URL da sua cobra.

---

## 📦 Pré-requisitos

- **Python 3.12 ou superior** — [python.org/downloads](https://www.python.org/downloads/)
  Confira com `python --version`.
- Noções básicas de **Python**, **API** e **Lambda**
- **Disposição, competitividade e força de vontade!**

Você **não** precisa instalar Terraform nem AWS CLI: quem cuida do deploy é o CD.

---

## 🚀 Como começar

1. Vá até o repositório [**devmaua_setup**](https://github.com/Maua-Dev/devmaua_setup),
   abra uma **issue** e escolha:
   - **project_name**: `battlesnake_python_{seu nome}`
   - **project template**: `battlesnake_fastapi_template`
   - marque o repositório como **público**

2. Aguarde cerca de **1 minuto** e confira em
   [Repositórios da organização](https://github.com/orgs/Maua-Dev/repositories).

3. Clone o repositório e prepare o ambiente:
   ```bash
   git clone https://github.com/Maua-Dev/Nome_Do_Seu_Repositorio
   cd Nome_Do_Seu_Repositorio
   ```

4. Crie o ambiente virtual (só na primeira vez):

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux / Mac**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

6. Abra [`src/logic.py`](src/logic.py) e comece a programar sua cobra 🐍

---

## 📂 Estrutura do projeto

```
.
├── requirements.txt            # dependências
├── src
│   ├── logic.py                # 👈 É AQUI QUE VOCÊ PROGRAMA
│   └── main.py                 # rotas FastAPI + handler da Lambda — não precisa mexer
├── tests
│   └── test_logic.py           # testes da sua lógica
├── terraform
│   ├── bootstrap/              # bucket de estado do Terraform
│   └── app/                    # Lambda + API Gateway
└── .github/workflows/CD.yaml   # testes + deploy automático
```

**Você só precisa de `src/logic.py`.** Os outros arquivos existem para levar o
estado do jogo até as suas quatro funções.

---

## 🧠 As quatro funções

Todas ficam em `src/logic.py` e recebem o `game_state` — o dicionário com o JSON
completo que o servidor do Battlesnake manda a cada requisição:

| Função | Rota | Quando é chamada | O que devolve |
|---|---|---|---|
| `info()` | `GET /` | ao cadastrar a cobra e no início de cada partida | aparência (cor, cabeça, cauda) |
| `start(game_state)` | `POST /start` | uma vez, no começo da partida | nada |
| `move(game_state)` | `POST /move` | **a cada turno** | `{"move": "up" \| "down" \| "left" \| "right"}` |
| `end(game_state)` | `POST /end` | uma vez, no fim da partida | nada |

A cobra já vem com a lógica que **impede ela de andar para trás**. A partir daí,
os `TODO` em `move()` marcam os próximos passos:

1. não sair do tabuleiro
2. não bater no próprio corpo
3. não bater nas cobras adversárias
4. ir atrás da comida em vez de sortear a direção

Documentação oficial da API: <https://docs.battlesnake.com/api>
Exemplo do JSON recebido: <https://docs.battlesnake.com/api/example-move>

> ⏱️ Você tem cerca de **500 ms** por jogada. Se estourar, o servidor escolhe
> uma direção qualquer por você — normalmente para a morte.

> 🧭 O tabuleiro tem a origem `(0, 0)` no **canto inferior esquerdo**: `x` cresce
> para a direita e `y` cresce para cima.

---

## 🧪 Testando

```bash
pytest
```

O template já vem com testes que garantem que a sua cobra **sempre devolve uma
direção válida** e **nunca volta por cima do próprio pescoço**, além de testes
de integração das rotas. Escreva mais testes conforme for implementando os
passos acima.

> 🚨 Os testes rodam no GitHub Actions **antes** do deploy. Se algum falhar, o
> deploy não acontece e a URL da sua cobra não é atualizada.

### Rodando localmente

```bash
uvicorn src.main:app --reload
```

Sobe a aplicação em `http://127.0.0.1:8000`. Em outro terminal:

```bash
curl http://127.0.0.1:8000/
```

O FastAPI ainda gera uma documentação interativa em
`http://127.0.0.1:8000/docs`, onde dá para disparar as rotas pelo navegador.

---

## ☁️ Deploy

O deploy é disparado por push na branch **`dev`**:

```bash
git add .
git commit -m "minha cobra agora desvia das paredes"
git push origin dev
```

O que o CD faz, nessa ordem:

1. **ExecuteTests** — roda `pytest`
2. **Bootstrap** — garante o bucket S3 que guarda o estado do Terraform
3. **build_python** — instala as dependências para **arm64** e empacota
   `src/` + bibliotecas num zip
4. **deploy_app** — `terraform apply`, criando a Lambda e o API Gateway

No fim, o resumo da execução mostra a **URL da sua cobra** e um link para os
logs no CloudWatch. Você também encontra a URL no output `api_url_base` do
passo *Terraform Apply*.

---

## 🎯 Cadastrando no Battlesnake

1. Entre em [play.battlesnake.com](https://play.battlesnake.com)
2. **My Battlesnakes** → **Create Battlesnake**
3. No campo **URL**, cole a URL do deploy
   (algo como `https://abc123.execute-api.us-east-1.amazonaws.com/dev`)
4. Salve e mande ver nos jogos e desafios!

Se o site reclamar da URL, teste antes no terminal:

```bash
curl https://SUA_URL_AQUI/
```

Deve responder o JSON do `info()`.

---

## 📌 Observações

- Toda a lógica da partida vive em `move()`.
- **Evite adicionar dependências pesadas.** Elas vão inteiras para o zip da
  Lambda, que tem limite de 50 MB. O pacote atual usa cerca de 14 MB.
- A Lambda roda em **arm64**, e o CD instala as dependências já compiladas para
  essa arquitetura. Se você adicionar uma biblioteca com código nativo que não
  tenha wheel `manylinux2014_aarch64`, o build vai falhar — prefira bibliotecas
  em Python puro.
- Os logs ficam no **CloudWatch**, com retenção de 14 dias. Tudo que você
  escrever com `print` aparece lá.
- A branch de deploy é **`dev`**. Push em outras branches roda só os testes.

---

## 🛠 Ferramentas úteis

- [Battlesnake Docs](https://docs.battlesnake.com/) — documentação da API
- [FastAPI](https://fastapi.tiangolo.com/) — o framework das rotas
- [Mangum](https://mangum.fastapiexpert.com/) — adaptador do FastAPI para Lambda
- [Postman](https://www.postman.com/) — testar requisições sem terminal
- [Python 3.12](https://docs.python.org/3.12/) — documentação da linguagem

---

## 📞 Fale com a gente

Dúvidas? Chama no [Discord](https://discord.gg/Yr2VPgAmcb) da Dev. Community Mauá.
