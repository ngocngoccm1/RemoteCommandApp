import socket
import threading

HOST = "0.0.0.0"
PORT = 8000

def handle_client(conn, addr):
    print(f"[AGENT] Kết nối từ {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode("utf-8").strip()
            print(f"[AGENT] Nhận lệnh: {command}")
            if command.lower() == "exit":
                conn.sendall(b"Ngat ket noi.\n")
                break
            # Demo phản hồi (sẽ thay bằng subprocess sau)
            response = f"Da nhan lenh: {command}\n".encode("utf-8")
            conn.sendall(response)
    except Exception as e:
        print(f"Loi: {e}")
    finally:
        conn.close()
        print(f"[AGENT] Dong ket noi {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[AGENT] Dang lang nghe tai {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
