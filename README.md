# Clock X Overlay

> Horloge OSD always-on-top pour Linux X11 — configurable, légère, universelle.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-6.4%2B-green)
![Linux X11](https://img.shields.io/badge/Linux-X11-orange)

---

## Fonctionnalités

- **Horloge toujours au-dessus** de toutes les fenêtres (OSD / overlay)
- **Click-through** : la souris traverse l'horloge sans l'interagir
- **Draggable** : glissez l'horloge à la souris pour la repositionner
- **Icône système tray** : show/hide, paramètres, quitter
- **Interface de paramétrage complète** :
  - Police, taille, gras, italique
  - Couleur et opacité du texte et du fond
  - Rayon de bordure, marges internes
  - Format de l'heure (strftime) avec préréglages
  - Position en % de l'écran avec raccourcis (9 zones)
  - Sélection de l'écran (multi-moniteur)
- **Prévisualisation en temps réel** dans les paramètres
- **Config persistante** : `~/.config/clock_x_overlay/config.json`
- Compatible : **Cinnamon, GNOME, KDE, XFCE, MATE, i3, Openbox…**

---

## Installation

### Prérequis

```bash
# Arch Linux / Manjaro
sudo pacman -S python-pyqt6 python-pip

# Debian/Ubuntu/Mint
sudo apt install python3-pip python3-pyqt6

# Fedora/RHEL
sudo dnf install python3-pyqt6 python3-pip

# ou via pip dans un venv (toutes distros)
pip install PyQt6
```

### Lancement direct

```bash
git clone https://github.com/dewiweb/clock_X_overlay.git
cd clock_X_overlay
pip install -r requirements.txt
python run.py
```

### Installation système (pip)

```bash
pip install -e .
clock-x-overlay
```

### Démarrage automatique

Copiez le fichier `.desktop` dans votre dossier d'autostart :

```bash
cp clock-x-overlay.desktop ~/.config/autostart/
```

---

## Utilisation

1. **Lancer l'app** → l'horloge apparaît en overlay
2. **Clic droit sur l'icône tray** → menu contextuel
3. **Paramètres** → configurer police, couleurs, format, position
4. **Appliquer** → changements immédiats sur l'overlay
5. **Glisser l'horloge** avec la souris pour ajuster la position (désactiver click-through d'abord si besoin)

---

## Format de l'heure (strftime)

| Code | Valeur |
|------|--------|
| `%H` | Heure 24h (00–23) |
| `%I` | Heure 12h (01–12) |
| `%M` | Minutes (00–59) |
| `%S` | Secondes (00–59) |
| `%p` | AM/PM |
| `%A` | Jour de la semaine |
| `%d` | Jour du mois |
| `%B` | Nom du mois |
| `%Y` | Année |

Exemple : `%H:%M:%S — %A %d %B %Y` → `14:32:07 — Mercredi 26 mars 2025`

---

## Configuration

Le fichier `~/.config/clock_x_overlay/config.json` est créé automatiquement.

```json
{
  "font_family": "Monospace",
  "font_size": 48,
  "font_bold": true,
  "text_color": "#FFFFFF",
  "bg_color": "#000000",
  "bg_opacity": 140,
  "time_format": "%H:%M:%S",
  "pos_x": 50,
  "pos_y": 50,
  "screen_index": 0,
  "click_through": true
}
```

---

## Licence

MIT
