import json
import os
from datetime import datetime
from collections import Counter # Utile per contare gli umori velocemente
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup # Nuova importazione per la finestra statistiche
from kivy.utils import get_color_from_hex

class MoodTrackerApp(App):
    def build(self):
        self.file_path = "storia_umore.json"
        self.umori_config = {
            "Radioso": "radioso.png",
            "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png",
            "Triste": "triste.png",
            "Rabbioso": "rabbioso.png",
            "Stanco": "stanco.png"
        }
        
        # Layout principale (sfondo blu scuro rilassante)
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Titolo
        main_layout.add_widget(Label(
            text="Come ti senti oggi?",
            font_size='28sp',
            bold=True,
            size_hint_y=0.1
        ))

        # Griglia icone
        grid = GridLayout(cols=2, spacing=15, size_hint_y=0.6)
        for nome, img in self.umori_config.items():
            btn = Button(
                background_normal=img,
                background_down=img,
                border=(0,0,0,0)
            )
            btn.bind(on_release=lambda x, n=nome: self.salva_umore(n))
            grid.add_widget(btn)
        main_layout.add_widget(grid)

        # Feedback immediato
        self.status_label = Label(text="Seleziona un'emozione", font_size='14sp', size_hint_y=0.1)
        main_layout.add_widget(self.status_label)

        # BOTTONE STATISTICHE (Design a "super impatto" con colore solare)
        stats_btn = Button(
            text="VEDI STATISTICHE",
            size_hint_y=0.15,
            background_normal='',
            background_color=get_color_from_hex('#FFD700'), # Giallo Oro Solare
            color=(0, 0, 0, 1),
            bold=True,
            font_size='18sp'
        )
        stats_btn.bind(on_release=self.mostra_statistiche)
        main_layout.add_widget(stats_btn)
        
        return main_layout

    def salva_umore(self, mood):
        data_ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuovo_dato = {"data": data_ora, "umore": mood}

        dati = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try: dati = json.load(f)
                except: dati = []

        dati.append(nuovo_dato)
        with open(self.file_path, 'w') as f:
            json.dump(dati, f, indent=4)

        self.status_label.text = f"Salvato: {mood}!"

    def mostra_statistiche(self, instance):
        # 1. Leggiamo i dati
        dati = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try: dati = json.load(f)
                except: dati = []
        
        if not dati:
            testo_stats = "Nessun dato ancora salvato.\nInizia a tracciare il tuo umore!"
        else:
            # 2. Contiamo le occorrenze di ogni umore
            elenco_umori = [d['umore'] for d in dati]
            conteggio = Counter(elenco_umori)
            
            testo_stats = f"Totale registrazioni: {len(dati)}\n\n"
            for umore, volte in conteggio.items():
                testo_stats += f"• {umore}: {volte} volte\n"

        # 3. Creiamo il Popup
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Label(text=testo_stats, font_size='16sp', halign='center'))
        
        close_btn = Button(text="CHIUDI", size_hint_y=0.2, background_color=get_color_from_hex('#808080'))
        content.add_widget(close_btn)

        popup = Popup(title='Il tuo Percorso', content=content, size_hint=(0.85, 0.7))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    MoodTrackerApp().run()