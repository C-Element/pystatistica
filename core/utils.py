import math
from decimal import Decimal


class StatisticClass(object):
    def __init__(self, min_range, max_range, data, complete_data, above_classes):
        if not isinstance(min_range, Decimal):
            raise TypeError('"min_range" value need be Decimal.')
        if not isinstance(max_range, Decimal):
            raise TypeError('"max_range" value need be Decimal.')
        if not isinstance(data, list):
            raise TypeError('"data" value need be list.')
        if not isinstance(complete_data, tuple):
            raise TypeError('"complete_data" value need be tuple.')
        if not isinstance(above_classes, list):
            raise TypeError('"above_classes" value need be list.')
        self.above_classes = above_classes
        self.data = data
        self.complete_data = complete_data
        self.min = min(data) if len(data) > 0 else min_range
        self.min_range = min_range
        self.max = max(data) if len(data) > 0 else max_range
        self.max_range = max_range
        self.amplitude = Decimal(self.max_range - self.min_range)
        self.mode = None
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
    def fri(self):
        return round(Decimal(len(self.data)) / Decimal(len(self.complete_data)), 3)

    @property
    def Fri(self):
        result = self.fri
        for other_class in self.above_classes:
            result += other_class.fri
        return round(result, 3)

    @property
    def Xi(self):
        return round((self.amplitude / Decimal(2)) + self.min_range, 3)

    @property
    def perc(self):
        return self.fri * 100

    @property
    def ang(self):
        return round(360 * self.Fri, 2)

    @property
    def Xifi(self):
        return round(self.Xi * self.fi, 1)

    @property
    def total_arithmetic_average(self):
        result = 0
        for i in self.complete_data:
            result += i
        return round(result / Decimal(len(self.complete_data)), 3)

    @property
    def Xi_minus_total_arithmetic_average(self):
        return abs(self.Xi - self.total_arithmetic_average)

    @property
    def Xi_minus_total_arithmetic_average_fi(self):
        return self.Xi_minus_total_arithmetic_average * self.fi

    @property
    def average(self):
        result = 0
        for i in self.data:
            result += i
        return round(result / Decimal(len(self.data)), 3)

    @property
    def variance(self):
        average = self.average
        result = 0
        length = len(self.data)
        for i in self.data:
            result += ((i - average) ** 2 / length)
        return round(result / Decimal(len(self.data)), 3)

    @property
    def default_deviation(self):
        return round(math.sqrt(self.variance), 3)

    @property
    def name(self):
        if self.max == self.max_range:
            return '{} |-| {}'.format(self.min_range, self.max_range)
        else:
            return '{} |- {}'.format(self.min_range, self.max_range)

    @property
    def data_rep(self):
        return '{{{}}}'.format(', '.join(str(i) for i in self.data))

    def get_modal_class(self):
        return sorted(self.above_classes, key=lambda x: x.fi)[-1]

    def __repr__(self):
        return 'class: {} -> {}'.format(self.name, self.data_rep)

    def __str__(self):
        return 'class: {} -> {}'.format(self.name, self.data_rep)


def get_mode(all_classes):
    greatest_fi = sorted(all_classes, key=lambda x: x.fi)[-1]
    i = all_classes.index(greatest_fi)
    i_minus_1 = all_classes[i - 1]
    i_plus_1 = all_classes[i + 1]
    li = Decimal(greatest_fi.min)
    d1 = Decimal(greatest_fi.fi) - Decimal(i_minus_1.fi)
    d2 = Decimal(greatest_fi.fi) - Decimal(i_plus_1.fi)
    return li + (d1 / (d1 + d2)) * Decimal(greatest_fi.amplitude)


def get_median(all_classes):
    above_middle = None
    half = Decimal(len(all_classes[0].complete_data) / 2)
    for x in all_classes:
        if x.Fi > half:
            above_middle = x
            break
    i = all_classes.index(above_middle)
    i_minus_1 = all_classes[i - 1]
    li = Decimal(above_middle.min)
    return li + ((half - Decimal(i_minus_1.Fi)) / Decimal(above_middle.fi)) * Decimal(above_middle.amplitude)


def create_class_from_bytes(data_bytes):
    result = []
    content = (b''.join(data_bytes)).decode()
    content = content.replace('\r\n', '').replace('\n', '').replace(',', ';')
    data = [Decimal(i) for i in content.split(';')]
    items_count = len(data)
    sturges = math.ceil(1 + 3.3 * math.log(items_count, 10))
    min_data = min(data)
    max_data = max(data)
    amplitude = math.ceil((max_data - min_data) / sturges)
    max_actual = min_data + amplitude
    min_actual = min_data
    data.sort()
    complete_data = tuple(data.copy())
    actual = data[0]
    while len(data) != 0:
        this_data = []
        while (actual < max_actual or (actual == max_actual == max_data)) and len(data) > 0:
            this_data.append(data.pop(0))
            if len(data) > 0:
                actual = data[0]
        result.append(StatisticClass(min_actual, max_actual, this_data, complete_data, result.copy()))
        min_actual = max_actual
        max_actual += amplitude
    return result, get_mode(result), get_median(result)
