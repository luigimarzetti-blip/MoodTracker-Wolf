import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.graphics import Color, Ellipse
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

### PUBBLICITÀ - Disattivata per il test anti-crash ###
# from kivmob import KivMob, TestIds

class GraficoStatistiche(RelativeLayout):
    def __init__(self, dati, **kwargs):
        super(GraficoStatistiche, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Mostra una lista testuale degli ultimi umori
        lista = BoxLayout(orientation='vertical', size_hint=(1, 0.8))
        if not dati:
            lista.add_widget(Label(text="Nessun dato disponibile ancora."))
        else:
            for entry in dati[-5:]: # Mostra gli ultimi 5 inserimenti
                testo = f"{entry.get('data', '')} | Umore: {entry.get('umore', '')}/10\nNote: {entry.get('nota', '')}"
                lista.add_widget(Label(text=testo))
        
        layout.add_widget(lista)
        self.add_widget(layout)

class MoodTrackerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#1A1A2E') 
        self.file_path = "storia_umore.json"
        
        # 1. Leggiamo i dati in modo sicuro
        self.dati = self.leggi_dati()
        
        # 2. Creiamo il layout principale
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        titolo = Label(text="Mood Tracker Wolf", font_size=32, size_hint=(1, 0.2), bold=True)
        self.main_layout.add_widget(titolo)

        # 3. Slider per l'umore
        self.main_layout.add_widget(Label(text="Come ti senti oggi? (1-10)", size_hint=(1, 0.1)))
        self.slider_umore = Slider(min=1, max=10, value=5, step=1, size_hint=(1, 0.1))
        self.main_layout.add_widget(self.slider_umore)
        
        self.label_valore = Label(text="Umore selezionato: 5", size_hint=(1, 0.1))
        self.slider_umore.bind(value=self.aggiorna_label_umore)
        self.main_layout.add_widget(self.label_valore)

        # 4. Input per le note
        self.input_note = TextInput(hint_text="Aggiungi una nota alla tua giornata...", multiline=True, size_hint=(1, 0.3))
        self.main_layout.add_widget(self.input_note)

        # 5. Bottoni Salva e Statistiche
        btn_layout = BoxLayout(spacing=10, size_hint=(1, 0.2))
        btn_salva = Button(text="Salva Umore", background_color=get_color_from_hex('#4CAF50'))
        btn_salva.bind(on_press=self.salva_dati)
        
        btn_statistiche = Button(text="Statistiche", background_color=get_color_from_hex('#2196F3'))
        btn_statistiche.bind(on_press=self.mostra_statistiche)
        
        btn_layout.add_widget(btn_salva)
        btn_layout.add_widget(btn_statistiche)
        self.main_layout.add_widget(btn_layout)
        
        # 6. Controllo limite giornaliero all'avvio
        self.controlla_limite_giornaliero()

        ### PUBBLICITÀ - TEMPORANEAMENTE DISATTIVATA PER TEST CRASH ###
        # self.ads = KivMob("ca-app-pub-2537033671132924~2254358352") 
        # self.ads.new_banner(TestIds.BANNER, top_pos=False) 
        # self.ads.request_banner()
        # self.ads.show_banner()
        #######################################################################

        return self.main_layout

    def aggiorna_label_umore(self, instance, value):
        self.label_valore.text = f"Umore selezionato: {int(value)}"

    def controlla_limite_giornaliero(self):
        oggi = datetime.now().strftime("%Y-%m-%d")
        for entry in self.dati:
            if entry.get("data") == oggi:
                # Disabilitiamo il pulsante salva se ha già salvato oggi
                self.apri_popup("Attenzione", "Hai già inserito l'umore per oggi!")
                break

    def leggi_dati(self):
        # VERSIONE ANTI-CRASH: Se il file non c'è, lo crea vuoto
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump([], f)
            return []
            
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def salva_dati(self, instance):
        umore = int(self.slider_umore.value)
        nota = self.input_note.text
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        # Controllo di sicurezza
        for entry in self.dati:
            if entry.get("data") == oggi:
                self.apri_popup("Errore", "Hai già salvato l'umore oggi.")
                return

        # Aggiungiamo i dati e salviamo il file JSON
        nuovo_dato = {"data": oggi, "umore": umore, "nota": nota}
        self.dati.append(nuovo_dato)
        
        try:
            with open(self.file_path, 'w') as f:
                json.dump(self.dati, f)
            self.apri_popup("Successo!", "Umore salvato correttamente.")
            self.input_note.text = ""
        except Exception as e:
            self.apri_popup("Errore di Sistema", f"Impossibile salvare: {str(e)}")

    def mostra_statistiche(self, instance):
        contenuto = GraficoStatistiche(dati=self.dati)
        btn_chiudi = Button(text="Chiudi Statistiche", size_hint=(1, 0.2))
        
        layout_popup = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout_popup.add_widget(contenuto)
        layout_popup.add_widget(btn_chiudi)
        
        popup = Popup(title="Storico Umore", content=layout_popup, size_hint=(0.9, 0.8))
        btn_chiudi.bind(on_press=popup.dismiss)
        popup.open()

    def apri_popup(self, titolo, messaggio):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=messaggio, text_size=(None, None))
        btn = Button(text="Chiudi", size_hint=(1, 0.4))
        
        layout.add_widget(label)
        layout.add_widget(btn)
        
        popup = Popup(title=titolo, content=layout, size_hint=(0.8, 0.4))
        btn.bind(on_press=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    MoodTrackerApp().run()
