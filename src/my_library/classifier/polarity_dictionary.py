"""
極性辞書データアクセス
  極性辞書データを管理する
  - 複数の辞書ファイルをディレクトリから読み込み
  - load_input_data.load_data を使用してファイルを読む
  - 単語を受け取ったら品詞と極性ラベルを返す
  - 未登録単語や空文字へのgetはKeyErrorを送出せずNoneを返す
"""

import os
from .. import load_input_data


class PolarityDictionary:
    """
    極性辞書：単語と極性ラベルのマッピング
    """
    def __init__(self, dict_dir: str):
        """
        初期化：指定ディレクトリdict_dirの辞書ファイルを読み込む。
        """
        pass
    
    def get_polarity(self, word: str) -> tuple[str, str] | None:
        """
        単語を受け取り品詞と極性ラベルを返す。
        KeyErrorの代わりに None を返す。
        """
        pass
