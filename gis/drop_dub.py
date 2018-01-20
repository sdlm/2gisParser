#!/usr/bin/env python
import json
from optparse import OptionParser


def remove_duplicates(filename):
    with open(filename) as file:
        data = json.loads(file.read())
    data_set = {'{name}#{address}'.format(name=item['name'], address=item['address']) for item in data}
    names_and_sddresses = [tuple(line.split('#')) for line in data_set]
    rez = []
    for name, address in names_and_sddresses:
        for org in data:
            if org['name'] == name and org['address'] == address:
                rez.append(org)
                break
    with open(filename, 'w') as file:
        file.write(json.dumps(rez, ensure_ascii=False, indent=4, sort_keys=True))


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename', help='input/output json file', metavar='FILE')

    (options, args) = parser.parse_args()

    file_name = None
    if len(args) > 0:
        remove_duplicates(args[0])
    elif options.filename:
        remove_duplicates(options.filename)
    else:
        print('''Usage: drop_dub.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  input/output file
''')
