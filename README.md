[![FR](https://img.shields.io/badge/lang-FR-red.svg)](https://github.com/Fawn06220/Youtube-Zik/blob/main/README.fr.md)

# 🎵 YoutubeZik DDL V2.5

**YouTube Downloader for Windows (audio & video) with a graphical user interface (wxPython)**  
Developed by Fawn — tested with Python 3.12 on Windows 11.

## ✨ Features

- 🔍 Direct YouTube music/video search within the interface
- 🎧 Audio-only downloads (`.m4a` format)
- 🎞️ Video downloads in `.mp4` format, with or without audio
- 🔊 Option to select video quality (Low or High)
- 📁 Automatic saving into separate folders:
  - `Audio Collection`
  - `Video Collection`
- 🌈 Color-coded indicators for downloaded files:
  - **Blue**: Available for download
  - **Green**: Video already exists
  - **Purple**: Audio already exists
  - **Red**: Both audio and video already exist
- 🔄 Duplicate management system with smart dialogs
- 🧵 Background downloading (multithreading)
- 💚 Integrated PayPal donation link
- 🆘 Built-in help via a dedicated button

## ⚠️ EXTREMELY IMPORTANT: Node.js Required

To ensure proper functionality, **Node.js must be installed on your system**.

➡️ Download the recommended version here:  
[https://nodejs.org/en/download](https://nodejs.org/en/download)

Without Node.js, the application will not be able to download music or videos correctly!

## 🖥️ Demo

- 🎬 Video demos: [http://ninjaaior.free.fr/devdemos/index.html](http://ninjaaior.free.fr/devdemos/index.html)

## Compiled EXE for Windows

- Compiled version: [http://ninjaaior.free.fr/YouTubeZik.rar](http://ninjaaior.free.fr/YouTubeZik.rar) (right-click and “save as...”)

## 🚀 Installation

### Prerequisites

- Python ≥ 3.10 recommended
- Windows only (wxPython is not cross-platform in this version)

### Installing Dependencies

```bash
pip install wxPython pytubefix moviepy
```

> **Note:** `pytubefix` is a patched version of `pytube`. Make sure it is properly installed.

### Launching the App

```bash
python Youtube-Zik.py
```

## 📁 Directory Structure

```
├── Youtube-Zik.py
├── Audio Collection/
└── Video Collection/
```

## ❤️ Acknowledgements

- 📺 [pytubefix](https://github.com/ldunn/pytubefix)
- 🎞️ [moviepy](https://zulko.github.io/moviepy/)
- 🖼️ [wxPython](https://wxpython.org/)

---

## ☕ Buy the Developer a Coffee?

If you found this tool helpful, consider supporting its development (and the developer’s coffee addiction ☕) here:

➡️ [![Donate](icone/donate.png)](https://www.paypal.com/paypalme/noobpythondev)

Thank you so much! 💙
