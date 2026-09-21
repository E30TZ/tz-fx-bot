# -*- coding: utf-8 -*-
from __future__ import print_function

import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WALLETS = [
    ("TRX", "TRON", "TF4TbyEu1eC1sYTW1oviBbmPKT1KkxViba"),
    ("TON", "TON", "UQDKUFjOEWXcyjOE459jWbniQRtdNYN1taRRn1XhdA8KKiqT"),
    ("USDT", "TRC20", "TF4TbyEu1eC1sYTW1oviBbmPKT1KkxViba"),
    ("USDT", "BEP20", "0x258380877EC849e04082C4A6795d01432c3F4B7B"),
]


def test_readme_wallets():
    text = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    support = open(os.path.join(HERE, "docs", "SUPPORT.md"), encoding="utf-8").read()
    for asset, net, addr in WALLETS:
        assert addr in text, addr
        assert addr in support, addr
        assert ("%s — %s" % (asset, net)) in text or ("%s — %s" % (asset, net)) in support
    assert "0xDEAD" not in text
    assert "TXXXXXXXX" not in text
    assert "guaranteed return" not in text.lower()
    assert "earn profit" not in text.lower()


def test_qr_files():
    d = os.path.join(HERE, "docs", "donations")
    for name in ("trx-tron.png", "ton-ton.png", "usdt-trc20.png", "usdt-bep20.png"):
        p = os.path.join(d, name)
        assert os.path.isfile(p), name
        assert os.path.getsize(p) > 200, name


if __name__ == "__main__":
    test_readme_wallets()
    test_qr_files()
    print("donations ok")
