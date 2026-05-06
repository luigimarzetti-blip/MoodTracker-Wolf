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

class GraficoStatistiche(RelativeLayout):
    def __init__(self, dati, lista_umori, colori_umori, **kwargs):
        super().__init__(**kwargs)
        # Prendiamo solo gli ultimi 7 giorni
        self.dati = dati[-7:] 
        self.lista_umori = lista_umori
        self.colori_umori = colori_umori
        self.bind(size=self.disegna_grafico, pos=self.disegna_grafico)

    def disegna_grafico(self, *args):
        self.canvas.clear()
        if not self.dati:
            return
            
        with self.canvas:
            w, h = self.size
            
            # Margini interni per il grafico
            margine_x = 20
            margine_y = 20
            w_utile = w - margine_x * 2
            h_utile = h - margine_y * 2
            
            for i, entry in enumerate(self.dati):
                # Calcolo posizione X (Date)
                step_x = w_utile / max(1, (len(self.dati) - 1))
                x = margine_x + i * step_x
                
                # Calcolo posizione Y (Umori) - L'indice fa da altezza
                umore = entry.get('umore', 'Così così')
                idx_umore = self.lista_umori.index(umore) if umore in self.lista_umori else 3
                step_y = h_utile / max(1, (len(self.lista_umori) - 1))
                y = margine_y + idx_umore * step_y
                
                # Colore e dimensione del punto
                hex_color = self.colori_umori.get(umore, "#FFFFFF")
                r, g, b, a = get_color_from_hex(hex_color)
                valore = entry.get('valore', 5)
                
                # Marcato/grande se > 5, tenue/piccolo se <= 5
                if valore > 5:
                    Color(r, g, b, 1) # Colore pieno
                    raggio = 16
                else:
                    Color(r, g, b, 0.4) # Semitrasparente
                    raggio = 8
                    
                Ellipse(pos=(x - raggio/2, y - raggio/2), size=(raggio, raggio))

class MoodTrackerApp(App):
    def build(self):
        # Sfondo scuro uniforme
        Window.clearcolor = get_color_from_hex('#1A1A2E') 
        self.file_path = "storia_umore.json"
        
        # 1. ORDINE BOTTONI (Schermata principale)
        self.umori_config = {
            "Radioso": "radioso.png",
            "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png",
            "Triste": "triste.png",
            "Rabbioso": "rabbioso.png",
            "Stanco": "stanco.png"
        }

        # 2. ORDINE GRAFICO (Dal peggiore in basso al migliore in alto)
        self.lista_umori = [
            "Rabbioso",   # Indice 0 (Fondo)
            "Triste",     # Indice 1
            "Stanco",     # Indice 2
            "Così così",  # Indice 3
            "Sereno",     # Indice 4
            "Radioso"     # Indice 5 (Cima)
        ]

        # 3. COLORI DELLE EMOZIONI (Per i puntini del grafico)
        self.colori_umori = {
            "Rabbioso": "#E74C3C",   # Rosso
            "Triste": "#3498DB",     # Blu
            "Stanco": "#9B59B6",     # Viola
            "Così così": "#F39C12",  # Arancione
            "Sereno": "#2ECC71",     # Verde Smeraldo
            "Radioso": "#FFD700"     # Giallo Oro
        }

        # Layout Principale
        self.main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.titolo = Label(text="Come ti senti oggi?", font_size='26sp', bold=True, size_hint_y=0.1)
        self.main_layout.add_widget(self.titolo)

        # Griglia Icone
        self.griglia = GridLayout(cols=2, spacing=15, size_hint_y=0.6)
        self.bottoni_umore = []
        
        for nome, img in self.umori_config.items():
            btn = Button(background_normal=img, background_down=img, border=(0,0,0,0))
            btn.bind(on_release=lambda instance, n=nome: self.apri_popup_dettagli(n))
            self.griglia.add_widget(btn)
            self.bottoni_umore.append(btn)
            
        self.main_layout.add_widget(self.griglia)

        self.status_label = Label(text="Seleziona un'emozione", font_size='14sp', size_hint_y=0.1)
        self.main_layout.add_widget(self.status_label)

        # Bottone Statistiche
        stats_btn = Button(
            text="VEDI STATISTICHE", size_hint_y=0.15,
            background_normal='', background_color=get_color_from_hex('#FFD700'),
            color=(0, 0, 0, 1), bold=True, font_size='18sp'
        )
        stats_btn.bind(on_release=self.mostra_statistiche)
        self.main_layout.add_widget(stats_btn)
        
        self.controlla_limite_giornaliero()
        return self.main_layout

    def leggi_dati(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                try: return json.load(f)
                except: return []
        return []

    def controlla_limite_giornaliero(self):
        dati = self.leggi_dati()
        oggi = datetime.now().strftime("%Y-%m-%d")
        
        if dati and dati[-1].get("data") == oggi:
            for btn in self.bottoni_umore:
                btn.disabled = True
            self.titolo.text = "A domani!"
            self.status_label.text = "Hai già registrato il tuo umore oggi. ✨"

    def apri_popup_dettagli(self, mood):
        box = BoxLayout(orientation='vertical', spacing=15, padding=10)
        
        lbl_valore = Label(text="Intensità (1-10): 5", size_hint_y=0.2, bold=True)
        slider = Slider(min=1, max=10, value=5, step=1, size_hint_y=0.3)
        slider.bind(value=lambda instance, v: setattr(lbl_valore, 'text', f"Intensità (1-10): {int(v)}"))
        
        input_nota = TextInput(hint_text="Scrivi un pensiero...", multiline=True, size_hint_y=0.4)
        salva_btn = Button(text="SALVA", size_hint_y=0.2, background_normal='', background_color=get_color_from_hex('#4CAF50'), bold=True)
        
        box.add_widget(lbl_valore)
        box.add_widget(slider)
        box.add_widget(input_nota)
        box.add_widget(salva_btn)
        
        popup = Popup(title=f"Hai scelto: {mood}", content=box, size_hint=(0.85, 0.6))
        salva_btn.bind(on_release=lambda x: self.salva_dati_finali(mood, int(slider.value), input_nota.text, popup))
        popup.open()

    def salva_dati_finali(self, mood, valore, nota, popup):
        oggi = datetime.now().strftime("%Y-%m-%d")
        nuovo_dato = {
            "data": oggi,
            "umore": mood,
            "valore": valore,
            "nota": nota
        }

        dati = self.leggi_dati()
        dati.append(nuovo_dato)
        with open(self.file_path, 'w') as f:
            json.dump(dati, f, indent=4)

        popup.dismiss()
        self.controlla_limite_giornaliero()

    def mostra_statistiche(self, instance):
        dati = self.leggi_dati()
        
        if not dati:
            contenuto = Label(text="Nessun dato ancora salvato.\nInizia a tracciare il tuo umore!", font_size='16sp', halign="center")
        else:
            contenuto = BoxLayout(orientation='vertical', padding=10)
            
            contenitore_grafico = BoxLayout(orientation='horizontal')
            
            # Asse Y: Aggiungiamo le label al contrario in modo che "Radioso" sia in cima
            asse_y = BoxLayout(orientation='vertical', size_hint_x=0.25)
            for u in reversed(self.lista_umori):
                asse_y.add_widget(Label(text=u[:4]+".", font_size='11sp', halign='right'))
                
            # Disegno grafico passandogli i dati e i colori
            area_disegno = GraficoStatistiche(
                dati=dati, 
                lista_umori=self.lista_umori, 
                colori_umori=self.colori_umori, 
                size_hint_x=0.75
            )
            
            contenitore_grafico.add_widget(asse_y)
            contenitore_grafico.add_widget(area_disegno)
            contenuto.add_widget(contenitore_grafico)
            
            # Asse X: Le date
            asse_x = BoxLayout(orientation='horizontal', size_hint_y=0.15, padding=[asse_y.width + 10, 0, 0, 0])
            for d in dati[-7:]:
                giorno_mese = f"{d['data'].split('-')[2]}/{d['data'].split('-')[1]}"
                asse_x.add_widget(Label(text=giorno_mese, font_size='10sp'))
            contenuto.add_widget(asse_x)

        chiudi_btn = Button(text="CHIUDI", size_hint_y=0.15, background_color=get_color_from_hex('#808080'))
        
        layout_finale = BoxLayout(orientation='vertical')
        layout_finale.add_widget(contenuto)
        layout_finale.add_widget(chiudi_btn)

        popup = Popup(title='Il tuo Bioritmo (Ultimi 7gg)', content=layout_finale, size_hint=(0.95, 0.75))
        chiudi_btn.bind(on_release=popup.dismiss)
        popup.open()

if __name__ == '__main__':
    MoodTrackerApp().run()
