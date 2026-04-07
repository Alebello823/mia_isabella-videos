import requests, threading, time, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform

API_URL = "https://TU-APP.onrender.com" # Cambia esto tras subir a Render

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.input = TextInput(hint_text="Pega el link aquí", multiline=False)
        self.add_widget(self.input)
        self.status = Label(text="Listo")
        self.add_widget(self.status)
        self.btn = Button(text="DESCARGAR", on_press=self.start_task)
        self.add_widget(self.btn)

    def start_task(self, instance):
        threading.Thread(target=self.download_logic).start()

    def download_logic(self):
        url = self.input.text
        if not url: return
        
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', "⏳ Procesando..."))
        
        try:
            # 1. Solicitar al servidor
            r = requests.post(f"{API_URL}/download", json={"url": url}, timeout=150)
            data = r.json()
            file_id = data["file_id"]
            total_size = data["size"]
            
            # 2. Preparar ruta en Android
            filename = f"video_{int(time.time())}.mp4"
            if platform == 'android':
                from android.storage import primary_external_storage_path
                save_path = os.path.join(primary_external_storage_path(), "Download", filename)
            else:
                save_path = filename

            # 3. Descarga real con progreso
            res = requests.get(f"{API_URL}/file/{file_id}", stream=True)
            downloaded = 0
            with open(save_path, "wb") as f:
                for chunk in res.iter_content(chunk_size=1024*512):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        percent = int((downloaded / total_size) * 100)
                        Clock.schedule_once(lambda dt, p=percent: setattr(self.status, 'text', f"📥 {p}%"))
            
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', f"✅ Guardado: {filename}"))
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.status, 'text', f"❌ Error: {str(e)}"))

class DownloaderApp(App):
    def build(self): return MainLayout()

if __name__ == "__main__":
    DownloaderApp().run()

