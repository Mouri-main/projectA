"""
極性判定アルゴリズム
トークン列と辞書を用いた感情極性の判定
  - アンルゴリズムはまかせた
  - 戻り値は厳密に "p", "n", "e" のいずれか
  - トークンリストが空、全極性が None、スコア拮抗時は安全に "e" を返す
"""

from .polarity_dictionary import PolarityDictionary


def predict(tokens: list[str], dictionary: PolarityDictionary) -> str:
    """
    トークン列から感情極性を予測する。
    dictionaryに対してget_polarityを呼び出して単語を与えると品詞と極性ラベルのタプルが返ってくる
    """
    