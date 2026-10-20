# Contrato da API — EcoRota

Este documento descreve os formatos de dados (JSON) que o backend Django/DRF devolve
e espera receber. É a fonte única de verdade pra equipe do frontend — na dúvida, vale
o que está escrito aqui.

Base URL (desenvolvimento): `http://localhost:8000/api`

---

## Informações gerais

- **Autenticação:** header `Authorization: Token <token>` em todas as rotas, exceto
  registro e login. Sem o header, a resposta é `401`.
- **Formato:** JSON (`Content-Type: application/json`).
- **Paginação:** não existe. As listas voltam como array simples mesmo.
- **Acentos:** os textos vêm com acentuação normal (UTF-8), tipo
  `"categoria": "Eletroeletrônicos e Pilhas"`.

### Categorias oficiais de resíduo

O backend usa examente estes nomes (com acento e maiúscula inicial):

```
Madeira
Orgânico de Estiagem
Construção
Secos e Recicláveis
Eletroeletrônicos e Pilhas
Móveis e Volumosos
```

---

## Autenticação

### 1. POST /api/auth/registro/

Cria a conta e já devolve o token.

Requisição:

```json
{
  "nome_completo": "Ana Souza",
  "email": "ana@exemplo.com",
  "password": "SenhaForte123"
}
```

Resposta (201 Created):

```json
{
  "token": "9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c",
  "email": "ana@exemplo.com",
  "nome_completo": "Ana Souza"
}
```

Erros possíveis (400):

```json
{
  "email": ["Este e-mail já está cadastrado."]
}
```

```json
{
  "password": ["This password is too short. It must contain at least 8 characters."]
}
```

Obs.: a senha é validada pelo Django — mínimo 8 caracteres, não pode ser só número
nem muito parecida com o e-mail. As mensagens de erro de senha saem em inglês mesmo
(efeito colateral do Django, pode ignorar).

---

### 2. POST /api/auth/login/

Requisição:

```json
{
  "email": "ana@exemplo.com",
  "password": "SenhaForte123"
}
```

Resposta (200 OK):

```json
{
  "token": "9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c",
  "email": "ana@exemplo.com",
  "nome_completo": "Ana Souza"
}
```

Resposta de erro (401):

```json
{
  "detail": "Credenciais inválidas."
}
```

**Dados do usuário logado:** não existe rota `GET /api/usuarios/me/`. O frontend deve
guardar `token`, `email` e `nome_completo` retornados pelo login/registro (por exemplo,
no `localStorage`) e usar esses dados nas telas.

---

## Classificação do resíduo

### 3. POST /api/classificar/

Recebe o texto livre do usuário e devolve a categoria classificada pela IA **junto com
os ecopontos compatíveis** — é esse endpoint que a tela de descrição deve chamar.

Requisição:

```json
{
  "descricao_texto": "entulho de obra: cimento, tijolo e areia"
}
```

Resposta (200 OK):

```json
{
  "categoria": "Construção",
  "destinos": [
    {
      "id": 7,
      "nome": "Ecoponto Zona Norte",
      "categoria": "Construção",
      "endereco": "Parque dos Bilhares - Zona Norte",
      "descricao": "Ecoponto oficial da Prefeitura de Manaus. Confirmar endereço exato pelo Manaus Atende (156).",
      "horario": "Seg a Sáb, 8h às 18h - confirme no Manaus Atende (156)"
    }
  ]
}
```

| Campo da resposta | O que é |
|---|---|
| `categoria` | categoria que a IA escolheu (uma das 6 oficiais) |
| `destinos` | array de ecopontos que **aceitam** essa categoria (mesmo formato do GET /api/destinos/) |

Erros possíveis (400):

```json
{
  "descricao_texto": ["Ensure this field has at least 3 characters."]
}
```

Sem token: `401`.

> Obs.: este endpoint **não cria** nenhum descarte — só classifica e sugere. O descarte
> mesmo é registrado depois, no `POST /api/descartes/`.

---

## Destinos (ecopontos)

### 4. GET /api/destinos/

Lista os ecopontos cadastrados (hoje são 21, de Manaus).

Sem filtro — retorna tudo:

```json
[
  {
    "id": 1,
    "nome": "Ecoponto Zona Sul",
    "categoria": "Madeira",
    "endereco": "Avenida Lourenço da Silva Braga, 1403-1409 - Educandos",
    "descricao": "Ecoponto oficial da Prefeitura de Manaus. Aceita eletrônicos, eletrodomésticos, pilhas, baterias e cabos.",
    "horario": "Seg a Sáb, 8h às 18h - confirme no Manaus Atende (156)"
  }
]
```

**Filtro por categoria** (o nome tem que ser exatamente igual ao da lista de categorias):

```
GET /api/destinos/?categoria=Eletroeletrônicos%20e%20Pilhas
```

> Lembrete: o mesmo ecoponto aparece em vários registros, um para cada categoria que
> ele aceita. Filtrar por categoria devolve só os locais que recebem aquele tipo de
> resíduo.

Sem token: `401`.

> **Permissão de escrita:** criar, editar e apagar ecoponto (POST/PUT/DELETE) é
> **restrito ao administrador** — usuário comum logado recebe `403`.

---

## Descartes

### 5. POST /api/descartes/

Registra a intenção de descarte. **O servidor classifica o resíduo** com a IA e preenche
a categoria sozinho.

Requisição:

```json
{
  "Usuario": 1,
  "Destino": 3,
  "peso_estimado_kg": "20.50",
  "descricao_texto": "sofá velho e quebrado"
}
```

⚠️ **Atenção aos nomes:** `Usuario` e `Destino` começam com maiúscula (é assim mesmo),
e são os **ids** (números), não o objeto.

| Campo | Obrigatório | Observação |
|---|---|---|
| `Usuario` | sim | id do usuário logado |
| `Destino` | sim | id do ecoponto (vem do GET /api/destinos/) |
| `peso_estimado_kg` | sim | número com 2 casas decimais, não pode ser negativo |
| `descricao_texto` | sim | texto livre, mínimo 3 e máximo 1000 caracteres |
| `categoria` | — | **não envia** — o servidor preenche (read-only) |
| `data_criacao` | — | **não envia** — o servidor preenche (read-only) |

Resposta (201 Created):

```json
{
  "id": 1,
  "Usuario": 1,
  "Destino": 3,
  "data_criacao": "2026-10-14T21:35:12-04:00",
  "peso_estimado_kg": "20.50",
  "categoria": "Móveis e Volumosos",
  "descricao_texto": "sofá velho e quebrado"
}
```

Erros possíveis (400):

```json
{
  "descricao_texto": ["Ensure this field has at least 3 characters."]
}
```

```json
{
  "peso_estimado_kg": ["Ensure this value is greater than or equal to 0."]
}
```

---

### 6. GET /api/descartes/

Lista os descartes registrados (mesmo formato de resposta do POST, em array).

```json
[
  {
    "id": 1,
    "Usuario": 1,
    "Destino": 3,
    "data_criacao": "2026-10-14T21:35:12-04:00",
    "peso_estimado_kg": "20.50",
    "categoria": "Móveis e Volumosos",
    "descricao_texto": "sofá velho e quebrado"
  }
]
```

⚠️ **Para o dashboard:** este endpoint retorna os descartes de todos os usuários.
O filtro por usuário (`?usuario=1`) ainda não funciona — o frontend deve filtrar no
cliente, comparando `item.Usuario === idDoUsuarioLogado`.

---

## Fluxo do app (telas do Angular)

O usuário **nunca escolhe o ecoponto às cegas** — ele descreve o resíduo e o app mostra
só os locais compatíveis:

1. **Login/Cadastro** → `POST /api/auth/login/` ou `/api/auth/registro/` → guarda
   `token`, `email`, `nome_completo` e o id... (obs.: o id do usuário não vem no login;
   se precisar dele, usar `GET /api/usuarios/` e localizar o registro pelo e-mail)
2. **Descrição do resíduo** → usuário escreve o texto livre (ex: "entulho de obra:
   cimento e tijolo")
3. **Classificação** → `POST /api/classificar/` com `descricao_texto` → devolve
   `{categoria, destinos}` — os ecopontos **já filtrados** pela categoria
4. **Resultado** → a tela mostra a categoria e só os `destinos` compatíveis vindos
   da resposta (não precisa de outro GET)
5. **Confirmação** → usuário escolhe um dos sugeridos e confirma →
   `POST /api/descartes/` com `Usuario`, `Destino` (o id escolhido),
   `peso_estimado_kg` e `descricao_texto`
6. **Dashboard** → `GET /api/descartes/` e filtra por `Usuario` no cliente

> Obs.: se o `ResiduoService` do frontend estiver enviando o campo `descricao`,
> ajustar para `descricao_texto` (padrão do backend).

---

## Resumo das rotas

| Método | Rota | Auth | O que faz |
|---|---|---|---|
| POST | /api/auth/registro/ | não | Cria conta, devolve token |
| POST | /api/auth/login/ | não | Login, devolve token |
| POST | /api/classificar/ | sim | Classifica o texto e devolve `{categoria, destinos}` |
| GET | /api/destinos/ | sim | Lista ecopontos (filtro `?categoria=`) |
| POST | /api/descartes/ | sim | Cria descarte e classifica |
| GET | /api/descartes/ | sim | Lista descartes (filtrar por usuário no cliente) |
| GET | /api/usuarios/ | sim | Lista usuários (usar só pra pegar o id pelo e-mail) |

---

## Erros comuns

| Código | Quando acontece | Resposta |
|---|---|---|
| 401 | Sem token ou token inválido/expirado | `{"detail": "Authentication credentials were not provided."}` |
| 400 | Dados inválidos no envio | objeto com o campo e a mensagem |
| 500 | Erro interno do servidor | (avisar o time do backend com o log do terminal) |
