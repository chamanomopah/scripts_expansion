module.exports = {
  apps: [
    {
      name: "whisper-hotkey",
      script: "3_HoldtoTalk-Whisper.py",
      interpreter: "python",
      cwd: "C:/Users/Lofrey/test/scripts_ativos/",
      watch: false,
      autorestart: true
    },
    // Adicione outros scripts aqui futuramente
    {
      name: "outro-script",
      script: "outro_arquivo.py",
      interpreter: "python",
      cwd: "C:/Users/Lofrey/test/scripts_ativos/",
      watch: false,
      autorestart: true
    }
  ]
}