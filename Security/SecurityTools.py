import random
import hashlib

SALT_LEN = 10
ALL_CHARS = ['a',
            'b',
            'c',
            'd',
            'e',
            'f',
            'g',
            'h',
            'i',
            'j',
            'k',
            'l',
            'm',
            'n',
            'o',
            'p',
            'q',
            'r',
            's',
            't',
            'u',
            'v',
            'w',
            'x',
            'y',
            'z',
            'A',
            'B',
            'C',
            'D',
            'E',
            'F',
            'G',
            'H',
            'I',
            'J',
            'K',
            'L',
            'M',
            'N',
            'O',
            'P',
            'Q',
            'R',
            'S',
            'T',
            'U',
            'V',
            'W',
            'X',
            'Y',
            'Z',
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '!',
            '@',
            '#',
            '$',
            '%',
            '&',
            '*',
            '(',
            ')',
            '-',
            '_',
            '+',
            '=',
            '[',
            ']',
            '{',
            '}',
            '|',
            '\\',
            ';',
            ':',
            "'",
            '"',
            ',',
            '.',
            '<',
            '>',
            '/',
            '?'
        ]

def genrate_salt():
    """
    Generates a salt {SALT_LEN} charecters long
    Returns:
        salt: str -  {SALT_LEN} charecters long str
    """
    return "".join([random.choice(ALL_CHARS) for char in range(SALT_LEN)]) 

def hash_str(str_to_hash: str) -> str:
    """
    Hashes a string in sha256 format
    Args:
        str_to_hash: (str) - string you want to hash
    Returns:
        hashed_str: (str) - hashed string 
    """
    return hashlib.sha256(str_to_hash.encode()).hexdigest()
