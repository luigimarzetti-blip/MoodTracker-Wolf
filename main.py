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
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line, Ellipse
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from collections import Counter

# --- PUBBLICITÀ ---
try:
    from kivmob import KivMob, TestIds
    KIVMOB_DISPONIBILE = True
except ImportError:
    KIVMOB_DISPONIBILE = False

# --- IL NUOVO GRAFICO PERSONALIZZATO ---
class MoodGraph(RelativeLayout):
    def __init__(self, dati, **kwargs):
        super().__init__(**kwargs)
        self.dati = dati
        # Ordine dal basso verso l'alto (dal peggiore al migliore)
        self.umori_ordinati = ["Rabbioso", "Stanco", "Triste", "Così così", "Sereno", "Radioso"]
        self.labels = []
        
        # Creiamo le etichette di testo per l'asse Y
        for u in self.umori_ordinati:
            lbl = Label(text=u, size_hint=(None, None), size=(80, 30), font_size='12sp', halign='right')
            self.add_widget(lbl)
            self.labels.append((u, lbl))
            
        self.bind(size=self.disegna_grafico, pos=self.disegna_grafico)

    def disegna_grafico(self, *args):
        self.canvas.clear()
        
        if self.height <= 0 or self.width <= 0:
            return

        margine_sinistro = 90
        margine_destro = 20
        spazio_x = self.width - margine_sinistro - margine_destro
        
        # Altezza dedicata a ogni umore (asse Y)
        step_y = self.height / len(self.umori_ordinati)
        
        with self.canvas:
            # 1. Posizioniamo le scritte e le linee di griglia orizzontali
            for i, (umore, lbl) in enumerate(self.labels):
                y_centro = (i * step_y) + (step_y / 2)
                lbl.pos = (0, y_centro - 15)
                
                Color(1, 1, 1, 0.1) # Griglia semitrasparente
                Line(points=[margine_sinistro, y_centro, self.width - margine_destro, y_centro])
            
            if not self.dati:
                return

            punti_linea = []
            info_punti = []
            
            # 2. Calcoliamo la posizione di ogni singola registrazione
            for i, record in enumerate(self.dati):
                umore = record.get("umore", "Così così")
                intensita = record.get("intensita", 5)
                
                # Trova l'altezza sull'asse Y in base all'umore
                try:
                    indice_y = self.umori_ordinati.index(umore)
                except ValueError:
                    indice_y = 3
                    
                y = (indice_y * step_y) + (step_y / 2)
                
                # Trova la posizione sull'asse X (cronologia)
                if len(self.dati) > 1:
                    x = margine_sinistro + (i * (spazio_x / (len(self.dati) - 1)))
                else:
                    x = margine_sinistro + (spazio_x / 2)
                    
                punti_linea.extend([x, y])
                
                # Regola Pallini: Raggio e Colore in base all'intensità
                raggio = 9 if intensita > 5 else 4
                info_punti.append((x, y, raggio, intensita))

            # 3. Disegniamo la linea di collegamento azzurra
            if len(punti_linea) >= 4:
                Color(0.2, 0.6, 1, 1) 
                Line(points=punti_linea, width=1.5)
                
            # 4. Disegniamo i pallini finali sopra la linea
            for x, y, r, intensita in info_punti:
                if intensita > 5:
                    Color(0.2, 0.8, 0.2, 1) # Verde acceso per intensità > 5
                else:
                    Color(0.7, 0.7, 0.7, 1) # Grigio per intensità <= 5
                Ellipse(pos=(x - r, y - r), size=(r * 2, r * 2))

# --- SCHERMATE DELL'APP ---
class IconScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 10], spacing=15)
        
        layout.add_widget(Label(text="Come ti senti oggi?", font_size='24sp', bold=True, size_hint_y=0.1))

        scroll = ScrollView(size_hint_y=0.65)
        grid = GridLayout(cols=2, spacing=20, size_hint_y=None, padding=10)
        grid.bind(minimum_height=grid.setter('height'))

        umori = {
            "Radioso": "radioso.png", "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png", "Triste": "triste.png",
            "Rabbioso": "rabbioso.png", "Stanco": "stanco.png"
        }

        for nome, img in umori.items():
            box_bottone = BoxLayout(orientation='vertical', size_hint_y=None, height=300, spacing=5)
            
            if os.path.exists(img):
                btn_img = Button(background_normal='', background_color=(0,0,0,0))
                foto = Image(source=img, allow_stretch=True, keep_ratio=True)
                btn_img.add_widget(foto)
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

        self.btn_stats = Button(
            text="VEDI STATISTICHE", 
            size_hint_y=0.12, 
            background_color=get_color_from_hex('#FFD700'), 
            color=(0,0,0,1), 
            bold=True
        )
        self.btn_stats.bind(on_release=lambda x: App.get_running_app().mostra_statistiche())
        layout.add_widget(self.btn_stats)

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
                # Banner di test di Google
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
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        if not dati:
            content.add_widget(Label(text="Nessun dato registrato.", halign='center'))
        else:
            # Info di testo in cima
            info_testo = f"Registrazioni totali: {len(dati)}\nPallino Verde = Forte (>5) | Grigio = Lieve (<=5)"
            content.add_widget(Label(text=info_testo, size_hint_y=0.15, font_size='14sp', halign='center'))
            
            # IL NUOVO GRAFICO VISIVO IN MEZZO
            grafico = MoodGraph(dati, size_hint_y=0.7)
            content.add_widget(grafico)
            
        btn = Button(text="CHIUDI", size_hint_y=0.15, background_color=get_color_from_hex('#2196F3'))
        
        # Facciamo il popup più grande per far respirare il grafico
        popup = Popup(title="Statistiche Umore", content=content, size_hint=(0.95, 0.85))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

if __name__ == '__main__':
    MoodTrackerApp().run()
