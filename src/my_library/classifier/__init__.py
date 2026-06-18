"""
分類器パッケージ
トークン化されたテキストを受け取って感情極性を返す
  - PolarityDictionary: 辞書データアクセス（polarity_dictionary.py）
  - predict_polarity: 極性判定アルゴリズム（predict_polarity.py）
  - SentimentClassifier: 全体のクラス（このファイル）
"""

from .polarity_dictionary import PolarityDictionary
from . import predict_polarity


class SentimentClassifier:
    """
    テキスト感情分類器
    内部で PolarityDictionary をインスタンス化し予測ロジックを統合する
    """
    
    def __init__(self, dict_dir: str):
        """
        初期化として極性辞書を読み込む。
        """
        self.dictionary = PolarityDictionary(dict_dir)
    
    def predict(self, tokens: list[str]) -> str:
        """
        トークン列から感情極性を予測する。
            内部で predict_polarity.predict に処理を委譲
        """
        return predict_polarity.predict(tokens, self.dictionary)
