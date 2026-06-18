"""
テスト: manage_output モジュール

検証項目：
  1. capsys フィクスチャを利用し、標準出力が規定のフォーマットに合致していること
  2. 指定したファイル（テスト用の一時ファイル等を利用）に結果が正しく追記されること
  3. 空文字を渡しても例外が発生しないこと
"""

import os
import sys
import tempfile
import pytest

# プロジェクトルートをパスに追加（モジュール検索パス）
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root_path)

from src.my_library import manage_output


def test_output_result_standard_output_positive(capsys):
    """ポジティブの標準出力が規定のフォーマットであること"""
    manage_output.output_result("素晴らしい一日だった。", "positive")
    
    captured = capsys.readouterr()
    assert "[POSITIVE] 素晴らしい一日だった。" in captured.out


def test_output_result_standard_output_negative(capsys):
    """ネガティブの標準出力が規定のフォーマットであること"""
    manage_output.output_result("つまらない日だった。", "negative")
    
    captured = capsys.readouterr()
    assert "[NEGATIVE] つまらない日だった。" in captured.out


def test_output_result_standard_output_neutral(capsys):
    """ニュートラルの標準出力が規定のフォーマットであること"""
    manage_output.output_result("朝食を食べた。", "neutral")
    
    captured = capsys.readouterr()
    assert "[NEUTRAL] 朝食を食べた。" in captured.out


def test_output_result_file_output_positive():
    """ポジティブの結果がファイルに正しく追記されること"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        # クリア
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        # 出力
        manage_output.output_result("素晴らしい", "positive", temp_file)
        
        # ファイルの内容を確認
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "素晴らしい,positive" in content
    finally:
        os.unlink(temp_file)


def test_output_result_file_output_negative():
    """ネガティブの結果がファイルに正しく追記されること"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        manage_output.output_result("つまらない", "negative", temp_file)
        
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "つまらない,negative" in content
    finally:
        os.unlink(temp_file)


def test_output_result_file_append_mode():
    """ファイルが追記モードで動作すること"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        # 初期内容を書き込む
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("初期行\n")
        
        # 追記
        manage_output.output_result("追記1", "positive", temp_file)
        manage_output.output_result("追記2", "negative", temp_file)
        
        # 確認
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "初期行" in content
        assert "追記1,positive" in content
        assert "追記2,negative" in content
    finally:
        os.unlink(temp_file)


def test_output_result_empty_sentence(capsys):
    """空文字を渡しても例外が発生しないこと"""
    # 例外が発生しないことを確認
    manage_output.output_result("", "neutral")
    
    captured = capsys.readouterr()
    # 空の標準出力でもフォーマットは正しく
    assert "[NEUTRAL]" in captured.out


def test_output_result_with_comma_in_text():
    """テキストにカンマが含まれている場合も正しく処理されること"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        manage_output.output_result("朝、昼、晩のご飯", "positive", temp_file)
        
        # ファイルを再度読み込んでCSVとして検証
        with open(temp_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # カンマを含むテキストが正しく処理されていること
        assert "朝、昼、晩のご飯" in content
    finally:
        os.unlink(temp_file)
