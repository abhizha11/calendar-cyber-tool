import tkinter as tk
from tkinter import ttk
import calendar
import requests
from typing import List

# ---------------------------- CYBER INCIDENTS (CISA) ---------------------------- #

KEV_FEED_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
)


def fetch_cyber_incidents(year: int) -> List[str]:
    """Return human‑readable list of KEV entries added in the given year."""
    try:
        resp = requests.get(KEV_FEED_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        return [f"⚠️  Failed to fetch CISA data: {exc}"]

    out = [
        f"{item['dateAdded']}: {item.get('cveID', 'Unknown')} — {item.get('vulnerabilityName', 'No description')}"
        for item in data.get("vulnerabilities", [])
        if item.get("dateAdded", "").startswith(str(year))
    ]
    return out or ["No incidents found for this year"]

# ---------------------------- CALENDAR UTILITIES ---------------------------- #

def same_calendar(a: int, b: int) -> bool:
    return (
        calendar.isleap(a) == calendar.isleap(b)
        and calendar.weekday(a, 1, 1) == calendar.weekday(b, 1, 1)
    )


def matching_years(target: int):
    return [y for y in range(1900, 2100) if y != target and same_calendar(target, y)]


def get_calendar_text(year: int) -> str:
    return calendar.TextCalendar(calendar.SUNDAY).formatyear(year)


def compare_calendars_text(y1: int, y2: int) -> str:
    cal = calendar.TextCalendar(calendar.SUNDAY)
    lines = []
    for m in range(1, 13):
        left = cal.formatmonth(y1, m).splitlines()
        right = cal.formatmonth(y2, m).splitlines()
        lines.append(f"--- {calendar.month_name[m]} ---")
        for l, r in zip(left, right):
            lines.append(f"{l:<22} | {r}")
        lines.append("")
    verdict = "✅ Calendars IDENTICAL" if same_calendar(y1, y2) else "❌ Calendars DIFFERENT"
    lines.append(verdict)
    return "\n".join(lines)

# ---------------------------- GUI CLASS ---------------------------- #

class CalendarApp:
    def __init__(self, root):
        self.root = root
        root.title("📅 Calendar & Cyber Tool")
        root.geometry("800x650")
        self.main_menu()

    # Utility to clear window
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # -------------------- MAIN MENU -------------------- #
    def main_menu(self):
        self.clear()
        ttk.Label(self.root, text="Choose an Option", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self.root, text="1️⃣ Calendar + Matching Years", command=self.option1).pack(pady=10)
        ttk.Button(self.root, text="2️⃣ Compare Two Years", command=self.option2).pack(pady=10)
        ttk.Button(self.root, text="3️⃣ Cyber Incidents (CISA)", command=self.option3).pack(pady=10)

    # -------------------- OPTION 1 -------------------- #
    def option1(self):
        self.clear()
        ttk.Label(self.root, text="Select a Year:").pack(pady=5)
        self.year_var = tk.IntVar(value=2025)
        years = list(range(1900, 2101))
        ttk.Combobox(self.root, textvariable=self.year_var, values=years, state="readonly").pack(pady=5)
        ttk.Button(self.root, text="Show Calendar", command=self.show_calendar_option1).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def show_calendar_option1(self):
        year = self.year_var.get()
        self.clear()
        ttk.Label(self.root, text=f"Calendar for {year}", font=("Courier", 12)).pack()
        cal_box = tk.Text(self.root, width=90, height=20)
        cal_box.pack()
        cal_box.insert("1.0", get_calendar_text(year))
        cal_box.configure(state="disabled")

        # Matching years dropdown powered by StringVar (persistent)
        matches = matching_years(year)
        ttk.Label(self.root, text="\nMatching Years:").pack()
        self.match_var = tk.StringVar()
        match_combo = ttk.Combobox(self.root, textvariable=self.match_var, values=matches, state="readonly")
        match_combo.pack(pady=5)

        ttk.Button(
            self.root,
            text="Show Selected Matching Year",
            command=self.show_selected_match,
        ).pack(pady=5)
        ttk.Button(self.root, text="Back", command=self.option1).pack(pady=10)

    def show_selected_match(self):
        sel = self.match_var.get()
        if not sel.isdigit():
            tk.messagebox.showwarning("No Selection", "Please choose a matching year first.")
            return
        year = int(sel)
        self.clear()
        ttk.Label(self.root, text=f"Calendar for {year}", font=("Courier", 12)).pack()
        box = tk.Text(self.root, width=90, height=20)
        box.pack()
        box.insert("1.0", get_calendar_text(year))
        box.configure(state="disabled")
        ttk.Button(self.root, text="Back", command=self.option1).pack(pady=10)

    # -------------------- OPTION 2 -------------------- #
    def option2(self):
        self.clear()
        ttk.Label(self.root, text="Select Two Years:").pack(pady=5)
        years = list(range(1900, 2101))
        self.y1 = tk.IntVar(value=2025)
        self.y2 = tk.IntVar(value=2031)
        ttk.Combobox(self.root, values=years, textvariable=self.y1, state="readonly").pack(pady=5)
        ttk.Combobox(self.root, values=years, textvariable=self.y2, state="readonly").pack(pady=5)
        ttk.Button(self.root, text="Compare", command=self.compare_years).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def compare_years(self):
        y1, y2 = self.y1.get(), self.y2.get()
        self.clear()
        ttk.Label(self.root, text=f"Comparison: {y1} vs {y2}", font=("Arial", 12)).pack()
        box = tk.Text(self.root, width=100, height=30)
        box.pack()
        box.insert("1.0", compare_calendars_text(y1, y2))
        box.configure(state="disabled")
        ttk.Button(self.root, text="Back", command=self.option2).pack(pady=10)

    # -------------------- OPTION 3 -------------------- #
    def option3(self):
        self.clear()
        ttk.Label(self.root, text="Select Year for Cyber Incidents:").pack(pady=5)
        years = list(range(2010, 2101))
        self.cisa_var = tk.IntVar(value=2025)
        ttk.Combobox(self.root, values=years, textvariable=self.cisa_var, state="readonly").pack(pady=5)
        ttk.Button(self.root, text="Fetch Incidents", command=self.show_incidents).pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.main_menu).pack(pady=10)

    def show_incidents(self):
        year = self.cisa_var.get()
        self.clear()
        ttk.Label(self.root, text=f"CISA Incidents in {year}", font=("Arial", 12)).pack()
        box = tk.Text(self.root, width=100, height=30)
        box.pack()
        box.insert("1.0", "\n".join(fetch_cyber_incidents(year)))
        box.configure(state="disabled")
        ttk.Button(self.root, text="Back", command=self.option3).pack(pady=10)

# ---------------------------- RUN ---------------------------- #

if __name__ == "__main__":
    root = tk.Tk()
    ttk.Style().theme_use("clam")  # nicer default look
    app = CalendarApp(root)
    root.mainloop()
