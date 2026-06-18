# テキスト感情極性分類

## プロジェクト概要

日本語のテキストデータを受け取って、その感情的な極性（ポジティブ/ネガティブ/ニュートラル）を自動分類する。

指定されたテキストファイルまたはユーザー入力から感情極性を判定し、結果を標準出力とCSVファイルに出力する。

---

## プロジェクト構成

```
src/
├── main.py                          # バッチ処理か対話型
└── my_library/
    ├── __init__.py                  # パッケージ初期化
    ├── load_input_data.py           # ファイル読み込み
    ├── tokenizer.py                 # 形態素解析
    ├── manage_output.py             # 結果出力
    └── classifier/
        ├── __init__.py              # SentimentClassifier（Facade）
        ├── polarity_dictionary.py   # 辞書データ管理
        └── predict_polarity.py      # 極性判定ロジック
```

---

## データフロー

```
ユーザー入力 or ファイル
        ↓
[load_input_data.load_data]  ← ファイルから複数行を読み込み
        ↓
1行ずつ処理：
    [tokenizer.tokenize]     ← 形態素解析でトークン化
        ↓
    [classifier.predict]     → [polarity_dictionary]（辞書参照）
                                → [predict_polarity]（スコアリング）
        ↓
    [manage_output.output_result]    ← 標準出力 + CSV出力
```
