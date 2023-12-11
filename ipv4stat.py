import os

BASEDIR = '/proc/sys/net/ipv4'


def read_file(filename: str):
    try:
        with open(filename) as f:
            yield filename, f.read().strip()
    except Exception as e:
        yield filename, str(e)


def get_stat(folder: str):

    entries = os.listdir(folder)
    for entry in entries:
        entry = os.path.join(folder, entry)
        if os.path.isdir(entry):
            for item in get_stat(entry):
                yield item
        else:
            yield from read_file(entry)


for item in get_stat(BASEDIR):
    print(f'{item[0]},{item[1]}')