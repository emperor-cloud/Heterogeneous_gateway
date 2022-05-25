from socket import *
from time import sleep
# from main import if_to_uart


ip="47.99.214.175"
port = 28082

class Zhiyun:
    def __init__(self,ip,port):
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.server_ip = ip
        self.server_port = port
        self.send_data = ''
        self.recv_data = ''
        self.slave_get = ''
        self.if_to_uart = False

    def tcp_con(self):
        self.tcp_client_socket.connect((self.server_ip, self.server_port))
        self.send_data = "{\"method\":\"authenticate\",\"uid\":\"729774038670\",\"key\":\"BwIJBgUEAgIIBAcFW11WWVBHX10Z\",\"version\":\"0.1.0\",\"autodb\":true}"
        self.tcp_client_socket.send(self.send_data.encode("gbk"))

    def recv_msg(self):
        while True:
            self.if_to_uart = False
            sleep(0.5)

            self.recv_data = self.tcp_client_socket.recv(1024)
            print('智云发来的数据为:', self.recv_data.decode('gbk'))
            get_data=self.recv_data.decode()
            print('智云的数据拆分为:',get_data.split('"'))
            method_str = get_data.split('"')[3]
            if (method_str == 'echo'):
                print("心跳中。。。")
                continue
            if (method_str == 'authenticate_rsp'):
                print("登录智云成功")
                continue
            if (method_str == 'control'):

                print("分析智云下发的数据中")
                data_str = get_data.split('"')[7]
                addr_str = get_data.split('"')[11]
                if addr_str[0:4]=="WIFI":
                    print("wifi mode")
                    self.slave_get = addr_str[5:] + "=" + data_str
                else:self.slave_get=addr_str + "=" + data_str
                self.if_to_uart=True
                print(self.slave_get)

    def heart_beat(self):
        while True:
            sleep(5)
            self.send_data = "{\"method\":\"echo\",\"timestamp\":1605141585800,\"seq\":5}"
            self.tcp_client_socket.send(self.send_data.encode("gbk"))
            # self.recv_data = self.tcp_client_socket.recv(1024)
            # print('心跳数据为:', self.recv_data.decode('gbk'))


    def tcp_stop(self):
        self.tcp_client_socket.close()


    def tcp_send(self,data):
        self.send_data = data
        print("上报智云中")
        print(self.send_data)
        self.tcp_client_socket.send(self.send_data.encode("gbk"))


if __name__ == '__main__':
    ZY=Zhiyun(ip,port)
    ZY.tcp_con()
    # ZY.recv_msg()
    ZY.heart_beat()
    ZY.tcp_stop()
