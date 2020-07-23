import getpass
import hashlib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

URL = "https://api.pwnedpasswords.com/range/"


def main():
    pswd = getpass.getpass()
    pswd_hash = hashlib.sha1(bytes(pswd, encoding="utf-8")).hexdigest().upper()
    first_five = pswd_hash[:5]

    try:
        response = urlopen(Request(f"{URL}{first_five}"))
    except HTTPError as e:
        print(e.code)
    except URLError as e:
        print(e.reason)
    else:
        content = response.read().decode("utf-8")

    hashes = content.split("\r\n")

    hash_dict = {}
    for line in hashes:
        h, q = line.split(":")
        hash_dict[f"{first_five}{h}"] = q

    if pswd_hash in hash_dict:
        print(f"Password appears in leaked databases {hash_dict[pswd_hash]} times")
    else:
        print("Password has not been leaked so far.")


if __name__ == "__main__":
    main()
