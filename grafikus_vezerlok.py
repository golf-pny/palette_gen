import customtkinter as ctk
import tkinter as tk

# Dizájn beállítások a tesztábra készítő program alapján
ctk.set_appearance_mode("Dark")  #[cite: 7]
ctk.set_default_color_theme("blue")  #[cite: 7]

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter / CustomTkinter Kezelőelemek Bemutatója")
        self.geometry("600x800")
        self.minsize(550, 750)  #[cite: 7]
        
        self.build_ui()

    def build_ui(self):
        # Fő görgethető keret, hogy minden elem elférjen
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True, padx=15, pady=15)

        # 1. Címke (Label)
        f_label = ctk.CTkFrame(scroll_frame)
        f_label.pack(fill="x", padx=10, pady=5)  #[cite: 7]
        ctk.CTkLabel(f_label, text="1. Címke (CTkLabel):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))  #[cite: 7]
        ctk.CTkLabel(f_label, text="Működés: Szövegek, feliratok és információk megjelenítésére szolgál. Nem szerkeszthető.", text_color="#aaaaaa").pack(anchor="w", padx=10, pady=(0,5))  #[cite: 7]

        # 2. Adatbeviteli mező (Entry)
        f_entry = ctk.CTkFrame(scroll_frame)
        f_entry.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_entry, text="2. Adatbeviteli mező (CTkEntry):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(f_entry, text="Működés: Egysoros szöveg vagy szám bekérésére szolgál a felhasználótól.", text_color="#aaaaaa").pack(anchor="w", padx=10)
        self.entry = ctk.CTkEntry(f_entry, placeholder_text="Írj be valamit...")
        self.entry.pack(fill="x", padx=10, pady=5)

        # 3. Jelölőnégyzet (Checkbox)
        f_check = ctk.CTkFrame(scroll_frame)
        f_check.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_check, text="3. Jelölőnégyzet (CTkCheckBox):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(f_check, text="Működés: Több, egymástól független opció be- és kikapcsolására való (Igen/Nem).", text_color="#aaaaaa").pack(anchor="w", padx=10)
        self.check = ctk.CTkCheckBox(f_check, text="Elfogadom a feltételeket", font=ctk.CTkFont(weight="bold"))  #[cite: 7]
        self.check.pack(anchor="w", padx=10, pady=5)

        # 4. Rádiógomb (RadioButton)
        f_radio = ctk.CTkFrame(scroll_frame)
        f_radio.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_radio, text="4. Rádiógomb (CTkRadioButton):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(f_radio, text="Működés: Egymást kizáró opciók közötti választást tesz lehetővé (csak egy választható).", text_color="#aaaaaa").pack(anchor="w", padx=10)
        
        self.radio_var = tk.StringVar(value="Opció 1")
        ctk.CTkRadioButton(f_radio, text="Opció 1", variable=self.radio_var, value="Opció 1").pack(anchor="w", padx=10, pady=2)
        ctk.CTkRadioButton(f_radio, text="Opció 2", variable=self.radio_var, value="Opció 2").pack(anchor="w", padx=10, pady=2)

        # 5. Legördülő menü (OptionMenu)
        f_option = ctk.CTkFrame(scroll_frame)
        f_option.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_option, text="5. Legördülő menü (CTkOptionMenu):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(f_option, text="Működés: Egy lenyíló lista, amelyből egyetlen elemet lehet kiválasztani.", text_color="#aaaaaa").pack(anchor="w", padx=10)
        self.combo = ctk.CTkOptionMenu(f_option, values=["Alma", "Körte", "Barack"])  #[cite: 7]
        self.combo.pack(anchor="w", padx=10, pady=5)

        # 6. Kapcsoló (Switch)
        f_switch = ctk.CTkFrame(scroll_frame)
        f_switch.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_switch, text="6. Kapcsoló (CTkSwitch):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(f_switch, text="Működés: Modern, kétállapotú kapcsoló (On/Off), hasonlóan a mobilalkalmazásokhoz.", text_color="#aaaaaa").pack(anchor="w", padx=10)
        self.switch = ctk.CTkSwitch(f_switch, text="Éjszakai mód")
        self.switch.pack(anchor="w", padx=10, pady=5)

        # 7. Csúszka (Slider)
        f_slider = ctk.CTkFrame(scroll_frame)
        f_slider.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(f_slider, text="7. Csúszka (CTkSlider):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(f_slider, text="Működés: Egy adott tartományon belüli számérték folyamatos vizuális beállítására szolgál.", text_color="#aaaaaa").pack(anchor="w", padx=10)
        self.slider = ctk.CTkSlider(f_slider, from_=0, to=100)
        self.slider.pack(fill="x", padx=10, pady=5)

        # 8. Gomb (Button) - Narancssárga kiemeléssel
        f_button = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        f_button.pack(fill="x", padx=10, pady=15)
        ctk.CTkLabel(f_button, text="8. Gomb (CTkButton):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=0, pady=(5,0))
        ctk.CTkLabel(f_button, text="Működés: Kattintásra valamilyen eseményt (függvényt) indít el.", text_color="#aaaaaa").pack(anchor="w", padx=0, pady=(0,10))
        
        self.btn = ctk.CTkButton(
            f_button, text="Teszt Akció Gomb", 
            height=45, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#d35b00", hover_color="#a84800"  #[cite: 7]
        )
        self.btn.pack(fill="x", padx=0)


class SplashScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Indítás...")
        self.geometry("400x250")
        self.eval('tk::PlaceWindow . center') # Ablak középre igazítása
        self.overrideredirect(True) # Címsor eltüntetése a klasszikus nyitóképernyő élményért
        
        # Nyitóképernyő tartalom
        frame = ctk.CTkFrame(self, fg_color="#1e1e1e", border_width=2, border_color="#d35b00")
        frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="UV Szoftver UI Demó", font=ctk.CTkFont(size=24, weight="bold")).pack(expand=True, pady=(40, 0))
        ctk.CTkLabel(frame, text="Rendszer betöltése...", text_color="#aaaaaa").pack(expand=True, pady=(0, 40))
        
        # 2000 ms (2 másodperc) múlva betölti a főablakot
        self.after(2000, self.start_main_app)

    def start_main_app(self):
        self.destroy() # Nyitóképernyő bezárása
        app = MainApp()
        app.mainloop()

if __name__ == "__main__":
    splash = SplashScreen()
    splash.mainloop()