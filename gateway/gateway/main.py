import threading
from time import sleep
import uart
# from uart import recv_slave

import web

ip = "47.99.214.175"
# ip="127.0.0.1"
port = 28082

com = "COM5"
bps = 115200
get_data = "{\"method\":\"sensor\",\"addr\":\"WIFI:01:01:20:22:55:4F\",\"data\":\"{A0=0.00,A1=0.80,A2=121.00,A3=40.00,A4=20.00,A6=0,A7=0}\"}"

part_1 = "{\"method\":\""
part_2 = "\",\"addr\":\""
part_3 = "\",\"data\":\""
part_4 = "\"}"
method = "sensor"
# addr="WIFI:01:01:20:22:55:4F"
addr = "00:12:4B:00:25:45:70:55"
data = "{A0=0.00,A1=0.80,A2=999.00,A3=40.00,A4=20.00,A6=0,A7=0}"
msg = part_1 + method + part_2 + addr + part_3 + data + part_4  # 这就是组装发送给智云的消息帧


# if_to_uart=False
# slave_get=''

def to_uart(uart, ZY):
    while True:
        # global if_to_uart
        # global slave_get
        if ZY.if_to_uart:
            get_data = ZY.slave_get
            print("下发控制中")
            uart.uart_send(get_data)
            # print(get_data)
            ZY.if_to_uart = False


def to_web(uart, ZY):
    while True:
        if uar.if_to_web:
            addr = uar.addr_str
            data = uar.data_str
            msg = part_1 + method + part_2 + addr + part_3 + data + part_4
            print("上报状态中")
            ZY.tcp_send(msg)
            print(msg)
            # print(get_data)
            uar.if_to_web = False


if __name__ == '__main__':
    # data="{\"method\":\"control\", \"addr\":\"01:01:20:22:55:4F\", \"data\":\"{OD1=64,D1=?}\"}"
    # msg_analyze(data)

    ZY = web.Zhiyun(ip, port)
    ZY.tcp_con()
    uar = uart.UART(com, bps)

    uart_recv = threading.Thread(target=uar.uart_recv, args=())  # 打开来自网关的串口接收线程
    uart_recv.setDaemon(True)  # 设置守护线程
    uart_recv.start()

    heart_beat = threading.Thread(target=ZY.heart_beat, args=())  # 打开来自网关的心跳线程
    heart_beat.setDaemon(True)  # 设置守护线程
    heart_beat.start()

    recv_tcp = threading.Thread(target=ZY.recv_msg, args=())  # 打开来自网关的接收线程
    recv_tcp.setDaemon(True)  # 设置守护线程
    recv_tcp.start()

    to_uart_thread = threading.Thread(target=to_uart, args=(uar, ZY))  # 打开来自网关的接收线程
    to_uart_thread.setDaemon(True)  # 设置守护线程
    to_uart_thread.start()

    to_uart_thread = threading.Thread(target=to_web, args=(uar, ZY))  # 打开来自网关的接收线程
    to_uart_thread.setDaemon(True)  # 设置守护线程
    to_uart_thread.start()

    sleep(1)
    # data=uart.recv_slave.decode()
    # print("给智云发送数据："+uart.recv_slave.decode())
    test_uart_to_web = "00:12:4B:00:25:45:70:55={A0=0.00,A1=0.80,A2=999.00,A3=40.00,A4=20.00,A6=0,A7=0}"
    getway_data = "01:01:20:22:55:4F={A0=0.00,A1=0.80,A2=777.00,A3=40.00,A4=20.00,A6=0,A7=0}"
    gps = "01:01:20:22:55:4F={V3=103.82857550595091&30.793158389530557}"

    uar.uart_send(test_uart_to_web)
    uar.uart_send(getway_data)
    uar.uart_send(gps)
    # to_web(uar, ZY)
    # ZY.tcp_send(gps)
    # ZY.tcp_send(msg)
    sleep(2)
    # data="{\"method\":\"sensor\",\"addr\":\"WIFI:01:01:20:22:55:4F\",\"data\":\"{A2=116.0}\"}"
    # ZY.tcp_send(data)
    sleep(1)
    # data=uart.recv_slave.decode()
    # ZY.tcp_send(data)

    # print("111")
    sleep(30)
    # ZY.heart_beat()
    # ZY.tcp_stop()
