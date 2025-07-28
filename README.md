# ⚔️ MITM Attack Automation Toolkit

A powerful **Man-in-the-Middle attack suite** that automates ARP spoofing, DNS spoofing, SSL stripping, session hijacking, and phishing login harvesting — all controlled via a sleek Python GUI.

> 🔥 Built by [Prince Kumar Yadav](https://github.com/YadavPrince28) | B.Tech CSE | Cybersecurity Enthusiast

---

## 🧩 Features

- 🔥 ARP Spoofing (target victim + gateway)
- 🌐 DNS Spoofing (redirect domain queries)
- 🔓 SSL Stripping (HTTPS → HTTP downgrade)
- 🍪 Session Hijacking (cookie sniffing)
- 🔑 Fake Login Site (credential harvesting)
- 🖥️ GUI Control Panel (`main.py`) to launch & monitor everything

---

## 🗂️ Project Structure

MITM_Project/
├── arp_spoof.py
├── dns_spoof.py
├── session_hijack.py
├── sslstrip.py
├── main.py
├── requirements.txt
├── README.md
│
├── captured_logins.txt
├── stolen_cookies.txt
│
└── fake_site/
├── server.py
└── templates/
└── login.html

## ⚙️ Setup Instructions

### 🔧 1. Clone the Repository
```bash
git clone https://github.com/YadavPrince28/MITM-Attack-Automation-Project.git
cd MITM-Attack-Automation-Project

```
 ### 🔧 2. Install Dependencies
    pip install -r requirements.txt
      ## If you get tkinter error:
                 sudo apt install python3-tk

### 🔧 3. Enable IP Forwarding
     sudo sysctl -w net.ipv4.ip_forward=1
### 🔧 4. Run GUI Control Panel
      sudo python3.13 main.py

### 📁 Log Files
| File                  | Description                         |
| --------------------- | ----------------------------------- |
| `captured_logins.txt` | Stores credentials from fake login  |
| `stolen_cookies.txt`  | Captures cookies from HTTP requests |


### ⚠️ Legal Disclaimer
 This tool is for educational purposes only.
The author does NOT promote or support illegal hacking activities. Use only in controlled labs or CTF environments with permission.

```
🙋 Author
Prince Kumar Yadav
🎓 B.Tech CSE | Cybersecurity Enthusiast
📍 I.K. Gujral Punjab Technical University, Jalandhar
🔗 GitHub: https://github.com/YadavPrince28)
📫 Mail: princekyadav2804@gmail.com

    
