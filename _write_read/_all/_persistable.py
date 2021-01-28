
import pathlib
import json

from ._main import FileNFolderProvider


def persist(symbol, data):
    WriteReadHandler(symbol).write(data)


def load(symbol):
    data = WriteReadHandler(symbol).read()
    return data


def data_exists(symbol):
    return WriteReadHandler(symbol).data_exists()


class WriteReadHandler:

    def __init__(self, symbol):
        self.symbol = symbol
        self._fnf_provider = FileNFolderProvider(symbol, "all_in_one")

    def write(self, data):
        fp = self._get_filepath()
        with fp.open(mode='w') as f:
            json.dump(data, f)

    def read(self):
        fp = self._get_filepath()
        with fp.open(mode='r') as f:
            data = json.load(f)
        return data

    def data_exists(self):
        return self._get_filepath().is_file()

    def _get_filepath(self):
        p = pathlib.Path(self._fnf_provider.get_folder()).joinpath(f'{self.symbol}_globdata.json')
        return p
