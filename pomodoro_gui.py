import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import winsound  # Windows için ses çalma

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x600")
        self.root.configure(bg="#2C2C2C")
        self.root.resizable(False, False)
        
        # Varsayılan değerler
        self.work_minutes = 25
        self.break_minutes = 5
        self.sets = 4
        self.current_set = 1
        self.time_left = self.work_minutes * 60
        self.is_running = False
        self.is_break = False
        self.timer_thread = None
        self.auto_break = True  # Otomatik mola başlatma
        self.sound_choice = 1  # Ses seçeneği (1, 2, veya 3)
        
        self.setup_ui()
        self.update_display()
        
    def setup_ui(self):
        # Ana başlık
        title_frame = tk.Frame(self.root, bg="#2C2C2C")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text="🍅 Pomodoro Timer",
            font=("Arial", 28, "bold"),
            fg="#FF6B35",
            bg="#2C2C2C"
        )
        title_label.pack()
        
        # Set ve durum bilgisi
        info_frame = tk.Frame(self.root, bg="#2C2C2C")
        info_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            info_frame,
            text=f"Set {self.current_set} / {self.sets} • Çalışma",
            font=("Arial", 14),
            fg="#FFFFFF",
            bg="#2C2C2C"
        )
        self.status_label.pack()
        
        # Timer gösterimi
        timer_frame = tk.Frame(self.root, bg="#2C2C2C")
        timer_frame.pack(pady=30)
        
        self.timer_label = tk.Label(
            timer_frame,
            text="25:00",
            font=("Arial", 48, "bold"),
            fg="#FF6B35",
            bg="#2C2C2C"
        )
        self.timer_label.pack()
        
        self.mode_label = tk.Label(
            timer_frame,
            text="Çalışma Zamanı",
            font=("Arial", 12),
            fg="#AAAAAA",
            bg="#2C2C2C"
        )
        self.mode_label.pack(pady=5)
        
        # Progress bar
        progress_frame = tk.Frame(self.root, bg="#2C2C2C")
        progress_frame.pack(pady=20, padx=50, fill="x")
        
        self.progress = ttk.Progressbar(
            progress_frame,
            length=400,
            mode='determinate',
            style="TProgressbar"
        )
        self.progress.pack(fill="x")
        
        # Progress bar ve Combobox stilini özelleştir
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar",
                        background="#FF6B35",
                        troughcolor="#4A4A4A",
                        borderwidth=0,
                        lightcolor="#FF6B35",
                        darkcolor="#FF6B35")
        style.configure("TCombobox",
                      fieldbackground="#3A3A3A",
                      background="#3A3A3A",
                      foreground="white",
                      borderwidth=2,
                      relief="flat")
        style.map("TCombobox",
                 fieldbackground=[("readonly", "#3A3A3A")],
                 background=[("readonly", "#3A3A3A")],
                 foreground=[("readonly", "white")])
        
        # Kontrol butonları
        button_frame = tk.Frame(self.root, bg="#2C2C2C")
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            button_frame,
            text="Başlat",
            font=("Arial", 14, "bold"),
            bg="#22C55E",
            fg="white",
            activebackground="#16A34A",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.toggle_timer
        )
        self.start_button.pack(side="left", padx=10)
        
        self.reset_button = tk.Button(
            button_frame,
            text="Sıfırla",
            font=("Arial", 14, "bold"),
            bg="#4A4A4A",
            fg="white",
            activebackground="#3A3A3A",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.reset_timer
        )
        self.reset_button.pack(side="left", padx=10)
        
        # Ayarlar butonu
        settings_button = tk.Button(
            self.root,
            text="⚙️ Ayarlar",
            font=("Arial", 12),
            bg="#3A3A3A",
            fg="white",
            activebackground="#2A2A2A",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.show_settings
        )
        settings_button.pack(pady=10)
        
    def update_display(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # Progress bar güncelleme
        if self.is_break:
            total = self.break_minutes * 60
            progress_value = ((total - self.time_left) / total) * 100
        else:
            total = self.work_minutes * 60
            progress_value = ((total - self.time_left) / total) * 100
        
        self.progress['value'] = progress_value
        
        # Durum güncelleme
        mode_text = "Mola" if self.is_break else "Çalışma"
        self.status_label.config(text=f"Set {self.current_set} / {self.sets} • {mode_text}")
        self.mode_label.config(text="Mola Zamanı" if self.is_break else "Çalışma Zamanı")
        
    def toggle_timer(self):
        if not self.is_running:
            self.start_timer()
        else:
            self.pause_timer()
    
    def start_timer(self):
        self.is_running = True
        self.start_button.config(text="Duraklat", bg="#EF4444", activebackground="#DC2626")
        
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def pause_timer(self):
        self.is_running = False
        self.start_button.config(text="Başlat", bg="#22C55E", activebackground="#16A34A")
    
    def reset_timer(self):
        self.is_running = False
        self.is_break = False
        self.current_set = 1
        self.time_left = self.work_minutes * 60
        self.start_button.config(text="Başlat", bg="#22C55E", activebackground="#16A34A")
        self.update_display()
    
    def play_sound(self):
        """Seçilen sese göre kısa melodi çal"""
        try:
            if self.sound_choice == 1:
                # Melodi 1: Basit yükselen dizi
                melody = [
                    (600, 200),
                    (800, 200),
                    (1000, 250),
                    (1200, 350),
                ]
                for freq, dur in melody:
                    winsound.Beep(freq, dur)
                    time.sleep(0.05)
            elif self.sound_choice == 2:
                # Melodi 2: Başarı/zafer hissi veren kısa motif
                melody = [
                    (900, 200),
                    (1100, 200),
                    (1300, 200),
                    (1100, 200),
                    (1400, 400),
                ]
                for freq, dur in melody:
                    winsound.Beep(freq, dur)
                    time.sleep(0.05)
            elif self.sound_choice == 3:
                # Melodi 3: Daha yumuşak, sakin bitiş sesi
                melody = [
                    (700, 250),
                    (600, 250),
                    (500, 300),
                    (650, 350),
                ]
                for freq, dur in melody:
                    winsound.Beep(freq, dur)
                    time.sleep(0.05)
        except:
            pass
    
    def run_timer(self):
        while self.is_running and self.time_left > 0:
            time.sleep(1)
            if self.is_running:
                self.time_left -= 1
                self.root.after(0, self.update_display)
        
        if self.time_left == 0 and self.is_running:
            self.root.after(0, self.timer_complete)
    
    def timer_complete(self):
        self.is_running = False
        self.start_button.config(text="Başlat", bg="#22C55E", activebackground="#16A34A")
        
        # Ses çal (üç kere dıt dıt dıt)
        self.play_sound()
        
        if not self.is_break:
            # Çalışma tamamlandı
            if self.current_set < self.sets:
                # Mola zamanı
                self.is_break = True
                self.time_left = self.break_minutes * 60
                
                if self.auto_break:
                    # Otomatik mola başlat
                    messagebox.showinfo("Mola Zamanı!", f"Set {self.current_set} tamamlandı!\nMola otomatik olarak başlıyor.")
                    self.update_display()
                    # Kısa bir bekleme sonrası otomatik başlat
                    self.root.after(1000, self.auto_start_break)
                else:
                    # Manuel mola
                    messagebox.showinfo("Mola Zamanı!", f"Set {self.current_set} tamamlandı!\nMola zamanı başlamak için 'Başlat' butonuna tıklayın.")
                    self.update_display()
            else:
                # Tüm setler tamamlandı
                self.is_break = False
                self.current_set = 1
                self.time_left = self.work_minutes * 60
                messagebox.showinfo("Tebrikler!", "Tüm pomodoro setleri tamamlandı!")
                self.update_display()
        else:
            # Mola tamamlandı
            self.is_break = False
            if self.current_set < self.sets:
                self.current_set += 1
                self.time_left = self.work_minutes * 60
                
                if self.auto_break:
                    # Otomatik çalışma başlat
                    messagebox.showinfo("Çalışma Zamanı", f"Set {self.current_set} otomatik olarak başlıyor!")
                    self.update_display()
                    self.root.after(1000, self.auto_start_work)
                else:
                    # Manuel çalışma
                    messagebox.showinfo("Çalışma Zamanı", f"Set {self.current_set} başlamak için 'Başlat' butonuna tıklayın!")
                    self.update_display()
            else:
                self.current_set = 1
                self.time_left = self.work_minutes * 60
                messagebox.showinfo("Tamamlandı", "Tüm setler tamamlandı!")
                self.update_display()
    
    def auto_start_break(self):
        """Otomatik olarak molayı başlat"""
        if not self.is_running:
            self.start_timer()
    
    def auto_start_work(self):
        """Otomatik olarak çalışmayı başlat"""
        if not self.is_running:
            self.start_timer()
    
    def create_dropdown(self, parent, var, values, max_visible=20):
        """Özel dropdown widget oluştur (sınırlı yükseklik, scroll desteği)"""
        frame = tk.Frame(parent, bg="#1A1A1A", relief="flat", borderwidth=2)
        top_level = parent.winfo_toplevel()
        
        # Gösterilen değer butonu
        display_btn = tk.Button(
            frame,
            textvariable=var,
            font=("Arial", 16, "bold"),
            bg="#1A1A1A",
            fg="white",
            activebackground="#3A3A3A",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            anchor="w",
            padx=10,
            pady=8,
            cursor="hand2"
        )
        display_btn.pack(fill="x")
        
        # Dropdown pencere referansı
        dropdown_window = None
        configure_bind_id = None
        click_bind_id = None
        
        def toggle_dropdown(event=None):
            nonlocal dropdown_window
            if dropdown_window is None or not dropdown_window.winfo_exists():
                show_dropdown()
            else:
                hide_dropdown()
        
        def show_dropdown():
            nonlocal dropdown_window, configure_bind_id, click_bind_id
            # Pencere konumunu al
            x = frame.winfo_rootx()
            y = frame.winfo_rooty() + frame.winfo_height()
            
            # Dropdown pencere oluştur (daha kısa yükseklik)
            item_height = 30  # Her öğe için 30 pixel
            max_height = min(max_visible * item_height, len(values) * item_height)
            dropdown_window = tk.Toplevel(parent)
            dropdown_window.overrideredirect(True)
            dropdown_window.geometry(f"200x{max_height}")
            dropdown_window.geometry(f"+{x}+{y}")
            dropdown_window.configure(bg="#1A1A1A")
            dropdown_window.attributes("-topmost", True)
            
            # Scrollbar için frame
            scroll_frame = tk.Frame(dropdown_window, bg="#1A1A1A")
            scroll_frame.pack(fill="both", expand=True)
            
            # Listbox
            listbox = tk.Listbox(
                scroll_frame,
                font=("Arial", 16, "bold"),
                bg="#1A1A1A",
                fg="white",
                selectbackground="#FF6B35",
                selectforeground="white",
                activestyle="none",
                relief="flat",
                borderwidth=0,
                highlightthickness=0,
                height=max_visible
            )
            
            # Scrollbar
            scrollbar = tk.Scrollbar(
                scroll_frame,
                orient="vertical",
                command=listbox.yview,
                bg="#3A3A3A",
                troughcolor="#1A1A1A",
                activebackground="#4A4A4A",
                width=12
            )
            
            listbox.config(yscrollcommand=scrollbar.set)
            
            # Değerleri ekle
            for value in values:
                listbox.insert("end", value)
            
            # Mevcut değeri seç
            try:
                current_index = values.index(var.get())
                listbox.selection_set(current_index)
                listbox.see(current_index)
            except:
                pass
            
            listbox.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            def select_value(event=None):
                selection = listbox.curselection()
                if selection:
                    var.set(listbox.get(selection[0]))
                    hide_dropdown()
            
            def on_mousewheel(event):
                listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
            listbox.bind("<Double-Button-1>", select_value)
            listbox.bind("<Return>", select_value)
            listbox.bind("<Button-1>", lambda e: listbox.after(200, select_value))
            listbox.bind("<MouseWheel>", on_mousewheel)
            
            def hide_on_click_outside(event):
                if dropdown_window and dropdown_window.winfo_exists():
                    event_top = event.widget.winfo_toplevel()
                    if event_top == dropdown_window:
                        return
                    if dropdown_window.winfo_exists():
                        hide_dropdown()
            
            def update_dropdown_position(event=None):
                """Ayarlar penceresi hareket ettiğinde dropdown'un konumunu güncelle"""
                if dropdown_window and dropdown_window.winfo_exists():
                    try:
                        x = frame.winfo_rootx()
                        y = frame.winfo_rooty() + frame.winfo_height()
                        dropdown_window.geometry(f"+{x}+{y}")
                    except:
                        pass
            
            # Ayarlar penceresi hareket ettiğinde dropdown'u güncelle
            configure_bind_id = top_level.bind("<Configure>", update_dropdown_position, add="+")
            
            dropdown_window.bind("<FocusOut>", hide_dropdown)
            click_bind_id = top_level.bind("<Button-1>", hide_on_click_outside, add="+")
            
            listbox.focus_set()
        
        def hide_dropdown(event=None):
            nonlocal dropdown_window, configure_bind_id, click_bind_id
            if dropdown_window and dropdown_window.winfo_exists():
                dropdown_window.destroy()
                dropdown_window = None
            # Event binding'i temizle
            try:
                if configure_bind_id is not None:
                    top_level.unbind("<Configure>", configure_bind_id)
                    configure_bind_id = None
            except:
                pass
            try:
                if click_bind_id is not None:
                    top_level.unbind("<Button-1>", click_bind_id)
                    click_bind_id = None
            except:
                pass
        
        display_btn.config(command=toggle_dropdown)
        
        return frame
    
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Ayarlar")
        settings_window.geometry("500x650")
        settings_window.configure(bg="#2C2C2C")
        settings_window.resizable(False, False)
        
        # Çalışma süresi
        work_frame = tk.Frame(settings_window, bg="#2C2C2C")
        work_frame.pack(pady=15, padx=30, fill="x")
        
        work_label = tk.Label(
            work_frame,
            text="Çalışma Süresi (dakika):",
            font=("Arial", 12),
            fg="white",
            bg="#2C2C2C"
        )
        work_label.pack(anchor="w")
        
        work_var = tk.StringVar(value=str(self.work_minutes))
        work_values = [str(i) for i in range(1, 61)]  # 1-60 dakika
        work_dropdown = self.create_dropdown(work_frame, work_var, work_values, max_visible=12)
        work_dropdown.pack(fill="x", pady=5)
        
        # Mola süresi
        break_frame = tk.Frame(settings_window, bg="#2C2C2C")
        break_frame.pack(pady=15, padx=30, fill="x")
        
        break_label = tk.Label(
            break_frame,
            text="Mola Süresi (dakika):",
            font=("Arial", 12),
            fg="white",
            bg="#2C2C2C"
        )
        break_label.pack(anchor="w")
        
        break_var = tk.StringVar(value=str(self.break_minutes))
        break_values = [str(i) for i in range(1, 31)]  # 1-30 dakika
        break_dropdown = self.create_dropdown(break_frame, break_var, break_values, max_visible=12)
        break_dropdown.pack(fill="x", pady=5)
        
        # Set sayısı
        sets_frame = tk.Frame(settings_window, bg="#2C2C2C")
        sets_frame.pack(pady=15, padx=30, fill="x")
        
        sets_label = tk.Label(
            sets_frame,
            text="Set Sayısı:",
            font=("Arial", 12),
            fg="white",
            bg="#2C2C2C"
        )
        sets_label.pack(anchor="w")
        
        sets_var = tk.StringVar(value=str(self.sets))
        sets_values = [str(i) for i in range(1, 11)]  # 1-10 set
        sets_dropdown = self.create_dropdown(sets_frame, sets_var, sets_values, max_visible=10)
        sets_dropdown.pack(fill="x", pady=5)
        
        # Otomatik mola seçeneği
        auto_frame = tk.Frame(settings_window, bg="#2C2C2C")
        auto_frame.pack(pady=15, padx=30, fill="x")
        
        auto_label = tk.Label(
            auto_frame,
            text="Mola Başlatma:",
            font=("Arial", 12),
            fg="white",
            bg="#2C2C2C"
        )
        auto_label.pack(anchor="w")
        
        auto_var = tk.BooleanVar(value=self.auto_break)
        auto_radio_frame = tk.Frame(auto_frame, bg="#2C2C2C")
        auto_radio_frame.pack(fill="x", pady=5)
        
        auto_on = tk.Radiobutton(
            auto_radio_frame,
            text="Otomatik",
            variable=auto_var,
            value=True,
            font=("Arial", 11),
            fg="white",
            bg="#2C2C2C",
            selectcolor="#3A3A3A",
            activebackground="#2C2C2C",
            activeforeground="white"
        )
        auto_on.pack(side="left", padx=10)
        
        auto_off = tk.Radiobutton(
            auto_radio_frame,
            text="Manuel",
            variable=auto_var,
            value=False,
            font=("Arial", 11),
            fg="white",
            bg="#2C2C2C",
            selectcolor="#3A3A3A",
            activebackground="#2C2C2C",
            activeforeground="white"
        )
        auto_off.pack(side="left", padx=10)
        
        # Ses seçeneği
        sound_frame = tk.Frame(settings_window, bg="#2C2C2C")
        sound_frame.pack(pady=15, padx=30, fill="x")
        
        sound_label = tk.Label(
            sound_frame,
            text="Ses Seçeneği:",
            font=("Arial", 12),
            fg="white",
            bg="#2C2C2C"
        )
        sound_label.pack(anchor="w")
        
        sound_var = tk.IntVar(value=self.sound_choice)
        sound_radio_frame = tk.Frame(sound_frame, bg="#2C2C2C")
        sound_radio_frame.pack(fill="x", pady=5)
        
        sound1 = tk.Radiobutton(
            sound_radio_frame,
            text="Ses 1 (Klasik)",
            variable=sound_var,
            value=1,
            font=("Arial", 11),
            fg="white",
            bg="#2C2C2C",
            selectcolor="#3A3A3A",
            activebackground="#2C2C2C",
            activeforeground="white"
        )
        sound1.pack(side="left", padx=8)
        
        sound2 = tk.Radiobutton(
            sound_radio_frame,
            text="Ses 2 (Yüksek)",
            variable=sound_var,
            value=2,
            font=("Arial", 11),
            fg="white",
            bg="#2C2C2C",
            selectcolor="#3A3A3A",
            activebackground="#2C2C2C",
            activeforeground="white"
        )
        sound2.pack(side="left", padx=8)
        
        sound3 = tk.Radiobutton(
            sound_radio_frame,
            text="Ses 3 (Düşük)",
            variable=sound_var,
            value=3,
            font=("Arial", 11),
            fg="white",
            bg="#2C2C2C",
            selectcolor="#3A3A3A",
            activebackground="#2C2C2C",
            activeforeground="white"
        )
        sound3.pack(side="left", padx=8)
        
        # Kaydet butonu
        def save_settings():
            try:
                work = int(work_var.get())
                break_time = int(break_var.get())
                sets_count = int(sets_var.get())
                
                if work < 1 or work > 60:
                    messagebox.showerror("Hata", "Çalışma süresi 1-60 dakika arasında olmalıdır.")
                    return
                if break_time < 1 or break_time > 30:
                    messagebox.showerror("Hata", "Mola süresi 1-30 dakika arasında olmalıdır.")
                    return
                if sets_count < 1 or sets_count > 10:
                    messagebox.showerror("Hata", "Set sayısı 1-10 arasında olmalıdır.")
                    return
                
                # Ayarları kaydet
                self.work_minutes = work
                self.break_minutes = break_time
                self.sets = sets_count
                self.auto_break = auto_var.get()
                self.sound_choice = sound_var.get()
                
                # Timer çalışmıyorsa zamanı hemen yeni ayarlara göre güncelle
                if not self.is_running:
                    if not self.is_break:
                        self.time_left = self.work_minutes * 60
                    else:
                        self.time_left = self.break_minutes * 60
                
                # Görünümü güncelle
                self.update_display()
                
                settings_window.destroy()
                messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli sayılar girin.")
        
        save_button = tk.Button(
            settings_window,
            text="Kaydet",
            font=("Arial", 14, "bold"),
            bg="#FF6B35",
            fg="white",
            activebackground="#E55A2B",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            command=save_settings
        )
        save_button.pack(pady=25)

def main():
    root = tk.Tk()

    # Uygulama simgesi ayarla (turuncu saat ikonu)
    # Not: Aynı klasöre `pomodoro_icon.ico` dosyasını koymalısın.
    try:
        root.iconbitmap("pomodoro_icon.ico")
    except Exception:
        # .ico bulunamazsa sessizce devam et
        pass

    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

