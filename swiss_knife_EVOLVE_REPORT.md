# Relatório de Evolução: Swiss Knife System

## Contexto do PoC

**Objetivo Principal**: Sistema pessoal de uso intensivo no dia a dia, precisando de mais ferramentas e melhor manutenibilidade

**Escala**: Uso pessoal single-user, mas com pretensão de uso extensivo

**Pain Points**:
- Falta de funcionalidades (quer mais ferramentas)
- Manutenibilidade precária
- Limitação de escalabilidade (múltiplas sessões)
- Necessidade de persistência de dados

## Análise Atual

### Padrões Identificados

- [x] Usa: `query()` (cria nova sessão a cada interação)
- [x] Tem: custom tools (não implementado ainda)
- [x] Hooks: não
- [x] MCP: não
- [x] Permission mode: "default" (linha 204)
- [x] Error handling: básico (try/except genérico)
- [x] Estrutura: monolítica em um único arquivo

### Pontos Fortes

✅ **PEP 723 bem estruturado** - Dependências inline com `uv`
✅ **Arquitetura modular** - `ToolRegistry` e `ToolConfig` bem separados
✅ **Interface intuitiva** - Hotkey ScrollLock, system tray, troca de ferramentas
✅ **Integração Whisper** - Transcrição de voz funcional
✅ **Uso do SDK** - Já utiliza `query()` do Claude Agent SDK

### Áreas de Melhoria

❌ **Query() vs ClaudeSDKClient** - Cria nova sessão a cada prompt (sem contexto)
❌ **Sem custom tools** - Ferramentas são funções internas, não SDK tools
❌ **Sem hooks** - Não há logging, métricas ou telemetria
❌ **Sem persistência** - Histórico de uso perdido ao encerrar
❌ **Monolítico** - 369 linhas em um único arquivo
❌ **Error handling genérico** - Não usa exceções específicas do SDK
❌ **Sem retry logic** - Falhas de rede não são recuperadas
❌ **Sem context manager** - Não usa `async with` para gerenciamento de conexão

## Sugestões de Evolução (Priorizadas)

### 🔥 CRÍTICAS (Fazer primeiro)

#### 1. **Migrar de `query()` para `ClaudeSDKClient`**

- **Problema**: Cada prompt cria uma nova sessão, sem conversação contínua. Claude não lembra contextos anteriores.
- **Solução**: Usar `ClaudeSDKClient` com context manager `async with`

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions

class PromptAssistantTool:
    def __init__(self):
        self.client: Optional[ClaudeSDKClient] = None
        self.options = ClaudeAgentOptions(
            system_prompt="Você é especialista em prompts...",
            permission_mode="default",
            cwd=str(PROJECT_DIR)
        )

    async def initialize(self):
        """Inicializa cliente persistente"""
        self.client = ClaudeSDKClient(options=self.options)
        await self.client.connect()

    async def process_prompt(self, text: str) -> str:
        """Processa com contexto mantido"""
        if not self.client:
            await self.initialize()

        await self.client.query(text)
        result = []

        async for message in self.client.receive_response():
            if hasattr(message, 'content'):
                for block in message.content:
                    if hasattr(block, 'text'):
                        result.append(block.text)

        return ''.join(result)

    async def cleanup(self):
        """Fecha conexão"""
        if self.client:
            await self.client.disconnect()
```

- **Benefício**: Maném contexto entre prompts, possibility de follow-ups, sessão persistente
- **Complexidade**: Média (requer refatoração de `SwissKnifeSystem`)
- **Partes do SDK**: Linhas 221-443 (ClaudeSDKClient)

#### 2. **Implementar Custom Tools com `@tool` decorator**

- **Problema**: Ferramentas atuais são funções Python comuns, não reaproveitáveis pelo SDK
- **Solução**: Criar MCP tools com decorator `@tool` para cada ferramenta

```python
from claude_agent_sdk import tool, create_sdk_mcp_server
from typing import Any

@tool(
    name="format_prompt",
    description="Formata texto como prompt bem estruturado",
    input_schema={"text": str, "style": str}
)
async def format_prompt_tool(args: dict[str, Any]) -> dict[str, Any]:
    """Tool para formatação de prompts"""
    text = args["text"]
    style = args.get("style", "detailed")

    # Lógica de formatação existente
    formatted = await format_text_as_prompt(text, style)

    return {
        "content": [{
            "type": "text",
            "text": formatted
        }]
    }

@tool(
    name="translate_text",
    description="Traduz texto para idioma especificado",
    input_schema={"text": str, "target_lang": str}
)
async def translate_tool(args: dict[str, Any]) -> dict[str, Any]:
    """Tool para tradução"""
    # Implementação de tradução
    pass

# Criar servidor MCP com as tools
mcp_server = create_sdk_mcp_server(
    name="swiss_knife_tools",
    version="1.0.0",
    tools=[format_prompt_tool, translate_tool]
)
```

- **Benefício**: Tools reaproveitáveis, documentação automática, validação de schema
- **Complexidade**: Média (requer criar MCP server)
- **Partes do SDK**: Linhas 99-157 (tool decorator), 159-217 (create_sdk_mcp_server)

#### 3. **Implementar Hooks para Logging e Métricas**

- **Problema**: Sem visibilidade do que está acontecendo (quais tools usadas, tempo de resposta, erros)
- **Solução**: Adicionar hooks `PreToolUse`, `PostToolUse` para telemetria

```python
from pathlib import Path
import json
from datetime import datetime

class SwissKnifeHooks:
    """Hooks para logging de uso do sistema"""

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_log = self.log_dir / f"usage_{datetime.now().strftime('%Y%m%d')}.jsonl"

    async def pre_tool_use(self, event):
        """Antes de usar uma tool"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "pre_tool_use",
            "tool": event.tool_name,
            "args": event.args
        }
        self._write_log(log_entry)

    async def post_tool_use(self, event):
        """Depois de usar uma tool"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "post_tool_use",
            "tool": event.tool_name,
            "duration_ms": event.duration_ms,
            "result": "success" if event.error is None else "error"
        }
        self._write_log(log_entry)

    def _write_log(self, entry: dict):
        with open(self.current_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

# Configurar hooks nas options
hooks = SwissKnifeHooks(CONFIG_DIR / "logs")

options = ClaudeAgentOptions(
    hooks={
        "PreToolUse": [hooks.pre_tool_use],
        "PostToolUse": [hooks.post_tool_use]
    }
)
```

- **Benefício**: Auditoria completa de uso, debugging facilitado, métricas de performance
- **Complexidade**: Baixa
- **Partes do SDK**: Linhas 510-511 (hooks parameter em ClaudeAgentOptions)

#### 4. **Adicionar Persistência de Dados**

- **Problema**: Perde histórico de prompts ao encerrar aplicação
- **Solução**: Implementar persistência com SQLite ou JSON

```python
import sqlite3
from dataclasses import dataclass
from datetime import datetime

@dataclass
class PromptHistory:
    id: int
    timestamp: str
    tool_name: str
    input_text: str
    output_text: str
    audio_duration_ms: int

class HistoryManager:
    """Gerencia histórico de uso"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                tool_name TEXT,
                input_text TEXT,
                output_text TEXT,
                audio_duration_ms INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def save_entry(self, entry: PromptHistory):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            INSERT INTO history (timestamp, tool_name, input_text, output_text, audio_duration_ms)
            VALUES (?, ?, ?, ?, ?)
        """, (entry.timestamp, entry.tool_name, entry.input_text, entry.output_text, entry.audio_duration_ms))
        conn.commit()
        conn.close()

    def get_recent(self, limit: int = 10) -> list[PromptHistory]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("""
            SELECT * FROM history ORDER BY id DESC LIMIT ?
        """, (limit,))
        results = [PromptHistory(*row) for row in cursor.fetchall()]
        conn.close()
        return results

# Usar em SwissKnifeSystem
history = HistoryManager(CONFIG_DIR / "history.db")

def on_scroll_lock_pressed(self):
    start_time = time.time()

    # ... gravação e processamento ...

    audio_duration = int((time.time() - start_time) * 1000)

    # Salvar no histórico
    history.save_entry(PromptHistory(
        timestamp=datetime.now().isoformat(),
        tool_name=self.tool_registry.get_current_tool().name,
        input_text=text,
        output_text=result,
        audio_duration_ms=audio_duration
    ))
```

- **Benefício**: Histórico completo, análise de uso posterior, recuperação de prompts úteis
- **Complexidade**: Baixa
- **Partes do SDK**: Não é específico do SDK (best practice geral)

### ⚡ IMPORTANTES (Fazer depois)

#### 5. **Implementar Structured Outputs com `output_format`**

- **Problema**: Respostas do Claude são texto livre, difícil de parsear de forma confiável
- **Solução**: Usar `output_format` com JSON Schema para validar saídas

```python
from claude_agent_sdk import ClaudeAgentOptions

prompt_schema = {
    "type": "object",
    "properties": {
        "formatted_prompt": {
            "type": "string",
            "description": "O prompt formatado e melhorado"
        },
        "changes_made": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Lista de mudanças realizadas no texto original"
        },
        "confidence_score": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
            "description": "Quão confiante está na formatação"
        }
    },
    "required": ["formatted_prompt", "changes_made", "confidence_score"]
}

options = ClaudeAgentOptions(
    system_prompt="Formate prompts...",
    output_format={
        "type": "json_schema",
        "schema": prompt_schema
    }
)
```

- **Benefício**: Saídas estruturadas e validadas, parsing confiável, menos erros
- **Complexidade**: Média (requer definir schemas para cada tool)
- **Partes do SDK**: Linhas 520-534 (OutputFormat), 500 (output_format parameter)

#### 6. **Adicionar Error Handling Específico do SDK**

- **Problema**: Exceções genéricas não permitem recovery adequado
- **Solução**: Capturar exceções específicas como `CLINotFoundError`, `ProcessError`

```python
from claude_agent_sdk.exceptions import (
    CLINotFoundError,
    ProcessError,
    ToolUseError
)

async def _process_prompt_assistant(self, text: str) -> str:
    try:
        options = ClaudeAgentOptions(...)
        result = []

        async for message in query(prompt=text, options=options):
            # Processar mensagens...

        return ''.join(result)

    except CLINotFoundError:
        print("[ERRO] CLI do Claude Code não encontrado. Instale com: pip install claude-agent-sdk")
        return text

    except ProcessError as e:
        print(f"[ERRO] Erro no processo CLI: {e}")
        # Retry logic
        return await self._retry_with_backoff(text)

    except ToolUseError as e:
        print(f"[ERRO] Erro ao usar tool: {e.tool_name}")
        # Fallback para formatação local
        return self._format_locally(text)

    except Exception as e:
        print(f"[ERRO INESPERADO] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return text

async def _retry_with_backoff(self, text: str, max_retries: int = 3) -> str:
    """Retry com exponential backoff"""
    import asyncio

    for attempt in range(max_retries):
        try:
            await asyncio.sleep(2 ** attempt)  # 1s, 2s, 4s
            return await self._process_internal(text)
        except Exception:
            if attempt == max_retries - 1:
                raise

    return text  # Fallback
```

- **Benefício**: Recovery inteligente de erros, melhor UX, menos crashes
- **Complexidade**: Baixa
- **Partes do SDK**: Documentação de exceções (não nas linhas lidas, mas existe)

#### 7. **Implementar Múltiplas Sessões Concorrentes**

- **Problema**: Sistema não suporta rodar múltiplas instâncias ao mesmo tempo
- **Solução**: Usar `session_id` diferente para cada instância do sistema

```python
import uuid

class PromptAssistantTool:
    def __init__(self):
        self.session_id = str(uuid.uuid4())
        self.client = None

    async def initialize(self):
        options = ClaudeAgentOptions(
            system_prompt="...",
            permission_mode="default"
        )

        self.client = ClaudeSDKClient(options=options)
        await self.client.connect()

    async def process_prompt(self, text: str) -> str:
        # Usa session_id único para esta instância
        await self.client.query(text, session_id=self.session_id)

        async for msg in self.client.receive_response():
            # Processa...

        return result
```

- **Benefício**: Pode rodar múltiplas instâncias do Swiss Knife ao mesmo tempo
- **Complexidade**: Baixa (basta adicionar session_id)
- **Partes do SDK**: Linhas 238 (query session_id parameter)

#### 8. **Modularizar Código em Múltiplos Arquivos**

- **Problema**: 369 linhas em um único arquivo é difícil de manter
- **Solução**: Separar em módulos por responsabilidade

```
.swiss_knife/
├── swiss_knife.py          # Entry point (main)
├── core/
│   ├── __init__.py
│   ├── system.py           # SwissKnifeSystem
│   ├── tool_registry.py    # ToolRegistry, ToolConfig
│   └── audio_handler.py    # Gravação/transcrição de áudio
├── tools/
│   ├── __init__.py
│   ├── base.py             # Tool base abstrata
│   ├── prompt_assistant.py # PromptAssistantTool
│   ├── translator.py       # TranslatorTool
│   └── code_reviewer.py    # CodeReviewerTool
├── sdk/
│   ├── __init__.py
│   ├── client.py           # ClaudeSDKClient wrapper
│   ├── tools.py            # @tool decorators
│   └── hooks.py            # Hooks personalizados
├── storage/
│   ├── __init__.py
│   ├── history.py          # HistoryManager
│   └── config.py           # ConfigManager
└── ui/
    ├── __init__.py
    └── tray.py             # System tray logic
```

- **Benefício**: Código organizado, fácil de testar, manutenibilidade
- **Complexidade**: Alta (refatoração completa)
- **Partes do SDK**: Não é específico (best practice de engenharia)

### 💡 NICE-TO-HAVE (Opcional)

#### 9. **Adicionar Streaming Input para Processamento em Tempo Real**

- **Problema**: Áudio é transcrito todo de uma vez, sem feedback durante a fala
- **Solução**: Usar streaming input para processamento progressivo

```python
async def audio_stream_generator():
    """Gera chunks de áudio em tempo real"""
    audio_data = []

    def callback(indata, frames, time, status):
        audio_data.append(indata.copy())
        # Yield chunks progressivamente
        if len(audio_data) % 10 == 0:  # A cada 10 chunks
            yield {
                "type": "audio",
                "audio": np.concatenate(audio_data[-10:]).flatten().tolist()
            }

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        while keyboard.is_pressed(HOTKEY):
            await asyncio.sleep(0.1)

# Usar streaming input no query
async for message in query(prompt=audio_stream_generator(), options=options):
    # Processa mensagens progressivas
    pass
```

- **Benefício**: Feedback em tempo real, UX mais responsiva
- **Complexidade**: Alta
- **Partes do SDK**: Linhas 311-344 (streaming input example)

#### 10. **Implementar Interrupts para Cancelamento**

- **Problema**: Não pode cancelar um prompt em andamento
- **Solução**: Adicionar hotkey para `interrupt()`

```python
class SwissKnifeSystem:
    def __init__(self):
        self.client = None
        self.processing = False

        # Hotkey para cancelar
        keyboard.add_hotkey('esc', self.cancel_processing)

    async def cancel_processing(self):
        """Cancela processamento atual"""
        if self.processing and self.client:
            print("[Cancelando...] Interrompendo processamento...")
            await self.client.interrupt()
            self.processing = False

    async def process_with_current_tool(self, text: str) -> str:
        self.processing = True

        try:
            await self.client.query(text)
            # Processar...
        finally:
            self.processing = False
```

- **Benefício**: Pode parar processamentos longos/demorados
- **Complexidade**: Baixa
- **Partes do SDK**: Linhas 241 (interrupt method)

#### 11. **Adicionar Agents Especializados**

- **Problema**: Uma única instância do Claude para tudo, sem especialização
- **Solução**: Delegar tarefas específicas para subagents

```python
from claude_agent_sdk import ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    system_prompt="Você é o coordenador do Swiss Knife...",
    agents={
        "prompt_expert": AgentDefinition(
            description="Especialista em criar prompts bem formatados",
            prompt="Você é um especialista em prompts. Transforme textos em prompts elaborados.",
            model="haiku"  # Modelo rápido
        ),
        "translator": AgentDefinition(
            description="Traduz textos para múltiplos idiomas",
            prompt="Você é um tradutor profissional. Traduza mantendo o contexto e tom.",
            model="sonnet"  # Modelo preciso
        ),
        "code_reviewer": AgentDefinition(
            description="Analisa e melhora código",
            prompt="Você é um code reviewer sênior. Analise código e sugira melhorias.",
            model="opus"  # Modelo mais capaz
        )
    }
)

# Delegar para agent específico
await client.query("Melhore este prompt: {...}", agent="prompt_expert")
```

- **Benefício**: Especialização por domínio, modelos diferentes por tarefa, melhor qualidade
- **Complexidade**: Média
- **Partes do SDK**: Linhas 659-678 (AgentDefinition), 484 (agents parameter)

#### 12. **Implementar Configuração Externalizada**

- **Problema**: Configurações hardcoded no código, difícil de modificar
- **Solução**: Carregar configurações de JSON/YAML

```python
import yaml
from dataclasses import dataclass

@dataclass
class SwissKnifeConfig:
    hotkey: str = "scroll_lock"
    whisper_model: str = "base"
    sample_rate: int = 16000
    auto_paste: bool = True
    log_enabled: bool = True
    tools: list[dict] = None

    @classmethod
    def from_file(cls, path: Path) -> "SwissKnifeConfig":
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls(**data)

# Usar
config = SwissKnifeConfig.from_file(CONFIG_DIR / "config.yaml")

# config.yaml:
# hotkey: scroll_lock
# whisper_model: base
# sample_rate: 16000
# auto_paste: true
# log_enabled: true
# tools:
#   - name: prompt_assistant
#     enabled: true
#     settings:
#       format_style: detailed
```

- **Benefício**: Configuração flexível sem editar código
- **Complexidade**: Baixa
- **Partes do SDK**: Não é específico (best practice)

## Recomendação de Implementação

### Fase 1 - Fundamentos (8-12 horas)

**Implementar:**
1. ✅ Migrar para `ClaudeSDKClient` (manutenção de contexto)
2. ✅ Implementar hooks de logging/telemetria
3. ✅ Adicionar persistência de histórico (SQLite)
4. ✅ Error handling específico do SDK com retry logic

**Impacto:** Sistema mais robusto, observável e com histórico de uso

### Fase 2 - Custom Tools & MCP (10-15 horas)

**Implementar:**
1. ✅ Criar custom tools com `@tool` decorator
2. ✅ Implementar MCP server com tools
3. ✅ Modularizar código em múltiplos arquivos
4. ✅ Adicionar 3-5 novas ferramentas (tradutor, resumidor, code reviewer, etc.)

**Impacto:** Arquitetura escalável, múltiplas ferramentas especializadas

### Fase 3 - Features Avançadas (8-12 horas)

**Implementar:**
1. ✅ Structured outputs com JSON Schema
2. ✅ Múltiplas sessões concorrentes
3. ✅ Interrupts para cancelamento
4. ✅ Configuração externalizada (YAML/JSON)

**Impacto:** Sistema production-ready, UX refinada, flexibilidade máxima

### Fase 4 - Polimento & Otimização (5-8 horas)

**Implementar:**
1. ✅ Streaming input para feedback em tempo real
2. ✅ Agents especializados por domínio
3. ✅ Interface gráfica de configurações (tkinter/PyQt)
4. ✅ Testes unitários e documentação

**Impacto:** Sistema profissional, usabilidade excelente

**Tempo Total Estimado:** 31-47 horas

## Seções do SDK Necessárias

Para implementar estas melhorias, consulte:

- **ClaudeSDKClient** (linhas 221-443) - Cliente persistente com sessão contínua
- **tool decorator** (linhas 99-157) - Criar custom tools com type safety
- **create_sdk_mcp_server()** (linhas 159-217) - Criar servidor MCP com tools
- **ClaudeAgentOptions** (linhas 453-518) - Configuração completa de options
- **hooks** (linhas 510-511) - PreToolUse, PostToolUse para telemetria
- **output_format** (linhas 520-534) - Structured outputs com JSON Schema
- **AgentDefinition** (linhas 659-678) - Subagents especializados
- **PermissionMode** (linhas 679-690) - Modos de permissão
- **Setting sources** (linhas 650-657) - Carregamento de configurações

## Próximos Passos

1. ✅ Revê este relatório
2. ✅ Selecionar as melhorias desejadas (recomendo Fase 1 completa)
3. ✅ Executar `/sdk_automation_implement c:\.swiss_knife\swiss_knife.py` com as escolhas

---

**Data**: 2025-12-27
**Analisado por**: Claude Code SDK Analyzer v2
**Arquivo Analisado**: `c:\.swiss_knife\swiss_knife.py`
**Total de Sugestões**: 4 críticas, 4 importantes, 4 nice-to-have
