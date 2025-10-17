import socket

def connect_to_agent(agent_ip="127.0.0.1", agent_port=8000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((agent_ip, agent_port))
    print(f"[CLIENT] Da ket noi toi Agent {agent_ip}:{agent_port}")

    try:
        while True:
            cmd = input("Nhap lenh ('exit' de thoat): ")
            s.sendall(cmd.encode("utf-8"))
            if cmd.lower() == "exit":
                break
            data = s.recv(4096)
            print("[KET QUA TU AGENT]:")
            print(data.decode("utf-8"))
    except Exception as e:
        print("Loi:", e)
    finally:
        s.close()
        print("[CLIENT] Ngat ket noi.")

if __name__ == "__main__":
    connect_to_agent()
