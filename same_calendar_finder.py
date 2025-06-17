import calendar
import requests
from typing import List, Dict

# ─────────────  LIVE CISA KEV FEED (used only in Option 3)  ───────────── #

KEV_FEED_URL = (
    "https://www.cisa.gov/sites/default/files/feeds/"
    "known_exploited_vulnerabilities.json"
)
HTTP_TIMEOUT = 15  # seconds

def fetch_cyber_incidents(year: int) -> List[Dict[str, str]]:
    try:
        r = requests.get(KEV_FEED_URL, timeout=HTTP_TIMEOUT)
        r.raise_for_status()
        data = r.json()
    except Exception as exc:
        print(f"⚠️  Could not fetch CISA data: {exc}")
        return []
    return sorted(
        (
            {
                "date": item["dateAdded"],
                "title": item.get("cveID", "Unknown CVE"),
                "description": item.get(
                    "vulnerabilityName", "Exploited vulnerability"
                ),
            }
            for item in data.get("vulnerabilities", [])
            if item.get("dateAdded", "").startswith(str(year))
        ),
        key=lambda x: x["date"],
        reverse=True,
    )

def show_cyber_summary(year: int) -> None:
    print(f"\n🛡️  CISA exploited vulnerabilities added in {year}:")
    inc = fetch_cyber_incidents(year)
    if not inc:
        print(" • No entries for this year in the KEV catalog.")
    else:
        for i in inc:
            print(f" • {i['date']}: {i['title']} — {i['description']}")

# ─────────────  CALENDAR UTILITIES  ───────────── #

def same_calendar(a: int, b: int) -> bool:
    return (
        calendar.isleap(a) == calendar.isleap(b)
        and calendar.weekday(a, 1, 1) == calendar.weekday(b, 1, 1)
    )

def matching_years(target: int) -> List[int]:
    return [
        y for y in range(1600, 2100)
        if y != target and same_calendar(target, y)
    ]

def show_calendar(year: int) -> None:
    print(f"\n📅 Full calendar for {year}:\n")
    print(calendar.TextCalendar(calendar.SUNDAY).formatyear(year))

def compare_calendars(y1: int, y2: int) -> None:
    print(f"\n🔍 Comparing {y1} vs {y2} calendars:\n")
    cal = calendar.TextCalendar(calendar.SUNDAY)
    for m in range(1, 13):
        left  = cal.formatmonth(y1, m).splitlines()
        right = cal.formatmonth(y2, m).splitlines()
        for l, r in zip(left, right):
            print(f"{l:<22} | {r}")
        print("-" * 50)

# ─────────────  MENU ACTIONS  ───────────── #

def option1() -> None:
    yr = int(input("\n🔢 Enter a year: "))
    show_calendar(yr)
    matches = matching_years(yr)
    if matches:
        print(f"\n✅ Years that share the same calendar as {yr}: {matches}")
        choice = input(
            "\nEnter one of these years to view its full calendar "
            "(or press Enter to skip): "
        ).strip()
        if choice.isdigit() and int(choice) in matches:
            show_calendar(int(choice))
    else:
        print("❌ No matching calendar years found.")

def option2() -> None:
    y1 = int(input("Enter first year: "))
    y2 = int(input("Enter second year: "))
    compare_calendars(y1, y2)
    verdict = "identical ✅" if same_calendar(y1, y2) else "different ❌"
    print(f"\nResult → Calendars of {y1} and {y2} are {verdict}.")

def option3() -> None:
    yr = int(input("\n🕵️  Enter a year to view CISA incidents: "))
    show_cyber_summary(yr)

# ─────────────  MAIN LOOP  ───────────── #

def main() -> None:
    print("📅 CALENDAR TOOL (CISA cyber data only in Option 3)")
    while True:
        print("\nOptions:")
        print("1 → Show calendar + matching years (plus optional calendar view)")
        print("2 → Compare two calendars (with identical/different verdict)")
        print("3 → Show CISA incidents for a single year")
        print("0 → Exit")
        choice = input("Your choice: ").strip()
        if choice == "1":
            option1()
        elif choice == "2":
            option2()
        elif choice == "3":
            option3()
        elif choice == "0":
            print("👋 Goodbye! Stay secure.")
            break
        else:
            print("❌ Invalid selection. Try again.")

if __name__ == "__main__":
    main()
