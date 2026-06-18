"""
テスト: polarity_dictionary モジュール

検証項目：
  1. ダミーのテキストファイルを読み込ませ、先頭と末尾の要素が正しくパースされ、
     辞書が構築されること
  2. get_polarity メソッドに登録済みの単語を与えた際に正しい極性が返却されること
  3. 未登録の単語、および空文字 "" を与えた際に、例外なく None が返却されること
"""

import os
import sys
import tempfile
import pytest

# プロジェクトルートをパスに追加（モジュール検索パス）
project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root_path)

from src.my_library.classifier import PolarityDictionary


def test_polarity_dictionary_initialization():
    """ダミーファイルを読み込んで辞書が構築されること"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # ダミー辞書ファイルを作成
        dict_file = os.path.join(tmpdir, 'dictionary1.txt')
        with open(dict_file, 'w', encoding='utf-8') as f:
            f.write("良い\t~である\tp\n")
            f.write("悪い\t~である\tn\n")
            f.write("普通\t~である\te\n")
        
        # dictionary2.txt は存在しなくても動作する
        dictionary = PolarityDictionary(tmpdir)
        
        # 辞書が正しく読み込まれていることを確認
        assert dictionary.get_polarity('良い') == 'p'
        assert dictionary.get_polarity('悪い') == 'n'
        assert dictionary.get_polarity('普通') == 'e'


def test_get_polarity_registered_word():
    """登録済みの単語を与えた際に正しい極性が返却されること"""
    with tempfile.TemporaryDirectory() as tmpdir:
        dict_file = os.path.join(tmpdir, 'dictionary1.txt')
        with open(dict_file, 'w', encoding='utf-8') as f:
            f.write("嬉しい\t~である\tp\n")
            f.write("悲しい\t~である\tn\n")
        
        dictionary = PolarityDictionary(tmpdir)
        
        assert dictionary.get_polarity('嬉しい') == 'p'
        assert dictionary.get_polarity('悲しい') == 'n'


def test_get_polarity_unregistered_word():
    """未登録の単語を与えた際に None が返却されること"""
    with tempfile.TemporaryDirectory() as tmpdir:
        dict_file = os.path.join(tmpdir, 'dictionary1.txt')
        with open(dict_file, 'w', encoding='utf-8') as f:
            f.write("良い\t~である\tp\n")
        
        dictionary = PolarityDictionary(tmpdir)
        
        assert dictionary.get_polarity('存在しない') is None


def test_get_polarity_empty_string():
    """空文字を与えた際に None が返却されること"""
    with tempfile.TemporaryDirectory() as tmpdir:
        dict_file = os.path.join(tmpdir, 'dictionary1.txt')
        with open(dict_file, 'w', encoding='utf-8') as f:
            f.write("良い\t~である\tp\n")
        
        dictionary = PolarityDictionary(tmpdir)
        
        assert dictionary.get_polarity('') is None


def test_get_polarity_no_exception_on_missing_word():
    """未登録の単語に対してキーエラーが発生しないこと"""
    with tempfile.TemporaryDirectory() as tmpdir:
        dict_file = os.path.join(tmpdir, 'dictionary1.txt')
        with open(dict_file, 'w', encoding='utf-8') as f:
            f.write("良い\t~である\tp\n")
        
        dictionary = PolarityDictionary(tmpdir)
        
        # 例外が発生しないことを確認
        result = dictionary.get_polarity('存在しない')
        assert result is None


def test_polarity_dictionary_with_both_dictionaries():
    """複数の辞書ファイルが正しく統合されること"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # dictionary1.txt
        dict1_file = os.path.join(tmpdir, 'dictionary1.txt')
        with open(dict1_file, 'w', encoding='utf-8') as f:
            f.write("良い\t~である\tp\n")
            f.write("楽しい\t~である\tp\n")
        
        # dictionary2.txt
        dict2_file = os.path.join(tmpdir, 'dictionary2.txt')
        with open(dict2_file, 'w', encoding='utf-8') as f:
            f.write("悪い\t~である\tn\n")
            f.write("つまらない\t~である\tn\n")
        
        dictionary = PolarityDictionary(tmpdir)
        
        # 両方の辞書の単語が検索できる
        assert dictionary.get_polarity('良い') == 'p'
        assert dictionary.get_polarity('楽しい') == 'p'
        assert dictionary.get_polarity('悪い') == 'n'
        assert dictionary.get_polarity('つまらない') == 'n'


def test_polarity_dictionary_parse_format():
    """複雑なフォーマットが正しくパースされること"""
    with tempfile.TemporaryDirectory() as tmpdir:
        dict_file = os.path.join(tmpdir, 'dictionary1.txt')
        with open(dict_file, 'w', encoding='utf-8') as f:
            # 複数のタブと列を含むフォーマット
            f.write("二度寝\t~する(行為)\t客観\t12345678910\tn\n")
            f.write("賑やか\t~である・になる(評価・感情)\t主観\tp\n")
        
        dictionary = PolarityDictionary(tmpdir)
        
        # 先頭と末尾の要素が正しく抽出されていること
        assert dictionary.get_polarity('二度寝') == 'n'
        assert dictionary.get_polarity('賑やか') == 'p'


def test_polarity_dictionary_empty_directory():
    """辞書ファイルがないディレクトリでも動作すること"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # ファイルを作成しない
        dictionary = PolarityDictionary(tmpdir)
        
        # 空の辞書が作成される
        assert dictionary.get_polarity('任意の単語') is None
