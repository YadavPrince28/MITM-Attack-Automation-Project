import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
import subprocess
import os

# Paths to your scripts
SCRIPTS = {
    "ARP Spoofing": "arp_spoof.py",
    "DNS Spoofing": "dns_spoof.py",
    "Fake Login Site": "fake_site/server.py",
    "Session Hijacking": "session_hijack.py",
    "SSL Strip": "sslstrip.py",
    
    
}

# Keep track of subprocesses
processes = {}

def run_script(name):
    if name in SCRIPTS:
        path = SCRIPTS[name]
        if not os.path.exists(path):
            messagebox.showerror("Missing File", f"{path} not found!")
            return
        try:
            proc = subprocess.Popen(['python3', path])
            processes[name] = proc
            log_text.insert(tk.END, f"[+] Started {name}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def stop_script(name):
    if name in processes:
        processes[name].terminate()
        log_text.insert(tk.END, f"[-] Stopped {name}\n")
        del processes[name]

def stop_all():
    for name in list(processes.keys()):
        stop_script(name)

def on_closing():
    if messagebox.askokcancel("Exit", "Do you want to exit and stop all processes?"):
        stop_all()
        root.destroy()

root = tk.Tk()
root.title("MITM Attack Automation Tool")
root.geometry("720x500")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("default")
style.configure("TButton",
                background="#333344",
                foreground="#ffffff",
                font=('Segoe UI', 10),
                padding=6)
style.configure("TLabel",
                background="#1e1e2f",
                foreground="#f0f0f5",
                font=('Segoe UI', 11))

# Title
ttk.Label(root, text="MITM Attack Control Panel", font=('Segoe UI', 16, 'bold')).pack(pady=10)

# Frame for buttons
frame = ttk.Frame(root)
frame.pack(pady=10)

# Create buttons for each script
for name in SCRIPTS:
    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill='x', pady=5)

    ttk.Label(btn_frame, text=name).pack(side='left', padx=10)
    ttk.Button(btn_frame, text="Start", command=lambda n=name: Thread(target=run_script, args=(n,)).start()).pack(side='left')
    ttk.Button(btn_frame, text="Stop", command=lambda n=name: stop_script(n)).pack(side='left', padx=5)

# Log output
log_label = ttk.Label(root, text="Logs:")
log_label.pack(anchor='w', padx=10)

log_text = tk.Text(root, height=12, bg="#2c2c44", fg="#e0e0f0", insertbackground="white")
log_text.pack(fill='both', padx=10, pady=10, expand=True)

# Exit button
ttk.Button(root, text="Exit & Stop All", command=on_closing).pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
