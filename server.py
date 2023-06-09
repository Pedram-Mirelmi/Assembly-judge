import socket
import threading
from ServerRequestHandler import handle, loadData
import json



class Server:
    def __init__(self, port_num: int = 9999, max_req_size: int = 5):
        self.port = port_num
        self.max_req_size = max_req_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        loadData()

    def runServer(self) -> None:
        self.sock.bind(('localhost', self.port))
        self.sock.listen()
        print(f"listening on port {self.port}")
        while True:
            sock_obj, address_info = self.sock.accept()
            print(f"connected to a client: IP: {address_info}")
            new_connection = threading.Thread(target=self.__talkToClient,
                                              args=(sock_obj,))
            new_connection.start()

    def __talkToClient(self, sock_obj: socket.socket) -> None:
        try:
            while True:
                req_dict = self.__get_req(sock_obj)
                if not req_dict:
                    print('connection ended by client')
                    break
                res_dict = handle(req_dict)
                self.__send_res(sock_obj, res_dict)
        except Exception as e:
            print(f'connection crashed! {e}')
            sock_obj.close()

    def __get_req(self, sock_obj: socket.socket) -> dict:
        req_len = int(sock_obj.recv(self.max_req_size).decode('utf-8'))
        req = json.loads(sock_obj.recv(req_len).decode('utf-8'))
        print(f"received this: {req}")
        return req

    def __send_res(self, sock_obj: socket.socket, res_dic: dict) -> None:
        res_str = json.dumps(res_dic, default=str)
        res_str = f"{len(res_str):<{self.max_req_size}}" + res_str
        print(f"sent this:{res_str}")
        sock_obj.send(bytes(res_str, encoding='utf-8'))


if __name__ == '__main__':
    server = Server()
    server.runServer()