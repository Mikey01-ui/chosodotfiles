#!/usr/bin/env python3
"""
Enhanced App Launcher
Smart search with recent apps and quick actions
"""

import subprocess
import json
import os
from pathlib import Path

def get_recent_apps():
    """Get recently used applications"""
    try:
        # Get recently used apps from Hyprland
        result = subprocess.run(['hyprctl', 'clients', '-j'], capture_output=True, text=True)
        if result.returncode == 0:
            clients = json.loads(result.stdout)
            recent_classes = []
            for client in clients[-5:]:  # Last 5 apps
                class_name = client.get('class', '').lower()
                if class_name and class_name not in recent_classes:
                    recent_classes.append(class_name)
            return recent_classes
    except:
        pass
    return []

def create_rofi_config():
    """Create enhanced rofi configuration"""
    config_dir = Path.home() / '.config' / 'rofi'
    config_dir.mkdir(exist_ok=True)
    
    rofi_config = """
configuration {
    modi: "drun,run,window,ssh";
    show-icons: true;
    icon-theme: "Papirus";
    display-drun: " Apps";
    display-run: " Run";
    display-window: " Windows";
    display-ssh: " SSH";
    drun-display-format: "{name}";
    window-format: "{w} · {c} · {t}";
    font: "JetBrains Mono Nerd Font 12";
    kb-row-up: "Up,Control+k,Control+p";
    kb-row-down: "Down,Control+j,Control+n";
    kb-accept-entry: "Return,KP_Enter";
    kb-remove-to-eol: "Control+Shift+e";
    kb-mode-next: "Shift+Right,Control+Tab";
    kb-mode-previous: "Shift+Left,Control+Shift+Tab";
    kb-remove-char-back: "BackSpace";
}

@theme "choso"
"""
    
    with open(config_dir / 'config.rasi', 'w') as f:
        f.write(rofi_config)

def create_choso_theme():
    """Create Choso-themed rofi appearance"""
    config_dir = Path.home() / '.config' / 'rofi'
    config_dir.mkdir(exist_ok=True)
    
    theme = """
* {
    background:     #1a1a1a;
    background-alt: #2d2d2d;
    foreground:     #ffffff;
    selected:       #8b0000;
    active:         #ff6b6b;
    urgent:         #ff4757;
    
    border-colour:               var(selected);
    handle-colour:               var(selected);
    background-colour:           var(background);
    foreground-colour:           var(foreground);
    alternate-background:        var(background-alt);
    normal-background:           var(background);
    normal-foreground:           var(foreground);
    urgent-background:           var(urgent);
    urgent-foreground:           var(background);
    active-background:           var(active);
    active-foreground:           var(background);
    selected-normal-background:  var(selected);
    selected-normal-foreground:  var(background);
    selected-urgent-background:  var(urgent);
    selected-urgent-foreground:  var(background);
    selected-active-background:  var(active);
    selected-active-foreground:  var(background);
    alternate-normal-background: var(background);
    alternate-normal-foreground: var(foreground);
    alternate-urgent-background: var(urgent);
    alternate-urgent-foreground: var(background);
    alternate-active-background: var(active);
    alternate-active-foreground: var(background);
}

window {
    transparency:                "real";
    location:                    center;
    anchor:                      center;
    fullscreen:                  false;
    width:                       600px;
    x-offset:                    0px;
    y-offset:                    0px;
    enabled:                     true;
    margin:                      0px;
    padding:                     0px;
    border:                      2px solid;
    border-radius:               12px;
    border-color:                @border-colour;
    background-color:            @background-colour;
    cursor:                      "default";
}

mainbox {
    enabled:                     true;
    spacing:                     10px;
    margin:                      0px;
    padding:                     20px;
    border:                      0px solid;
    border-radius:               0px 0px 0px 0px;
    border-color:                @border-colour;
    background-color:            transparent;
    children:                    [ "inputbar", "message", "listview" ];
}

inputbar {
    enabled:                     true;
    spacing:                     10px;
    margin:                      0px 0px 10px 0px;
    padding:                     12px;
    border:                      0px solid;
    border-radius:               8px;
    border-color:                @border-colour;
    background-color:            @alternate-background;
    text-color:                  @foreground-colour;
    children:                    [ "prompt", "entry" ];
}

prompt {
    enabled:                     true;
    background-color:            inherit;
    text-color:                  inherit;
}

textbox-prompt-colon {
    enabled:                     true;
    expand:                      false;
    str:                         "::";
    background-color:            inherit;
    text-color:                  inherit;
}

entry {
    enabled:                     true;
    background-color:            inherit;
    text-color:                  inherit;
    cursor:                      text;
    placeholder:                 "Search applications...";
    placeholder-color:           @foreground-colour;
}

listview {
    enabled:                     true;
    columns:                     1;
    lines:                       8;
    cycle:                       true;
    dynamic:                     true;
    scrollbar:                   false;
    layout:                      vertical;
    reverse:                     false;
    fixed-height:                true;
    fixed-columns:               true;
    spacing:                     5px;
    margin:                      0px;
    padding:                     0px;
    border:                      0px solid;
    border-radius:               0px;
    border-color:                @border-colour;
    background-color:            transparent;
    text-color:                  @foreground-colour;
    cursor:                      "default";
}

scrollbar {
    handle-width:                5px ;
    handle-color:                @handle-colour;
    border-radius:               8px;
    background-color:            @alternate-background;
}

element {
    enabled:                     true;
    spacing:                     10px;
    margin:                      0px;
    padding:                     8px;
    border:                      0px solid;
    border-radius:               6px;
    border-color:                @border-colour;
    background-color:            transparent;
    text-color:                  @foreground-colour;
    cursor:                      pointer;
}

element normal.normal {
    background-color:            var(normal-background);
    text-color:                  var(normal-foreground);
}

element selected.normal {
    background-color:            var(selected-normal-background);
    text-color:                  var(selected-normal-foreground);
}

element-icon {
    background-color:            transparent;
    text-color:                  inherit;
    size:                        24px;
    cursor:                      inherit;
}

element-text {
    background-color:            transparent;
    text-color:                  inherit;
    highlight:                   inherit;
    cursor:                      inherit;
    vertical-align:              0.5;
    horizontal-align:            0.0;
}

mode-switcher{
    enabled:                     true;
    spacing:                     10px;
    margin:                      0px;
    padding:                     0px;
    border:                      0px solid;
    border-radius:               0px;
    border-color:                @border-colour;
    background-color:            transparent;
    text-color:                  @foreground-colour;
}

button {
    padding:                     8px;
    border:                      0px solid;
    border-radius:               6px;
    border-color:                @border-colour;
    background-color:            @alternate-background;
    text-color:                  inherit;
    cursor:                      pointer;
}

button selected {
    background-color:            var(selected-normal-background);
    text-color:                  var(selected-normal-foreground);
}

message {
    enabled:                     true;
    margin:                      0px 0px 10px 0px;
    padding:                     8px;
    border:                      0px solid;
    border-radius:               6px;
    border-color:                @border-colour;
    background-color:            @alternate-background;
    text-color:                  @foreground-colour;
}

textbox {
    background-color:            inherit;
    text-color:                  inherit;
    vertical-align:              0.5;
    horizontal-align:            0.0;
    highlight:                   none;
}
"""
    
    with open(config_dir / 'choso.rasi', 'w') as f:
        f.write(theme)

def launch_enhanced_rofi():
    """Launch rofi with enhanced search capabilities"""
    create_rofi_config()
    create_choso_theme()
    
    # Enhanced rofi command with better search
    cmd = [
        'rofi', 
        '-show', 'drun',
        '-theme', 'choso',
        '-matching', 'fuzzy',
        '-sort', '-sorting-method', 'fzf',
        '-drun-match-fields', 'name,generic,exec,categories',
        '-drun-show-actions'
    ]
    
    subprocess.run(cmd)

if __name__ == "__main__":
    launch_enhanced_rofi()