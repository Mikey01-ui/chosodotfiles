#!/usr/bin/env python3
"""
Enhanced Wallpaper Switcher
Features:
- Smart wallpaper management
- Preview support
- Random wallpaper selection
- Better error handling
- Notification support
"""

import os
import random
import subprocess
import sys
from pathlib import Path

class WallpaperSwitcher:
    def __init__(self):
        self.home = Path.home()
        self.wallpaper_dir = self.home / "Wallpapers"
        self.config_dir = self.home / ".config" / "hypr"
        self.wallpaper_config = self.config_dir / "wallpapers.conf"
        self.hyprpaper_config = self.config_dir / "hyprpaper.conf"
        
        # Ensure wallpaper directory exists
        self.wallpaper_dir.mkdir(exist_ok=True)
        
    def notify(self, message, title="Wallpaper Switcher"):
        """Send desktop notification"""
        try:
            subprocess.run([
                "notify-send", "-i", "preferences-desktop-wallpaper",
                "-t", "3000", title, message
            ], check=False)
        except FileNotFoundError:
            print(f"📱 {title}: {message}")
    
    def get_image_files(self):
        """Get all image files from wallpaper directory"""
        extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
        return [f for f in self.wallpaper_dir.iterdir() 
                if f.suffix.lower() in extensions and f.is_file()]
    
    def set_wallpaper(self, image_path):
        """Set wallpaper and update configs"""
        image_path = Path(image_path).expanduser().resolve()
        
        if not image_path.exists():
            self.notify(f"❌ Image not found: {image_path}", "Error")
            return False
            
        try:
            # Generate color scheme with pywal
            subprocess.run(["wal", "-i", str(image_path)], check=True)
            
            # Update Hyprland wallpaper config
            with open(self.wallpaper_config, "w") as f:
                f.write(f"$wallpaper = {image_path}\n")
            
            # Update Hyprpaper config
            with open(self.hyprpaper_config, "w") as f:
                f.write(f"preload = {image_path}\n")
                f.write(f"wallpaper = , {image_path}\n")
            
            # Restart services
            subprocess.run(["killall", "hyprpaper"], check=False)
            subprocess.run(["killall", "waybar"], check=False)
            subprocess.run(["waybar"], check=False)
            subprocess.run(["hyprpaper"], check=False)
            
            self.notify(f"✅ Wallpaper set: {image_path.name}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.notify(f"❌ Failed to set wallpaper: {e}", "Error")
            return False
    
    def random_wallpaper(self):
        """Set a random wallpaper from the wallpaper directory"""
        images = self.get_image_files()
        if not images:
            self.notify("❌ No wallpapers found in ~/Wallpapers", "Error")
            return False
            
        random_image = random.choice(images)
        return self.set_wallpaper(random_image)
    
    def interactive_mode(self):
        """Interactive wallpaper selection"""
        print("🖼️  Enhanced Wallpaper Switcher")
        print("=" * 40)
        print("1. Set specific wallpaper")
        print("2. Random wallpaper")
        print("3. List available wallpapers")
        print("4. Exit")
        
        while True:
            try:
                choice = input("\n➤ Choose option (1-4): ").strip()
                
                if choice == "1":
                    image_path = input("📁 Enter wallpaper path (or drag & drop): ").strip().strip('"\'')
                    if image_path:
                        self.set_wallpaper(image_path)
                    break
                    
                elif choice == "2":
                    self.random_wallpaper()
                    break
                    
                elif choice == "3":
                    images = self.get_image_files()
                    if images:
                        print("\n📂 Available wallpapers:")
                        for i, img in enumerate(images, 1):
                            print(f"  {i}. {img.name}")
                        
                        try:
                            selection = int(input(f"\n➤ Select wallpaper (1-{len(images)}): ")) - 1
                            if 0 <= selection < len(images):
                                self.set_wallpaper(images[selection])
                                break
                        except ValueError:
                            print("❌ Invalid selection")
                    else:
                        print("❌ No wallpapers found in ~/Wallpapers")
                        
                elif choice == "4":
                    print("👋 Goodbye!")
                    break
                    
                else:
                    print("❌ Invalid option")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

def main():
    switcher = WallpaperSwitcher()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--random":
            switcher.random_wallpaper()
        else:
            switcher.set_wallpaper(sys.argv[1])
    else:
        switcher.interactive_mode()

if __name__ == "__main__":
    main()
