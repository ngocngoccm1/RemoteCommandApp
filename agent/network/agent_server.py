
import socket
import threading
import json
from agent.executor.command_executor import execute_command
 
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

            # Gọi hàm executor để chạy thật
            result = execute_command(command)

            # Ghép nội dung gửi lại Controller
            response = {
                "command": command,
                "stdout": result["stdout"],
                "stderr": result["stderr"],
                "exit_code": result["exit_code"]
            }
            conn.sendall(json.dumps(response, ensure_ascii=False).encode("utf-8") + b"\n")
    except Exception as e:
        print(f"Loi: {e}")
    finally:
        conn.close()
        print(f"[AGENT] Đóng kết nối {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[AGENT] Đang lắng nghe tại {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
