import hashlib
import requests
import sys


def request_pwned_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + str(query_char)
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}.')
    return response


def get_password_leaks_count(response, private_seq):
    hashes_generator = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes_generator:
        if h == private_seq:
            return count
    return 0


def split_password(password, split_index):
    return password[:split_index], password[split_index:]


def check_password(password):
    password_sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    public_seq, private_seq = split_password(password_sha1, 5)
    response = request_pwned_api_data(public_seq)
    return get_password_leaks_count(response, private_seq)


def check_passwords_list(passwords_list):
    result = []
    for password in passwords_list:
        result.append([password, check_password(password)])
    return result


def pretty_print_data(api_data):
    h0 = 'Password'
    h1 = 'Hacked Count'
    api_data_with_headers = [
        ['-'*len(h0), '-'*len(h1)],
        [h0, h1],
        ['-'*len(h0), '-'*len(h1)]
    ] + api_data + [
        ['-'*len(h0), '-'*len(h1)]
    ]
    s = [[str(e) for e in row] for row in api_data_with_headers]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def main(args):
    api_data = check_passwords_list(args)
    pretty_print_data(api_data)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
