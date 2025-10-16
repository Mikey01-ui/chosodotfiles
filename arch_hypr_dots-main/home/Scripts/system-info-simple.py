#!/usr/bin/env python3
"""
Simple System Info Display
Basic system information using standard Unix tools (no psutil dependency)
"""

import subprocess
import os
import sys
from datetime import datetime, timedelta

class SimpleSystemInfo:
    def __init__(self):
        self.hostname = os.uname().nodename
        
    def get_uptime(self):
        """Get system uptime"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime = timedelta(seconds=uptime_seconds)
                days = uptime.days
                hours, remainder = divmod(uptime.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                return f"{days}d {hours}h {minutes}m"
        except:
            return "Unknown"
    
    def get_cpu_info(self):
        """Get CPU information using /proc/stat"""
        try:
            # Get CPU usage from /proc/stat
            with open('/proc/stat', 'r') as f:
                line = f.readline()
                cpu_times = [int(x) for x in line.split()[1:]]
                idle = cpu_times[3]
                total = sum(cpu_times)
                usage = 100 * (1 - idle / total) if total > 0 else 0
            
            # Get CPU count
            cpu_count = len([line for line in open('/proc/cpuinfo') if line.startswith('processor')])
            
            return {
                "usage": usage,
                "cores": cpu_count,
                "frequency": "N/A"
            }
        except:
            return {"usage": 0, "cores": "N/A", "frequency": "N/A"}
    
    def get_memory_info(self):
        """Get memory information using /proc/meminfo"""
        try:
            meminfo = {}
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 2:
                        key = parts[0].rstrip(':')
                        value = int(parts[1]) * 1024  # Convert kB to bytes
                        meminfo[key] = value
            
            total = meminfo.get('MemTotal', 0)
            free = meminfo.get('MemFree', 0)
            available = meminfo.get('MemAvailable', free)
            used = total - available
            percent = (used / total * 100) if total > 0 else 0
            
            return {
                "total": self.bytes_to_gb(total),
                "used": self.bytes_to_gb(used),
                "available": self.bytes_to_gb(available),
                "percent": percent,
                "swap_total": 0,
                "swap_used": 0,
                "swap_percent": 0
            }
        except:
            return {"total": 0, "used": 0, "available": 0, "percent": 0, "swap_total": 0, "swap_used": 0, "swap_percent": 0}
    
    def get_disk_info(self):
        """Get disk information using df command"""
        try:
            result = subprocess.run(['df', '/'], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 4:
                    total = int(parts[1]) * 1024  # Convert from 1K blocks to bytes
                    used = int(parts[2]) * 1024
                    available = int(parts[3]) * 1024
                    percent = (used / total * 100) if total > 0 else 0
                    
                    return {
                        "total": self.bytes_to_gb(total),
                        "used": self.bytes_to_gb(used),
                        "free": self.bytes_to_gb(available),
                        "percent": percent
                    }
        except:
            pass
        return {"total": 0, "used": 0, "free": 0, "percent": 0}
    
    def get_temperature(self):
        """Get CPU temperature from /sys/class/thermal"""
        try:
            temp_paths = [
                '/sys/class/thermal/thermal_zone0/temp',
                '/sys/class/thermal/thermal_zone1/temp'
            ]
            
            for path in temp_paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        temp = int(f.read().strip()) / 1000  # Convert millidegree to degree
                        return f"{temp:.1f}°C"
        except:
            pass
        return "N/A"
    
    def bytes_to_gb(self, bytes_val):
        """Convert bytes to GB"""
        return round(bytes_val / (1024**3), 2)
    
    def get_progress_bar(self, percent, width=20):
        """Create a text progress bar"""
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percent:.1f}%"
    
    def display_dashboard(self):
        """Display the complete system dashboard"""
        print("🖥️  SIMPLE SYSTEM DASHBOARD")
        print("=" * 50)
        
        # Basic info
        print(f"🏠 Hostname: {self.hostname}")
        print(f"⏰ Uptime: {self.get_uptime()}")
        print(f"📅 Date: {datetime.now().strftime('%A, %B %d, %Y %H:%M:%S')}")
        print()
        
        # CPU Info
        cpu = self.get_cpu_info()
        print(f"🔧 CPU: {cpu['cores']} cores @ {cpu['frequency']}")
        print(f"   Usage: {self.get_progress_bar(cpu['usage'])}")
        print(f"   Temperature: {self.get_temperature()}")
        print()
        
        # Memory Info
        memory = self.get_memory_info()
        print(f"💾 Memory: {memory['used']}GB / {memory['total']}GB")
        print(f"   Usage: {self.get_progress_bar(memory['percent'])}")
        print()
        
        # Disk Info
        disk = self.get_disk_info()
        print(f"💿 Disk: {disk['used']}GB / {disk['total']}GB")
        print(f"   Usage: {self.get_progress_bar(disk['percent'])}")
        print(f"   Free: {disk['free']}GB")
        print()
        
        print("💡 Note: This is a simplified version. Install python-psutil for detailed system info.")

def main():
    system_info = SimpleSystemInfo()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--notify":
        # Send a notification with basic info
        cpu = system_info.get_cpu_info()
        memory = system_info.get_memory_info()
        temp = system_info.get_temperature()
        
        message = f"CPU: {cpu['usage']:.1f}% | RAM: {memory['percent']:.1f}% | Temp: {temp}"
        
        try:
            subprocess.run([
                "notify-send", "-i", "computer",
                "-t", "5000", "System Stats", message
            ], check=False)
        except:
            print(message)
    else:
        system_info.display_dashboard()

if __name__ == "__main__":
    main()