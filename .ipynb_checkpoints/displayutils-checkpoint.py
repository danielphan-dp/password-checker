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
