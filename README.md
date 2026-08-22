# Hi, I'm Jhannes

I live in Potsdam, Germany and build tools for problems I actually have. Lately that meant appointment scraping, a pocket-sized pentest rig and making file transfers between my laptop and Android phone less annoying.

## What I built

**[TherapyAlert](https://therapyalert.netlify.app/)**
Finds free psychotherapy slots for adults in Berlin-Brandenburg. One search run covers the KVBB doctor directory and the 116117 booking service, results show up as a weekly calendar instead of endless clicking through forms. React frontend, a Python and Flask backend doing the scraping. Code is private, the app itself is public.

**[ChonkyFlipper](https://github.com/jhannesreimann/chonkyflipper)**
A portable pentest device built around a Raspberry Pi 4 running Kali. It hosts its own WiFi access point and handles WiFi recon, BLE scanning, infrared capture and replay, sub-GHz radio, Zigbee, NFC and BadUSB, all controlled from a phone browser. Mostly Python, some JavaScript for the interface.

**[email-client-selftest-service](https://github.com/jhannesreimann/email-client-selftest-service)**
From a network security seminar at HPI: we ran a deliberately misbehaving mail server so anyone could point their own mail client at it and see whether it survives STARTTLS downgrade attempts or falls back to plaintext authentication. Team project, finished in March 2026, no longer maintained, but it still works if you host it yourself.

**[DankQuickShare](https://github.com/jhannesreimann/dms-quickshare)**
Android Quick Share integration for DankMaterialShell. A QML plugin on top and a small Rust daemon underneath that takes care of mDNS, Bluetooth LE and TCP transfers.

## Stack

Mostly Python with Flask or FastAPI on the backend side, React plus Vite and Tailwind for frontends. Java from university projects, Rust whenever something needs to run as a background service, a bit of QML for desktop widgets. Daily driver is Arch with Wayland, and a Raspberry Pi sits on the desk more often than not.

## Currently

Poking at ChonkyFlipper again. Before that it was the mail client selftest and getting TherapyAlert stable enough for daily use.

---

You can reach me at reimann.jhannes@gmail.com.
