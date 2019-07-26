from datetime import timedelta
from time import time
import itertools, string
import zipfile, zlib


class BruteZip:

    def __init__(self, src='', chars=string.printable.strip(), min_length=1, max_length=None):
        """This script cracks a zip file via brute force. This is intended for educational purposes only.

        :param src: Path of zip file.
        :param chars: Character to scan for.
        :param min_length: Minimum length of password.
        :param max_length: Maximum length of password
        """
        
        self.src = src
        self.chars = chars
        self.min_length = min_length
        self.max_length = max_length

    def crack_zip(self):
        """Iterates through each possible combination and prints the results of each scan."""
        
        start = time()
        count = 1
        minimum = self.min_length
        with zipfile.ZipFile(self.src, 'r') as zf:
            while True:
                self.check_length_queries()
                for pwd in itertools.product(self.chars, repeat=self.min_length):
                    try:
                        zf.extractall(pwd=bytes(''.join(pwd), encoding='utf-8'))
                        return self.success_message(count, minimum, pwd, start)
                    except (RuntimeError, zlib.error, zipfile.BadZipFile):
                        print(f"[{count}] [-] Password Failed: {''.join(pwd)} | "
                              f"Elapsed Time: {timedelta(seconds=time() - start)}")
                        count += 1
                self.min_length += 1

    def check_length_queries(self):
        """Checks the params for 'max_length' and 'min_length'. 'min_length cannot be greater than 'max_length'."""
        
        if self.max_length is not None:
            if self.min_length > self.max_length:
                raise ValueError("'min_length' cannot be greater than 'max_length'")
        if self.max_length is not None and self.min_length == self.max_length + 1:
            input('Scan exceeded max length. Press ENTER to exit...')
            raise SystemExit

    def total_scan_results(self, minimum):
        """Calculates the possible amount of combinations it would take to crack a password."""
        
        exponent = minimum
        results = []
        while exponent <= self.max_length:
            results.append(len(self.chars) ** exponent)
            exponent += 1
        return sum(results)

    def success_message(self, count, minimum, pwd, start):
        """Message printed when the password has successfully been cracked."""
        
        if self.max_length is not None:
            fmt = "\n+{}+\n|{:^88}|\n|{:^88}|\n|{:^88}|\n+{}+"
            return print(fmt.format(
                f"{'-' * 88}",
                "[+] Password Found!",
                f"Attempts: {count} / {self.total_scan_results(minimum)}",
                f"Password: {''.join(pwd)} | Elapsed Time: {timedelta(seconds=time() - start)}",
                '-' * 88))
        fmt = "\n+{}+\n|{:^88}|\n|{:^88}|\n+{}+"
        return print(fmt.format(
            f"{'-' * 88}",
            "[+] Password Found!",
            f"Attempts: {count} | Password: {''.join(pwd)} | Elapsed Time: {timedelta(seconds=time() - start)}",
            '-' * 88))


if __name__ == '__main__':
    BruteZip(r'C:\Users\PC\PycharmProjects\ZipBruteForce\Lock.zip',
             chars=string.ascii_lowercase, min_length=1, max_length=8).crack_zip()
