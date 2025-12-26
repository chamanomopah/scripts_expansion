import keyboard
import sounddevice as sd
import whisper
import numpy as np
import subprocess
import os

# --- CONFIGURAÇÃO ---
HOTKEY = 'f9'         # Tecla que você vai segurar
MODEL_TYPE = 'base'    # Modelo 'base' é rápido e excelente para PT-BR
SAMPLE_RATE = 16000   # Frequência nativa do Whisper
# ---------------------

print(f"Carregando IA Whisper (modelo {MODEL_TYPE})...")
model = whisper.load_model(MODEL_TYPE)
print(f"\n>>> SISTEMA PRONTO!")
print(f">>> Segure [{HOTKEY.upper()}] em qualquer programa para falar com o Claude.")

def record_and_trigger():
    recording = []
    
    # Callback para capturar o áudio continuamente
    def callback(indata, frames, time, status):
        recording.append(indata.copy())

    print("\n[Ouvindo...] Solte a tecla para enviar.")
    
    # Inicia a captura do microfone
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        while keyboard.is_pressed(HOTKEY):
            pass # Fica aqui enquanto a tecla estiver pressionada
            
    print("[Processando...] Transcrevendo áudio...")
    
    # Converte a lista de áudio capturado para o formato da IA
    if not recording:
        print("Erro: Nenhum áudio capturado.")
        return

    audio_data = np.concatenate(recording).flatten().astype(np.float32)
    
    # Transcrição (Whisper detecta automaticamente que é português)
    result = model.transcribe(audio_data, language="pt")
    text = result["text"].strip()
    
    if text:
        print(f"[Comando Identificado]: \"{text}\"")
        print("[Executando] Abrindo Claude Code em nova janela...")
        
        # Comando para abrir uma NOVA janela de CMD e rodar o Claude
        # O 'start cmd /k' garante que a janela não feche após o comando
        # Usa --dangerously-skip-permissions para execução direta sem prompts de permissão
        full_command = f'start cmd /k "claude --dangerously-skip-permissions \"{text}\""'
        subprocess.run(full_command, shell=True)
    else:
        print("Aviso: Não entendi o que você disse.")

def main():
    while True:
        # Espera o próximo pressionamento da tecla configurada
        keyboard.wait(HOTKEY)
        record_and_trigger()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSistema encerrado.")