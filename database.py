import datetime
import qrcode
import hashlib
import io
from typing import Dict


class DataBase:
    times = [f'{x}:00' for x in range(11, 22)]
    times_set = set(times)

    def __init__(self):
        self.__records: Dict[str, Dict[str, Dict[int, Dict[str, str]]]] = dict()
        self.__qr_codes: Dict[str, bytes] = dict()

    def check_can_book(self, date: str, time: str, table: int) -> bool:
        if date not in self.__records.keys():
            return True
        if time not in self.__records[date].keys():
            return True
        return table not in self.__records[date][time].keys()

    def add_record(self, name: str, phone: str, date: str, time: str, table: int, comment: str) -> str:
        year, month, day = map(int, date.split('-'))
        hour, minute = map(int, time.split(':'))
        if datetime.datetime(year, month, day, hour, minute) < datetime.datetime.now():
            raise ValueError()
        if date not in self.__records.keys():
            self.__records[date] = dict()
        if time not in self.__records[date].keys():
            self.__records[date][time] = dict()

        if not (1 <= table <= 5):
            raise ValueError()

        phone = phone.replace('+', '').replace('(', '').replace(')', '')\
            .replace('-', '').replace(' ', '')
        if len(phone) != 11:
            raise ValueError()

        self.__records[date][time][table] = {
            'name': name,
            'phone': phone,
            'comment': comment,
        }

        data = f'Name: {name}\nPhone: {phone}\nTable: {table}\nComment: {comment}'.encode()
        uuid = hashlib.sha1(data).hexdigest()
        img_byte_arr = io.BytesIO()
        qrcode.make(data).save(img_byte_arr, format='PNG')
        self.__qr_codes[uuid] = img_byte_arr.getvalue()

        return uuid

    def get_qr_code(self, uuid: str) -> bytes:
        if uuid not in self.__qr_codes.keys():
            raise ValueError()
        return self.__qr_codes[uuid]
