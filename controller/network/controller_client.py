import socket
import json

def connect_to_agent(agent_ip="127.0.0.1", agent_port=8000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((agent_ip, agent_port))
    print(f"[CLIENT] Đã kết nối tới Agent {agent_ip}:{agent_port}")

    try:
        while True:
            cmd = input("Nhập lệnh ('exit' để thoát): ")
            s.sendall(cmd.encode("utf-8"))
            if cmd.lower() == "exit":
                break

            data = s.recv(8192).decode("utf-8").strip()
            if not data:
                continue

            try:
                result = json.loads(data)
                print("\n=== KẾT QUẢ THỰC THI ===")
                print(f"📜 Lệnh: {result['command']}")
                print(f"✅ Exit code: {result['exit_code']}")
                if result["stdout"]:
                    print(f"\n--- STDOUT ---\n{result['stdout']}")
                if result["stderr"]:
                    print(f"\n--- STDERR ---\n{result['stderr']}")
                print("=========================\n")
            except json.JSONDecodeError:
                print("[Lỗi] Không đọc được dữ liệu JSON:", data)

    except Exception as e:
        print("Lỗi:", e)
    finally:
        s.close()
        print("[CLIENT] Ngắt kết nối.")

if __name__ == "__main__":
    connect_to_agent()
