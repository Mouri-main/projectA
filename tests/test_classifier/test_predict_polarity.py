"""
テスト: predict_polarity モジュール

検証方針：
  実環境のテキストファイルに依存させず、依存性の注入（DI）を利用して
  辞書オブジェクトをMock化してテストする。

検証項目：
  1. ポジティブ・ネガティブの基本スコアリングが正確に機能すること
  2. 入力トークンが空リスト [] の場合、結果が "neutral" になること
"""

import os
import sys
import pytest

# プロジェクトルートをパスに追加（モジュール検索パス）
project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root_path)

from src.my_library.classifier import predict_polarity


class MockDictionary:
    """テスト用のMock辞書"""
    
    def __init__(self, word_polarity_map=None):
        """
        Args:
            word_polarity_map (dict): 単語→極性のマッピング
        """
        self.word_polarity_map = word_polarity_map or {}
    
    def get_polarity(self, word):
        return self.word_polarity_map.get(word, None)


def test_predict_positive_sentiment():
    """ポジティブな単語のみの場合、positive が返されること"""
    mock_dict = MockDictionary({
        '良い': 'p',
        '素晴らしい': 'p',
        '素敵': 'p'
    })
    
    result = predict_polarity.predict(['良い', '素晴らしい', '素敵'], mock_dict)
    assert result == "positive"


def test_predict_negative_sentiment():
    """ネガティブな単語のみの場合、negative が返されること"""
    mock_dict = MockDictionary({
        '悪い': 'n',
        'つまらない': 'n',
        '醜い': 'n'
    })
    
    result = predict_polarity.predict(['悪い', 'つまらない', '醜い'], mock_dict)
    assert result == "negative"


def test_predict_neutral_balanced():
    """ポジティブとネガティブが同数の場合、neutral が返されること"""
    mock_dict = MockDictionary({
        '良い': 'p',
        '悪い': 'n'
    })
    
    result = predict_polarity.predict(['良い', '悪い'], mock_dict)
    assert result == "neutral"


def test_predict_neutral_empty_list():
    """入力トークンが空リストの場合、neutral が返されること"""
    mock_dict = MockDictionary({'良い': 'p'})
    
    result = predict_polarity.predict([], mock_dict)
    assert result == "neutral"


def test_predict_neutral_no_polarity_words():
    """全トークンの極性が None の場合、neutral が返されること"""
    mock_dict = MockDictionary({'良い': 'p'})  # '良い'だけ登録
    
    result = predict_polarity.predict(['存在しない', 'テスト', 'です'], mock_dict)
    assert result == "neutral"


def test_predict_positive_majority():
    """ポジティブが多数派の場合、positive が返されること"""
    mock_dict = MockDictionary({
        '良い': 'p',
        '素晴らしい': 'p',
        '楽しい': 'p',
        '悪い': 'n'
    })
    
    result = predict_polarity.predict(['良い', '素晴らしい', '楽しい', '悪い'], mock_dict)
    assert result == "positive"


def test_predict_negative_majority():
    """ネガティブが多数派の場合、negative が返されること"""
    mock_dict = MockDictionary({
        '悪い': 'n',
        'つまらない': 'n',
        '最悪': 'n',
        '良い': 'p'
    })
    
    result = predict_polarity.predict(['悪い', 'つまらない', '最悪', '良い'], mock_dict)
    assert result == "negative"


def test_predict_with_neutral_polarity():
    """中立的な極性 'e' を含む場合、スコアに影響しないこと"""
    mock_dict = MockDictionary({
        '良い': 'p',
        '悪い': 'n',
        '普通': 'e'
    })
    
    # 'e' はスコアに影響しない
    result = predict_polarity.predict(['良い', '普通', '悪い'], mock_dict)
    assert result == "neutral"


def test_predict_mixed_tokens():
    """登録・未登録の単語が混在する場合、登録済みのみがスコアに反映されること"""
    mock_dict = MockDictionary({
        '良い': 'p',
        '悪い': 'n'
    })
    
    result = predict_polarity.predict(['良い', '存在しない1', '悪い', '存在しない2'], mock_dict)
    assert result == "neutral"


def test_predict_string_return_type():
    """戻り値が常に "positive", "negative", "neutral" のいずれかであること"""
    mock_dict = MockDictionary({
        '良い': 'p',
        '悪い': 'n'
    })
    
    test_cases = [
        (['良い', '良い', '良い'], "positive"),
        (['悪い', '悪い'], "negative"),
        ([], "neutral"),
        (['存在しない'], "neutral"),
    ]
    
    for tokens, expected in test_cases:
        result = predict_polarity.predict(tokens, mock_dict)
        assert result in ["positive", "negative", "neutral"]
        assert isinstance(result, str)
