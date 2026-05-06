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

### PUBBLICITÀ - Importa KivMob ###
from kivmob import KivMob, TestIds

# ... (qui tieni la classe GraficoStatistiche intatta, non cambia nulla) ...
class GraficoStatistiche(RelativeLayout):
    # ... [il tuo codice del grafico] ...
    pass

class MoodTrackerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex('#1A1A2E') 
        self.file_path = "storia_umore.json"
        
        # ... [tieni tutta la tua configurazione di liste e layout] ...
        
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # ... [tieni tutti i tuoi bottoni e logiche del layout] ...

        self.controlla_limite_giornaliero()

        ### PUBBLICITÀ - Inizializza il banner prima di ritornare il layout ###
        # Inserisci il tuo VERO App ID qui (quello con la tilde ~)
        self.ads = KivMob("ca-app-pub-2537033671132924~2254358352") 
        
        # Per ora usiamo il banner di test per non farci bannare da Google.
        # Quando pubblicherai, cambierai TestIds.BANNER con: "ca-app-pub-2537033671132924/3780944436"
        self.ads.new_banner(TestIds.BANNER, top_pos=False) 
        self.ads.request_banner()
        self.ads.show_banner()
        #######################################################################

        return self.main_layout

    ### PUBBLICITÀ - Aggiungi queste due funzioni per gestire quando l'app va in background ###
    def on_resume(self):
        self.ads.request_banner()
        
    def on_pause(self):
        return True
    #####################################################################################

    # ... [tieni tutte le altre tue funzioni (leggi_dati, apri_popup, salva_dati, mostra_statistiche)] ...
