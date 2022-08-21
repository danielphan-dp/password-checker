from checkpassword import check_passwords_list
from displayutils import pretty_print_data

with open('.\sample-data\common-passwords.txt', 'r') as file:
    passwords_list = []
    for line in file:
        for word in line.split():
            if len(word) > 0:
                passwords_list.append(word)
    print('Example Passwords')
    print(passwords_list)
    print('Result')
    api_data = check_passwords_list(passwords_list)
    pretty_print_data(api_data)
