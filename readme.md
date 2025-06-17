---

## 🧰 About the Project

This project provides two powerful tools — a **GUI** and a **CLI** — to:

- 📅 Display full-year calendars
- 🔁 Find years with identical calendars
- 🔍 Compare two calendar years for exact match
- 🛡️ Fetch **cybersecurity incidents** from CISA for any year

---

## 📂 Contents

| File Name                 | Description                       |
| ------------------------- | --------------------------------- |
| `calendar_gui.py`         | Graphical tool built with Tkinter |
| `same_calendar_finder.py` | Command-line version (CLI)        |
| `requirements.txt`        | Lists Python packages needed      |
| `README.md`               | You’re reading it!                |

---

## 🖼️ GUI Version (`calendar_gui.py`)

### Features:

- Clean Tkinter interface with dropdowns and back navigation
- Option 1: Show full calendar for a year + matching years
- Option 2: Compare calendars of two years
- Option 3: View cybersecurity incidents (via CISA) for a year

### To Run:

```bash
python calendar_gui.py
```

📝 *No API key required for CISA data.*

---

## 💻 CLI Version (`same_calendar_finder.py`)

### Features:

- Show calendar of a year
- Compare calendars between two years
- Match identical calendar years
- Fetch cyber incident summary for a year

### To Run:

```bash
python same_calendar_finder.py
```

You’ll be prompted to:

- Enter a year
- Choose an operation
- Optionally fetch CISA cyber data

---

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/calendar-cyber-tool.git
cd calendar-cyber-tool
```

2. Install required libraries:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Requirements

- Python 3.8+
- `requests`
- `beautifulsoup4`
- Tkinter (comes with Python by default)

---

## 📊 CISA Cyber Incidents

All cyber threat data is pulled from:

- 🛡️ [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

This ensures you stay updated with real-world cybersecurity incident history by year.

---

## ✨ Screenshots

*You can add screenshots of GUI here if needed.*

---

## 🙇‍♂️ Author

**Sagar Jha**

Contributions, suggestions, or issues are welcome via pull requests or GitHub Issues.

---

## 🛠️ Future Improvements

- Export calendar or reports to PDF
- Add map/timeline view for cyber threats
- Package as `.exe` for offline users

---

