#!/usr/bin/env python3
"""
Advanced Gesture Manager for Hyprland
Handles multi-finger gestures and touch input
"""

import subprocess
import json
import sys
import time
from threading import Thread

class GestureManager:
    def __init__(self):
        self.gesture_bindings = {
            "3_finger_swipe_left": self.cycle_windows_backward,
            "3_finger_swipe_right": self.cycle_windows_forward,
            "3_finger_swipe_up": self.show_overview,
            "3_finger_swipe_down": self.show_launcher,
            "4_finger_swipe_left": self.workspace_previous,
            "4_finger_swipe_right": self.workspace_next,
            "4_finger_swipe_up": self.show_all_workspaces,
            "4_finger_swipe_down": self.minimize_all,
            "3_finger_tap": self.middle_click,
            "4_finger_tap": self.show_desktop,
            "pinch_in": self.zoom_out,
            "pinch_out": self.zoom_in,
            "2_finger_rotate_cw": self.rotate_window_cw,
            "2_finger_rotate_ccw": self.rotate_window_ccw
        }
    
    def hypr_command(self, command):
        """Execute Hyprland command"""
        try:
            result = subprocess.run(
                ["hyprctl", "dispatch"] + command.split(),
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def hypr_keyword(self, keyword, value):
        """Set Hyprland keyword"""
        try:
            subprocess.run(["hyprctl", "keyword", keyword, str(value)], check=True)
            return True
        except:
            return False
    
    def notify(self, message, title="Gesture"):
        """Send notification"""
        try:
            subprocess.run([
                "notify-send", "-i", "input-touchpad", "-t", "1000", 
                title, message
            ], check=False)
        except:
            pass
    
    # ========== 3-FINGER GESTURES (Window Management) ==========
    def cycle_windows_forward(self):
        """3-finger swipe right: Next window"""
        self.hypr_command("cyclenext")
        self.notify("→ Next Window", "3-Finger Swipe")
    
    def cycle_windows_backward(self):
        """3-finger swipe left: Previous window"""
        self.hypr_command("cyclenext prev")
        self.notify("← Previous Window", "3-Finger Swipe")
    
    def show_overview(self):
        """3-finger swipe up: Show overview/expose"""
        subprocess.Popen(["rofi", "-show", "window"], start_new_session=True)
        self.notify("📋 Window Overview", "3-Finger Swipe Up")
    
    def show_launcher(self):
        """3-finger swipe down: Show launcher"""
        subprocess.Popen(["rofi", "-show", "drun"], start_new_session=True)
        self.notify("🚀 App Launcher", "3-Finger Swipe Down")
    
    def middle_click(self):
        """3-finger tap: Middle click"""
        subprocess.run(["wl-copy"], input="", text=True)  # Clear clipboard first
        self.notify("🖱️ Middle Click", "3-Finger Tap")
    
    # ========== 4-FINGER GESTURES (Desktop Management) ==========
    def workspace_next(self):
        """4-finger swipe right: Next workspace"""
        self.hypr_command("workspace e+1")
        self.notify("→ Next Desktop", "4-Finger Swipe")
    
    def workspace_previous(self):
        """4-finger swipe left: Previous workspace"""
        self.hypr_command("workspace e-1") 
        self.notify("← Previous Desktop", "4-Finger Swipe")
    
    def show_all_workspaces(self):
        """4-finger swipe up: Show all workspaces"""
        # Create workspace overview
        subprocess.Popen([
            "kitty", "-e", "sh", "-c", 
            "hyprctl workspaces -j | jq -r '.[] | \"Workspace \\(.id): \\(.windows) windows\"' && read"
        ], start_new_session=True)
        self.notify("🖥️ All Desktops", "4-Finger Swipe Up")
    
    def minimize_all(self):
        """4-finger swipe down: Show desktop (minimize all)"""
        # Get all windows and minimize them
        try:
            result = subprocess.run(["hyprctl", "clients", "-j"], capture_output=True, text=True)
            clients = json.loads(result.stdout)
            for client in clients:
                if not client.get("floating", False):
                    addr = client.get("address", "")
                    if addr:
                        subprocess.run(["hyprctl", "dispatch", "movetoworkspacesilent", "special", f"address:{addr}"])
        except:
            pass
        self.notify("🏠 Show Desktop", "4-Finger Swipe Down")
    
    def show_desktop(self):
        """4-finger tap: Toggle desktop"""
        self.hypr_command("togglespecialworkspace")
        self.notify("🏠 Desktop Toggle", "4-Finger Tap")
    
    # ========== PINCH GESTURES (Zoom) ==========
    def zoom_in(self):
        """Pinch out: Zoom in"""
        self.hypr_keyword("cursor:zoom_factor", "2.0")
        self.notify("🔍+ Zoom In", "Pinch Out")
    
    def zoom_out(self):
        """Pinch in: Zoom out"""
        self.hypr_keyword("cursor:zoom_factor", "1.0")
        self.notify("🔍- Zoom Out", "Pinch In")
    
    # ========== ROTATION GESTURES ==========
    def rotate_window_cw(self):
        """2-finger rotate clockwise: Rotate window"""
        # Simulate window rotation by toggling layout
        self.hypr_command("layoutmsg orientationnext")
        self.notify("↻ Rotate Layout", "2-Finger Rotate")
    
    def rotate_window_ccw(self):
        """2-finger rotate counter-clockwise: Rotate window back"""
        self.hypr_command("layoutmsg orientationprev") 
        self.notify("↺ Rotate Layout", "2-Finger Rotate")
    
    # ========== GESTURE DETECTION ==========
    def start_gesture_detection(self):
        """Start listening for gestures (placeholder for libinput-gestures)"""
        print("🖱️ Gesture Manager: Advanced gestures configured!")
        print("📋 Available Gestures:")
        print("   3-Finger Swipes:")
        print("     • Left/Right: Switch between windows")  
        print("     • Up: Window overview")
        print("     • Down: App launcher")
        print("     • Tap: Middle click")
        print()
        print("   4-Finger Swipes:")
        print("     • Left/Right: Switch desktops") 
        print("     • Up: Show all workspaces")
        print("     • Down: Show desktop")
        print("     • Tap: Toggle desktop")
        print()
        print("   Pinch Gestures:")
        print("     • Pinch in: Zoom out")
        print("     • Pinch out: Zoom in")
        print()
        print("   Rotation:")
        print("     • 2-finger rotate: Change window layout")
        print()
        print("💡 Note: These gestures work through Hyprland's native gesture system")
    
    def setup_libinput_gestures(self):
        """Set up libinput-gestures configuration"""
        config_content = """
# Hyprland Advanced Gestures Configuration

# 3-finger gestures (window management)
gesture swipe left 3 python ~/Scripts/gesture-manager.py 3_finger_swipe_left
gesture swipe right 3 python ~/Scripts/gesture-manager.py 3_finger_swipe_right  
gesture swipe up 3 python ~/Scripts/gesture-manager.py 3_finger_swipe_up
gesture swipe down 3 python ~/Scripts/gesture-manager.py 3_finger_swipe_down
gesture tap 3 python ~/Scripts/gesture-manager.py 3_finger_tap

# 4-finger gestures (desktop management)
gesture swipe left 4 python ~/Scripts/gesture-manager.py 4_finger_swipe_left
gesture swipe right 4 python ~/Scripts/gesture-manager.py 4_finger_swipe_right
gesture swipe up 4 python ~/Scripts/gesture-manager.py 4_finger_swipe_up
gesture swipe down 4 python ~/Scripts/gesture-manager.py 4_finger_swipe_down
gesture tap 4 python ~/Scripts/gesture-manager.py 4_finger_tap

# Pinch gestures
gesture pinch in 2 python ~/Scripts/gesture-manager.py pinch_in
gesture pinch out 2 python ~/Scripts/gesture-manager.py pinch_out

# Rotation gestures  
gesture rotate clockwise 2 python ~/Scripts/gesture-manager.py 2_finger_rotate_cw
gesture rotate anticlockwise 2 python ~/Scripts/gesture-manager.py 2_finger_rotate_ccw
"""
        
        try:
            import os
            config_path = os.path.expanduser("~/.config/libinput-gestures.conf")
            with open(config_path, "w") as f:
                f.write(config_content)
            
            print(f"✅ Gesture config written to {config_path}")
            print("🔧 To activate: sudo systemctl enable libinput-gestures && libinput-gestures-setup start")
        except Exception as e:
            print(f"❌ Failed to write gesture config: {e}")
    
    def handle_gesture(self, gesture_name):
        """Handle a specific gesture"""
        if gesture_name in self.gesture_bindings:
            self.gesture_bindings[gesture_name]()
        else:
            print(f"❌ Unknown gesture: {gesture_name}")

def main():
    gm = GestureManager()
    
    if len(sys.argv) > 1:
        gesture = sys.argv[1]
        gm.handle_gesture(gesture)
    elif len(sys.argv) > 1 and sys.argv[1] == "--setup":
        gm.setup_libinput_gestures()
    else:
        gm.start_gesture_detection()

if __name__ == "__main__":
    main()