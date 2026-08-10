# TrilhaSonora

## Decisões de modelagem

### Por que não criei classes como `Musica`, `Album` ou `Usuario`

Optei por manter os conteúdos e usuários como dicionários puros, indexados
dentro da própria `Catalogo`, em vez de criar classes específicas pra cada
entidade. A razão é que, neste projeto, nenhuma dessas entidades carrega
comportamento próprio: uma "música" ou um "álbum" não fazem nada sozinhos,
eles só são consultados de formas diferentes (`duracao_total_de` soma
faixas pra álbum, retorna direto pra música). Essa diferença de tratamento
já é resolvida com um `if conteudo["tipo"] == "musica"` dentro do próprio
método da `Catalogo`, sem precisar de polimorfismo entre classes.

Criar uma classe `Musica` que só guarda `titulo`, `artista`, `duracao_seg`
sem nenhum método que use esse estado de forma exclusiva seria, na prática,
um dicionário com passos a mais. Preferi concentrar o comportamento na
`Catalogo`, que é a única entidade do projeto que de fato faz algo com os
dados: constrói índices, resolve buscas, mantém o estado da fila.

### Por que a `Catalogo` é a única classe

A `Catalogo` agrupa estado e comportamento que pertencem juntos porque ela
é o único objeto do projeto que muda ao longo do tempo (a fila de
reprodução) e que precisa de estrutura de acesso rápido (os dicionários
`conteudos_por_id`, `usuarios_por_id`, `usuarios_por_nome`, construídos uma
vez no `__init__`). Ela justifica sua existência porque não é só um
container de dados, ela expõe os 16 métodos que resolvem consultas de
formas diferentes sobre o mesmo estado interno.

### Índices construídos no `__init__`

Com 20 mil conteúdos e 10 mil consultas no modo batch, buscar por id
varrendo uma lista a cada consulta seria caro. Por isso o `__init__`
constrói três dicionários:

- `conteudos_por_id`, id do conteúdo para o dicionário completo
- `usuarios_por_id`, id do usuário para o dicionário completo
- `usuarios_por_nome`, nome em minúsculo para o id do usuário, usado por
  `buscar_usuario_por_nome`, que precisa ser case-insensitive

Isso transforma toda busca por id em acesso O(1), em vez de O(n) por
consulta.

### `intersecao_playlists` não pode ser pré-indexado

Diferente dos outros métodos, a interseção depende de uma combinação
arbitrária de `usuario_ids` que só é conhecida no momento da consulta, não
dá pra pré-computar todas as interseções possíveis no `__init__`. Por isso
esse método monta os `sets` de cada playlist e cruza sob demanda.

### Fila de reprodução

Usei `collections.deque` para a fila (`enfileirar`, `proximo`,
`fila_atual`), porque é O(1) nas duas pontas, diferente de `list.pop(0)`,
que é O(n). A fila é o único estado da `Catalogo` que muda depois do
`__init__`, e não é persistida entre execuções.

### Tratamento das sujeiras dos dados

Cada uma das 7 sujeiras é tratada no ponto exato onde aparece:

- rating ausente ou como string, tratado em `rating_de`
- data em dois formatos, tratado em `data_adicionado_de`
- gênero como string solta ou lista aninhada, achatado recursivamente em
  `generos_de`
- execuções com vírgula, tratado em `execucoes_de`
- faixa de álbum com duração nula, ignorada na soma em `duracao_total_de`

Nenhum `try/except` genérico envolvendo blocos inteiros, cada tratamento é
específico pro campo e pro formato esperado.

## Como rodar

```bash
python3 cli.py catalogo_final.json
python3 main.py consultas.json respostas.json
```

## Uso de IA

Usei assistência de IA ao longo do desenvolvimento deste projeto,
principalmente pra revisão de código e explicação de conceitos, devido ao
prazo apertado, só consegui parar pra fazer esse projeto de última hora, e às dificuldades que enfrentei no processo. Todas as
decisões de modelagem e o entendimento do código são meus.