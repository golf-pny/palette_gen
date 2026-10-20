import os
import math
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw

# =====================================================================
# 1. GENERÁLÓ MOTOR (Engine)
# =====================================================================

def create_steps(start, end):
    """A megadott kezdő és végpontot felosztja 11 egyenlő lépésre."""
    return [int(round(start + i * (end - start) / 10.0)) for i in range(11)]

def generate_uv_matrix(output_path, ch_x, steps_x, ch_y, steps_y, stable_ch=None, stable_val=0, box_size=300, dpi=300):
    """Legenerál egy adott CMY tesztmátrixot a csatornák egyedi lépései alapján."""
    n_x = len(steps_x)
    n_y = len(steps_y)
    img_w = n_x * box_size
    img_h = n_y * box_size
    
    # Üres CMYK kép (K mindig 0)
    cmyk_image = Image.new('CMYK', (img_w, img_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(cmyk_image)
    
    for i, y_percent in enumerate(steps_y):
        for j, x_percent in enumerate(steps_x):
            
            x0 = j * box_size
            y0 = i * box_size
            x1 = x0 + box_size
            y1 = y0 + box_size
            
            # Százalékok átváltása 8-bites (0-255) értékre
            val_x = int((x_percent / 100.0) * 255)
            val_y = int((y_percent / 100.0) * 255)
            val_stable = int((stable_val / 100.0) * 255) if stable_ch else 0
            
            c_val, m_val, y_val = 0, 0, 0
            
            # X tengely hozzárendelése
            if ch_x == 'C': c_val = val_x
            elif ch_x == 'M': m_val = val_x
            elif ch_x == 'Y': y_val = val_x
            
            # Y tengely hozzárendelése
            if ch_y == 'C': c_val = val_y
            elif ch_y == 'M': m_val = val_y
            elif ch_y == 'Y': y_val = val_y
            
            # Stabil 3. szín hozzárendelése (ha van)
            if stable_ch == 'C': c_val = val_stable
            elif stable_ch == 'M': m_val = val_stable
            elif stable_ch == 'Y': y_val = val_stable
            
            # Blokk kirajzolása
            draw.rectangle(
                [x0, y0, x1, y1], 
                fill=(c_val, m_val, y_val, 0), 
                outline=(0, 0, 0, 60)
            )
            
            # Felirat (K csatornán)
            text_label = f"{ch_x}: {x_percent}%\n{ch_y}: {y_percent}%"
            if stable_ch:
                text_label += f"\n{stable_ch}: {stable_val}%"
                
            draw.text((x0 + 15, y0 + 15), text_label, fill=(0, 0, 0, 255))
            
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cmyk_image.save(output_path, compression="tiff_deflate", dpi=(dpi, dpi))


# =====================================================================
# 2. GRAFIKUS FELÜLET (GUI)
# =====================================================================

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MatrixGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("UV Tesztábra Generátor")
        self.geometry("500x650")
        self.minsize(450, 600)
        
        # Célmappa
        self.hot_folder_path = r"C:\PrintFab\_HotFolder"
        
        # UI Változók
        self.c_start_var = tk.IntVar(value=0)
        self.c_end_var = tk.IntVar(value=100)
        self.m_start_var = tk.IntVar(value=0)
        self.m_end_var = tk.IntVar(value=100)
        self.y_start_var = tk.IntVar(value=0)
        self.y_end_var = tk.IntVar(value=100)
        
        self.gen_standard_var = tk.BooleanVar(value=True)
        self.gen_series_var = tk.BooleanVar(value=True)
        self.stable_ch_var = tk.StringVar(value="Cyan (C)")
        
        self.build_ui()

    def build_ui(self):
        # 1. Célmappa kijelzése
        frame_top = ctk.CTkFrame(self)
        frame_top.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(frame_top, text="Kimeneti mappa:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(frame_top, text=self.hot_folder_path, text_color="#aaaaaa").pack(side="left", padx=10, pady=5)

        # 2. Tartományok beállítása (Range Settings)
        frame_ranges = ctk.CTkFrame(self)
        frame_ranges.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(frame_ranges, text="Csatornák tartományainak beállítása (0-100%):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=5)
        
        self.create_range_row(frame_ranges, "Cyan (C)", self.c_start_var, self.c_end_var, "#00E5FF")
        self.create_range_row(frame_ranges, "Magenta (M)", self.m_start_var, self.m_end_var, "#FF007F")
        self.create_range_row(frame_ranges, "Sárga (Y)", self.y_start_var, self.y_end_var, "#FFEA00")

        # 3. Standard mátrixok kiválasztása
        frame_std = ctk.CTkFrame(self)
        frame_std.pack(fill="x", padx=15, pady=10)
        self.chk_std = ctk.CTkCheckBox(frame_std, text="Standard 2D mátrixok generálása (CM, CY, MY)", variable=self.gen_standard_var, font=ctk.CTkFont(weight="bold"))
        self.chk_std.pack(anchor="w", padx=15, pady=15)

        # 4. Sorozat beállítása (Stable Channel)
        frame_series = ctk.CTkFrame(self)
        frame_series.pack(fill="x", padx=15, pady=5)
        
        self.chk_series = ctk.CTkCheckBox(frame_series, text="11 darabos 3D sorozat generálása", variable=self.gen_series_var, font=ctk.CTkFont(weight="bold"))
        self.chk_series.pack(anchor="w", padx=15, pady=10)
        
        row_stable = ctk.CTkFrame(frame_series, fg_color="transparent")
        row_stable.pack(fill="x", padx=15, pady=(0, 10))
        
        ctk.CTkLabel(row_stable, text="Stabil (mátrixonként növekvő) szín:").pack(side="left", padx=(0, 10))
        self.combo_stable = ctk.CTkOptionMenu(
            row_stable, 
            variable=self.stable_ch_var, 
            values=["Cyan (C)", "Magenta (M)", "Sárga (Y)"]
        )
        self.combo_stable.pack(side="left")

        # 5. Generálás Gomb
        self.btn_generate = ctk.CTkButton(
            self, text="Generálás Indítása a PrintFab-nak", 
            height=45, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#d35b00", hover_color="#a84800",
            command=self.run_generation
        )
        self.btn_generate.pack(fill="x", padx=30, pady=25)

    def create_range_row(self, parent, label_text, var_start, var_end, color_hex):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(row, text=label_text, width=80, text_color=color_hex, font=ctk.CTkFont(weight="bold"), anchor="w").pack(side="left")
        
        ctk.CTkLabel(row, text="Kezdő:").pack(side="left", padx=5)
        ctk.CTkEntry(row, textvariable=var_start, width=50).pack(side="left")
        ctk.CTkLabel(row, text="%").pack(side="left")
        
        ctk.CTkLabel(row, text="  Vég:").pack(side="left", padx=5)
        ctk.CTkEntry(row, textvariable=var_end, width=50).pack(side="left")
        ctk.CTkLabel(row, text="%").pack(side="left")

    def clear_hot_folder(self):
        """Biztonsági törlés: kiüríti a Hot Folder-t generálás előtt, hogy ne maradjanak bent régebbi TIFF fájlok."""
        if os.path.exists(self.hot_folder_path):
            for file in os.listdir(self.hot_folder_path):
                file_path = os.path.join(self.hot_folder_path, file)
                try:
                    # Csak a .tif és .tiff fájlokat töröljük ki a biztonság kedvéért
                    if os.path.isfile(file_path) and file.lower().endswith(('.tif', '.tiff')):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Hiba a fájl törlésekor: {file_path} - {e}")

    def run_generation(self):
        try:
            # Lépések kiszámítása mind a 3 csatornára külön
            steps = {
                'C': create_steps(self.c_start_var.get(), self.c_end_var.get()),
                'M': create_steps(self.m_start_var.get(), self.m_end_var.get()),
                'Y': create_steps(self.y_start_var.get(), self.y_end_var.get())
            }
        except ValueError:
            messagebox.showerror("Hiba", "Kérlek csak számokat adj meg a tartományoknál!")
            return

        # --- BIZTONSÁGI TÖRLÉS HÍVÁSA GENERÁLÁS ELŐTT ---
        self.clear_hot_folder()

        generated_count = 0
        os.makedirs(self.hot_folder_path, exist_ok=True)
        
        # 1. Standard Mátrixok (C-M, C-Y, M-Y)
        if self.gen_standard_var.get():
            pairs = [('C', 'M'), ('C', 'Y'), ('M', 'Y')]
            for ch_x, ch_y in pairs:
                filename = f"UV_Std_{ch_x}{ch_y}_Matrix.tif"
                out_path = os.path.join(self.hot_folder_path, filename)
                generate_uv_matrix(out_path, ch_x, steps[ch_x], ch_y, steps[ch_y])
                generated_count += 1

        # 2. 11 darabos sorozat generálása
        if self.gen_series_var.get():
            stable_sel = self.stable_ch_var.get()
            
            # A logikát úgy írtam meg, hogy automatikusan kiválasztja a két "maradék" színt X és Y tengelynek
            if "Cyan" in stable_sel:
                stable_ch, x_ch, y_ch = 'C', 'Y', 'M'  # Ha a C stabil, az Y és M változik a tengelyeken
            elif "Magenta" in stable_sel:
                stable_ch, x_ch, y_ch = 'M', 'C', 'Y'
            else:
                stable_ch, x_ch, y_ch = 'Y', 'C', 'M'
                
            stable_steps = steps[stable_ch]
            
            for val in stable_steps:
                filename = f"UV_Series_{x_ch}{y_ch}_Stable_{stable_ch}_{val}pct.tif"
                out_path = os.path.join(self.hot_folder_path, filename)
                generate_uv_matrix(out_path, x_ch, steps[x_ch], y_ch, steps[y_ch], stable_ch=stable_ch, stable_val=val)
                generated_count += 1

        if generated_count > 0:
            messagebox.showinfo("Kész", f"Sikeresen legenerálva {generated_count} db TIFF fájl a PrintFab figyelőmappájába!\n(A mappában lévő régi fájlok automatikusan törlésre kerültek.)")
        else:
            messagebox.showwarning("Figyelmeztetés", "Nem választottál ki semmit generálásra (jelölőnégyzetek üresek).")

if __name__ == "__main__":
    app = MatrixGeneratorApp()
    app.mainloop()