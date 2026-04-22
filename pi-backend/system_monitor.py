"""
PHANTOM CONTROLLER — System Monitor
Tracks Pi Zero W resources: CPU temp, memory, load, disk.
"""

import os
import time


class SystemMonitor:
    def __init__(self):
        self.start_time = time.time()

    def get_snapshot(self) -> dict:
        """Get a full system resource snapshot."""
        return {
            "cpu_temp": self._get_cpu_temp(),
            "cpu_load": self._get_cpu_load(),
            "memory": self._get_memory(),
            "disk": self._get_disk(),
            "uptime": round(time.time() - self.start_time, 1),
            "hostname": self._get_hostname(),
            "ip": self._get_ip(),
        }

    def get_thermal(self) -> dict:
        """Get thermal data only."""
        return {
            "cpu_temp": self._get_cpu_temp(),
            "cpu_load": self._get_cpu_load(),
        }

    def _get_cpu_temp(self) -> float:
        """Read CPU temperature from thermal zone."""
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                return round(int(f.read().strip()) / 1000.0, 1)
        except:
            return 0.0

    def _get_cpu_load(self) -> float:
        """Get 1-minute load average."""
        try:
            return round(os.getloadavg()[0], 2)
        except:
            return 0.0

    def _get_memory(self) -> dict:
        """Parse memory info from /proc/meminfo."""
        try:
            info = {}
            with open("/proc/meminfo", "r") as f:
                for line in f:
                    parts = line.split()
                    key = parts[0].rstrip(":")
                    value = int(parts[1]) // 1024  # Convert KB to MB
                    info[key] = value

            total = info.get("MemTotal", 0)
            available = info.get("MemAvailable", 0)
            used = total - available

            return {
                "total_mb": total,
                "used_mb": used,
                "available_mb": available,
                "percent": round((used / total) * 100, 1) if total else 0,
            }
        except:
            return {"total_mb": 0, "used_mb": 0, "available_mb": 0, "percent": 0}

    def _get_disk(self) -> dict:
        """Get disk usage for root partition."""
        try:
            stat = os.statvfs("/")
            total = stat.f_blocks * stat.f_frsize // (1024 * 1024)
            free = stat.f_bavail * stat.f_frsize // (1024 * 1024)
            used = total - free
            return {
                "total_mb": total,
                "used_mb": used,
                "free_mb": free,
                "percent": round((used / total) * 100, 1) if total else 0,
            }
        except:
            return {"total_mb": 0, "used_mb": 0, "free_mb": 0, "percent": 0}

    def _get_hostname(self) -> str:
        try:
            return os.uname().nodename
        except:
            return "unknown"

    def _get_ip(self) -> str:
        """Get wlan0 IP address."""
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "0.0.0.0"
