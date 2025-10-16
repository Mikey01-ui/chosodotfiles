#!/usr/bin/env python3
"""
Quick App Launcher
Launch your favorite apps with style
"""

import subprocess
import sys
import os

class QuickLauncher:
    def __init__(self):
        self.apps = {
            "chrome": {
                "cmd": "google-chrome-stable",
                "name": "🌐 Google Chrome",
                "description": "Web Browser"
            },
            "vscode": {
                "cmd": "code",
                "name": "💻 VS Code",
                "description": "Code Editor"
            },
            "whatsapp": {
                "cmd": "whatsapp-for-linux",
                "name": "💬 WhatsApp",
                "description": "Messaging"
            },
            "youtube": {
                "cmd": "google-chrome-stable --app=https://youtube.com",
                "name": "📺 YouTube",
                "description": "Video Platform"
            },
            "discord": {
                "cmd": "discord",
                "name": "🎮 Discord",
                "description": "Gaming Chat"
            },
            "spotify": {
                "cmd": "spotify-launcher",
                "name": "🎵 Spotify",
                "description": "Music Streaming"
            },
            "terminal": {
                "cmd": "kitty",
                "name": "⚡ Terminal",
                "description": "Command Line"
            },
            "files": {
                "cmd": "nautilus",
                "name": "📁 Files",
                "description": "File Manager"
            }
        }
    
    def notify(self, message, title="Quick Launcher"):
        """Send desktop notification"""
        try:
            subprocess.run([
                "notify-send", "-i", "applications-system",
                "-t", "2000", title, message
            ], check=False)
        except FileNotFoundError:
            print(f"🚀 {title}: {message}")
    
    def launch_app(self, app_key):
        """Launch application"""
        if app_key not in self.apps:
            self.notify(f"❌ Unknown app: {app_key}", "Error")
            return False
        
        app = self.apps[app_key]
        try:
            subprocess.Popen(app["cmd"], shell=True, start_new_session=True)
            self.notify(f"🚀 Launching {app['name']}")
            return True
        except Exception as e:
            self.notify(f"❌ Failed to launch {app['name']}: {e}", "Error")
            return False
    
    def show_menu(self):
        """Show interactive menu"""
        print("🚀 Quick App Launcher")
        print("=" * 30)
        
        for i, (key, app) in enumerate(self.apps.items(), 1):
            print(f"{i:2}. {app['name']} - {app['description']}")
        
        print(f"{len(self.apps) + 1:2}. Exit")
        
        while True:
            try:
                choice = input(f"\n➤ Choose app (1-{len(self.apps) + 1}): ").strip()
                
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(self.apps):
                        app_key = list(self.apps.keys())[choice_num - 1]
                        self.launch_app(app_key)
                        break
                    elif choice_num == len(self.apps) + 1:
                        print("👋 Goodbye!")
                        break
                    else:
                        print("❌ Invalid choice")
                else:
                    # Try to launch by name
                    if choice.lower() in self.apps:
                        self.launch_app(choice.lower())
                        break
                    else:
                        print("❌ Invalid choice")
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

def main():
    launcher = QuickLauncher()
    
    if len(sys.argv) > 1:
        app_name = sys.argv[1].lower()
        launcher.launch_app(app_name)
    else:
        launcher.show_menu()

if __name__ == "__main__":
    main()