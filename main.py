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
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        layout.add_widget(Label(text="Come ti senti oggi?", font_size='24sp', bold=True, size_hint_y=0.1))

        # --- SCROLLVIEW PER LE ICONE ---
        scroll = ScrollView(size_hint_y=0.75)
        grid = GridLayout(cols=2, spacing=15, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        umori = {
            "Radioso": "radioso.png", "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png", "Triste": "triste.png",
            "Rabbioso": "rabbioso.png", "Stanco": "stanco.png"
        }

        for nome, img in umori.items():
            if os.path.exists(img):
                btn = Button(background_normal=img, size_hint_y=None, height=250)
            else:
                btn = Button(text=nome, size_hint_y=None, height=250, background_color=get_color_from_hex('#3E3E3E'))
            
            btn.bind(on_release=lambda x, n=nome: self.vai_a_dettagli(n))
            grid.add_widget(btn)
        
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        # --- TASTO STATISTICHE FISSO IN FONDO ---
        btn_stats = Button(
            text="VEDI STATISTICHE", 
            size_hint_y=0.15, 
            background_color=get_color_from_hex('#FFD700'), 
            color=(0,0,0,1), 
            bold=True
        )
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
        self.lbl_info = Label(text="Dettagli Umore", font_size='20sp', size_hint_y=0.1)
        layout.add_widget(self.lbl_info)
        
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
        # La pubblicità viene caricata DOPO che l'app si è disegnata per evitare crash
        if KIVMOB_DISPONIBILE:
            try:
                self.ads = KivMob("ca-app-pub-2537033671132924~2254358352") 
                self.ads.new_banner("ca-app-pub-25
