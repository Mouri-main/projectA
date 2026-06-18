"""
テスト: load_input_data モジュール

検証項目：
  1. 正常なテキストファイルが正しくリスト化されること
  2. 空行や空白のみの行が適切に除外されること
  3. 末尾の改行コード（\n）が除去されていること
  4. 存在しないパスを指定した際に FileNotFoundError が送出されること
  5. ファイルが空の場合は [] を返すこと
"""

import os
import sys
import pytest
import tempfile

# プロジェクトルートをパスに追加（モジュール検索パスの設定）
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root_path)

from src.my_library import load_input_data


def test_load_data_normal_file():
    """正常なテキストファイルが正しくリスト化されること"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("これはテストです。\n")
        f.write("2行目のテキスト\n")
        f.write("3行目のテキスト")
        temp_file = f.name
    
    try:
        result = load_input_data.load_data(temp_file)
        assert result == ["これはテストです。", "2行目のテキスト", "3行目のテキスト"]
    finally:
        os.unlink(temp_file)


def test_load_data_with_empty_lines():
    """空行が適切に除外されること"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("1行目\n")
        f.write("\n")
        f.write("3行目\n")
        f.write("   \n")  # 空白のみの行
        f.write("5行目")
        temp_file = f.name
    
    try:
        result = load_input_data.load_data(temp_file)
        assert result == ["1行目", "3行目", "5行目"]
    finally:
        os.unlink(temp_file)


def test_load_data_newline_removal():
    """末尾の改行コード（\n）が除去されていること"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("テキスト1\n")
        f.write("テキスト2\n")
        temp_file = f.name
    
    try:
        result = load_input_data.load_data(temp_file)
        for line in result:
            assert not line.endswith('\n')
        assert result == ["テキスト1", "テキスト2"]
    finally:
        os.unlink(temp_file)


def test_load_data_file_not_found():
    """存在しないパスを指定した際に FileNotFoundError が送出されること"""
    with pytest.raises(FileNotFoundError):
        load_input_data.load_data("/nonexistent/path/file.txt")


def test_load_data_empty_file():
    """ファイルが空の場合は [] を返すこと"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        temp_file = f.name
    
    try:
        result = load_input_data.load_data(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


def test_load_data_only_empty_lines():
    """空行だけのファイルの場合は [] を返すこと"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("\n")
        f.write("   \n")
        f.write("\n")
        temp_file = f.name
    
    try:
        result = load_input_data.load_data(temp_file)
        assert result == []
    finally:
        os.unlink(temp_file)


def test_load_data_with_leading_trailing_spaces():
    """前後の空白が除去されること"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("  テキスト1  \n")
        f.write("\tテキスト2\t\n")
        temp_file = f.name
    
    try:
        result = load_input_data.load_data(temp_file)
        assert result == ["テキスト1", "テキスト2"]
    finally:
        os.unlink(temp_file)
