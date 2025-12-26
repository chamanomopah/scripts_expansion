# Evoluir PoC do Claude Code SDK - Análise e Sugestões v2

Analisa PoCs existentes criados com Claude Code SDK e gera relatório de melhorias especializadas. Use quando você tiver um PoC funcional que precisa evoluir para production-ready, ou quando quiser identificar oportunidades de usar features avançadas do SDK (custom tools, hooks, MCP servers, streaming). Siga ``Instruções`` para o fluxo completo de análise e relatório, e confirme os resultados em ``Relatório``.

## Contexto & Variáveis

**Persona**: Arquiteto de Software especializado em Claude Code SDK Python, focado em refatoração, performance, escalabilidade e melhores práticas de async/await, MCP servers, hooks e estruturas do SDK.

**Variáveis:**
- `$ARGUMENTS`: Caminho para o arquivo PoC ou descrição do PoC a analisar

**Documentação de Referência:**
- **Arquivo completo**: `C:\Users\Lofrey\test\docs\claude_code_docs\claude_sdk_py_docs.md`
- **Conhecimento especializado**:
  - Padrões avançados do SDK (ClaudeSDKClient vs query, streaming, interrupts)
  - Best practices de performance (buffering, conexões, async patterns)
  - Custom tools e MCP servers (escalabilidade, organização)
  - Hooks para modificação de comportamento
  - Permission modes e segurança
  - Error handling e retry logic
  - Estrutura de mensagens e content blocks

## Análise de Contexto

- **Complexidade**: alta (análise de código, planejamento, decisões do usuário)
- **Interatividade**: alta (perguntas específicas, seleção de melhorias)
- **Dependências**: nenhuma (análise estática + conhecimento SDK)
- **Validação Necessária**: não (relatório analítico)
- **Tipo Principal**: análise e planejamento de evolução

## Instruções Principais

### 1. Leitura e Análise do PoC

**Ler o arquivo PoC:**
- Usar `Read` no caminho fornecido em `$ARGUMENTS`
- Identificar padrões atuais:
  - Usa `query()` ou `ClaudeSDKClient`?
  - Tem custom tools? Hooks?
  - Permission mode definido?
  - Error handling presente?
  - Estrutura de async/await correta?
  - Dependencies PEP 723 completas?

### 2. Modo Plan - Perguntas Específicas

Fazer perguntas ao usuário para entender contexto:

**Sobre Objetivo:**
1. "Qual é o objetivo principal deste PoC?"
   - [ ] Automação de tarefas simples
   - [ ] Sistema de conversação contínua
   - [ ] Processamento de dados em lote
   - [ ] Interface interativa com usuário
   - [ ] Serviço/background worker
   - [ ] Outro: ________

2. "Qual é a escala pretendida?"
   - [ ] Uso pessoal/single-user
   - [ ] Pequeno time (2-5 pessoas)
   - [ ] Time médio/grande
   - [ ] Produção pública

3. "Quais são os principais pain points atuais?"
   - [ ] Performance/lentidão
   - [ ] Falta de recursos/funcionalidades
   - [ ] Erros frequentes
   - [ ] Dificuldade de manutenção
   - [ ] Limitação de escalabilidade
   - [ ] Outro: ________

4. "Há requisitos específicos?"
   - [ ] Needs custom tools/MCP
   - [ ] Precisa de hooks (logging, validação)
   - [ ] Requer persistência de sessão
   - [ ] Deve ser tolerante a falhas
   - [ ] Requer monitoramento/logging
   - [ ] Outro: ________

### 3. Análise de Melhorias Potenciais

Baseado nas respostas, analisar e sugerir melhorias do SDK:

**A) Padronização de Estrutura:**
- Migrar de `query()` para `ClaudeSDKClient` se precisar de contexto
- Adicionar contexto manager (`async with`)
- Implementar retry logic para erros
- Estruturar em classes/funções modulares

**B) Features do SDK:**
- **Custom Tools**: Criar `@tool` decorators para lógica reutilizável
- **MCP Server**: `create_sdk_mcp_server()` para expor funcionalidades
- **Hooks**: Adicionar `PreToolUse`, `PostToolUse` para logging/validação
- **Streaming**: Usar streaming input para dados em tempo real
- **Interrupts**: Implementar `interrupt()` para cancelamento

**C) Performance & Confiabilidade:**
- Configurar `max_buffer_size` adequadamente
- Usar `permission_mode` apropriado (evitar prompts desnecessários)
- Implementar timeout handling
- Adicionar structured outputs (`output_format`) se aplicável
- Error handling específico (CLINotFoundError, ProcessError, etc.)

**D) Segurança & Permissões:**
- Usar `can_use_tool` callback para validação customizada
- Configurar `allowed_tools` whitelist
- Implementar sandboxing se necessário
- Adicionar hooks de segurança para operações perigosas

**E) Manutenibilidade:**
- Separar configuração (ClaudeAgentOptions) em módulo próprio
- Criar factories para options reutilizáveis
- Adicionar logging estruturado
- Documentar com docstrings
- Type hints completos

**F) Escalabilidade:**
- Implementar connection pooling se múltiplas sessões
- Usar `agents` para delegar tarefas especializadas
- Configurar `setting_sources` para settings compartilhados
- Adicionar monitoramento (hooks para métricas)

### 4. Geração do Relatório de Melhorias

Estrutura do relatório (markdown):

```markdown
# Relatório de Evolução: [nome_do_poc.py]

## Contexto do PoC

**Objetivo Principal**: [extraído das respostas]
**Escala**: [extraído das respostas]
**Pain Points**: [extraído das respostas]

## Análise Atual

### Padrões Identificados
- [x] Usa: `query()` / `ClaudeSDKClient`
- [x] Tem: custom tools / hooks / MCP
- [x] Permission mode: [atual]
- [x] Error handling: [presente/ausente]
- [x] Estrutura: [modular/monolítico]

### Pontos Fortes
- [Lista do que está bom]

### Áreas de Melhoria
- [Lista do que pode evoluir]

## Sugestões de Evolução (Priorizadas)

### 🔥 CRÍTICAS (Fazer primeiro)

1. **[Título da melhoria]**
   - **Problema**: [Descrição]
   - **Solução**: [Como implementar com SDK]
   - **Benefício**: [Impacto]
   - **Complexidade**: [baixa/média/alta]
   - **Partes do SDK**: [Referência à doc, ex: linhas 221-443]

2. **[Outra melhoria crítica]**
   - ...

### ⚡ IMPORTANTES (Fazer depois)

1. **[Título]**
   - **Problema**: ...
   - **Solução**: ...
   - **Benefício**: ...
   - **Complexidade**: ...
   - **Partes do SDK**: ...

### 💡 NICE-TO-HAVE (Opcional)

1. **[Título]**
   - ...

## Recomendação de Implementação

### Fase 1 - Fundamentos
- Implementar: [lista das críticas]
- Tempo estimado: [X horas]
- Impacto: [descrição]

### Fase 2 - Features Avançadas
- Implementar: [lista das importantes]
- Tempo estimado: [X horas]
- Impacto: [descrição]

### Fase 3 - Otimização & Polimento
- Implementar: [lista das nice-to-have]
- Tempo estimado: [X horas]
- Impacto: [descrição]

## Seções do SDK Necessárias

Para implementar estas melhorias, consulte:
- [Lista de seções específicas da doc com linhas]

## Próximos Passos

1. Revê este relatório
2. Selecionar as melhorias desejadas
3. Executar `/sdk_automation_implement [arquivo_poc]` com as escolhas

---

**Data**: [timestamp]
**Analisado por**: Claude Code SDK Analyzer
```

### 5. Interação com Usuário

**Após análise, perguntar:**
- "Estas sugestões fazem sentido para seu caso?"
- "Quer priorizar alguma área específica?"
- "Há alguma melhoria que não gostaria de implementar?"

**Ajustar relatório baseado no feedback.**

## Critérios de Qualidade

- Análise profunda do código existente
- Perguntas relevantes para entender contexto
- Sugestões baseadas em features reais do SDK
- Priorização clara (críticas vs nice-to-have)
- Referências precisas à documentação (linhas)
- Relatório estruturado e acionável

## Entrega & Finalização

Após análise, apresente:

1. **Relatório completo** em formato markdown salvo como `[nome]_EVOLVE_REPORT.md`
2. **Resumo executivo** (3-5 bullets principais)
3. **Seções do SDK** relevantes para implementação
4. **Próximo comando** para usar: `/sdk_automation_implement [arquivo_poc]`

## Relatório

Ao final, confirme:

1. **Arquivo analisado**: `[caminho/para/poc.py]`
2. **Relatório gerado**: `[caminho/para/poc_EVOLVE_REPORT.md]`
3. **Total de sugestões**: `[X críticas, Y importantes, Z nice-to-have]`
4. **Comando para implementação**: `/sdk_automation_implement [arquivo_poc]`
