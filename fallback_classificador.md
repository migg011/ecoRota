# Fallback por palavras-chave — como funciona

Este documento explica como o EcoRota classifica um resíduo quando a **IA não consegue
dar conta**. É o "plano B" do app.

Relacionado: [contrato_api.md](contrato_api.md) (formato das rotas da API).

---

## O que é o fallback

O classificador principal usa a IA da Groq. Mas se a IA falhar, o app **não quebra**:
um mecanismo local chama o **fallback por palavras-chave**, que procura palavras do
texto digitado pelo morador e devolve uma categoria.

Tudo acontece em um arquivo só:
`backend/EcoRota/services/classificador_ia.py`

| Função | Papel |
|---|---|
| `classificar_residuo(texto)` | porta de entrada — é ela que as views chamam |
| `classificar_por_llm(texto)` | tenta a IA primeiro |
| `classificar_por_palavras_chave(texto)` | o fallback (plano B) |

O mesmo serviço é usado pelas duas rotas: `POST /api/descartes/` e `POST /api/classificar/`.

---

## Quando o fallback entra em ação

O fallback roda quando `classificar_por_llm` devolve `None`, o que acontece em 2 casos:

1. **A API da Groq falhou** — erro de rede, de quota ou qualquer `GroqError`
2. **A IA devolveu algo irreconhecível** — texto que não bate com nenhuma das
   6 categorias oficiais

Nesses casos o servidor registra um aviso no log do terminal e segue pelo plano B.

---

## Como a regra por palavras-chave funciona

O texto digitado é comparado (em letras minúsculas) com listas de palavras de cada
categoria. A verificação acontece **nesta ordem** — e a **primeira categoria com acerto
é a vencedora**:

| Ordem | Categoria | Palavras que ativam |
|---|---|---|
| 1º | Madeira | madeira, tabua, tábua, palete, pallet, compensado, ripa |
| 2º | Orgânico de Estiagem | folha, galho, poda, tronco, grama, arvore, árvore, vegetação, cinza, queimada |
| 3º | Construção | tijolo, gesso, entulho, concreto, cimento, piso, azulejo, pedra, areia, brita |
| 4º | Secos e Recicláveis | plastico, plástico, garrafa, papel, papelao, papelão, caixa, lata, metal, vidro |
| 5º | Eletroeletrônicos e Pilhas | computador, tv, televisao, televisão, fio, cabo, bateria, pilha, celular, eletro |
| 6º | Móveis e Volumosos | sofa, sofá, colchão, colchao, armario, armário, mesa, cadeira, estante |

Detalhes importantes:

- A comparação é por **parte da palavra** — "galhos" é achado pela palavra "galho"
- Texto com acento e sem acento funciona, porque as duas versões estão na lista
- Quando o texto mistura materiais de categorias diferentes, **vale a ordem da tabela**
  (ex: "tábua com folhas" → a Madeira vem antes da Orgânico, então vira **Madeira**)

---

## Se nenhuma palavra bater

O fallback tem uma categoria padrão: **Construção**.
Ou seja: o resíduo nunca fica sem categoria.

---

## Garantias do serviço

Independentemente de IA ou fallback, `classificar_residuo` **sempre devolve**:

- **uma única categoria** (nunca lista, mesmo com vários materiais no texto)
- o nome **exatamente igual** a um das 6 categorias oficiais

Isso garante que o `POST /api/descartes/` nunca quebra por causa do campo categoria.

---

## Como testar

- Script manual: `backend/scripts/testar_descarte_multi.py` — tem uma checagem que
  simula a IA fora do ar e confere que o fallback responde certo
  (ex: "sofá velho e quebrado" → "Móveis e Volumosos")
- Testes automáticos: `backend/EcoRota/tests/test_categoria_unica.py`

---

## Como mexer nisso no futuro

Para acrescentar palavra a uma categoria, é só adicionar na lista correspondente
dentro de `classificar_por_palavras_chave` (ex: "tijoleira" em Construção).
Atenção: como a ordem da tabela define o vencedor em caso de empate, trocar a ordem
dos `if` muda o comportamento do app.
