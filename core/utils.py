import math


class StatisticClass(object):
    def __init__(self, min_range, max_range, data):
        if not isinstance(data, list):
            raise TypeError('"data" value need be list.')
        self.data = data
        self.min = min(data)
        self.min_range = min_range
        self.max = max(data)
        self.max_range = max_range
        self.data.sort()

    @property
    def name(self):
        return '{} |- {}'.format(self.min_range, self.max_range)

    @property
    def data_rep(self):
        return '{{{}}}'.format(', '.join(str(i) for i in self.data))

    def __repr__(self):
        return 'class: {} -> {}'.format(self.name, self.data_rep)

    def __str__(self):
        return 'class: {} -> {}'.format(self.name, self.data_rep)


def create_class_from_bytes(bytes):
    result = []
    content = (b''.join(bytes)).decode()
    content = content.replace('\r\n', '').replace('\n', '')
    data = [int(i) for i in content.split(';')]
    items_count = len(data)
    sturges = round(1 + 3.3 * math.log(items_count, 10))
    min_data = min(data)
    amplitude = math.ceil((max(data) - min_data) / sturges)
    max_actual = min_data + amplitude
    min_actual = min_data
    data.sort()
    actual = data[0]
    while len(data) != 0:
        this_data = []
        while actual < max_actual and len(data) > 0:
            this_data.append(data.pop(0))
            if len(data) > 0:
                actual = data[0]
        result.append(StatisticClass(min_actual, max_actual, this_data))
        min_actual = max_actual
        max_actual += amplitude
    return result
