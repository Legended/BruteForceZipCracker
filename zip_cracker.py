#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from time import time
from zipfile import ZipFile, BadZipFile
import itertools, string


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

        if self.max_length is not None and self.min_length > self.max_length:
            min_max_error = f"'min_length' cannot be greater than 'max_length'. " \
                            f"'min_length' should be less than or equal to {self.max_length}."
            raise ValueError(min_max_error)

    def crack_zip(self):
        """Iterates through each possible combination and prints the results of each scan until a password is found."""

        count = 1
        start = time()
        minimum = self.min_length
        filename = self.get_smallest_member()

        with ZipFile(self.src, 'r') as zf:
            while True:
                self.check_max_length(minimum)
                for pwd in itertools.product(self.chars, repeat=minimum):
                    try:
                        zf.read(filename, pwd=bytes(''.join(pwd), encoding='utf-8'))
                        self.success_message(count, ''.join(pwd), start)
                        self.unzip(''.join(pwd))
                        return
                    except (RuntimeError, BadZipFile):
                        self.failed_message(count, ''.join(pwd), start)
                        count += 1
                minimum += 1

    def unzip(self, pwd):
        """Extracts the contents of the zip file to the current working directory if 'extract_file' is True."""

        if self.extract_file:
            with ZipFile(self.src, 'r') as zf:
                print('Extracting zip file...')
                zf.extractall(pwd=bytes(pwd, encoding='utf-8'))
                print('Zip file extracted!')

    def get_smallest_member(self):
        """Returns the name of the smallest file from the zip file."""

        with ZipFile(self.src, 'r') as zf:
            return sorted(zip([f.filename for f in zf.infolist()],
                              [f.file_size for f in zf.infolist()]), key=lambda x: x[1])[0][0]

    def check_max_length(self, minimum):
        """Checks to see if the scan has reached 'max_length'. If 'max_length' has been reached then the password
        exceeds'max_length' and/or the password contains characters not defined in 'chars'."""

        if self.max_length is not None and minimum > self.max_length:
            print(f"Password not found. Password length exceeds {self.max_length} and/or the password contains "
                  f"characters not defined in '{self.chars}'.")
            input('Press ENTER to exit...')
            raise SystemExit

    def total_combinations(self):
        """Calculates the possible amount of combinations it would take to crack a password."""

        exponent = self.min_length
        results = []

        while exponent <= self.max_length:
            results.append(len(self.chars) ** exponent)
            exponent += 1
        return sum(results)

    @staticmethod
    def failed_message(count, pwd, start):
        """Message printed when password has failed."""

        print(f"[{count}] [-] Password Failed: {pwd} | "
              f"Elapsed Time: {timedelta(seconds=time() - start)}")

    def success_message(self, count, pwd, start):
        """Message printed when the password has successfully been cracked."""

        if self.max_length is not None:
            fmt = f"\n+{'-'*88}+\n|{{:^88}}|\n|{{:^88}}|\n|{{:^88}}|\n+{'-'*88}+"
            print(fmt.format("[+] Password Found!",
                             f"Attempts: {count} / {self.total_combinations()}",
                             f"Password: {pwd} | Elapsed Time: {timedelta(seconds=time() - start)}"))
        else:
            fmt = f"\n+{'-'*88}+\n|{{:^88}}|\n|{{:^88}}|\n+{'-'*88}+"
            print(fmt.format("[+] Password Found!",
                             f"Attempts: {count} | Password: {pwd} | "
                             f"Elapsed Time: {timedelta(seconds=time() - start)}"))


if __name__ == '__main__':
    BruteZip('Lock.zip', chars=string.ascii_lowercase, min_length=1, max_length=8).crack_zip()
