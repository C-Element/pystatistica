import math


class StatisticClass(object):
    def __init__(self, min_range, max_range, data, complete_data, above_classes):
        if not isinstance(min_range, int):
            raise TypeError('"min_range" value need be int.')
        if not isinstance(max_range, int):
            raise TypeError('"max_range" value need be int.')
        if not isinstance(data, list):
            raise TypeError('"data" value need be list.')
        if not isinstance(complete_data, tuple):
            raise TypeError('"complete_data" value need be tuple.')
        if not isinstance(above_classes, list):
            raise TypeError('"above_classes" value need be list.')
        self.above_classes = above_classes
        self.data = data
        self.complete_data = complete_data
        self.min = min(data)
        self.min_range = min_range
        self.max = max(data)
        self.max_range = max_range
        self.data.sort()

    @property
    def fi(self):
        return len(self.data)

    @property
    def Fi(self):
        result = self.fi
        for other_class in self.above_classes:
            result += other_class.fi
        return result

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
    complete_data = tuple(data.copy())
    actual = data[0]
    while len(data) != 0:
        this_data = []
        while actual < max_actual and len(data) > 0:
            this_data.append(data.pop(0))
            if len(data) > 0:
                actual = data[0]
        result.append(StatisticClass(min_actual, max_actual, this_data, complete_data, result.copy()))
        min_actual = max_actual
        max_actual += amplitude

    return result
