from typing import Sequence
import argparse


def check_file_for_custom_write(
        filenames: Sequence[str],
        keys: set[bytes],
) -> bool:
    """Check if files contain AWS secrets.
    Return a list of all files containing AWS secrets and keys found, with all
    but the first four characters obfuscated to ease debugging.
    """

    for filename in filenames:
        with open(filename, 'rb') as content:
            text_body = content.read()
            for key in keys:
                # naively match the entire file, low chance of incorrect
                # collision
                if key in text_body:
                    return True
    return False


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='+', help='Filenames to run')


    args = parser.parse_args(argv)
    keys = {
        "write."
    }
    keys_b = {key.encode() for key in keys}
    exist_custom_write = check_file_for_custom_write(args.filenames, keys_b)
    if not exist_custom_write:
        return 0
    return 2


if __name__ == '__main__':
    raise SystemExit(main())