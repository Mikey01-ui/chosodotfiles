#!/usr/bin/env python3
"""
System Info Dashboard
Show cool system statistics and information
"""

import subprocess
import os
import sys
from datetime import datetime, timedelta

# Handle optional psutil import
PSUTIL_AVAILABLE = False
psutil = None

try:
    import psutil  # type: ignore # pylint: disable=import-error
    PSUTIL_AVAILABLE = True
except ImportError:
    # Create a mock psutil object to prevent attribute errors
    class MockPsutil:
        POWER_TIME_UNLIMITED = -1
        def cpu_percent(self, interval=1): return 0
        def cpu_count(self): return 0
        def cpu_freq(self): return None
        def virtual_memory(self): return type('obj', (object,), {'total': 0, 'used': 0, 'available': 0, 'percent': 0})
        def swap_memory(self): return type('obj', (object,), {'total': 0, 'used': 0, 'percent': 0})
        def disk_usage(self, path): return type('obj', (object,), {'total': 0, 'used': 0, 'free': 0})
        def net_io_counters(self): return None
        def sensors_temperatures(self): return {}
        def sensors_battery(self): return None
        def process_iter(self, attrs): return []
    
    psutil = MockPsutil()
    PSUTIL_AVAILABLE = False

class SystemInfo:
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
        """Get CPU information"""
        if not PSUTIL_AVAILABLE:
            return {"usage": 0, "cores": "N/A", "frequency": "N/A"}
            
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        freq_str = f"{cpu_freq.current:.0f}MHz" if cpu_freq else "Unknown"
        return {
            "usage": cpu_percent,
            "cores": cpu_count,
            "frequency": freq_str
        }
    
    def get_memory_info(self):
        """Get memory information"""
        if not PSUTIL_AVAILABLE:
            return {"total": 0, "used": 0, "available": 0, "percent": 0, "swap_total": 0, "swap_used": 0, "swap_percent": 0}
            
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "total": self.bytes_to_gb(memory.total),
            "used": self.bytes_to_gb(memory.used),
            "available": self.bytes_to_gb(memory.available),
            "percent": memory.percent,
            "swap_total": self.bytes_to_gb(swap.total),
            "swap_used": self.bytes_to_gb(swap.used),
            "swap_percent": swap.percent if swap.total > 0 else 0
        }
    
    def get_disk_info(self):
        """Get disk information"""
        if not PSUTIL_AVAILABLE:
            return {"total": 0, "used": 0, "free": 0, "percent": 0}
            
        disk = psutil.disk_usage('/')
        return {
            "total": self.bytes_to_gb(disk.total),
            "used": self.bytes_to_gb(disk.used),
            "free": self.bytes_to_gb(disk.free),
            "percent": (disk.used / disk.total) * 100
        }
    
    def get_network_info(self):
        """Get network information"""
        if not PSUTIL_AVAILABLE:
            return None
            
        try:
            stats = psutil.net_io_counters()
            return {
                "bytes_sent": self.bytes_to_mb(stats.bytes_sent),
                "bytes_recv": self.bytes_to_mb(stats.bytes_recv),
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv
            }
        except:
            return None
    
    def get_temperature(self):
        """Get CPU temperature"""
        if not PSUTIL_AVAILABLE:
            return "N/A"
            
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return f"{temps['coretemp'][0].current:.1f}°C"
            elif 'cpu_thermal' in temps:
                return f"{temps['cpu_thermal'][0].current:.1f}°C"
        except:
            pass
        return "N/A"
    
    def get_battery_info(self):
        """Get battery information"""
        if not PSUTIL_AVAILABLE:
            return None
            
        try:
            battery = psutil.sensors_battery()
            if battery:
                status = "🔌 Charging" if battery.power_plugged else "🔋 Discharging"
                return {
                    "percent": battery.percent,
                    "status": status,
                    "time_left": str(timedelta(seconds=battery.secsleft)) if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unknown"
                }
        except:
            pass
        return None
    
    def bytes_to_gb(self, bytes_val):
        """Convert bytes to GB"""
        return round(bytes_val / (1024**3), 2)
    
    def bytes_to_mb(self, bytes_val):
        """Convert bytes to MB"""
        return round(bytes_val / (1024**2), 2)
    
    def get_progress_bar(self, percent, width=20):
        """Create a text progress bar"""
        filled = int(width * percent / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percent:.1f}%"
    
    def display_dashboard(self):
        """Display the complete system dashboard"""
        print("🖥️  SYSTEM DASHBOARD")
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
        if memory['swap_total'] > 0:
            print(f"   Swap: {memory['swap_used']}GB / {memory['swap_total']}GB")
            print(f"   Swap: {self.get_progress_bar(memory['swap_percent'])}")
        print()
        
        # Disk Info
        disk = self.get_disk_info()
        print(f"💿 Disk: {disk['used']}GB / {disk['total']}GB")
        print(f"   Usage: {self.get_progress_bar(disk['percent'])}")
        print(f"   Free: {disk['free']}GB")
        print()
        
        # Network Info
        network = self.get_network_info()
        if network:
            print(f"🌐 Network:")
            print(f"   Sent: {network['bytes_sent']}MB ({network['packets_sent']} packets)")
            print(f"   Received: {network['bytes_recv']}MB ({network['packets_recv']} packets)")
            print()
        
        # Battery Info
        battery = self.get_battery_info()
        if battery:
            print(f"🔋 Battery: {battery['percent']}% - {battery['status']}")
            print(f"   Time left: {battery['time_left']}")
            print()
        
        # Top processes
        print("🔝 Top 5 Processes (by CPU):")
        if not PSUTIL_AVAILABLE:
            print("   psutil not available - install with: sudo pacman -S python-psutil")
        else:
            try:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                    try:
                        proc_info = proc.info
                        if proc_info['cpu_percent'] > 0:
                            processes.append(proc_info)
                    except:
                        pass
                
                processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
                for i, proc in enumerate(processes[:5], 1):
                    print(f"   {i}. {proc['name']} (PID: {proc['pid']}) - {proc['cpu_percent']:.1f}%")
            except:
                print("   Unable to fetch process information")

def main():
    system_info = SystemInfo()
    
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