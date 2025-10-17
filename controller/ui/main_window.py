import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import json

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Remote CLI Controller")
        self.root.geometry("800x550")
        self.root.resizable(False, False)

        # ===== HEADER =====
        title = tk.Label(
            root,
            text="🧠 Remote CLI Controller",
            font=("Segoe UI", 16, "bold"),
            fg="#0ff",
        )
        title.pack(pady=10)

        # ===== FRAME KẾT NỐI =====
        frm_conn = tk.Frame(root)
        frm_conn.pack(pady=5)

        tk.Label(frm_conn, text="IP Agent:").grid(row=0, column=0, padx=5)
        self.ip_entry = tk.Entry(frm_conn, width=18)
        self.ip_entry.insert(0, "127.0.0.1")
        self.ip_entry.grid(row=0, column=1)

        tk.Label(frm_conn, text="Port:").grid(row=0, column=2, padx=5)
        self.port_entry = tk.Entry(frm_conn, width=6)
        self.port_entry.insert(0, "8000")
        self.port_entry.grid(row=0, column=3)

        tk.Label(frm_conn, text="Mật khẩu:").grid(row=0, column=4, padx=5)
        self.pass_entry = tk.Entry(frm_conn, show="*", width=12)
        self.pass_entry.insert(0, "123456")
        self.pass_entry.grid(row=0, column=5)

        self.btn_connect = tk.Button(
            frm_conn, text="🔌 Kết nối", width=12, command=self.connect_to_agent
        )
        self.btn_connect.grid(row=0, column=6, padx=5)

        self.btn_disconnect = tk.Button(
            frm_conn, text="❌ Ngắt", width=10, command=self.disconnect, state="disabled"
        )
        self.btn_disconnect.grid(row=0, column=7, padx=5)

        # ===== KHUNG LOG / CONSOLE =====
        self.console = scrolledtext.ScrolledText(
            root, width=95, height=25, bg="#111", fg="#0f0", font=("Consolas", 10)
        )
        self.console.pack(padx=10, pady=10)
        self.console.insert(tk.END, "💡 Sẵn sàng kết nối tới Agent...\n")
        self.console.config(state="disabled")

        # ===== FRAME GỬI LỆNH =====
        frm_cmd = tk.Frame(root)
        frm_cmd.pack(pady=5)

        self.cmd_entry = tk.Entry(frm_cmd, width=70, font=("Consolas", 10))
        self.cmd_entry.grid(row=0, column=0, padx=5)
        tk.Button(frm_cmd, text="▶ Gửi", command=self.send_command, width=10).grid(
            row=0, column=1, padx=5
        )

        # ===== BIẾN MẠNG =====
        self.sock = None
        self.connected = False

    # ==========================
    # SOCKET CLIENT FUNCTIONS
    # ==========================
    def connect_to_agent(self):
        ip = self.ip_entry.get().strip()
        port = int(self.port_entry.get().strip())
        password = self.pass_entry.get().strip()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((ip, port))
            self.connected = True
            self.display(f"[+] Đã kết nối tới {ip}:{port}")

            # Nhận prompt mật khẩu từ server
            prompt = self.sock.recv(1024).decode("utf-8")
            self.display(prompt)

            # Gửi mật khẩu
            self.sock.sendall(password.encode("utf-8"))

            # Nhận phản hồi xác thực
            resp = self.sock.recv(1024).decode("utf-8")
            self.display(resp)
            if "Sai mật khẩu" in resp:
                self.sock.close()
                self.connected = False
                return

            self.btn_connect.config(state="disabled")
            self.btn_disconnect.config(state="normal")

            threading.Thread(target=self.listen_from_server, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối tới Agent:\n{e}")
            self.display(f"[LỖI] {e}")

    def listen_from_server(self):
        while self.connected:
            try:
                data = self.sock.recv(8192)
                if not data:
                    break
                msg = data.decode("utf-8").strip()

                try:
                    result = json.loads(msg)
                    out = f"\n📜 {result['command']}\n"
                    if result["stdout"]:
                        out += f"\n--- STDOUT ---\n{result['stdout']}\n"
                    if result["stderr"]:
                        out += f"\n--- STDERR ---\n{result['stderr']}\n"
                    out += f"\nExit code: {result['exit_code']}\n"
                    self.display(out)
                except json.JSONDecodeError:
                    self.display(msg)
            except Exception as e:
                self.display(f"[LỖI] {e}")
                break
        self.display("🚪 Kết nối bị đóng.")
        self.connected = False
        self.sock.close()
        self.btn_connect.config(state="normal")
        self.btn_disconnect.config(state="disabled")

    def send_command(self):
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        if not self.connected:
            self.display("[!] Chưa kết nối Agent.")
            return

        self.display(f">>> {cmd}")
        try:
            self.sock.sendall(cmd.encode("utf-8"))
        except Exception as e:
            self.display(f"[LỖI GỬI] {e}")
        self.cmd_entry.delete(0, tk.END)

    def disconnect(self):
        if self.connected:
            try:
                self.sock.sendall("exit".encode("utf-8"))
                self.sock.close()
            except:
                pass
            self.connected = False
            self.display("🚪 Ngắt kết nối thủ công.")
            self.btn_connect.config(state="normal")
            self.btn_disconnect.config(state="disabled")

    # ==========================
    # GUI UTILS
    # ==========================
    def display(self, msg: str):
        self.console.config(state="normal")
        self.console.insert(tk.END, msg + "\n")
        self.console.see(tk.END)
        self.console.config(state="disabled")
