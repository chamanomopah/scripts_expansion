Perfeito! Agora tenho informações suficientes. Vou compilar uma pesquisa completa sobre high level prompts em slash commands no Claude Code.

## Pesquisa Completa: High Level Prompts em Slash Commands no Claude Code

### O que são Slash Commands no Claude Code?

Os **slash commands** no Claude Code são prompts customizados armazenados em arquivos Markdown que você pode disparar com a sintaxe `/command-name`. Eles funcionam como templates de prompts reutilizáveis que encapsulam workflows específicos e instruções, oferecendo uma forma elegante de automatizar tarefas repetitivas.[1][2]

#### Localização e Tipos

Existem dois escopos para criar slash commands:[3]

- **Project commands** (`.claude/commands/`): Compartilhados com o time do projeto
- **Personal commands** (`~/.claude/commands/`): Disponíveis em todos os seus projetos

### High Level Prompts: Conceito Fundamental

Um **high level prompt** no contexto de Claude Code refere-se a instruções generalizadas e conceituais que permitem ao Claude raciocinar profundamente sobre uma tarefa, em vez de prescrever passos específicos. Segundo a documentação oficial, Claude frequentemente apresenta melhor desempenho com instruções de alto nível que facilitam o pensamento profundo, em comparação com orientações prescritivas passo a passo.[4]

**Exemplo de contraste:**

Menos efetivo (step-by-step prescritivo):
```
Pense neste problema matemático passo a passo:
1. Primeiro, identifique as variáveis
2. Depois, configure a equação
3. A seguir, resolva para x
```

Mais efetivo (high level):
```
Pense profundamente neste problema matemático e resolva-o.
```

### Princípios para Estruturação de High Level Prompts em Slash Commands

#### 1. **Clareza e Especificidade**

Apesar de serem "high level", os prompts devem ser explícitos sobre o que você quer. A chave é encontrar o equilíbrio entre generalização e direcionamento.[5][6][4]

**Exemplo de slash command bem estruturado:**

```markdown
---
description: Otimizar código para performance
argument-hint: [file-path]
allowed-tools: Read, Write
---

Analise o arquivo $1 para problemas de performance.
Identifique gargalos e sugira otimizações.
Considere complexidade de tempo, uso de memória e padrões de acesso.
```

#### 2. **Uso de Tags XML**

As tags XML são fundamentais para estruturar high level prompts no Claude Code. Elas ajudam Claude a entender distinções entre diferentes componentes do prompt.[7][8]

Tags recomendadas pela Anthropic:[7]

- `<instructions>`: Instruções da tarefa
- `<context>`: Informações de background
- `<example>`: Exemplos para guiar respostas
- `<formatting>`: Requisitos de formatação de saída
- `<constraints>`: Restrições ou limitações
- `<thinking>`: Espaço para raciocínio interno

**Exemplo em slash command:**

```markdown
---
description: Revisar código
---

<instructions>
Faça uma revisão completa do código fornecido.
</instructions>

<constraints>
- Foque em segurança, performance e estilo
- Cite exemplos específicos
- Seja construtivo nas críticas
</constraints>

<formatting>
Use seções com headers markdown para organizar feedback.
</formatting>

Analise @src/main.js
```

#### 3. **Parametrização com $ARGUMENTS**

Os slash commands suportam dois tipos de parameterização:[3]

- **`$ARGUMENTS`**: Captura todos os argumentos passados
- **`$1`, `$2`, etc.**: Argumentos posicionais individuais

```markdown
---
description: Criar commit com mensagem
argument-hint: [message]
---

Crie um git commit com a mensagem: $ARGUMENTS

Passos:
- Revise as mudanças com git diff
- Valide o formato conventional commit
- Execute o commit
```

#### 4. **Execução de Comandos Bash**

High level prompts podem incorporar contexto dinâmico através de comandos bash executados durante o comando:[3]

```markdown
---
allowed-tools: Bash(git status:*), Bash(git diff HEAD:*)
description: Comitar mudanças
---

## Contexto

- Status atual: !`git status`
- Mudanças: !`git diff HEAD`

## Sua tarefa

Baseado nas mudanças acima, crie um commit seguindo conventional commits.
```

#### 5. **Referência a Arquivos**

Você pode referenciar arquivos dentro de slash commands usando a sintaxe `@`:[3]
exemplo: 
```markdown
---
description: Revisar segurança
---

<instructions>
Revise os seguintes arquivos para vulnerabilidades de segurança:
</instructions>

Arquivos para revisar:
- @src/auth.js
- @src/api/routes.js
- @src/database.js

Procure por:
- SQL injection
- XSS vulnerabilities
- CSRF protection issues
```
SLASH COMMANDS deve SEMPRE a descrição principal do slash command referenciar os topicos principais usando o `@` (ex: `instruções`, `arquivos relevantes`)
exemplo:
´´´
<Use THINK HARD para seguir as `Instructions` para transformar o `arquivo_alvo` usando a estrutura SDLC. Siga a seção `Relatório` para relatar corretamente os resultados da transformação, criando um arquivo atualizado (v2) e deixando o arquivo citado intacto.>
´´´

### Integração com Extended Thinking

High level prompts funcionam particularmente bem com **extended thinking** do Claude. Em vez de prescrever exatamente como pensar, você deixa o modelo usar sua criatividade:[4]

```markdown
---
description: Arquitetar solução complexa
model: claude-opus-4.1
---

<instructions>
Pense profundamente sobre como arquitetar uma solução para o seguinte problema.

Não prescreva passos específicos—deixe-se explorar diferentes abordagens,
avaliar trade-offs, e fundamentar sua recomendação final em análise sólida.
</instructions>

Problema: $ARGUMENTS
```

### Architetura de Slash Commands de Alto Nível

#### Estrutura Frontmatter

Os slash commands usam **frontmatter YAML** para metadados:[3]

```yaml
---
allowed-tools: Read, Write, Bash
argument-hint: [project-type] [language]
description: Scaffold um novo projeto
model: claude-opus-4.1
disable-model-invocation: false
---
```

#### Namespace e Organização

Você pode organizar commands em subdiretorios para criar namespaces:[3]

```
.claude/commands/
├── backend/
│   ├── api-scaffold.md
│   └── database-setup.md
├── frontend/
│   ├── component.md
│   └── styling.md
└── deploy.md
```

Isto cria commands como `/api-scaffold`, `/component`, etc.

### SlashCommand Tool: Invocação Automática

Uma feature crucial lançada recentemente é o **SlashCommand tool**, que permite ao Claude invocar seus slash commands automaticamente. Isto transforma o fluxo de:[9]

- **Antes**: Usuário → Slash Command (manual)
- **Depois**: Claude Agent → SlashCommand Tool → Seu Comando (automático)

Para isto funcionar, o Claude precisa que o comando seja referenciado em suas instruções ou CLAUDE.md:[3]

```markdown
# Instruções para Claude

Se o usuário solicitar uma revisão de código, execute `/code-review`.
Se pedir para debugar, execute `/smart-debug`.
```

### Otimização de Token e Performance

#### Redução de Token Consumption

Slash commands reduzem significativamente o uso de tokens ao extrair workflows fixos da memória do `CLAUDE.md`. Um desenvolvedor reportou **20% de redução** em token usage convertendo workflows fixos para slash commands.[2]

#### Context Decay

Um consideration importante: instruções no system prompt tendem a degradar após 80-120k tokens. Para mitigar isso:[10]

- Posicione instruções críticas perto do inicio
- Use "core_questions" em vez de "core_instructions" para reforçar compliance
- Considere reiniciar contexto para tarefas muito longas

### Técnicas Avançadas para High Level Prompts

#### 1. **Chain of Thought com High Level Instructions**

Combine instructions de alto nível com espaço explícito para raciocínio:

```markdown
---
description: Analisar padrões
---

<instructions>
Analise o código fornecido para identificar padrões arquiteturais.
Pense profundamente—não se limite a padrões óbvios.
</instructions>

<output_format>
Use <analysis> tags para apresentar seu pensamento
Use <findings> tags para conclusões finais
</output_format>

Analise: @src/architecture.ts
```

#### 2. **Multi-Agent Orchestration**

Slash commands podem coordenar subagentes para tarefas complexas:[11]

```markdown
---
description: Pipeline de desenvolvimento completo
---

<instructions>
Orquestre os seguintes agentes para implementar este recurso:

1. requirements-analyst: Analise os requisitos
2. system-architect: Designe a solução
3. code-reviewer: Revise a implementação

Cada agente deve focar em seu domínio de expertise.
</instructions>

Recurso a implementar: $ARGUMENTS
```

#### 3. **Frameworks de Pensamento Estruturado**

Para prompts de alto nível em problema estratégicos, estruture o pensamento:

```markdown
---
description: Estratégia de arquitetura
---

<thinking_framework>
Considere:
- Constraints técnicas e de negócio
- Trade-offs entre opções
- Escalabilidade futura
- Tempo de implementação
- Risco e complexidade
</thinking_framework>

Desenvolva uma estratégia para: $ARGUMENTS
```

### Skills vs Slash Commands

É importante entender a diferença:[3]

| Aspecto | Slash Commands | Skills |
|---------|---|---|
| **Uso** | Prompts frequentes e simples | Workflows complexos multi-arquivo |
| **Invocação** | Manual ou via keywords em CLAUDE.md | Descoberta automática pelo Claude |
| **Complexidade** | Uma arquivo, prompt simples | Scripts, múltiplos arquivos |
| **Controle** | Explícito pelo usuário | Claude decide automaticamente |

Use **slash commands** para prompts reutilizáveis que você invoca explicitamente. Use **Skills** para capabilities que Claude deveria descobrir automaticamente.[3]

### Best Practices para High Level Prompts em Slash Commands

1. **Comece Generalizado, Itere para Específico**: Teste seu prompt com instruções high level primeiro, depois refine com mais detalhes baseado em output[4]

2. **Combine Técnicas**: Use XML tags + chain of thought + multishot examples para máxima performance[7]

3. **Limite Context Overload**: Não carregue 10k tokens de system prompt extras—cause context decay[10]

4. **Use Palavras-Chave de Ação**: Comece com verbos claros (Analise, Otimize, Refatore) em vez de "Você poderia…"[12]

5. **Prefill de Respostas**: Use assistant message para guiar o formato de output[13]

6. **Teste com Exemplos**: Use multishot prompting com exemplos reais de entrada/saída esperada[14]

7. **Documentação Clara**: Descreva o command com `description` no frontmatter para que Claude (e você) entendam quando usá-lo[3]

### Ferramentas para Otimizar High Level Prompts

Existe uma ferramenta open-source chamada **Claude Code Prompt Optimizer** que transforma prompts simples em instruções abrangentes e estruturadas usando Claude Opus 4.1:[15]

- Detecta tag `<optimize>` em prompts
- Adiciona frameworks de raciocínio estruturado
- Integra UltraThink mode (10,000 tokens de extended thinking)
- Aprimora com meta-instruções

### Exemplo Prático Completo: Slash Command para Code Review

```markdown
---
allowed-tools: Read, Write
argument-hint: [file-path]
description: Revisar código para qualidade e segurança
model: claude-opus-4.1
---

<instructions>
Conduza uma revisão de código profunda e construtiva.
Pense profundamente sobre o impacto, maintainability, e riscos.
Não apenas liste problemas—explique por quê cada um importa.
</instructions>

<review_focus>
- **Security**: Vulnerabilidades, input validation, autenticação
- **Performance**: Complexidade algorítmica, uso de memória, queries
- **Maintainability**: Nomes claros, duplicação, testabilidade
- **Best Practices**: Padrões apropriados, error handling, logging
</review_focus>

<output_format>
Organize feedback em seções. Para cada issue:
1. Local exato no código
2. O que está errado
3. Por quê é problemático
4. Como corrigir
5. Importância (crítica/importante/sugestão)
</output_format>

Revise: @$1
```

### Conclusão

High level prompts em slash commands representam a evolução de como trabalhar com Claude Code—de prompts conversacionais para instruções precisas e reutilizáveis. Ao combinar estrutura (XML tags, frontmatter), parametrização (`$ARGUMENTS`), e instruções conceituais de alto nível, você cria workflows automáticos que Claude pode executar consistentemente e com qualidade excepcional.

A chave é encontrar o equilíbrio certo entre generalização (deixando Claude pensar criativamente) e direcionamento (fornecendo contexto e constraints suficientes para mantê-lo nomantê-lo no caminho).

[1](https://www.builder.io/blog/claude-code)
[2](https://alexop.dev/tils/claude-code-slash-commands-boost-productivity/)
[3](https://code.claude.com/docs/en/slash-commands)
[4](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips)
[5](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
[6](https://claude.com/blog/best-practices-for-prompt-engineering)
[7](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
[8](https://beginswithai.com/xml-tags-vs-other-dividers-in-prompt-quality/)
[9](https://www.reddit.com/r/ClaudeAI/comments/1noyvmq/claude_code_can_invoke_your_custom_slash_commands/)
[10](https://www.reddit.com/r/ClaudeCode/comments/1o65jva/understanding_claude_codes_3_system_prompt/)
[11](https://superprompt.com/blog/best-claude-code-agents-and-use-cases)
[12](https://mirascope.com/blog/prompt-engineering-best-practices)
[13](https://aws.amazon.com/blogs/machine-learning/prompt-engineering-techniques-and-best-practices-learn-by-doing-with-anthropics-claude-3-on-amazon-bedrock/)
[14](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/prompt-improver)
[15](https://github.com/johnpsasser/claude-code-prompt-optimizer)
[16](https://www.youtube.com/watch?v=52KBhQqqHuc&vl=pt-BR)
[17](https://www.walturn.com/insights/mastering-prompt-engineering-for-claude)
[18](https://shipyard.build/blog/claude-code-cheat-sheet/)
[19](https://creatoreconomy.so/p/claude-code-tutorial-build-a-youtube-research-agent-in-15-min)
[20](https://www.claude.com/blog/best-practices-for-prompt-engineering)
[21](https://www.youtube.com/watch?v=ysPbXH0LpIE)
[22](https://www.anthropic.com/engineering/claude-code-best-practices)
[23](https://apidog.com/blog/claude-code-prompts/)
[24](https://www.curiousmints.com/creating-reusable-prompts-in-claude/)
[25](https://www.youtube.com/watch?v=OfUn6HjwXhI)
[26](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
[27](https://codeconductor.ai/blog/structured-prompting-techniques-xml-json/)
[28](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
[29](https://www.parloa.com/knowledge-hub/prompt-engineering-frameworks/)
[30](https://github.com/carterlasalle/aipromptxml)
[31](https://www.eesel.ai/blog/claude-code-slash-commands)
[32](https://github.com/wshobson/commands)
[33](https://www.youtube.com/watch?v=XSZP9GhhuAc&vl=pt-BR)