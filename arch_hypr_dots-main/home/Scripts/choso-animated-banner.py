#!/usr/bin/env python3
"""
Animated Choso Terminal Banner
Displays animated ASCII art of Choso with dynamic effects
Created for the enhanced Hyprland dotfiles
"""

import time
import os
import sys
import random
import threading
from datetime import datetime

class Colors:
    """ANSI color codes for terminal styling"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Basic colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_MAGENTA = '\033[45m'

class AnimatedChoso:
    def __init__(self):
        self.frame = 0
        self.eye_states = ["●", "◐", "○", "◑"]
        self.current_eye = 0
        self.blink_counter = 0
        self.blood_flow = 0
        
    def get_choso_frame(self, frame_num):
        """Generate Choso ASCII art with animated elements"""
        
        # Animated eyes
        if self.blink_counter > 0:
            eye = "━"  # Closed eye
            self.blink_counter -= 1
        else:
            if frame_num % 30 == 0:  # Blink occasionally
                self.blink_counter = 2
                eye = "━"
            else:
                eye = self.eye_states[self.current_eye]
                if frame_num % 8 == 0:
                    self.current_eye = (self.current_eye + 1) % len(self.eye_states)
        
        # Animated blood effects
        blood_chars = ["▓", "▒", "░", "▬"]
        blood = blood_chars[self.blood_flow % len(blood_chars)]
        self.blood_flow += 1
        
        # Dynamic shading
        shade = "▓" if frame_num % 4 < 2 else "▒"
        
        choso_art = f"""
{Colors.BRIGHT_BLACK}                    ████████████████                    
{Colors.BRIGHT_BLACK}                ████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}████                
{Colors.BRIGHT_BLACK}              ████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}████              
{Colors.BRIGHT_BLACK}            ████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}████            
{Colors.BRIGHT_BLACK}          ████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}████          
{Colors.BRIGHT_BLACK}        ████{Colors.WHITE}▓▓▓▓▓▓{Colors.RED}{blood}{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.RED}{blood}{Colors.WHITE}▓▓▓▓▓▓{Colors.BRIGHT_BLACK}████        
{Colors.BRIGHT_BLACK}      ████{Colors.WHITE}▓▓▓▓▓▓▓▓{Colors.RED}▬▬▬{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.RED}▬▬▬{Colors.WHITE}▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}████      
{Colors.BRIGHT_BLACK}      ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.RED}██{Colors.BLACK}{eye}{Colors.RED}██{Colors.WHITE}▓▓▓▓▓▓▓▓{Colors.RED}██{Colors.BLACK}{eye}{Colors.RED}██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██      
{Colors.BRIGHT_BLACK}      ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.RED}█████{Colors.WHITE}▓▓▓▓▓▓▓▓{Colors.RED}█████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██      
{Colors.BRIGHT_BLACK}      ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.RED}▬▬▬▬▬{Colors.WHITE}▓▓▓▓▓▓▓▓{Colors.RED}▬▬▬▬▬{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██      
{Colors.BRIGHT_BLACK}      ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██      
{Colors.BRIGHT_BLACK}      ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BLACK}████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██      
{Colors.BRIGHT_BLACK}      ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BLACK}████████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██      
{Colors.BRIGHT_BLACK}        ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BLACK}██████████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██        
{Colors.BRIGHT_BLACK}        ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BLACK}██████████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██        
{Colors.BRIGHT_BLACK}          ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.BLACK}████████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██          
{Colors.BRIGHT_BLACK}          ██{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BLACK}████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}██          
{Colors.BRIGHT_BLACK}            ████{Colors.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓{Colors.BRIGHT_BLACK}████            
{Colors.BRIGHT_BLACK}            ████{Colors.BLACK}████████████████████{Colors.BRIGHT_BLACK}████            
{Colors.BRIGHT_BLACK}          ████{Colors.BLACK}██████████████████████{Colors.BRIGHT_BLACK}████          
{Colors.BRIGHT_BLACK}        ████{Colors.BLACK}████████████████████████{Colors.BRIGHT_BLACK}████        
{Colors.BRIGHT_BLACK}      ████{Colors.BLACK}██████{shade}████{shade}██████{shade}████{Colors.BRIGHT_BLACK}████      
{Colors.BRIGHT_BLACK}    ████{Colors.BLACK}████████{shade}██████{shade}██████{shade}████{Colors.BRIGHT_BLACK}████    
{Colors.BRIGHT_BLACK}  ████{Colors.BLACK}██████████{shade}████████{shade}██████{Colors.BRIGHT_BLACK}████  
{Colors.BRIGHT_BLACK}████{Colors.BLACK}████████████{shade}██████████{shade}████{Colors.BRIGHT_BLACK}████
{Colors.BRIGHT_BLACK}██{Colors.BLACK}████████████████{shade}██████{shade}████████{Colors.BRIGHT_BLACK}██
{Colors.BLACK}████████████████████████████████
{Colors.RESET}"""
        
        return choso_art
    
    def get_title_frame(self, frame_num):
        """Animated title text"""
        glow_chars = ["▓", "▒", "░", " "]
        glow = glow_chars[frame_num % len(glow_chars)]
        
        title = f"""
{Colors.BRIGHT_RED}{Colors.BOLD}        ▄████▄   ██░ ██  ▒█████   ██████  ▒█████  
{Colors.RED}       ▒██▀ ▀█  ▓██░ ██▒▒██▒  ██▒▒██    ▒ ▒██▒  ██▒
{Colors.BRIGHT_RED}       ▒▓█    ▄ ▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒██░  ██▒
{Colors.RED}       ▒▓▓▄ ▄██▒░▓█ ░██ ▒██   ██░  ▒   ██▒▒██   ██░
{Colors.BRIGHT_RED}       ▒ ▓███▀ ░░▓█▒░██▓░ ████▓▒░▒██████▒▒░ ████▓▒░
{Colors.RED}       ░ ░▒ ▒  ░ ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ 
{Colors.BRIGHT_RED}         ░  ▒    ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░  ░ ▒ ▒░ 
{Colors.RED}       ░         ░  ░░ ░░ ░ ░ ▒  ░  ░  ░  ░ ░ ░ ▒  
{Colors.BRIGHT_RED}       ░ ░       ░  ░  ░    ░ ░        ░      ░ ░  
{Colors.RED}       ░                                              
{Colors.RESET}"""
        return title
    
    def display_system_info(self):
        """Display system information with Choso theme"""
        try:
            import psutil  # type: ignore # Will be available after installation
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = f"""
{Colors.BRIGHT_CYAN}┌─────────────────────────────────────────────────┐
{Colors.CYAN}│ {Colors.BRIGHT_WHITE}System Status - Blood Manipulation Domain{Colors.CYAN}    │
{Colors.BRIGHT_CYAN}├─────────────────────────────────────────────────┤
{Colors.CYAN}│ {Colors.BRIGHT_YELLOW}CPU Usage:{Colors.WHITE} {cpu_percent:>6.1f}%{Colors.CYAN}                        │
{Colors.CYAN}│ {Colors.BRIGHT_YELLOW}Memory:  {Colors.WHITE} {memory.percent:>6.1f}% ({memory.used//1024//1024//1024}GB/{memory.total//1024//1024//1024}GB){Colors.CYAN}     │
{Colors.CYAN}│ {Colors.BRIGHT_YELLOW}Disk:    {Colors.WHITE} {disk.percent:>6.1f}% ({disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB){Colors.CYAN}        │
{Colors.CYAN}│ {Colors.BRIGHT_YELLOW}Time:    {Colors.WHITE} {datetime.now().strftime('%H:%M:%S')}{Colors.CYAN}                     │
{Colors.BRIGHT_CYAN}└─────────────────────────────────────────────────┘{Colors.RESET}
"""
        except (ImportError, Exception):
            info = f"""
{Colors.BRIGHT_CYAN}┌─────────────────────────────────────────────────┐
{Colors.CYAN}│ {Colors.BRIGHT_WHITE}Blood Manipulation Domain - Initialized{Colors.CYAN}       │
{Colors.CYAN}│ {Colors.BRIGHT_YELLOW}Time: {Colors.WHITE}{datetime.now().strftime('%H:%M:%S')}{Colors.CYAN}                           │
{Colors.BRIGHT_CYAN}└─────────────────────────────────────────────────┘{Colors.RESET}
"""
        return info

def animate_choso(duration=8):
    """Main animation function"""
    choso = AnimatedChoso()
    
    try:
        # Clear screen
        os.system('clear')
        
        # Hide cursor
        print('\033[?25l', end='')
        
        frames = duration * 10  # 10 FPS
        
        for frame in range(frames):
            # Move cursor to top
            print('\033[H', end='')
            
            # Display animated Choso
            choso_frame = choso.get_choso_frame(frame)
            title_frame = choso.get_title_frame(frame)
            system_info = choso.display_system_info()
            
            print(choso_frame)
            print(title_frame)
            print(system_info)
            
            # Blood drip effect
            if frame % 20 == 0:
                print(f"{Colors.RED}                    ·   ·   ·{Colors.RESET}")
            else:
                print()
            
            # Quote rotation
            quotes = [
                f"{Colors.BRIGHT_MAGENTA}\"I am Choso. I exist for my younger brothers.\"{Colors.RESET}",
                f"{Colors.BRIGHT_RED}\"Blood Manipulation: Flowing Red Scale!\"{Colors.RESET}",
                f"{Colors.BRIGHT_YELLOW}\"My duty is to my family.\"{Colors.RESET}",
                f"{Colors.BRIGHT_CYAN}\"The cursed womb paintings... my brothers.\"{Colors.RESET}"
            ]
            
            quote = quotes[frame // 20 % len(quotes)]
            print(f"\n                    {quote}")
            
            time.sleep(0.1)
        
        # Show cursor again
        print('\033[?25h', end='')
        
    except KeyboardInterrupt:
        print('\033[?25h', end='')  # Show cursor
        print(f"\n{Colors.RESET}")

def static_choso():
    """Display static version for quick loading"""
    choso = AnimatedChoso()
    choso_art = choso.get_choso_frame(0)
    title = choso.get_title_frame(0)
    info = choso.display_system_info()
    
    print(choso_art)
    print(title)
    print(info)
    print(f"\n{Colors.BRIGHT_MAGENTA}\"I am Choso. I exist for my younger brothers.\"{Colors.RESET}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--static":
        static_choso()
    elif len(sys.argv) > 1 and sys.argv[1] == "--animate":
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        animate_choso(duration)
    else:
        # Default: show static for fast terminal startup
        static_choso()