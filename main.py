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
from collections import Counter

# --- IMPORT PUBBLICITÀ ---
try:
    from kivmob import KivMob, TestIds
    KIVMOB_DISPONIBILE = True
except ImportError:
    KIVMOB_DISPONIBILE = False

class IconScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        layout.add_widget(Label(text="Come ti senti oggi?", font_size='24sp', bold=True, size_hint_y=0.15))

        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.6)
        umori = {
            "Radioso": "radioso.png", "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png", "Triste": "triste.png",
            "Rabbioso": "rabbioso.png", "Stanco": "stanco.png"
        }

        for nome, img in umori.items():
            # Tolto il testo (text=nome) per non vederlo due volte sopra l'icona
            btn = Button(background_normal=img) 
            btn.bind(on_release=lambda x, n=nome: self.vai_a_dettagli(n))
            grid.add_widget(btn)
        
        layout.add_widget(grid)

        # AGGIUNTO TASTO STATISTICHE
        btn_stats = Button(text="VEDI STATISTICHE", size_hint_y=0.15, background_color=get_color_from_hex('#FFD700'), color=(0,0,0,1), bold=True)
        btn_stats.bind(on_release=lambda x: App.get_running_app().mostra_statistiche())
        layout.add_widget(btn_stats)

        self.add_widget(layout)

    def vai_a_dettagli(self, nome_umore):
        app = App.get_running_app()
        app.umore_scelto = nome_umore
        self.manager.current = 'details'

class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.lbl_info = Label(text="Dettagli", font_size='20sp', size_hint_y=0.1)
        layout.add_widget(self.lbl_info)

        layout.add_widget(Label(text="Intensità (1-10):", size_hint_y=0.1))
        self.slider = Slider(min=1, max=10, value=5, step=1, size_hint_y=0.1)
        layout.add_widget(self.slider)

        self.input_note = TextInput(hint_text="Nota del giorno...", multiline=True, size_hint_y=0.4)
        layout.add_widget(self.input_note)

        btn_box = BoxLayout(size_hint_y=0.2, spacing=10)
        btn_salva = Button(text="SALVA", background_color=get_color_from_hex('#4CAF50'))
        btn_salva.bind(on_press=self.salva_e_torna)
        
        btn_back = Button(text="ANNULLA", background_color=get_color_from_hex('#808080'))
        btn_back.bind(on_press=self.annulla)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_salva)
        layout.add_widget(btn_box)
        self.add_widget(layout)

    def annulla(self, instance):
        self.manager.current = 'icons'

    def salva_e_torna(self, instance):
        app = App.get_running_app()
        app.salva_dati(app.umore_scelto, int(self.slider.value), self.input_note.text)
        self.input_note.text = ""
        self.manager.current = 'icons'

class MoodTrackerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#1A1A2E')
        self.file_path = "storia_umore.json"
        self.umore_scelto = ""
        
        # --- LOGICA PUBBLICITÀ ---
        if KIVMOB_DISPONIBILE:
            # Sostituisci con il tuo ID reale se lo hai
            self.ads = KivMob("ca-app-pub-3940256099942544~3347511713") 
            self.ads.new_banner(TestIds.BANNER, top_pos=False)
            self.ads.request_banner()
            self.ads.show_banner()

        sm = ScreenManager()
        sm.add_widget(IconScreen(name='icons'))
        sm.add_widget(DetailScreen(name='details'))
        return sm

    def leggi_dati(self):
        if not os.path.exists(self.file_path): return []
        try:
            with open(self.file_path, 'r') as f: return json.load(f)
        except: return []

    def salva_dati(self, icona, intensita, nota):
        dati = self.leggi_dati()
        dati.append({
            "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "umore": icona,
            "intensita": intensita,
            "nota": nota
        })
        with open(self.file_path, 'w') as f:
            json.dump(dati, f, indent=4)

    def mostra_statistiche(self):
        dati = self.leggi_dati()
        if not dati:
            testo = "Ancora nessun dato."
        else:
            conteggio = Counter([d['umore'] for d in dati])
            testo = f"Registrazioni totali: {len(dati)}\n\n"
            for u, v in conteggio.items():
                testo += f"• {u}: {v} volte\n"

        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=testo))
        btn = Button(text="CHIUDI", size_hint_y=0.2)
        popup = Popup(title="Statistiche", content=content, size_hint=(0.85, 0.7))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    MoodTrackerApp().run()
