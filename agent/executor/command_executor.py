import subprocess

def execute_command(command: str, timeout: int = 15):
    """
    Chạy command trên Windows CMD (hoặc PowerShell nếu cần)
    Trả về: dict {stdout, stderr, exit_code}
    """
    try:
        # Dùng shell=True để chạy lệnh như trên CMD
        completed = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
            "exit_code": completed.returncode
        }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": f"Lệnh vượt quá thời gian {timeout}s",
            "exit_code": -1
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Lỗi khi chạy lệnh: {e}",
            "exit_code": -1
        }
