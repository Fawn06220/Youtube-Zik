# 🎵 YoutubeZik DDL V2.5

**Téléchargeur YouTube pour Windows (audio & vidéo) avec interface graphique (wxPython)**  
Développé par Fawn — testé sous Python 3.12 et Windows 11.

## ✨ Fonctionnalités

- 🔍 Recherche directe de musiques/vidéos YouTube dans l'interface
- 🎧 Téléchargement audio uniquement (format `.m4a`)
- 🎞️ Téléchargement vidéo `.mp4` avec ou sans son
- 🔊 Choix de la qualité vidéo (Low ou High)
- 📁 Sauvegarde automatique dans des dossiers distincts :
  - `Audio Collection`
  - `Video Collection`
- 🌈 Couleurs pour identifier les fichiers déjà téléchargés :
  - **Bleu** : Téléchargeable
  - **Vert** : Vidéo déjà présente
  - **Violet** : Audio déjà présent
  - **Rouge** : Audio + Vidéo déjà présents
- 🔄 Système de gestion de doublons avec boîtes de dialogue intelligentes
- 🧵 Téléchargements en arrière-plan (multithreading)
- 💚 Lien de donation PayPal intégré
- 🆘 Aide intégrée via un bouton

## 🖥️ Démo

- 🎬 Démos vidéo : [http://ninjaaior.free.fr/devdemos/index.html](http://ninjaaior.free.fr/devdemos/index.html)

## EXE compilé pour windows

- Version compilée : [http://ninjaaior.free.fr/YouTubeZik.rar](http://ninjaaior.free.fr/YouTubeZik.rar)

## 🚀 Installation

### Prérequis

- Python ≥ 3.10 recommandé
- Windows uniquement (wxPython n'est pas cross-platform dans cette version)

### Installation des dépendances

```bash
pip install wxPython pytubefix moviepy
```

> **Note :** `pytubefix` est une version corrigée de `pytube`. Assure-toi qu’elle est bien installée.

### Lancement

```bash
python Youtube-Zik.py
```

## 📁 Arborescence

```
├── Youtube-Zik.py
├── Audio Collection/
└── Video Collection/
```

## ❤️ Remerciements

- 📺 [pytubefix](https://github.com/ldunn/pytubefix)
- 🎞️ [moviepy](https://zulko.github.io/moviepy/)
- 🖼️ [wxPython](https://wxpython.org/)

---

## ☕ Offrez un p'tit café au développeur ?

Si cet outil vous a été utile, vous pouvez soutenir le développement (et la consommation excessive de café ☕) ici :

➡️ [![Donate](icone/donate.png)](https://www.paypal.com/paypalme/noobpythondev)

Un grand merci ! 💙


