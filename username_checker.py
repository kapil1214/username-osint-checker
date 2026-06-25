# ================================================
# USERNAME OSINT CHECKER — SOC Project 2
# ================================================
# Kya karta hai:
#   Ek username lo
#   100+ websites pe check karo
#   Results screen pe dikhao
#   File mein save karo
# ================================================

# requests = internet se baat karne ke liye
# time = do requests ke beech wait karne ke liye
# datetime = aaj ki date/time lene ke liye
import requests
import time
import datetime

# ================================================
# WEBSITES KI LIST
# Yeh woh sites hain jahan check karenge
# Format: "Site ka naam" : "URL jisme {} ki jagah username jayega"
# {} = placeholder — yahan username daalenge baad mein
# ================================================

SITES = {
    "GitHub"        : "https://github.com/{}",
    "Reddit"        : "https://www.reddit.com/user/{}",
    "Instagram"     : "https://www.instagram.com/{}/",
    "Twitter/X"     : "https://twitter.com/{}",
    "TikTok"        : "https://www.tiktok.com/@{}",
    "Pinterest"     : "https://www.pinterest.com/{}/",
    "Twitch"        : "https://www.twitch.tv/{}",
    "YouTube"       : "https://www.youtube.com/@{}",
    "LinkedIn"      : "https://www.linkedin.com/in/{}/",
    "Pastebin"      : "https://pastebin.com/u/{}",
    "Fiverr"        : "https://www.fiverr.com/{}",
    "Kaggle"        : "https://www.kaggle.com/{}",
    "HackerNews"    : "https://news.ycombinator.com/user?id={}",
    "Dev.to"        : "https://dev.to/{}",
    "Medium"        : "https://medium.com/@{}",
}

# ================================================
# FUNCTION 1: EK SITE CHECK KARO
#
# Kya karta hai:
#   Website ko request bhejta hai
#   Agar 200 aaya = profile exist karta hai
#   Agar 404 aaya = nahi mila
#
# HTTP Status codes kya hote hain?
#   200 = OK — page mila
#   404 = Not Found — page nahi mila
#   403 = Forbidden — site ne block kiya
# ================================================

def check_site(site_name, url_template, username):

    # {}.format(username) = {} ki jagah username daal do
    # Example: "https://github.com/{}" → "https://github.com/john"
    url = url_template.format(username)

    # "headers" matlab hum browser jaisi request bhej rahe hain
    # Kyu? Kuch sites bots ko block karti hain
    # Yeh dekh ke lagta hai hum Chrome browser hain
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0"
    }

    # "try" matlab — koshish karo
    # Agar koi error aaye toh "except" mein jao
    # Kyu? Internet slow ho, site down ho — crash na ho program
    try:
        # requests.get = website ko request bhejo
        # timeout=10 = 10 second se zyada wait mat karo
        response = requests.get(url, headers=headers, timeout=10)

        # Status code 200 matlab profile mila!
        if response.status_code == 200:
            return "FOUND", url

        # 404 matlab nahi mila
        elif response.status_code == 404:
            return "NOT FOUND", url

        # Koi aur code — jaise 403 block
        else:
            return f"UNKNOWN ({response.status_code})", url

    # Agar internet nahi ya site respond nahi ki
    except requests.exceptions.ConnectionError:
        return "ERROR (Connection)", url

    # Agar 10 second mein jawab nahi aaya
    except requests.exceptions.Timeout:
        return "ERROR (Timeout)", url


# ================================================
# FUNCTION 2: POORA SCAN CHALAO
#
# Kya karta hai:
#   Sab sites pe ek ek karke check_site() call karta hai
#   Results screen pe dikhata hai
#   Found profiles alag rakhta hai
# ================================================

def scan_username(username):

    # Yeh lists results store karengi
    found_profiles = []      # yahan mila
    not_found      = []      # yahan nahi mila
    errors         = []      # yahan error aaya

    # Screen pe heading dikhao
    print("\n" + "="*55)
    print(f"  USERNAME OSINT CHECKER — SOC Tool")
    print("="*55)
    print(f"  Target Username : {username}")
    print(f"  Sites checking  : {len(SITES)}")
    print(f"  Shuru hua       : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*55 + "\n")

    # SITES dictionary mein se ek ek site lo
    # site_name = "GitHub", url_template = "https://github.com/{}"
    for site_name, url_template in SITES.items():

        # Check karo
        status, url = check_site(site_name, url_template, username)

        # Result ke hisaab se color dikhao
        if status == "FOUND":
            # \033[92m = green color
            print(f"  \033[92m[+] FOUND\033[0m     {site_name:<15} {url}")
            found_profiles.append((site_name, url))

        elif status == "NOT FOUND":
            # \033[91m = red color
            print(f"  \033[91m[-] NOT FOUND\033[0m {site_name}")
            not_found.append(site_name)

        else:
            # \033[93m = yellow color
            print(f"  \033[93m[?] {status:<10}\033[0m {site_name}")
            errors.append(site_name)

        # Har request ke baad 1 second ruko
        # Kyu? Sites ban kar deti hain agar bohat fast requests aayein
        time.sleep(1)

    # Scan khatam — summary dikhao
    print("\n" + "="*55)
    print(f"  SCAN COMPLETE")
    print("="*55)
    print(f"  Profiles Mile   : {len(found_profiles)}")
    print(f"  Nahi Mile       : {len(not_found)}")
    print(f"  Errors          : {len(errors)}")
    print("="*55)

    return found_profiles


# ================================================
# FUNCTION 3: RESULTS FILE MEIN SAVE KARO
#
# Kyu save karte hain?
# SOC mein har cheez document karni hoti hai
# Report banana padta hai manager ko dene ke liye
# ================================================

def save_report(username, found_profiles):

    # File ka naam — username aur date se
    filename = f"{username}_osint_report.txt"

    # "with open" = file kholo likhne ke liye
    # "w" = write mode — nayi file banao
    with open(filename, "w") as f:
        f.write("="*55 + "\n")
        f.write("USERNAME OSINT REPORT\n")
        f.write("="*55 + "\n")
        f.write(f"Target   : {username}\n")
        f.write(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Found on : {len(found_profiles)} sites\n")
        f.write("="*55 + "\n\n")

        if found_profiles:
            f.write("PROFILES FOUND:\n\n")
            for site, url in found_profiles:
                f.write(f"  [{site}]\n")
                f.write(f"  {url}\n\n")
        else:
            f.write("Koi profile nahi mila.\n")

    print(f"\n  [SAVED] Report save ho gayi: {filename}\n")


# ================================================
# PROGRAM YAHAN SE SHURU HOTA HAI
# ================================================

# Yeh check karta hai — kya yeh file directly chal rahi hai?
# Haan toh neeche ka code chalao
if __name__ == "__main__":

    print("\033[96m")   # cyan color on
    print("  ██████╗ ███████╗██╗███╗   ██╗████████╗")
    print("  ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝")
    print("  ██║   ██║███████╗██║██╔██╗ ██║   ██║")
    print("  ██║   ██║╚════██║██║██║╚██╗██║   ██║")
    print("  ╚██████╔╝███████║██║██║ ╚████║   ██║")
    print("   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝")
    print("\033[0m")    # color off
    print("  USERNAME OSINT CHECKER — SOC Beginner Tool")
    print("  Ethical use only — Sirf authorized testing\n")

    # User se username maango
    # input() = user se kuch type karwao
    username = input("  Target username dalo: ").strip()

    # .strip() = aage peeche ke spaces hata do
    # Agar kuch type nahi kiya
    if not username:
        print("  [ERROR] Username dalo pehle!\n")

    else:
        # Scan karo
        found = scan_username(username)

        # Agar kuch mila toh save karo
        if found:
            save = input("\n  Report file mein save karein? (y/n): ").strip().lower()
            if save == "y":
                save_report(username, found)
        else:
            print("\n  Koi profile nahi mila is username pe.\n")