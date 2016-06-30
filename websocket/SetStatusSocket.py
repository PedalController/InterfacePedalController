# -*- coding: utf-8 -*-
from tornado import websocket

from websocket.AbstractSocketHandler import AbstractSocketHandler


class SetStatusSocket(AbstractSocketHandler):

    def putBank(self, bank):
        self.send({"bank": bank})
