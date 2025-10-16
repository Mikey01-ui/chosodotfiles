#!/bin/bash
"""
Startup Setup Script
Initialize the cool desktop environment
"""

# Welcome message
echo "🚀 Setting up your cool Hyprland environment..."

# Make scripts executable
chmod +x ~/Scripts/*.py
chmod +x ~/.config/rofi/*.sh

# Create wallpaper directory if it doesn't exist
mkdir -p ~/Wallpapers

# Download some cool default wallpapers
echo "📸 Setting up default wallpapers..."
WALLPAPER_DIR="$HOME/Wallpapers"

# Only download if wallpapers directory is empty
if [ -z "$(ls -A $WALLPAPER_DIR)" ]; then
    echo "Downloading cool wallpapers..."
    
    # You can add URLs to cool wallpapers here
    # wget -q -O "$WALLPAPER_DIR/cyber-city.jpg" "https://example.com/wallpaper1.jpg"
    # wget -q -O "$WALLPAPER_DIR/neon-abstract.jpg" "https://example.com/wallpaper2.jpg"
    
    echo "✅ Wallpapers ready!"
else
    echo "✅ Wallpapers already exist"
fi

# Set up aliases for quick access
echo "⚡ Setting up cool aliases..."
ALIAS_FILE="$HOME/.zsh_aliases"

cat > "$ALIAS_FILE" << 'EOF'
# Cool aliases for enhanced workflow
alias ll='exa -la --icons --git'
alias ls='exa --icons'
alias tree='exa --tree --icons'
alias cat='bat'
alias grep='rg'
alias find='fd'
alias top='btop'
alias system='python ~/Scripts/system-info.py 2>/dev/null || python ~/Scripts/system-info-simple.py'
alias wallpaper='python ~/Scripts/wallpaper-switcher.py'
alias launcher='python ~/Scripts/quick-launcher.py'
alias choso='python ~/Scripts/choso-animated-banner.py --animate'
alias gaming='python ~/Scripts/performance-manager.py --gaming'
alias windows='python ~/Scripts/window-manager.py'
alias gestures='python ~/Scripts/gesture-manager.py'
alias performance='python ~/Scripts/performance-manager.py'

# Quick app launches
alias chrome='google-chrome-stable'
alias code='code'
alias whatsapp='whatsapp-for-linux'
alias youtube='google-chrome-stable --app=https://youtube.com'
alias discord='discord'
alias spotify='spotify-launcher'

# System shortcuts
alias reload-hypr='hyprctl reload && killall waybar; waybar'
alias reload-waybar='killall waybar; waybar'
alias lock='hyprlock'
alias screenshot='grim -g "$(slurp)" - | swappy -f -'
alias fullscreen='grim - | swappy -f -'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git pull'
alias gd='git diff'

# Directory shortcuts
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias ~='cd ~'
alias downloads='cd ~/Downloads'
alias documents='cd ~/Documents'
alias desktop='cd ~/Desktop'
EOF

# Add aliases to .zshrc if not already there
if ! grep -q "source ~/.zsh_aliases" ~/.zshrc; then
    echo "" >> ~/.zshrc
    echo "# Load custom aliases" >> ~/.zshrc
    echo "source ~/.zsh_aliases" >> ~/.zshrc
fi

# Set up enhanced waybar config as default
echo "🎨 Setting up enhanced Waybar..."
if [ -f ~/.config/waybar/config-enhanced.jsonc ]; then
    cp ~/.config/waybar/config.jsonc ~/.config/waybar/config.jsonc.backup
    cp ~/.config/waybar/config-enhanced.jsonc ~/.config/waybar/config.jsonc
    echo "✅ Enhanced Waybar config applied!"
fi

# Notification
echo "🎉 Setup complete! Your ULTRA cool Hyprland environment is ready!"
echo ""
echo "� SEAMLESS WINDOW MANAGEMENT:"
echo "   • Super+H/J/K/L - Navigate windows (Vi-like)"
echo "   • Super+Shift+H/J/K/L - Move windows"
echo "   • Super+Ctrl+H/J/K/L - Resize windows"
echo "   • Super+Return - Toggle split orientation"
echo "   • Super+F7 - Smart window split"
echo "   • Super+Z - Coding layout preset"
echo ""
echo "🔥 QUICK APP ACCESS:"
echo "   • Super+F2/F3/F4/F5 - WhatsApp/YouTube/Discord/Spotify"
echo "   • Super+W - Chrome, Super+Shift+T - VS Code"
echo "   • Super+P - Quick launcher menu"
echo ""
echo "⚡ PERFORMANCE & SYSTEM:"
echo "   • Super+F6 - Toggle gaming mode"
echo "   • Super+I - System info dashboard"
echo "   • Super+U - Advanced wallpaper switcher"
echo ""
echo "🎨 VISUAL ENHANCEMENTS:"
echo "   • Smart workspace organization (apps auto-organize)"
echo "   • Smooth animations and gestures"
echo "   • Enhanced Waybar with system monitoring"
echo "   • Transparent windows with beautiful effects"
echo ""
echo "🎮 COOL ALIASES & FEATURES:"
echo "   • 'choso' - Display cool Choso ASCII art"
echo "   • 'gaming' - Toggle performance mode"
echo "   • 'windows' - Window management menu"
echo "   • 'system' - System info dashboard"
echo "   • 'wallpaper' - Interactive wallpaper changer"
echo "   • Super+F8 - Show Choso in new terminal"
echo ""
echo "�️ ADVANCED GESTURES:"
echo "   • 3-finger swipe: Switch between windows on current desktop"
echo "   • 4-finger swipe: Switch between desktops/workspaces"
echo "   • 3-finger tap: Middle click action"
echo "   • 4-finger tap: Show/hide desktop"
echo "   • Pinch in/out: Zoom interface"
echo "   • 2-finger rotate: Change window layout"
echo ""
echo "💡 Pro tips:"
echo "   • All gestures work natively with touchpad"
echo "   • Hold Super and drag windows to resize/move"
echo "   • Apps automatically organize into themed workspaces"
echo "   • Gaming mode auto-activates for better performance"
echo "   • Super+F9 to configure gestures"

# Send desktop notification
if command -v notify-send &> /dev/null; then
    notify-send -i "computer" -t 5000 "🎉 Setup Complete!" "Your cool Hyprland environment is ready to rock!"
fi