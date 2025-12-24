# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "keyboard",
#     "sounddevice",
#     "openai-whisper",
#     "numpy",
# ]
# ///

"""
Agente Pessoal ativado por voz com gerenciamento de projetos e integração Claude Code.

Funcionalidades:
- Segure F12 → grava áudio
- Solte F12 → transcreve com Whisper e processa comando
- Gerenciamento de projetos (criar, adicionar info, listar, consultar)
- Integração com Claude Code com contexto automático
"""

import keyboard
import sounddevice as sd
import whisper
import numpy as np
import subprocess
import os
import json
from pathlib import Path
from datetime import datetime

# ==================== CONFIGURAÇÃO ====================
HOTKEY = 'f12'
MODEL_TYPE = 'base'
SAMPLE_RATE = 16000

# Diretórios
BASE_DIR = Path.home() / "Agente_Pessoal"
PROJETOS_DIR = BASE_DIR / "projetos"
MEMORY_DIR = BASE_DIR / ".claude" / "memory"
AGENT_MEMORY_DIR = MEMORY_DIR / "agent_memory"
PROJECTS_METADATA_DIR = MEMORY_DIR / "projects"

# Criar estrutura de diretórios
for dir_path in [PROJETOS_DIR, AGENT_MEMORY_DIR, PROJECTS_METADATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)
# =====================================================

print(f"Carregando IA Whisper (modelo {MODEL_TYPE})...")
model = whisper.load_model(MODEL_TYPE)
print(f"\n>>> SISTEMA PRONTO!")
print(f">>> Segure [{HOTKEY.upper()}] para falar com o Agente Pessoal")

# ==================== SISTEMA DE PROJETOS ====================

def criar_projeto(nome_projeto):
    """Cria um novo projeto com sua estrutura de arquivos."""
    projeto_dir = PROJETOS_DIR / nome_projeto

    if projeto_dir.exists():
        return f"Projeto '{nome_projeto}' já existe."

    projeto_dir.mkdir(exist_ok=True)

    # Arquivo principal do projeto
    projeto_file = projeto_dir / f"{nome_projeto}.md"
    projeto_file.write_text(f"# Projeto: {nome_projeto}\n\nCriado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")

    # Metadados do projeto
    metadata = {
        "nome": nome_projeto,
        "criado_em": datetime.now().isoformat(),
        "atualizado_em": datetime.now().isoformat(),
        "arquivos": [str(projeto_file)],
        "acoes_historico": []
    }

    metadata_file = PROJECTS_METADATA_DIR / f"{nome_projeto}.json"
    metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    return f"Projeto '{nome_projeto}' criado com sucesso."

def adicionar_info_projeto(nome_projeto, informacao):
    """Adiciona informação a um projeto existente."""
    projeto_dir = PROJETOS_DIR / nome_projeto

    if not projeto_dir.exists():
        return f"Projeto '{nome_projeto}' não encontrado."

    projeto_file = projeto_dir / f"{nome_projeto}.md"

    # Adiciona nova entrada com timestamp
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    novo_conteudo = projeto_file.read_text() + f"\n## {timestamp}\n{informacao}\n"
    projeto_file.write_text(novo_conteudo)

    # Atualiza metadados
    metadata_file = PROJECTS_METADATA_DIR / f"{nome_projeto}.json"
    if metadata_file.exists():
        metadata = json.loads(metadata_file.read_text())
        metadata["atualizado_em"] = datetime.now().isoformat()
        metadata["acoes_historico"].append({
            "acao": "adicionar_info",
            "timestamp": datetime.now().isoformat(),
            "detalhes": informacao[:100] + "..." if len(informacao) > 100 else informacao
        })
        metadata_file.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    return f"Informação adicionada ao projeto '{nome_projeto}'."

def listar_projetos():
    """Lista todos os projetos disponíveis."""
    projetos = [d.name for d in PROJETOS_DIR.iterdir() if d.is_dir()]

    if not projetos:
        return "Você não tem nenhum projeto ainda."

    lista_formatada = "Seus projetos:\n" + "\n".join(f"• {p}" for p in projetos)
    return lista_formatada

def consultar_projeto(nome_projeto):
    """Consulta informações de um projeto específico."""
    projeto_dir = PROJETOS_DIR / nome_projeto

    if not projeto_dir.exists():
        return f"Projeto '{nome_projeto}' não encontrado."

    projeto_file = projeto_dir / f"{nome_projeto}.md"
    conteudo = projeto_file.read_text()

    return f"=== {nome_projeto} ===\n{conteudo}"

def salvar_acao_agente(acao, detalhes):
    """Salva histórico de ações do agente."""
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {acao}: {detalhes}\n"

    log_file = AGENT_MEMORY_DIR / "agent_log.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

# ==================== PROCESSADOR DE COMANDOS ====================

def processar_comando(texto):
    """Processa o comando de voz e executa a ação apropriada."""

    # Comandos de gerenciamento de projetos
    texto_lower = texto.lower()

    # Criar projeto
    if texto_lower.startswith("criar projeto "):
        nome_projeto = texto_lower.replace("criar projeto ", "").strip()
        resultado = criar_projeto(nome_projeto)
        salvar_acao_agente("CRIAR_PROJETO", nome_projeto)
        print(f"\n[Agente]: {resultado}")
        return

    # Adicionar ao projeto
    if texto_lower.startswith("adicionar ao projeto ") or texto_lower.startswith("adicionar a "):
        partes = texto_lower.replace("adicionar ao projeto ", "").replace("adicionar a ", "").split(" ", 1)
        if len(partes) >= 2:
            nome_projeto = partes[0]
            informacao = partes[1]
            resultado = adicionar_info_projeto(nome_projeto, informacao)
            salvar_acao_agente("ADICIONAR_INFO", f"{nome_projeto}: {informacao[:50]}...")
            print(f"\n[Agente]: {resultado}")
            return

    # Listar projetos
    if texto_lower in ["meus projetos", "listar projetos", "quais são meus projetos"]:
        resultado = listar_projetos()
        print(f"\n[Agente]: {resultado}")
        return

    # Consultar projeto
    if texto_lower.startswith("sobre o projeto ") or texto_lower.startswith("sobre "):
        nome_projeto = texto_lower.replace("sobre o projeto ", "").replace("sobre ", "").strip()
        resultado = consultar_projeto(nome_projeto)
        print(f"\n[Agente]:\n{resultado}")
        return

    # Se não for um comando de projeto, abrir Claude Code com contexto
    abrir_claude_com_contexto(texto)

def obter_contexto_projetos():
    """Obtém resumo de todos os projetos para contexto do Claude."""
    projetos = [d.name for d in PROJETOS_DIR.iterdir() if d.is_dir()]

    if not projetos:
        return ""

    contexto = "\n\n=== CONTEXTO DOS SEUS PROJETOS ===\n"

    for nome_projeto in projetos:
        metadata_file = PROJECTS_METADATA_DIR / f"{nome_projeto}.json"
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            contexto += f"\nProjeto: {nome_projeto}"
            criado_em = metadata.get('criado_em', 'N/A')
            atualizado_em = metadata.get('atualizado_em', 'N/A')
            contexto += f"\nCriado em: {criado_em[:10] if criado_em != 'N/A' else 'N/A'}"
            contexto += f"\nÚltima atualização: {atualizado_em[:10] if atualizado_em != 'N/A' else 'N/A'}"
            contexto += f"\nAções registradas: {len(metadata.get('acoes_historico', []))}\n"

    return contexto

def abrir_claude_com_contexto(texto):
    """Abre Claude Code em nova janela sem adicionar contexto extra ao prompt."""

    # Apenas o texto transcrito, sem contexto adicional
    prompt_completo = texto

    print(f"\n[Comando Geral]: \"{texto}\"")
    print("[Executando] Abrindo Claude Code...")
    salvar_acao_agente("CLAUDE_CODE", texto)

    # Comando para abrir nova janela do Claude
    full_command = f'start cmd /k "claude --dangerously-skip-permissions \"{prompt_completo}\""'
    subprocess.run(full_command, shell=True)

# ==================== CAPTURA DE ÁUDIO ====================

def record_and_trigger():
    """Grava áudio enquanto a tecla está pressionada e processa o comando."""
    import time
    recording = []

    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    print("\n[Ouvindo...] Solte F12 para enviar.")

    # Inicia stream de áudio
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        # Pequeno delay para o stream estabilizar antes de começar a capturar
        time.sleep(0.15)

        # Continua gravando enquanto a tecla estiver pressionada
        while keyboard.is_pressed(HOTKEY):
            pass

    print("[Processando...] Transcrevendo áudio...")

    if not recording:
        print("Erro: Nenhum áudio capturado.")
        return

    audio_data = np.concatenate(recording).flatten().astype(np.float32)

    # Transcrição com Whisper em português
    result = model.transcribe(audio_data, language="pt")
    text = result["text"].strip()

    if text:
        print(f"[Transcrição]: \"{text}\"")
        processar_comando(text)
    else:
        print("Aviso: Não entendi o que você disse.")

# ==================== LOOP PRINCIPAL ====================

def main():
    """Loop principal do agente."""
    print("\n" + "="*50)
    print("     AGENTE PESSOAL - SISTEMA ATIVO")
    print("="*50)
    print("\nComandos disponíveis:")
    print("  - Criar projeto [nome]")
    print("  - Adicionar ao projeto [nome] [informacao]")
    print("  - Meus projetos")
    print("  - Sobre o projeto [nome]")
    print("  - [Qualquer outro comando] -> Abre Claude Code")
    print("\n" + "="*50 + "\n")

    while True:
        keyboard.wait(HOTKEY)
        record_and_trigger()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n>>> Agente Pessoal encerrado.")
