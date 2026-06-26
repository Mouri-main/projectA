"""
形態素解析モジュール
生のテキストデータから形態素解析によるトークン列を生成する。

仕様：
  - janome.tokenizer.Tokenizer を使用
  - 返り値は Token オブジェクトではなく、単語の表層形のリスト (list[str])
  - 入力が空文字 "" または空白のみの場合は [] を返す
  - 助詞や記号のフィルタリングは一切行わない
"""

from janome.tokenizer import Tokenizer

_tokenizer = Tokenizer()

def tokenize(raw_sentence: str) -> list[str]:
    if not raw_sentence.strip():
        return []
    return [token.surface for token in _tokenizer.tokenize(raw_sentence)]

def tokenize_base(raw_sentence: str) -> list[str]:
    """基本形（原形）のリストを返す"""
    if not raw_sentence.strip():
        return []
    return [token.base_form for token in _tokenizer.tokenize(raw_sentence)]