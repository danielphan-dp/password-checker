from cgitb import lookup
import hashlib
import requests
import sys

from displayutils import pretty_print_data
from parsingutils import split_password, parse_response_to_dict

BASE_URL = 'https://api.pwnedpasswords.com/range/'


def request_api_data(public_seq: str):
    # get server's response about the password
    url = BASE_URL + public_seq
    response = None
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    # error(s) happened
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}.')

    # successfully processing the password
    return response


def check_password(password):
    # perform SHA1 hash on password
    password_sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    # convert to upper-case as the API requires a sequence upper-case characters
    password_sha1 = password_sha1.upper()

    # k-anonymity
    public_seq, private_seq = split_password(password_sha1, 5)
    response = request_api_data(public_seq)
    cache = parse_response_to_dict(response)
    return cache[private_seq]


def check_passwords_list(passwords_list):
    result = []
    for password in passwords_list:
        result.append([password, check_password(password)])
    return result


def main(args):
    api_data = check_passwords_list(args)
    pretty_print_data(api_data)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
