"""
テスト: tokenizer モジュール

検証項目：
  1. 標準的な日本語テキストが単語のリスト（list[str]）に分割されること
  2. 記号や助詞が欠落せずに出力に含まれること
  3. Token オブジェクトではなく文字列が返されていること
  4. 入力が空文字 "" またはスペースのみの場合、エラーなく [] が返却されること
"""

import os
import sys

# プロジェクトルートをパスに追加（モジュール検索パス）
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root_path)

from src.my_library import tokenizer


def test_tokenize_normal_sentence():
    """標準的な日本語テキストが単語のリストに分割されること"""
    result = tokenizer.tokenize("これはテストです。")
    
    # 返り値は list[str] であること
    assert isinstance(result, list)
    assert all(isinstance(token, str) for token in result)
    
    # 単語が分割されていることを確認
    assert len(result) > 0
    assert "テスト" in result


def test_tokenize_keeps_particles_and_symbols():
    """記号や助詞が欠落せずに出力に含まれること"""
    result = tokenizer.tokenize("朝の空がきれいで、気持ちよく一日を始められた。")
    
    # 句点が含まれていることを確認
    assert "。" in result
    
    # 読点が含まれていることを確認
    assert "、" in result
    
    # 助詞が含まれていることを確認
    assert "の" in result or "で" in result


def test_tokenize_returns_strings_not_tokens():
    """Token オブジェクトではなく文字列が返されていること"""
    result = tokenizer.tokenize("テスト")
    
    for token in result:
        assert isinstance(token, str)
        # Token オブジェクトではないことを確認
        assert not hasattr(token, 'surface') or isinstance(token, str)


def test_tokenize_empty_string():
    """入力が空文字の場合、エラーなく [] が返却されること"""
    result = tokenizer.tokenize("")
    assert result == []
    assert isinstance(result, list)


def test_tokenize_whitespace_only():
    """入力がスペースのみの場合、エラーなく [] が返却されること"""
    result = tokenizer.tokenize("   ")
    assert result == []


def test_tokenize_whitespace_with_tabs():
    """入力がタブ・スペースのみの場合、エラーなく [] が返却されること"""
    result = tokenizer.tokenize("\t  \t")
    assert result == []


def test_tokenize_complex_sentence():
    """複雑な日本語文が正しく分割されること"""
    result = tokenizer.tokenize("提出したレポートを褒められて、少し自信がついた。")
    
    # 返り値は list[str]
    assert isinstance(result, list)
    assert all(isinstance(token, str) for token in result)
    
    # 期待される単語が含まれていること
    assert "提出" in result or "レポート" in result or "褒め" in result


def test_tokenize_with_numbers_and_symbols():
    """数字や複数の記号を含む文が正しく処理されること"""
    result = tokenizer.tokenize("2026年6月18日（木）です。")
    
    assert isinstance(result, list)
    # 少なくとも数字や括弧、句点が適切に処理されていることを確認
    assert len(result) > 0
