from itertools import izip_longest

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

n = 100

with open('trips.csv') as f:
    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
        with open('trips_{0}.csv'.format(i), 'w') as fout:
            fout.writelines(g)