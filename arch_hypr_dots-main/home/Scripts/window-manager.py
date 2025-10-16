#!/usr/bin/env python3
"""
Advanced Window Manager for Hyprland
Seamless window management with presets and smart layouts
"""

import subprocess
import sys
import json
import time

class HyprlandWindowManager:
    def __init__(self):
        self.presets = {
            "coding": {
                "name": "🖥️ Coding Layout",
                "description": "Perfect setup for development",
                "apps": [
                    {"app": "code", "workspace": 2, "size": "60%"},
                    {"app": "google-chrome-stable", "workspace": 1, "size": "40%"},
                    {"app": "kitty", "workspace": 2, "size": "40%", "position": "right"}
                ]
            },
            "media": {
                "name": "🎵 Media Layout", 
                "description": "Entertainment and media consumption",
                "apps": [
                    {"app": "spotify-launcher", "workspace": 5, "size": "50%"},
                    {"app": "google-chrome-stable --app=https://youtube.com", "workspace": 5, "size": "50%"},
                    {"app": "discord", "workspace": 4, "size": "30%"}
                ]
            },
            "communication": {
                "name": "💬 Communication Layout",
                "description": "Chat and social applications", 
                "apps": [
                    {"app": "whatsapp-for-linux", "workspace": 4, "size": "50%"},
                    {"app": "discord", "workspace": 4, "size": "50%"},
                    {"app": "telegram-desktop", "workspace": 4, "size": "30%"}
                ]
            },
            "productivity": {
                "name": "📊 Productivity Layout",
                "description": "Work and productivity apps",
                "apps": [
                    {"app": "code", "workspace": 2, "size": "40%"},
                    {"app": "google-chrome-stable", "workspace": 1, "size": "40%"}, 
                    {"app": "nautilus", "workspace": 3, "size": "20%"},
                    {"app": "kitty", "workspace": 2, "size": "20%"}
                ]
            }
        }
    
    def hypr_command(self, command):
        """Execute Hyprland command"""
        try:
            result = subprocess.run(
                ["hyprctl", command],
                capture_output=True,
                text=True,
                shell=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"❌ Error executing command: {e}")
            return None
    
    def get_active_window(self):
        """Get currently active window info"""
        try:
            result = subprocess.run(
                ["hyprctl", "activewindow", "-j"],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except:
            return None
    
    def get_workspaces(self):
        """Get all workspace information"""
        try:
            result = subprocess.run(
                ["hyprctl", "workspaces", "-j"],
                capture_output=True,
                text=True
            )
            return json.loads(result.stdout)
        except:
            return []
    
    def notify(self, message, title="Window Manager"):
        """Send desktop notification"""
        try:
            subprocess.run([
                "notify-send", "-i", "preferences-system-windows",
                "-t", "3000", title, message
            ], check=False)
        except:
            print(f"🪟 {title}: {message}")
    
    def smart_split(self, direction="auto"):
        """Smart window splitting"""
        window = self.get_active_window()
        if not window:
            self.notify("❌ No active window")
            return
        
        # Determine best split direction based on window size
        if direction == "auto":
            width = window.get("size", [0, 0])[0]
            height = window.get("size", [0, 0])[1]
            direction = "horizontal" if width > height * 1.5 else "vertical"
        
        split_cmd = "layoutmsg orientationcycle left right" if direction == "horizontal" else "layoutmsg orientationcycle top bottom"
        self.hypr_command(split_cmd)
        self.notify(f"✂️ Split window {direction}ly")
    
    def tile_windows(self, layout="auto"):
        """Smart window tiling"""
        if layout == "master":
            self.hypr_command("layoutmsg orientationcycle left right")
            self.hypr_command("layoutmsg focusmaster")
        elif layout == "grid": 
            self.hypr_command("layoutmsg orientationcycle top bottom")
        else:
            # Auto-detect best layout based on number of windows
            window = self.get_active_window()
            workspaces = self.get_workspaces()
            current_ws = next((ws for ws in workspaces if ws.get("id") == window.get("workspace", {}).get("id")), None) if window else None
            window_count = current_ws.get("windows", 0) if current_ws else 0
            
            if window_count <= 2:
                self.smart_split("horizontal")
            else:
                self.smart_split("vertical")
    
    def organize_workspace(self, workspace_id, theme="default"):
        """Organize workspace with specific theme"""
        themes = {
            "coding": ["code", "google-chrome-stable", "kitty"],
            "media": ["spotify-launcher", "youtube", "vlc"],
            "communication": ["whatsapp-for-linux", "discord", "telegram-desktop"]
        }
        
        if theme in themes:
            self.hypr_command(f"workspace {workspace_id}")
            time.sleep(0.5)
            
            for i, app in enumerate(themes[theme]):
                subprocess.Popen(app.split(), start_new_session=True)
                if i < len(themes[theme]) - 1:
                    time.sleep(2)  # Give time for app to open
        
        self.notify(f"🎯 Organized workspace {workspace_id} with {theme} theme")
    
    def apply_preset(self, preset_name):
        """Apply a window layout preset"""
        if preset_name not in self.presets:
            self.notify(f"❌ Unknown preset: {preset_name}")
            return
        
        preset = self.presets[preset_name]
        self.notify(f"🚀 Applying {preset['name']}", "Layout Manager")
        
        # Launch apps with delays
        for i, app_config in enumerate(preset["apps"]):
            workspace = app_config.get("workspace", 1)
            app_cmd = app_config["app"]
            
            # Switch to workspace first
            self.hypr_command(f"workspace {workspace}")
            time.sleep(0.3)
            
            # Launch app
            subprocess.Popen(app_cmd.split(), start_new_session=True)
            
            # Small delay between launches
            if i < len(preset["apps"]) - 1:
                time.sleep(1.5)
        
        self.notify(f"✅ {preset['name']} applied successfully!")
    
    def focus_direction(self, direction):
        """Smart directional focus"""
        direction_map = {
            "left": "l", "right": "r", 
            "up": "u", "down": "d",
            "h": "l", "l": "r", "k": "u", "j": "d"
        }
        
        hypr_direction = direction_map.get(direction, direction)
        self.hypr_command(f"movefocus {hypr_direction}")
    
    def resize_window(self, direction, amount=50):
        """Smart window resizing"""
        direction_map = {
            "left": f"-{amount} 0", "right": f"{amount} 0",
            "up": f"0 -{amount}", "down": f"0 {amount}",
            "h": f"-{amount} 0", "l": f"{amount} 0",
            "k": f"0 -{amount}", "j": f"0 {amount}"
        }
        
        resize_params = direction_map.get(direction, "50 0")
        self.hypr_command(f"resizeactive {resize_params}")
    
    def window_menu(self):
        """Interactive window management menu"""
        print("🪟 Advanced Window Manager")
        print("=" * 40)
        print("1. Apply coding layout")
        print("2. Apply media layout")  
        print("3. Apply communication layout")
        print("4. Apply productivity layout")
        print("5. Smart split current window")
        print("6. Organize current workspace")
        print("7. Show window info")
        print("8. Exit")
        
        while True:
            try:
                choice = input("\n➤ Choose action (1-8): ").strip()
                
                if choice == "1":
                    self.apply_preset("coding")
                    break
                elif choice == "2":
                    self.apply_preset("media")
                    break
                elif choice == "3":
                    self.apply_preset("communication")
                    break
                elif choice == "4":
                    self.apply_preset("productivity")
                    break
                elif choice == "5":
                    self.smart_split()
                    break
                elif choice == "6":
                    workspace = input("Enter workspace ID (1-10): ").strip()
                    theme = input("Enter theme (coding/media/communication): ").strip()
                    if workspace.isdigit():
                        self.organize_workspace(int(workspace), theme)
                    break
                elif choice == "7":
                    self.show_window_info()
                elif choice == "8":
                    print("👋 Goodbye!")
                    break
                else:
                    print("❌ Invalid choice")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
    
    def show_window_info(self):
        """Show active window information"""
        window = self.get_active_window()
        if window:
            print(f"\n📊 Active Window Info:")
            print(f"   Class: {window.get('class', 'Unknown')}")
            print(f"   Title: {window.get('title', 'Unknown')}")
            print(f"   Workspace: {window.get('workspace', {}).get('id', 'Unknown')}")
            print(f"   Size: {window.get('size', [0, 0])}")
            print(f"   Position: {window.get('at', [0, 0])}")
            print(f"   Floating: {window.get('floating', False)}")
        else:
            print("❌ No active window found")

def main():
    wm = HyprlandWindowManager()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "--preset" and len(sys.argv) > 2:
            wm.apply_preset(sys.argv[2])
        elif action == "--split":
            direction = sys.argv[2] if len(sys.argv) > 2 else "auto"
            wm.smart_split(direction)
        elif action == "--focus" and len(sys.argv) > 2:
            wm.focus_direction(sys.argv[2])
        elif action == "--resize" and len(sys.argv) > 2:
            direction = sys.argv[2]
            amount = int(sys.argv[3]) if len(sys.argv) > 3 else 50
            wm.resize_window(direction, amount)
        elif action == "--organize" and len(sys.argv) > 3:
            workspace = int(sys.argv[2])
            theme = sys.argv[3]
            wm.organize_workspace(workspace, theme)
        else:
            print("Usage: window-manager.py [--preset name] [--split direction] [--focus direction] [--resize direction amount] [--organize workspace theme]")
    else:
        wm.window_menu()

if __name__ == "__main__":
    main()