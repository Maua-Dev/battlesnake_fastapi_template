# 🐍 Battlesnake FastAPI Template

Template de [Battlesnake](https://play.battlesnake.com) em **Python** com
**FastAPI**, rodando em **AWS Lambda** com **Mangum**. O deploy é automático:
você programa, dá push, e o GitHub Actions devolve a URL da sua cobra.

---

## 📦 Pré-requisitos

- **Python 3.12 ou superior** — [python.org](https://www.python.org/downloads/)
  Confira com `python --version`.
- Noções básicas de **Python**, **API** e **Lambda**
- **Disposição, competitividade e força de vontade!**

Você **não** precisa instalar Terraform, CDK nem AWS CLI: quem cuida do deploy é o CD.

---

## 🚀 Como começar

1. Vá até o repositório [**devmaua_setup**](https://github.com/Maua-Dev/devmaua_setup),
   abra uma **issue** e escolha:
   - **project_name**: `battlesnake_{seu nome}`
   - **project template**: `battlesnake_fastapi_template`
   - marque o repositório como **público**

2. Aguarde cerca de **1 minuto** e confira em
   [Repositórios da organização](https://github.com/orgs/Maua-Dev/repositories).

3. Clone e instale:
   ```bash
   git clone https://github.com/Maua-Dev/Nome_Do_Seu_Repositorio
   cd Nome_Do_Seu_Repositorio

   # Criar e ativar o ambiente virtual
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux / macOS
   source venv/bin/activate

   # Instalar dependências
   pip install -r requirements-dev.txt
   pip install -r requirements.txt
   ```

4. Abra [`src/app/logic.py`](src/app/logic.py) e comece a programar sua cobra 🐍

---

## ⭐ Onde implementar sua snake

**Você só precisa editar `src/app/logic.py`.** Os outros arquivos existem para
levar o estado do jogo até as suas quatro funções.

### O que você deve alterar:
- `src/app/logic.py` — **este é o seu arquivo principal**

### O que você normalmente NÃO precisa alterar:
- `src/app/main.py` — endpoints FastAPI
- `src/app/models.py` — modelos Pydantic do estado do jogo
- Infraestrutura (IAC)
- GitHub Actions

---

## 📂 Estrutura do projeto

```
.
├── requirements.txt            # dependências de produção
├── requirements-dev.txt        # dependências de desenvolvimento/teste
├── src/app/
│   ├── logic.py                # 👈 É AQUI QUE VOCÊ PROGRAMA
│   ├── models.py               # modelos Pydantic do estado do jogo
│   └── main.py                 # endpoints FastAPI — não precisa mexer
├── tests/
│   └── app/
│       ├── test_logic.py       # testes unitários da lógica
│       └── test_app.py         # testes de integração dos endpoints
├── iac/                        # infraestrutura (não precisa mexer)
└── .github/workflows/          # testes + deploy automático
```

---

## 🧠 As quatro funções

Todas ficam em `src/app/logic.py` e recebem um `GameState` (definido em `models.py`):

| Função | Rota | Quando é chamada | O que devolve |
|---|---|---|---|
| `info()` | `GET /` | ao cadastrar a cobra e no início de cada partida | aparência (cor, cabeça, cauda) |
| `start(state)` | `POST /start` | uma vez, no começo da partida | nada |
| `get_move(state)` | `POST /move` | **a cada turno** | `MoveResponse(move="up"/"down"/"left"/"right")` |
| `end(state)` | `POST /end` | uma vez, no fim da partida | nada |

A cobra já vem com a lógica que **impede ela de andar para trás**. A partir daí,
os `TODO` em `get_move()` marcam os próximos passos:

1. não sair do tabuleiro
2. não bater no próprio corpo
3. não bater nas cobras adversárias
4. ir atrás da comida em vez de sortear a direção

Documentação oficial da API: <https://docs.battlesnake.com/api>

> ⏱️ Você tem cerca de **500 ms** por jogada.

---

## 🧪 Testando

```bash
pytest
```

O template já vem com testes que garantem que a sua cobra **sempre devolve uma
direção válida** e **nunca volta por cima do próprio pescoço**. Escreva mais
testes conforme for implementando os passos acima.

> 🚨 Os testes rodam no GitHub Actions **antes** do deploy. Se algum falhar, o
> deploy não acontece e a URL da sua cobra não é atualizada.

### Rodando localmente

```bash
uvicorn src.app.main:app --reload
```

Sobe a aplicação em `http://localhost:8000`. Em outro terminal:

```bash
curl http://localhost:8000/
curl -X POST http://localhost:8000/move \
  -H 'Content-Type: application/json' \
  -d '{"turn":1,"game":{"id":"1","ruleset":{},"timeout":500},"board":{"width":11,"height":11,"food":[],"hazards":[],"snakes":[]},"you":{"id":"s1","name":"eu","health":100,"body":[{"x":5,"y":4},{"x":4,"y":4},{"x":3,"y":4}],"head":{"x":5,"y":4},"length":3}}'
```

---

## ☁️ Deploy

O deploy é disparado por push na branch **`dev`**:

```bash
git add .
git commit -m "minha cobra agora desvia das paredes"
git push origin dev
```

O GitHub Actions vai:
1. Rodar os testes (`pytest`)
2. Empacotar e fazer deploy na AWS Lambda via CDK

No fim, o resumo da execução mostra a **URL da sua cobra**.

---

## 🎯 Cadastrando na Arena Mauá

1. Acesse [arena.devmaua.com](https://arena.devmaua.com)
2. Faça login com sua conta
3. No campo **URL**, cole a URL gerada pelo deploy
4. Salve e participe das partidas!

Se quiser testar antes, use o [Battlesnake](https://play.battlesnake.com) oficial.

---

## 📈 Progressão pedagógica

| Nível | Nome | O que implementar |
|---|---|---|
| 0 | **Random** | movimento aleatório (já vem pronto) |
| 1 | **Don't Die** | não voltar, não bater na parede, não bater em si mesmo |
| 2 | **Food** | procurar comida |
| 3 | **Space** | avaliar espaço disponível, evitar becos |
| 4 | **Opponents** | considerar outras cobras, head-to-head |
| 5 | **Advanced** | BFS, flood fill, A*, avaliação de território |

---

## 🛠 Ferramentas úteis

- [Battlesnake Docs](https://docs.battlesnake.com/) — documentação da API
- [FastAPI Docs](https://fastapi.tiangolo.com/) — documentação do framework
- [Pydantic](https://docs.pydantic.dev/) — validação de dados
- [Postman](https://www.postman.com/) — testar requisições sem terminal

---

## 📞 Fale com a gente

Dúvidas? Chama no [Discord](https://discord.gg/Yr2VPgAmcb) da Dev. Community Mauá.
