from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window
import yt_dlp
import os
import sys

# Configura o ícone
Window.icon = "assets/icon.ico"

# Define o caminho correto para o arquivo KV
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
kv_path = os.path.join(base_path, "app.kv")

# Verifica se o arquivo KV existe antes de carregar
if os.path.exists(kv_path):
    Builder.load_file(kv_path)
else:
    print(f"Erro: Arquivo {kv_path} não encontrado!")
    sys.exit(1)  # Fecha o programa se não encontrar o KV

# Pasta de download
DOWNLOAD_PATH = os.path.expanduser("~/Downloads/Youtube")
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

class VideoDownloader:
    def __init__(self, url, formato):
        self.url = url
        self.formato = formato
        self.ffmpeg_path = r"C:\ffmpeg\bin\ffmpeg.exe"  # Ajuste se necessário

    def baixar(self):
        try:
            ydl_opts = {
                'ffmpeg_location': self.ffmpeg_path,
                'outtmpl': os.path.join(DOWNLOAD_PATH, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [self.hook]  # Adiciona feedback do progresso
            }

            if self.formato == 'mp3':
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            else:
                ydl_opts.update({'format': 'bestvideo+bestaudio', 'merge_output_format': 'mp4'})

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])

            return "✅ Download concluído!"
        except Exception as e:
            return f"❌ Erro: {e}"

    def hook(self, d):
        """ Feedback sobre o progresso do download """
        if d['status'] == 'finished':
            print(f"🎉 Download concluído: {d['filename']}")
        elif d['status'] == 'error':
            print(f"❌ Erro no download: {d}")

class MainWidget(BoxLayout):
    def iniciar_download(self):
        url = self.ids.url_input.text.strip()
        formato = 'mp3' if self.ids.audio_toggle.state == 'down' else 'mp4'
        
        if url:
            downloader = VideoDownloader(url, formato)
            resultado = downloader.baixar()
            self.ids.status_label.text = resultado
        else:
            self.ids.status_label.text = "⚠️ Insira um link válido."

class VideoDownloadApp(App):
    def build(self):
        return MainWidget()

if __name__ == "__main__":
    VideoDownloadApp().run()
