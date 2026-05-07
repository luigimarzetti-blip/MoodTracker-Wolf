from kivy.uix.scrollview import ScrollView # Assicurati che questo import sia in alto

class IconScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Layout principale
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Titolo
        layout.add_widget(Label(text="Come ti senti oggi?", font_size='24sp', bold=True, size_hint_y=0.1))

        # --- AGGIUNTA DELLO SCROLLVIEW PER LE ICONE ---
        scroll = ScrollView(size_hint_y=0.75) # Occupa il centro dello schermo
        grid = GridLayout(cols=2, spacing=15, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height')) # Necessario per far scorrere la griglia

        umori = {
            "Radioso": "radioso.png", "Sereno": "sereno.png",
            "Così così": "cosi_cosi.png", "Triste": "triste.png",
            "Rabbioso": "rabbioso.png", "Stanco": "stanco.png"
        }

        for nome, img in umori.items():
            if os.path.exists(img):
                btn = Button(background_normal=img, size_hint_y=None, height=250) # Altezza fissa per scorrimento
            else:
                btn = Button(text=nome, size_hint_y=None, height=250, background_color=get_color_from_hex('#3E3E3E'))
            
            btn.bind(on_release=lambda x, n=nome: self.vai_a_dettagli(n))
            grid.add_widget(btn)
        
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        # Tasto statistiche - Ora avrà il suo spazio garantito in fondo
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
