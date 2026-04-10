import os
import time
import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform
from kivy.properties import StringProperty, NumericProperty

API_URL = "https://Ale2398.pythonanywhere.com"


class MainLayout(BoxLayout):
    status_text = StringProperty("Listo")
    progress = NumericProperty(0)

    def start_download(self):
        url = self.ids.url_input.text.strip()

        if not url:
            self.update_status("⚠️ Pega un enlace primero")
            return

        self.ids.download_btn.disabled = True
        self.progress = 0
        self.update_status("⏳ Conectando...")

        threading.Thread(target=self.download_logic, args=(url,), daemon=True).start()

    def download_logic(self, video_url):
        try:
            # 🔹 Paso 1: pedir info al servidor
            response = requests.post(
                f"{API_URL}/download",
                json={"url": video_url},
                timeout=35
            )

            if response.status_code != 200:
                self.safe_update("❌ Error en servidor")
                return

            data = response.json()
            file_id = data.get("file_id")

            if not file_id:
                self.safe_update("❌ Respuesta inválida")
                return

            total_size = data.get("size", 0)
            filename = data.get("filename", f"video_{int(time.time())}.mp4")

            # 🔹 Ruta Android segura
            if platform == 'android':
                from android.storage import primary_external_storage_path
                base = primary_external_storage_path()
                download_dir = os.path.join(base, "Download")

                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)

                save_path = os.path.join(download_dir, filename)
            else:
                save_path = filename

            # 🔹 Paso 2: descargar archivo
            res = requests.get(
                f"{API_URL}/file/{file_id}",
                stream=True,
                timeout=30
            )

            if res.status_code != 200:
                self.safe_update("❌ Error descargando archivo")
                return

            downloaded = 0

            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=1024 * 512):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            Clock.schedule_once(lambda dt, p=percent: self.update_progress(p))

            self.safe_update("✅ Descarga completada")
        except Exception as e:
            self.safe_update(f"❌ {str(e)[:40]}")

        finally:
            Clock.schedule_once(lambda dt: setattr(self.ids.download_btn, 'disabled', False))

    def update_progress(self, value):
        self.progress = value
        self.status_text = f"📥 Descargando... {value}%"

    def update_status(self, text):
        self.status_text = text

    def safe_update(self, text):
        Clock.schedule_once(lambda dt: self.update_status(text))


class DownloaderApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    DownloaderApp().run()

