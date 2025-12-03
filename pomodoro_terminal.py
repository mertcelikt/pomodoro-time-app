import time
import os
import sys

class PomodoroTimer:
    def __init__(self):
        self.work_minutes = 25
        self.break_minutes = 5
        self.sets = 4
        self.current_set = 1
        self.time_left = self.work_minutes * 60
        self.is_running = False
        self.is_break = False
    
    def clear_screen(self):
        """Ekranı temizle (platform bağımsız)"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_time(self, seconds):
        """Saniyeyi MM:SS formatına çevir"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
    
    def display_timer(self):
        """Timer'ı ekranda göster"""
        self.clear_screen()
        
        print("=" * 50)
        print("🍅 POMODORO TIMER".center(50))
        print("=" * 50)
        print()
        
        mode = "MOLA" if self.is_break else "ÇALIŞMA"
        print(f"Set: {self.current_set} / {self.sets} | Mod: {mode}")
        print()
        
        # Progress bar
        if self.is_break:
            total = self.break_minutes * 60
        else:
            total = self.work_minutes * 60
        
        progress = ((total - self.time_left) / total) * 100
        bar_length = 40
        filled = int(bar_length * progress / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"[{bar}] {progress:.1f}%")
        print()
        
        # Büyük timer gösterimi
        time_str = self.format_time(self.time_left)
        print(" " * 15 + time_str)
        print()
        
        print("=" * 50)
        print("Kontroller:")
        print("  [ENTER] - Başlat/Duraklat")
        print("  [R] - Sıfırla")
        print("  [S] - Ayarlar")
        print("  [Q] - Çıkış")
        print("=" * 50)
    
    def run_timer(self):
        """Timer'ı çalıştır"""
        self.is_running = True
        
        while self.is_running and self.time_left > 0:
            self.display_timer()
            time.sleep(1)
            self.time_left -= 1
        
        if self.time_left == 0:
            self.timer_complete()
    
    def timer_complete(self):
        """Timer tamamlandığında"""
        self.is_running = False
        
        # Windows için ses
        try:
            import winsound
            winsound.Beep(800, 500)
        except:
            # Diğer platformlar için
            print("\a")  # Sistem beep
        
        self.clear_screen()
        
        if not self.is_break:
            # Çalışma tamamlandı
            if self.current_set < self.sets:
                print("=" * 50)
                print("✅ Çalışma tamamlandı!")
                print(f"Set {self.current_set} / {self.sets} bitti.")
                print("Mola zamanı başlıyor...")
                print("=" * 50)
                time.sleep(3)
                
                self.is_break = True
                self.time_left = self.break_minutes * 60
            else:
                print("=" * 50)
                print("🎉 TEBRİKLER!")
                print("Tüm pomodoro setleri tamamlandı!")
                print("=" * 50)
                time.sleep(3)
                
                self.is_break = False
                self.current_set = 1
                self.time_left = self.work_minutes * 60
        else:
            # Mola tamamlandı
            print("=" * 50)
            print("⏰ Mola bitti!")
            print("Çalışma zamanı başlıyor...")
            print("=" * 50)
            time.sleep(3)
            
            self.is_break = False
            if self.current_set < self.sets:
                self.current_set += 1
            else:
                self.current_set = 1
            self.time_left = self.work_minutes * 60
        
        self.display_timer()
    
    def reset_timer(self):
        """Timer'ı sıfırla"""
        self.is_running = False
        self.is_break = False
        self.current_set = 1
        self.time_left = self.work_minutes * 60
        self.display_timer()
    
    def show_settings(self):
        """Ayarları göster ve değiştir"""
        self.clear_screen()
        print("=" * 50)
        print("⚙️  AYARLAR".center(50))
        print("=" * 50)
        print()
        
        try:
            work = input(f"Çalışma süresi (dakika) [{self.work_minutes}]: ").strip()
            if work:
                self.work_minutes = max(1, min(60, int(work)))
            
            break_time = input(f"Mola süresi (dakika) [{self.break_minutes}]: ").strip()
            if break_time:
                self.break_minutes = max(1, min(30, int(break_time)))
            
            sets = input(f"Set sayısı [{self.sets}]: ").strip()
            if sets:
                self.sets = max(1, min(10, int(sets)))
            
            if not self.is_running:
                if not self.is_break:
                    self.time_left = self.work_minutes * 60
                else:
                    self.time_left = self.break_minutes * 60
            
            print()
            print("Ayarlar kaydedildi!")
            time.sleep(1)
        except ValueError:
            print("Geçersiz değer! Ayarlar değiştirilmedi.")
            time.sleep(2)
        
        self.display_timer()
    
    def handle_input(self):
        """Kullanıcı girdisini işle"""
        if sys.platform == 'win32':
            import msvcrt  # Windows için
            # Windows için non-blocking input
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8').lower()
                if key == '\r':  # Enter
                    if not self.is_running:
                        self.run_timer()
                    else:
                        self.is_running = False
                elif key == 'r':
                    self.reset_timer()
                elif key == 's':
                    self.is_running = False
                    self.show_settings()
                elif key == 'q':
                    print("\nÇıkılıyor...")
                    sys.exit(0)
        else:
            # Linux/Mac için (select kullanarak)
            import select
            if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                key = sys.stdin.read(1).lower()
                if key == '\n':  # Enter
                    if not self.is_running:
                        self.run_timer()
                    else:
                        self.is_running = False
                elif key == 'r':
                    self.reset_timer()
                elif key == 's':
                    self.is_running = False
                    self.show_settings()
                elif key == 'q':
                    print("\nÇıkılıyor...")
                    sys.exit(0)
    
    def start(self):
        """Ana döngü"""
        self.display_timer()
        
        print("\nTimer'ı başlatmak için [ENTER] tuşuna basın...")
        
        while True:
            if not self.is_running:
                self.handle_input()
                time.sleep(0.1)
            else:
                self.run_timer()

def main():
    timer = PomodoroTimer()
    try:
        timer.start()
    except KeyboardInterrupt:
        print("\n\nÇıkılıyor...")
        sys.exit(0)

if __name__ == "__main__":
    main()

