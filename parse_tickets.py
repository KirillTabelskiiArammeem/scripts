import re
from itertools import chain

pattern = re.compile(r'tickets:\[([\d\, ]+)\]')
logs = '''
'''

tickets = pattern.findall(logs)

tickets = [int(item) for item in chain.from_iterable([t.split(',' ) for t in tickets])]