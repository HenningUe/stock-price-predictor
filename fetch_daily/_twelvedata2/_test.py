import json
import numpy as np

import fetch_daily.twelvedata2
import plot


def test():
    with open("_resources\\sample_return.json", "r") as f:
        content = f.read()
    as_dict = json.loads(content)
    x = 1


if __name__ == "__main__":
    test()
