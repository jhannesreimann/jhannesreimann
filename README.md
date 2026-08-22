# Hi, I'm Jhannes

<p align="center">
  <a href="https://www.linkedin.com/in/jhannes-reimann/"><img src="https://readme-typing-svg.herokuapp.com?font=JetBrains+Mono&weight=600&size=22&pause=1000&color=58A6FF&center=true&vCenter=true&width=600&lines=MSc+Computer+Science+student+at+HPI;Security+Engineering+focus;Working+student+at+SAP;Breaking+things+to+understand+them+better" alt="MSc Computer Science student at HPI, Security Engineering focus, working student at SAP" /></a>
</p>

I live in Potsdam, Germany and build tools for problems I actually have. Lately that meant appointment scraping, a pocket-sized pentest rig and making file transfers between my laptop and Android phone less annoying.

<!-- The card below is regenerated daily by .github/workflows/fetch.py runs: live repo, star, follower and contribution numbers straight from the GitHub API, no third party involved. -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jhannesreimann/jhannesreimann/main/assets/fetch-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/jhannesreimann/jhannesreimann/main/assets/fetch-light.svg" />
    <img alt="Neofetch style profile card: ASCII portrait on the left, OS, studies, languages, contact and GitHub stats on the right" src="https://raw.githubusercontent.com/jhannesreimann/jhannesreimann/main/assets/fetch-light.svg" />
  </picture>
</p>

I study Computer Science at the Hasso Plattner Institute, Masters track, with a focus on Security Engineering. On the side I work at SAP as a working student. Security is the common thread in most of what I tinker with: figuring out how systems fail turns out to be the fastest way to understand how they work.

## What I built

**[TherapyAlert](https://therapyalert.netlify.app/)**
Finds free psychotherapy slots for adults in Berlin-Brandenburg. One search run covers the KVBB doctor directory and the 116117 booking service, results show up as a weekly calendar instead of endless clicking through forms. React frontend, a Python and Flask backend doing the scraping. Code is private, the app itself is public.

**[ChonkyFlipper](https://github.com/jhannesreimann/chonkyflipper)**
A portable pentest device built around a Raspberry Pi 4 running Kali. It hosts its own WiFi access point and handles WiFi recon, BLE scanning, infrared capture and replay, sub-GHz radio, Zigbee, NFC and BadUSB, all controlled from a phone browser. Mostly Python, some JavaScript for the interface.

**[email-client-selftest-service](https://github.com/jhannesreimann/email-client-selftest-service)**
From a network security seminar at HPI: we ran a deliberately misbehaving mail server so anyone could point their own mail client at it and see whether it survives STARTTLS downgrade attempts or falls back to plaintext authentication. Team project, finished in March 2026, no longer maintained, but it still works if you host it yourself.

**[dns-resolver-recommender](https://github.com/jhannesreimann/dns-resolver-recommender)**
Measures and ranks DNS-over-HTTPS resolvers straight from the browser. A Rust WebAssembly core runs the latency probes so timing happens client-side, a React frontend shows the ranking and a small Python backend takes care of resolver rotation. Another HPI course project, mirrored from GitLab, running at [dns.diic-hpi.org](https://dns.diic-hpi.org/).

**[DankQuickShare](https://github.com/jhannesreimann/dms-quickshare)**
Android Quick Share integration for DankMaterialShell. A QML plugin on top and a small Rust daemon underneath that takes care of mDNS, Bluetooth LE and TCP transfers.

## Stack

<p align="center">
  <img src="https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/-Jupyter-F37626?style=flat-square&logo=jupyter&logoColor=white" alt="Jupyter" />
  <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" alt="JavaScript" />
  <img src="https://img.shields.io/badge/-Java-007396?style=flat-square&logo=openjdk&logoColor=white" alt="Java" />
  <img src="https://img.shields.io/badge/-C%23-512BD4?style=flat-square&logo=dotnet&logoColor=white" alt="C#" />
  <img src="https://img.shields.io/badge/-Rust-DEA584?style=flat-square&logo=rust&logoColor=black" alt="Rust" />
  <img src="https://img.shields.io/badge/-QML-41CD52?style=flat-square&logo=qt&logoColor=white" alt="QML" />
  <img src="https://img.shields.io/badge/-Linux-FCC624?style=flat-square&logo=linux&logoColor=black" alt="Linux" />
  <img src="https://img.shields.io/badge/-Raspberry%20Pi-C51A4A?style=flat-square&logo=raspberrypi&logoColor=white" alt="Raspberry Pi" />
</p>

Mostly Python with Flask or FastAPI on the backend side, React plus Vite and Tailwind for frontends. Java from the bachelor thesis, C# from KeySafe, Jupyter for everything research adjacent. Rust whenever something needs to run as a background service, a bit of QML for desktop widgets. Daily driver is Arch with Wayland, and a Raspberry Pi sits on the desk more often than not.

## Numbers

<!-- The snake SVGs are generated by .github/workflows/snake.yml and pushed to the output branch. They appear after the first Actions run post-push, then refresh daily at midnight UTC. -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jhannesreimann/jhannesreimann/output/github-contribution-grid-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/jhannesreimann/jhannesreimann/output/github-contribution-grid-snake.svg" />
    <img alt="Contribution snake" src="https://raw.githubusercontent.com/jhannesreimann/jhannesreimann/output/github-contribution-grid-snake.svg" />
  </picture>
</p>

## Currently

Poking at ChonkyFlipper again. Before that it was the mail client selftest and getting TherapyAlert stable enough for daily use.

---

You can reach me at reimann.jhannes@gmail.com, or find me on [LinkedIn](https://www.linkedin.com/in/jhannes-reimann/).
