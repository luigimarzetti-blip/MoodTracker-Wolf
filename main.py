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
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from collections import Counter

# --- PUBBLICITÀ ---
try:
    from kivmob import KivMob, TestIds
    KIVMOB_DISPONIBILE = True
except ImportError:
    KIVMOB_DISPONIBILE = False

class IconScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 10], spacing=15)
        
        # Titolo
        layout.add_widget(Label(text="Come ti senti oggi?", font_size='24sp', bold=True, size_hint_y=0.1))

        # --- SCROLLVIEW PER LE ICONE ---
        scroll = ScrollView(size_hint_y=0.65)
        grid = GridLayout(cols=2, spacing=20, size_hint_y=None, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        umori = {
            "Radioso": "radioso.png", "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png", "Triste": "triste.png",
            "Rabbioso": "rabbioso.png", "Stanco": "stanco.png"
        }

        for nome, img in umori.items():
            # Creiamo un Box per ogni umore per non schiacciare l'immagine
            box_bottone = BoxLayout(orientation='vertical', size_hint_y=None, height=300, spacing=5)
            
            if os.path.exists(img):
                # Usiamo il widget Image dentro il bottone per mantenere le proporzioni
                btn_img = Button(background_normal='', background_color=(0,0,0,0))
                foto = Image(source=img, allow_stretch=True, keep_ratio=True)
                btn_img.add_widget(foto)
                # Centriamo l'immagine nel bottone
                foto.center = btn_img.center
                btn_img.bind(size=lambda instance, value, f=foto: setattr(f, 'size', value))
                btn_img.bind(pos=lambda instance, value, f=foto: setattr(f, 'pos', value))
            else:
                btn_img = Button(text=nome, background_color=get_color_from_hex('#3E3E3E'))
            
            btn_img.bind(on_release=lambda x, n=nome: self.vai_a_dettagli(n))
            
            box_bottone.add_widget(btn_img)
            box_bottone.add_widget(Label(text=nome, size_hint_y=None, height=30, font_size='14sp'))
            grid.add_widget(box_bottone)
        
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        # --- TASTO STATISTICHE ---
        self.btn_stats = Button(
            text="VEDI STATISTICHE", 
            size_hint_y=0.12, 
            background_color=get_color_from_hex('#FFD700'), 
            color=(0,0,0,1), 
            bold=True
        )
        self.btn_stats.bind(on_release=lambda x: App.get_running_app().mostra_statistiche())
        layout.add_widget(self.btn_stats)

        # --- SPAZIATORE PER IL BANNER ADMOB ---
        # Aggiungiamo un vuoto in fondo così il banner non copre il tasto statistiche
        layout.add_widget(Widget(size_hint_y=None, height=120))

        self.add_widget(layout)

    def vai_a_dettagli(self, nome_umore):
        app = App.get_running_app()
        app.umore_scelto = nome_umore
        self.manager.current = 'details'

class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="Dettagli Umore", font_size='20sp', size_hint_y=0.1))
        layout.add_widget(Label(text="Intensità (1-10):", size_hint_y=0.1))
        self.slider = Slider(min=1, max=10, value=5, step=1, size_hint_y=0.1)
        layout.add_widget(self.slider)
        self.input_note = TextInput(hint_text="Aggiungi una nota...", multiline=True, size_hint_y=0.4)
        layout.add_widget(self.input_note)
        btn_box = BoxLayout(size_hint_y=0.2, spacing=10)
        btn_salva = Button(text="SALVA", background_color=get_color_from_hex('#4CAF50'), bold=True)
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
        self.file_path = os.path.join(self.user_data_dir, "storia_umore.json")
        self.umore_scelto = ""
        sm = ScreenManager()
        sm.add_widget(IconScreen(name='icons'))
        sm.add_widget(DetailScreen(name='details'))
        return sm

    def on_start(self):
        if KIVMOB_DISPONIBILE:
            try:
                # --- USIAMO ID DI TEST PER VEDERE SE FUNZIONA ---
                # ID Test AdMob generico (Funziona sempre per i test)
                self.ads = KivMob("ca-app-pub-3940256099942544~3347511713") 
                self.ads.new_banner("ca-app-pub-3940256099942544/6300978111", top_pos=False)
                self.ads.request_banner()
                self.ads.show_banner()
            except Exception as e:
                print(f"Errore Ads: {e}")

    def leggi_dati(self):
        if not os.path.exists(self.file_path): return []
        try:
            with open(self.file_path, 'r') as f: return json.load(f)
        except: return []

    def salva_dati(self, icona, intensita, nota):
        dati = self.leggi_dati()
        dati.append({"data": datetime.now().strftime("%Y-%m-%d %H:%M"), "umore": icona, "intensita": intensita, "nota": nota})
        with open(self.file_path, 'w') as f: json.dump(dati, f, indent=4)

    def mostra_statistiche(self):
        dati = self.leggi_dati()
        testo = "Nessun dato." if not dati else f"Registrazioni: {len(dati)}\n\n" + "\n".join([f"• {u}: {v}" for u, v in Counter([d['umore'] for d in dati]).items()])
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=testo))
        btn = Button(text="CHIUDI", size_hint_y=0.2, background_color=get_color_from_hex('#2196F3'))
        popup = Popup(title="Statistiche Umore", content=content, size_hint=(0.85, 0.7))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    MoodTrackerApp().run()
