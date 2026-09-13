import ctypes
import subprocess
import sys
import time
import urllib.request

SERVICE = "Jenkins"
URL = "http://localhost:8080"


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def relaunch_elevated():
    params = " ".join(f'"{a}"' for a in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)


def service_state():
    result = subprocess.run(
        ["sc", "query", SERVICE], capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("STATE"):
            return line.split()[-1]
    return "UNKNOWN"


def wait_for_http(timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(URL, timeout=3)
            return True
        except Exception:
            time.sleep(2)
    return False


def start():
    print("Starting Jenkins service...")
    subprocess.run(["net", "start", SERVICE])
    print(f"Service state: {service_state()}")
    print(f"Waiting for {URL} to respond...")
    if wait_for_http():
        print(f"Jenkins is up at {URL}")
    else:
        print("Jenkins service started but is not responding on port 8080 yet. Check again shortly.")


def stop():
    print("Stopping Jenkins service...")
    subprocess.run(["net", "stop", SERVICE])
    print(f"Service state: {service_state()}")


def status():
    print(f"Service state: {service_state()}")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("start", "stop", "status"):
        print("Usage: python jenkins_ctl.py [start|stop|status]")
        sys.exit(1)

    action = sys.argv[1]

    if action in ("start", "stop") and not is_admin():
        print("Admin rights required, requesting elevation (UAC prompt)...")
        relaunch_elevated()
        return

    if action == "start":
        start()
    elif action == "stop":
        stop()
    elif action == "status":
        status()


if __name__ == "__main__":
    main()
