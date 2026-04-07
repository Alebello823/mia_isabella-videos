import os
import time
import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform

API_URL = "https://Ale2398.pythonanywhere.com"

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        self.input = TextInput(hint_text="Pega el enlace aquí", multiline=False)
        self.add_widget(self.input)

        self.status = Label(text="Listo", color=(1, 1, 1, 1))
        self.add_widget(self.status)

        self.btn = Button(text="DESCARGAR AHORA", background_color=(0, 0.6, 0, 1))
        self.btn.bind(on_press=self.start_download)
        self.add_widget(self.btn)

    def start_download(self, instance):
        url = self.input.text.strip()
        if url:
            self.btn.disabled = True
            self.status.text = "⏳ Conectando..."
            threading.Thread(target=self.download_logic, args=(url,)).start()

    def download_logic(self, video_url):
        try:
            # 1. Solicitud al servidor
            response = requests.post(f"{API_URL}/download", json={"url": video_url}, timeout=35)

            if response.status_code != 200:
                Clock.schedule_once(lambda dt: self.update_status("❌ Error en servidor"))
                self.enable_button()
                return

            data = response.json()
            file_id = data.get("file_id")

            if not file_id:
                Clock.schedule_once(lambda dt: self.update_status("❌ Respuesta inválida"))
                self.enable_button()
                return

            total_size = data.get("size", 0)
            filename = data.get("filename", f"video_{int(time.time())}.mp4")

            # 2. Ruta de guardado robusta
            if platform == 'android':
                from android.storage import primary_external_storage_path
                download_dir = os.path.join(primary_external_storage_path(), "Download")

                if not os.path.exists(download_dir):
                    download_dir = "/storage/emulated/0/Download"

                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)

                save_path = os.path.join(download_dir, filename)
            else:
                save_path = filename

            # 3. Descargar archivo
            res = requests.get(f"{API_URL}/file/{file_id}", stream=True, timeout=30)

            if res.status_code != 200:
                Clock.schedule_once(lambda dt: self.update_status("❌ Error descargando archivo"))
                self.enable_button()
                return

            downloaded = 0

            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            Clock.schedule_once(lambda dt, p=percent: self.update_status(f"📥 {p}%"))

            Clock.schedule_once(lambda dt: self.update_status("✅ Guardado en Descargas"))
            self.enable_button()

        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f"❌ Error: {str(e)[:30]}"))
            self.enable_button()

    def update_status(self, text):
        self.status.text = text

    def enable_button(self):
        Clock.schedule_once(lambda dt: setattr(self.btn, 'disabled', False))


class DownloaderApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    DownloaderApp().run()

