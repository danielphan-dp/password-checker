from collections import defaultdict


def split_password(password, split_index):
    return password[:split_index], password[split_index:]


def parse_response_to_dict(response):
    cache = defaultdict(lambda: 0)
    data_generator = (line.split(':') for line in response.text.splitlines())
    for _hash, hacked_count in data_generator:
        cache[_hash] = hacked_count
    return cache
