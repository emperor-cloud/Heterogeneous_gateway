import binascii
import threading
from time import sleep
import serial




class UART:
    def __init__(self,com,bps):
        # 端口：CNU； Linux上的/dev /ttyUSB0等； windows上的COM3等
        self.portx = "COM5"
        # 波特率，标准值有：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
        self.bps = 115200
        # 超时设置，None：永远等待操作；
        #         0：立即返回请求结果；.02
        #        其他：等待超时时间（单位为秒）
        self.timex = 5
        # 打开串口，并得到串口对象
        self.ser = serial.Serial(self.portx, self.bps, timeout=self.timex)
        # 写数据
        # a = '01 10 00 10 00 01 02 55 55 5B AF'
        # rtu_all = '0110001000010255555BAF'
        self.recv_slave = ""
        self.if_to_web = False

    def uart_send(self,getway_data):
        # while True:
            try:

                # 串口发送数据
                # result = ser.write("02040000000271F8".encode("gbk"))
                result = self.ser.write(getway_data.encode())
                print("写总字节数：", result)
                print("发送数据：", getway_data)
                # 数据的接收
                # ser.close()  # 关闭串口
            except Exception as e:
                print("error!", e)
            sleep(1)

    def uart_recv(self):

        while True:

            sleep(0.2)
            self.if_to_web = False
            # data = ser.readall()
            count = self.ser.inWaiting()
            if count > 0:
                self.recv_slave = (self.ser.read(count)).decode()
                data = self.recv_slave.split("=",1)
                self.addr_str=data[0]
                self.data_str=data[1]
                # print(data)
                self.if_to_web = True
                print("接收数据：", self.recv_slave)
            # return  recv_slave


if __name__ == '__main__':
    com = "COM5"
    bps = 115200
    uart = UART(com,bps)
    while True:
        getway_data="01:01:20:22:55:4F={A0=0.00,A1=0.80,A2=121.00,A3=40.00,A4=20.00,A6=0,A7=0}"
        # sen = threading.Thread(target=uart_send,args=(getway_data))
        # sen.setDaemon(True)
        # sen.start()
        uart_rec = threading.Thread(target=uart.uart_recv,args=())
        uart_rec.setDaemon(True)
        uart_rec.start()

        uart.uart_send(getway_data)
        # uart_recv()


        sleep(60)