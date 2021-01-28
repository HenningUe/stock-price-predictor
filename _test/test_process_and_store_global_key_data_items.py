
import _init  # @UnresolvedImport @UnusedImport

import _write_read


def main():
    _write_read.all_in_one.process_and_store_global_key_data_items(symbol="SPY")
    data = _write_read.all_in_one.read_global_key_data_items(symbol="SPY")
    print(data)


main()
