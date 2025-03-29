import logging
import sys
from typing import Optional

def setup_logging(level: int = logging.INFO) -> None:
    """设置日志配置"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_ip(ip: str) -> bool:
    """验证 IP 地址格式"""
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
    except (AttributeError, TypeError, ValueError):
        return False

def validate_port(port: int) -> bool:
    """验证端口号"""
    try:
        port = int(port)
        return 0 <= port <= 65535
    except (TypeError, ValueError):
        return False

def get_interface(ip: Optional[str] = None) -> str:
    """获取网络接口名称"""
    import netifaces
    if ip:
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            if netifaces.AF_INET in addrs:
                for addr in addrs[netifaces.AF_INET]:
                    if addr['addr'] == ip:
                        return interface
    return netifaces.gateways()['default'][netifaces.AF_INET][1]