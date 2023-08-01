import re
import pandas

spaces = re.compile(r'\s+')
numbers = re.compile(r'\d+')
device_regex = re.compile(r'(\d+\,?\d+)|([0x]+)')
type_regex = re.compile(r'([A-Z]+)|(unknown)|(unix)')
size_of_regex = re.compile(r'(\d+)|(0t0)')

data = []
with open('lsof_good.txt') as file:
    lines = iter(file)
    head: str = next(lines)

    name_start = head.find('NAME')


    for i, line in enumerate(lines):
        line = line.strip()
        name = line[name_start:].strip()
        line = line[:name_start].strip()
        line = [item.strip() for item in spaces.split(line)]
        command = line[0]
        pid = line[1]
        line_2 = line[2]
        tid = line_2 if numbers.match(line_2) else None

        user_column = 3 if tid else 2
        user = line[user_column]

        fd_column = user_column + 1
        fd = line[fd_column]

        type_column = fd_column + 1
        if len(line) >= type_column + 1:
            type_ = line[type_column]
            if type_regex.match(type_):
                pass
            else:
                device = None
                type_column -= 1
        else:
            device = None

        device_column = type_column + 1
        if len(line) >= device_column + 1:
            device = line[device_column]
            if device_regex.match(device):
                pass
            else:
                device = None
                device_column -= 1
        else:
            device = None

        size_of_column = device_column + 1
        if len(line) >= size_of_column + 1:
            size_of = line[size_of_column]
            if size_of_regex.match(size_of):
                pass
            else:
                size_of = None
                size_of_column -= 1
        else:
            size_of = None

        node_column = 1
        if len(line) >= size_of_column + 1:
            node = line[node_column]
        else:
            node = None

        data.append(
            {
                'command': command, 'pid': pid, 'tid': tid, 'user': user, 'fd': fd, 'type': type_, 'device': device,
                'size_of': size_of, 'node': node, 'name': name
             }
        )


data = pandas.DataFrame(
    data=data, columns=['command', 'pid', 'tid', 'user', 'fd', 'type', 'device', 'size_of', 'node', 'name']
)


data.to_csv('data_good.csv')
print(data)



