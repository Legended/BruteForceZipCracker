from datetime import timedelta
from time import time
import itertools, string
import zipfile


class BruteZip:

    def __init__(self, src='', chars=string.printable.strip(), min_length=1, max_length=None, extract_file=False):
        """This script cracks a zip file via brute force. This is intended for educational purposes only.

        :param src: Path of zip file.
        :param chars: Characters to scan through.
        :param min_length: Minimum length of password.
        :param max_length: Maximum length of password. If 'max_length' is None, the password will be
         scanned for indefinitely.
        :param extract_file: If True, extract the contents of the zip file to the current working directory.
        """

        self.src = src
        self.chars = chars
        self.min_length = min_length
        self.max_length = max_length
        self.extract_file = extract_file

        if self.max_length is not None:
            if self.min_length > self.max_length:
                raise ValueError("'min_length' cannot be greater than 'max_length'")

    def crack_zip(self):
        """Iterates through each possible combination and prints the results of each scan."""

        start = time()
        count = 1
        minimum = self.min_length
        filename = self.get_smallest_file_from_zip()

        with zipfile.ZipFile(self.src, 'r') as zf:
            while True:
                self.check_max_length()
                for pwd in itertools.product(self.chars, repeat=self.min_length):
                    try:
                        zf.read(filename, pwd=bytes(''.join(pwd), encoding='utf-8'))
                        self.success_message(count, minimum, pwd, start)
                        self.unzip(''.join(pwd))
                        return
                    except (RuntimeError, zipfile.BadZipFile):
                        print(f"[{count}] [-] Password Failed: {''.join(pwd)} | "
                              f"Elapsed Time: {timedelta(seconds=time() - start)}")
                        count += 1
                self.min_length += 1

    def unzip(self, pwd):
        """Extracts the contents of the zip file to the current working directory if 'extract_file' is True."""
        if self.extract_file:
            with zipfile.ZipFile(self.src, 'r') as zf:
                zf.extractall(pwd=bytes(pwd, encoding='utf-8'))

    def get_smallest_file_from_zip(self):
        """Returns the name of the smallest file from the zip file."""
        with zipfile.ZipFile(self.src, 'r') as zf:
            return sorted(zip([f.filename for f in zf.infolist()],
                              [f.file_size for f in zf.infolist()]), key=lambda x: x[1])[0][0]

    def check_max_length(self):
        """Checks to see if the scan has reached 'max_length'. If 'max_length' has been reached then the password
        exceeds'max_length' and/or the password contains characters not defined in 'chars'."""

        if self.max_length is not None and self.min_length == self.max_length + 1:
            input('Scan exceeded max length. Press ENTER to exit...')
            raise SystemExit

    def total_combinations(self, minimum):
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
            fmt = f"\n+{'-'*88}+\n|{{:^88}}|\n|{{:^88}}|\n|{{:^88}}|\n+{'-'*88}+"
            return print(fmt.format(
                "[+] Password Found!",
                f"Attempts: {count} / {self.total_combinations(minimum)}",
                f"Password: {''.join(pwd)} | Elapsed Time: {timedelta(seconds=time() - start)}"))
        fmt = f"\n+{'-' * 88}+\n|{{:^88}}|\n|{{:^88}}|\n+{'-' * 88}+"
        return print(fmt.format(
            "[+] Password Found!",
            f"Attempts: {count} | Password: {''.join(pwd)} | Elapsed Time: {timedelta(seconds=time() - start)}"))


if __name__ == '__main__':
    BruteZip('Lock.zip', chars=string.ascii_lowercase, min_length=1, max_length=8, extract_file=True).crack_zip()
