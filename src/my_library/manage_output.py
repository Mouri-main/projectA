"""
出力モジュール

機能：
  評価結果の標準出力およびファイルへの書き込み
  raw_sentenceは生のテキスト、predictionは極性ラベル（"p", "n", "n")、それぞれ(positive, negative, neutral)を表す
  - 標準出力： [極性] テキスト
        [POSITIVE] テキスト
        [NEGATIVE] テキスト
        [NEUTRAL] テキスト
        みたいな感じで出力
  - ファイル出力：CSV形式（テキスト,極性）で追記
  - raw_sentence が空文字の場合でも処理を続行
"""

import csv


def output_result(raw_sentence: str, prediction: str, output_file: str = "data/processed_data.txt") -> None:
    pass
