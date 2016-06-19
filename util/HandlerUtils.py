# -*- coding: utf-8 -*-


class HandlerUtils(object):
    @staticmethod
    def toInt(*params):
        data = []
        for element in params:
            value = int(element) if element is not None else None
            data.append(value)

        return data