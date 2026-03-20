import urllib.request
import json
import re


USERNAME = "razorrtx"



def get_contributions(username: str) -> int:
    try:
       
        url = f"https://github.com/users/{username}/contributions"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8")

        matches = re.findall(r'data-count="(\d+)"', html)
        if matches:
            total = sum(int(x) for x in matches)
            return total
    except Exception as e:
        print(f"[WARN] Tidak bisa fetch contributions: {e}")

   
    print("[INFO] Tidak bisa otomatis. Buka github.com/USERNAME dan lihat angka contributions di profil.")
    manual = input("  Masukkan jumlah contributions kamu: ").strip()
    return int(manual) if manual.isdigit() else 0


def calc_level(contributions: int) -> int:
    """Level naik tiap 200 contributions, maksimal 99."""
    return min(contributions // 200 + 1, 99)


def fill_svg(username: str, contributions: int, level: int):
    """Replace placeholder di pixel-card.svg."""
    with open("pixel-card.svg", "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("%%USERNAME%%",      username)
    content = content.replace("%%CONTRIBUTIONS%%", str(contributions))
    content = content.replace("%%LEVEL%%",         str(level))

    with open("pixel-card.svg", "w", encoding="utf-8") as f:
        f.write(content)


def main():
    print(f"\n=== Pixel Card Setup ===")
    print(f"Username : {USERNAME}")

    print(f"Mengambil data contributions dari GitHub...")
    contributions = get_contributions(USERNAME)
    level = calc_level(contributions)

    print(f"\nHasil:")
    print(f"  Username      : {USERNAME}")
    print(f"  Contributions : {contributions}")
    print(f"  Level         : {level}  (rumus: {contributions} // 200 + 1)")

    fill_svg(USERNAME, contributions, level)

    print(f"\n[OK] pixel-card.svg berhasil diupdate!")
    print(f"     Sekarang upload pixel-card.svg ke repo GitHub kamu.")


if __name__ == "__main__":
    main()
