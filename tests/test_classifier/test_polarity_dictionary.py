"""
テスト: polarity_dictionary モジュール

検証項目：
  1. ダミーのテキストファイルを読み込ませ、先頭と末尾の要素が正しくパースされ、
     辞書が構築されること
  2. get_polarity メソッドに登録済みの単語を与えた際に正しい極性が返却されること
  3. 未登録の単語、および空文字 "" を与えた際に、例外なく None が返却されること
"""

import os
import tempfile

from src.my_library.classifier.polarity_dictionary import (
    PolarityDictionary
)


def test_polarity_dictionary_initialization():
    """
    ダミーファイルを読み込んで辞書が構築されること
    """

    with tempfile.TemporaryDirectory() as tmpdir:

        dict_file = os.path.join(
            tmpdir,
            "dictionary1.txt"
        )

        with open(
            dict_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "良い\t~である\tp\n"
            )

            f.write(
                "悪い\t~である\tn\n"
            )

            f.write(
                "普通\t~である\te\n"
            )

        dictionary = PolarityDictionary(
            tmpdir
        )

        assert (
            dictionary.get_polarity(
                "良い"
            )
            == "p"
        )

        assert (
            dictionary.get_polarity(
                "悪い"
            )
            == "n"
        )

        assert (
            dictionary.get_polarity(
                "普通"
            )
            == "e"
        )


def test_get_polarity_registered_word():

    with tempfile.TemporaryDirectory() as tmpdir:

        dict_file = os.path.join(
            tmpdir,
            "dictionary1.txt"
        )

        with open(
            dict_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "嬉しい\t~である\tp\n"
            )

            f.write(
                "悲しい\t~である\tn\n"
            )

        dictionary = PolarityDictionary(
            tmpdir
        )

        assert (
            dictionary.get_polarity(
                "嬉しい"
            )
            == "p"
        )

        assert (
            dictionary.get_polarity(
                "悲しい"
            )
            == "n"
        )


def test_get_polarity_unknown_word():

    with tempfile.TemporaryDirectory() as tmpdir:

        dict_file = os.path.join(
            tmpdir,
            "dictionary1.txt"
        )

        with open(
            dict_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "良い\t~である\tp\n"
            )

        dictionary = PolarityDictionary(
            tmpdir
        )

        assert (
            dictionary.get_polarity(
                "存在しない単語"
            )
            is None
        )


def test_get_polarity_empty_string():

    with tempfile.TemporaryDirectory() as tmpdir:

        dict_file = os.path.join(
            tmpdir,
            "dictionary1.txt"
        )

        with open(
            dict_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "良い\t~である\tp\n"
            )

        dictionary = PolarityDictionary(
            tmpdir
        )

        assert (
            dictionary.get_polarity("")
            is None
        )


def test_polarity_dictionary_with_both_dictionaries():

    with tempfile.TemporaryDirectory() as tmpdir:

        dict1_file = os.path.join(
            tmpdir,
            "dictionary1.txt"
        )

        with open(
            dict1_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "良い\t~である\tp\n"
            )

            f.write(
                "楽しい\t~である\tp\n"
            )

        dict2_file = os.path.join(
            tmpdir,
            "dictionary2.txt"
        )

        with open(
            dict2_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "悪い\t~である\tn\n"
            )

            f.write(
                "つまらない\t~である\tn\n"
            )

        dictionary = PolarityDictionary(
            tmpdir
        )

        assert (
            dictionary.get_polarity(
                "良い"
            )
            == "p"
        )

        assert (
            dictionary.get_polarity(
                "楽しい"
            )
            == "p"
        )

        assert (
            dictionary.get_polarity(
                "悪い"
            )
            == "n"
        )

        assert (
            dictionary.get_polarity(
                "つまらない"
            )
            == "n"
        )


def test_polarity_dictionary_parse_format():

    with tempfile.TemporaryDirectory() as tmpdir:

        dict_file = os.path.join(
            tmpdir,
            "dictionary1.txt"
        )

        with open(
            dict_file,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "二度寝\t~する(行為)\t客観\t12345678910\tn\n"
            )

            f.write(
                "賑やか\t~である・になる(評価・感情)\t主観\tp\n"
            )

        dictionary = PolarityDictionary(
            tmpdir
        )

        assert (
            dictionary.get_polarity(
                "二度寝"
            )
            == "n"
        )

        assert (
            dictionary.get_polarity(
                "賑やか"
            )
            == "p"
        )