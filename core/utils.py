import math
from decimal import Decimal
from typing import List

test_data = '17,19,29,44,27,19,34,28,14,35,52,40,59,30,40,15,43,52,43,45,15,32,15,33,38,29,33,18,17,29,27,20,21,18,' \
            '48,22,15,24,38,28,23,22,23,17,29,30,16,16,22,15,21,15,21,30,34,17,19,17,34,15,16,18,18,29,34,22,20,19,' \
            '16,17,20,15,17,19,38,32,29,18,14,25,24,21,16,16,24,21,46,20,45,20,42,68,16,26,20,55,55,42,20,47,38,53,' \
            '17,51,22,21,16,21,34,20,18,18,20,22,17,37,34,15,28,15,28,16,19,25,15,17,16,15,16,15,19,23,20,16,17,18,' \
            '17,16,16,21,19,15,31,31,17,32,18,54,16,18,31,36,21,18,30,15,15,15,21,16,18,30,33,15,17,30,20,33,18,23,' \
            '38,25,46,18,23,17,60,18,20,24,47,48,39,17,15,18,18,23,22,25,20,23,18,16,16,15,19,33,15,18,16,18,21,16,' \
            '15,15,19,37,43,16,18,16,16,16,16'


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
        self.average = Decimal(0)
        self.data.sort()

    @property
    def fi(self):
        return Decimal(len(self.data))

    @property
    def Fi(self):
        result = self.fi
        for other_class in self.above_classes:
            result += other_class.fi
        return result

    @property
    def fri(self):
        return round(self.fi / Decimal(len(self.complete_data)), 3)

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
        return self.fri * Decimal(100)

    @property
    def ang(self):
        return round(360 * self.Fri, 2)

    @property
    def Xifi(self):
        return round(self.Xi * self.fi, 1)

    @property
    def Xi_minus_total_arithmetic_average(self):
        return round(abs(self.Xi - self.average), 3)

    @property
    def Xi_minus_total_arithmetic_average_fi(self):
        return self.Xi_minus_total_arithmetic_average * self.fi

    @property
    def name(self):
        if self.max == self.max_range:
            return '{} |-| {}'.format(self.min_range, self.max_range)
        else:
            return '{} |- {}'.format(self.min_range, self.max_range)

    @property
    def data_rep(self):
        return '{{{}}}'.format(', '.join(str(i) for i in self.data))

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __repr__(self):
        return 'class: {} -> {}'.format(self.name, self.data_rep)

    def __str__(self):
        return 'class: {} -> {}'.format(self.name, self.data_rep)


class GroupedData(object):
    def __init__(self):
        self._data: List[StatisticClass] = []

    def append(self, value):
        self._data.append(value)

    def copy(self):
        return self._data.copy()

    def index(self, value):
        return self._data.index(value)

    def average(self):
        sum_xifi = 0
        sum_fi = 0
        for c in self._data:
            sum_xifi += c.Xifi
            sum_fi += c.fi
        return round(sum_xifi / sum_fi, 3)

    def median_class(self):
        above_middle = None
        if len(self._data) == 0:
            return None
        half = Decimal(len(self._data[0].complete_data) / 2)
        for x in self._data:
            if x.Fi > half:
                above_middle = x
                break
        return above_middle

    def median(self):
        above_middle = self.median_class()
        if above_middle is None:
            return None
        half = Decimal(len(self._data[0].complete_data) / 2)
        i = self._data.index(above_middle)
        i_minus_1 = self._data[i - 1]
        li = Decimal(above_middle.min)
        return round(li + ((half - i_minus_1.Fi) / above_middle.fi) * above_middle.amplitude, 3)

    def modal_class(self):
        mc = None
        avrg = self.average()
        for c in self._data:
            if c.min_range <= avrg < c.max_range:
                mc = c
                break
        return mc

    def mode(self):
        mc = self.modal_class()
        if mc is None:
            return mc
        i = self._data.index(mc)
        i_minus_1 = self._data[i - 1]
        i_plus_1 = self._data[i + 1]
        li = Decimal(mc.min)
        d1 = Decimal(mc.fi) - Decimal(i_minus_1.fi)
        d2 = Decimal(mc.fi) - Decimal(i_plus_1.fi)
        return round(li + (d1 / (d1 + d2)) * Decimal(mc.amplitude), 3)

    def update_data(self):
        avrg = self.average()
        for c in self._data:
            c.average = avrg

    def variance(self):
        if len(self._data) == 0:
            return None
        result = 0
        avrg = self.average()
        for i in self._data[0].complete_data:
            result += (i - avrg) ** 2
        return round(result / Decimal(len(self._data[0].complete_data) - 1), 3)

    def standard_deviation(self):
        return round(math.sqrt(self.variance()), 3)

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __iter__(self):
        return self._data.__iter__()


def create_class_from_bytes(data_bytes):
    result = GroupedData()
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
    result.update_data()
    return result
