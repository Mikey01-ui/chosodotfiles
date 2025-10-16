#!/usr/bin/env python3
"""
Gaming Mode & Performance Optimizer
Toggle between different performance profiles for optimal experience
"""

import subprocess
import json
import os
import sys

class PerformanceManager:
    def __init__(self):
        self.config_file = os.path.expanduser("~/.config/hypr/performance_mode")
        self.current_mode = self.load_current_mode()
        
        self.modes = {
            "performance": {
                "name": "🚀 Performance Mode",
                "description": "Maximum performance for gaming and heavy tasks",
                "settings": {
                    "animations": False,
                    "blur": False, 
                    "shadows": False,
                    "transparency": False,
                    "vfr": False,
                    "gaps": 0,
                    "rounding": 0,
                    "border_size": 1
                }
            },
            "balanced": {
                "name": "⚖️ Balanced Mode", 
                "description": "Good performance with some visual effects",
                "settings": {
                    "animations": True,
                    "blur": True,
                    "shadows": False,
                    "transparency": True,
                    "vfr": True,
                    "gaps": 4,
                    "rounding": 8,
                    "border_size": 2
                }
            },
            "beauty": {
                "name": "✨ Beauty Mode",
                "description": "Maximum visual effects for showcase",
                "settings": {
                    "animations": True,
                    "blur": True,
                    "shadows": True,
                    "transparency": True,
                    "vfr": True,
                    "gaps": 10,
                    "rounding": 14,
                    "border_size": 2
                }
            },
            "battery": {
                "name": "🔋 Battery Mode",
                "description": "Optimized for battery life",
                "settings": {
                    "animations": False,
                    "blur": False,
                    "shadows": False, 
                    "transparency": False,
                    "vfr": True,
                    "gaps": 2,
                    "rounding": 4,
                    "border_size": 1
                }
            }
        }
    
    def load_current_mode(self):
        """Load current performance mode"""
        try:
            with open(self.config_file, 'r') as f:
                return f.read().strip()
        except:
            return "balanced"
    
    def save_current_mode(self, mode):
        """Save current performance mode"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                f.write(mode)
        except Exception as e:
            print(f"❌ Failed to save mode: {e}")
    
    def hypr_command(self, command):
        """Execute Hyprland command"""
        try:
            subprocess.run(["hyprctl", "keyword", command], check=True)
            return True
        except Exception as e:
            print(f"❌ Error executing command '{command}': {e}")
            return False
    
    def notify(self, message, title="Performance Manager"):
        """Send desktop notification"""
        try:
            subprocess.run([
                "notify-send", "-i", "preferences-system-performance",
                "-t", "4000", title, message
            ], check=False)
        except:
            print(f"⚡ {title}: {message}")
    
    def apply_mode(self, mode_name):
        """Apply performance mode"""
        if mode_name not in self.modes:
            self.notify(f"❌ Unknown mode: {mode_name}", "Error")
            return False
        
        mode = self.modes[mode_name]
        settings = mode["settings"]
        
        self.notify(f"🔄 Switching to {mode['name']}")
        
        # Apply animation settings
        if settings["animations"]:
            self.hypr_command("animations:enabled true")
        else:
            self.hypr_command("animations:enabled false")
        
        # Apply blur settings
        if settings["blur"]:
            self.hypr_command("decoration:blur:enabled true")
            self.hypr_command("decoration:blur:size 2")
            self.hypr_command("decoration:blur:passes 4")
        else:
            self.hypr_command("decoration:blur:enabled false")
        
        # Apply shadow settings
        if settings["shadows"]:
            self.hypr_command("decoration:drop_shadow true")
            self.hypr_command("decoration:shadow_range 4")
            self.hypr_command("decoration:shadow_render_power 3")
        else:
            self.hypr_command("decoration:drop_shadow false")
        
        # Apply transparency settings
        if settings["transparency"]:
            self.hypr_command("decoration:active_opacity 0.95")
            self.hypr_command("decoration:inactive_opacity 0.90")
        else:
            self.hypr_command("decoration:active_opacity 1.0")
            self.hypr_command("decoration:inactive_opacity 1.0")
        
        # Apply VFR (Variable Frame Rate)
        self.hypr_command(f"misc:vfr {str(settings['vfr']).lower()}")
        
        # Apply visual settings
        self.hypr_command(f"general:gaps_in {settings['gaps']}")
        self.hypr_command(f"general:gaps_out {settings['gaps'] + 2}")
        self.hypr_command(f"decoration:rounding {settings['rounding']}")
        self.hypr_command(f"general:border_size {settings['border_size']}")
        
        # Save current mode
        self.current_mode = mode_name
        self.save_current_mode(mode_name)
        
        self.notify(f"✅ {mode['name']} applied successfully!")
        return True
    
    def toggle_gaming_mode(self):
        """Toggle between performance and previous mode"""
        if self.current_mode == "performance":
            # Switch back to balanced
            self.apply_mode("balanced")
        else:
            # Switch to performance mode
            self.apply_mode("performance")
    
    def auto_detect_mode(self):
        """Auto-detect best mode based on running applications"""
        try:
            # Get list of running applications
            result = subprocess.run(
                ["hyprctl", "clients", "-j"],
                capture_output=True,
                text=True
            )
            clients = json.loads(result.stdout)
            
            # Check for gaming applications
            gaming_apps = ["steam_app_", "lutris", "heroic", "minecraft", "wine"]
            for client in clients:
                class_name = client.get("class", "").lower()
                if any(game_app in class_name for game_app in gaming_apps):
                    self.apply_mode("performance")
                    return "performance"
            
            # Check for battery (if laptop)
            try:
                with open("/sys/class/power_supply/BAT0/status", "r") as f:
                    battery_status = f.read().strip()
                with open("/sys/class/power_supply/BAT0/capacity", "r") as f:
                    battery_level = int(f.read().strip())
                
                if battery_status == "Discharging" and battery_level < 30:
                    self.apply_mode("battery")
                    return "battery"
            except:
                pass  # Not a laptop or no battery info
            
            # Default to balanced
            if self.current_mode != "balanced":
                self.apply_mode("balanced")
            return "balanced"
            
        except Exception as e:
            print(f"❌ Auto-detection failed: {e}")
            return self.current_mode
    
    def show_current_status(self):
        """Show current performance status"""
        mode = self.modes.get(self.current_mode, {"name": "Unknown", "description": "Unknown mode"})
        print(f"\n⚡ Current Performance Mode: {mode['name']}")
        print(f"📝 Description: {mode['description']}")
        
        # Show system info
        try:
            # CPU usage
            cpu_usage = subprocess.run(
                ["sh", "-c", "grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage \"%\"}'"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            # Memory usage 
            mem_info = subprocess.run(
                ["sh", "-c", "free | grep Mem | awk '{printf \"%.1f%%\", $3/$2 * 100.0}'"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            print(f"🖥️ CPU Usage: {cpu_usage}")
            print(f"💾 Memory Usage: {mem_info}")
            
        except:
            print("📊 System info unavailable")
    
    def interactive_menu(self):
        """Interactive performance mode selector"""
        print("⚡ Performance Manager")
        print("=" * 30)
        print(f"Current Mode: {self.modes[self.current_mode]['name']}")
        print()
        
        for i, (key, mode) in enumerate(self.modes.items(), 1):
            status = " (ACTIVE)" if key == self.current_mode else ""
            print(f"{i}. {mode['name']}{status}")
            print(f"   {mode['description']}")
        
        print(f"{len(self.modes) + 1}. Auto-detect optimal mode")
        print(f"{len(self.modes) + 2}. Show system status")
        print(f"{len(self.modes) + 3}. Exit")
        
        while True:
            try:
                choice = input(f"\n➤ Choose mode (1-{len(self.modes) + 3}): ").strip()
                
                if choice.isdigit():
                    choice_num = int(choice)
                    if 1 <= choice_num <= len(self.modes):
                        mode_name = list(self.modes.keys())[choice_num - 1]
                        self.apply_mode(mode_name)
                        break
                    elif choice_num == len(self.modes) + 1:
                        detected = self.auto_detect_mode()
                        print(f"🤖 Auto-detected and applied: {self.modes[detected]['name']}")
                        break
                    elif choice_num == len(self.modes) + 2:
                        self.show_current_status()
                    elif choice_num == len(self.modes) + 3:
                        print("👋 Goodbye!")
                        break
                    else:
                        print("❌ Invalid choice")
                else:
                    print("❌ Please enter a number")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

def main():
    pm = PerformanceManager()
    
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "--mode" and len(sys.argv) > 2:
            pm.apply_mode(sys.argv[2])
        elif action == "--gaming":
            pm.toggle_gaming_mode()
        elif action == "--auto":
            pm.auto_detect_mode()
        elif action == "--status":
            pm.show_current_status()
        else:
            print("Usage: performance-manager.py [--mode name] [--gaming] [--auto] [--status]")
            print("Available modes: performance, balanced, beauty, battery")
    else:
        pm.interactive_menu()

if __name__ == "__main__":
    main()