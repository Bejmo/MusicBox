from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.lang import Builder
import threading
from modules.download_music import descargar_video

Builder.load_file("interface.kv")

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.thread = None

    def start_loading(self):
        url = self.ids.link_input.text  # Obtener el texto de la barra de URL
        self.ids.feedback_label.text = f"Procesando: {url}" if url else "Introduce un enlace válido."
        
        if url:
            def download_thread(url):
                descargar_video(url)

            try:
                self.thread = threading.Thread(target=download_thread, args=(url,))
                self.thread.start()
                # self.thread.join()
            except:
                self.ids.feedback_label.text = "Se ha producido un error inesperado."

            self.ids.spinner.opacity = 1
            self.ids.stop_button.opacity = 1


    def stop_loading(self):
        if hasattr(self, 'thread') and self.thread.is_alive():
            self.thread.join(timeout=1)
        self.ids.feedback_label.text = "Descarga detenida."
        self.ids.spinner.opacity = 0
        self.ids.stop_button.opacity = 0

    def end_process(self):
        self.ids.feedback_label.text = "Proceso terminado."
        self.ids.spinner.opacity = 0
        self.ids.stop_button.opacity = 0

class MyApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    MyApp().run()