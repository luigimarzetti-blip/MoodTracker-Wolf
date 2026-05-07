import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

# --- SCHERMATA 1: SELEZIONE ICONE ---
class IconScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        layout.add_widget(Label(text="Come ti senti oggi?", font_size='24sp', bold=True, size_hint_y=0.2))

        grid = GridLayout(cols=2, spacing=15)
        umori = {
            "Radioso": "radioso.png", "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png", "Triste": "triste.png",
            "Rabbioso": "rabbioso.png", "Stanco": "stanco.png"
        }

        for nome, img in umori.items():
            # Nota: se non hai i file .png, l'app userà dei rettangoli bianchi, ma non crasherà
            btn = Button(text=nome, background_normal=img) 
            btn.bind(on_release=self.seleziona_umore)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)

    def seleziona_umore(self, instance):
        # Passa l'umore scelto alla schermata successiva e cambia schermata
        app = App.get_running_app()
        app.umore_scelto = instance.text
        self.manager.current = 'details'

# --- SCHERMATA 2: SLIDER E NOTE ---
class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.lbl_titolo = Label(text="Dettagli Umore", font_size='20sp', size_hint_y=0.1)
        self.layout.add_widget(self.lbl_titolo)

        self.layout.add_widget(Label(text="Affina l'intensità (1-10):", size_hint_y=0.1))
        self.slider = Slider(min=1, max=10, value=5, step=1, size_hint_y=0.1)
        self.layout.add_widget(self.slider)

        self.input_note = TextInput(hint_text="Aggiungi una nota...", multiline=True, size_hint_y=0.4)
        self.layout.add_widget(self.input_note)

        btn_box = BoxLayout(size_hint_y=0.2, spacing=10)
        btn_salva = Button(text="SALVA TUTTO", background_color=get_color_from_hex('#4CAF50'))
        btn_salva.bind(on_press=self.salva_finale)
        
        btn_back = Button(text="INDIETRO", background_color=get_color_from_hex('#808080'))
        btn_back.bind(on_press=self.vai_indietro)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_salva)
        self.layout.add_widget(btn_box)
        self.add_widget(self.layout)

    def vai_indietro(self, instance):
        self.manager.current = 'icons'

    def salva_finale(self, instance):
        app = App.get_running_app()
        app.salva_dati(app.umore_scelto, int(self.slider.value), self.input_note.text)
        self.input_note.text = ""
        self.manager.current = 'icons'

# --- APP PRINCIPALE ---
class MoodTrackerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#1A1A2E')
        self.file_path = "storia_umore.json"
        self.umore_scelto = ""
        
        sm = ScreenManager()
        sm.add_widget(IconScreen(name='icons'))
        sm.add_widget(DetailScreen(name='details'))
        return sm

    def salva_dati(self, icona, intensita, nota):
        oggi = datetime.now().strftime("%Y-%m-%d %H:%M")
        nuovo_dato = {"data": oggi, "tipo": icona, "intensita": intensita, "nota": nota}
        
        dati = self.leggi_dati()
        dati.append(nuovo_dato)
        
        with open(self.file_path, 'w') as f:
            json.dump(dati, f, indent=4)
        
        self.apri_popup("Successo", f"Umore {icona} salvato!")

    def leggi_dati(self):
        if not os.path.exists(self.file_path): return []
        try:
            with open(self.file_path, 'r') as f: return json.load(f)
        except: return []

    def apri_popup(self, titolo, messaggio):
        layout = BoxLayout(orientation='vertical', padding=10)
        layout.add_widget(Label(text=messaggio))
        btn = Button(text="OK", size_hint_y=0.4)
        popup = Popup(title=titolo, content=layout, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        layout.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    MoodTrackerApp().run()
