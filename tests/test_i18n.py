# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)

import i18n  # noqa: E402


def test_catalog_aligned():
    assert set(i18n.FA) == set(i18n.EN)
    assert len(i18n.FA) >= 80


def test_default_fa():
    assert i18n.norm_lang(None) == "fa"
    assert i18n.norm_lang("") == "fa"
    assert i18n.norm_lang("fa-IR") == "fa"
    assert i18n.norm_lang("en-US") == "en"


def test_t_switches():
    fa = i18n.t("fa", "btn.home")
    en = i18n.t("en", "btn.home")
    assert fa != en
    assert "Home" in en or "home" in en.lower()


def test_wait_first_class():
    assert i18n.t("en", "txt.wait") == "WAIT"
    assert i18n.t("fa", "txt.wait") == u"صبر"


def test_no_guaranteed_profit_en():
    blob = " ".join(i18n.EN.values()).lower()
    assert "90% win" not in blob
    assert "sure profit" not in blob
    assert "no guaranteed profit" in blob


def test_lessons_en_complete():
    for i in range(1, 27):
        key = "edu_%s" % i
        title = i18n.edu_title("en", key, "")
        html = i18n.edu_html("en", key, "")
        assert title, key
        assert html, key


if __name__ == "__main__":
    for fn in (
        test_catalog_aligned,
        test_default_fa,
        test_t_switches,
        test_wait_first_class,
        test_no_guaranteed_profit_en,
        test_lessons_en_complete,
    ):
        fn()
        print("ok", fn.__name__)
    print("i18n ok")
