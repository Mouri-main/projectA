# テキスト感情極性分類システム アーキテクチャおよび開発仕様書

## 1. プロジェクト概要

本プロジェクトは、入力された日本語テキストデータに対して感情の極性（ポジティブ・ネガティブ・ニュートラル）を分類するシステムを構築する。
システムは前処理、データアクセス、ドメインロジック、出力層にモジュール分割されたクリーンなアーキテクチャを採用している。各開発者は、本仕様書で定義されたインターフェース（入出力の型と境界値の振る舞い）を厳守し、並行開発を推進すること。

## 2. 環境構築および実行手順

* **言語要件:** Python 3.8 以上
* **依存ライブラリ:** `requirements.txt` に定義（`janome`, `pytest` 等）

### 2.1. 環境構築
```bash
pip install -r requirements.txt
```

### 2.2. アプリケーションの実行
プロジェクトのルートディレクトリ（`projectA/`）を起点として実行する。

**バッチ処理モード（ファイル一括評価）**
```bash
python src/main.py data/data.txt
```

**対話型モード（標準入力からの評価）**
```bash
python src/main.py
```

### 2.3. テストの実行
品質保証プロセスおよびCI/CDパイプラインへの統合を見据え、テスト実行時は必ずモジュール検索パス（`PYTHONPATH`）を明示的に指定して実行すること。
```bash
PYTHONPATH=. pytest tests/
```

---

## 3. ディレクトリおよびファイル構成

```text
projectA/
├── README.md                           # 本仕様書
├── requirements.txt                    # 依存パッケージ定義
├── data/                               # [データ層] 各種リソース
│   ├── dictionary1.txt                 # 極性辞書（主観表現）
│   ├── dictionary2.txt                 # 極性辞書（客観表現）
│   └── data.txt                        # 入力テキストデータ
├── src/
│   ├── main.py                         # [エントリポイント] アプリケーション制御
│   └── my_library/                     # [自作ライブラリ群]
│       ├── __init__.py
│       ├── load_input_data.py          # ファイルI/Oユーティリティ
│       ├── tokenizer.py                # 形態素解析モジュール
│       ├── manage_output.py            # 出力フォーマット・永続化モジュール
│       └── classifier/                 # ▼ 分類器パッケージ
│           ├── __init__.py             # Facadeクラス（外部API）
│           ├── polarity_dictionary.py  # 辞書データアクセス（リポジトリ）
│           └── predict_polarity.py     # 極性判定アルゴリズム（ドメインロジック）
└── tests/                              # [テスト層]
    ├── __init__.py
    ├── test_load_input_data.py         # I/Oユーティリティのテスト
    ├── test_tokenizer.py               # 形態素解析のテスト
    ├── test_manage_output.py           # 出力モジュールのテスト
    └── test_classifier/
        ├── test_polarity_dictionary.py # データアクセスのテスト
        └── test_predict_polarity.py    # 判定アルゴリズムのテスト（Mock使用）
```

---

## 4. データ仕様

システムが扱う外部ファイルのフォーマット定義。データアクセス層の実装者は本仕様に基づいてパース処理を実装すること。

### 4.1. `data.txt` (入力データ)
分析対象のテキストが1行に1文ずつ格納されたプレーンテキスト（UTF-8エンコーディング）。空行が含まれる場合がある。

### 4.2. `dictionary1.txt`, `dictionary2.txt` (極性辞書データ)
東北大学提供の評価極性辞書。各行はタブ（`\t`）またはスペース区切りで構成される。
* **データ構造例:** `二度寝    ~する(行為)    客観    12345678910    n`
* **パース要件:** フォーマットの揺らぎ（列数の増減など）を考慮し、行を分割した際の**「先頭の要素（単語）」**と**「末尾の要素（極性ラベル: `p`, `n`, `e` 等）」**のみを抽出すること。

---

## 5. 自作ライブラリ API リファレンス

各モジュールの厳密なインターフェース定義。実装者は異常系のハンドリング（コーナーケース）においてシステムをクラッシュさせない堅牢なコードを担保すること。

### 5.1. `my_library.load_input_data`
* **機能:** ファイルI/O処理の抽象化。
* **関数:** `load_data(file_path: str) -> list[str]`
* **仕様:**
  * 指定されたパスのファイルを読み込み、行ごとの文字列リストを返す。
  * 各行の改行コード（`\n`）および前後の空白は除去すること。
  * 空行（空白のみの行を含む）はリストから除外する。
  * **コーナーケース:** ファイルが存在しない場合は `FileNotFoundError` を送出する。ファイルが空の場合は `[]` を返す。

### 5.2. `my_library.tokenizer`
* **機能:** 生のテキストデータから形態素解析によるトークン列の生成。
* **関数:** `tokenize(raw_sentence: str) -> list[str]`
* **仕様:**
  * `janome.tokenizer.Tokenizer` を用いて文字列を単語（表層形）のリストに分割する。
  * **コーナーケース:** 入力が空文字 `""` または空白のみの場合は `[]` を返す。
  * **制限事項:** 助詞や記号のフィルタリング（除外処理）は一切行わないこと。後続のドメインロジックが文脈を解析するために全トークンが必須となる。

### 5.3. `my_library.classifier.polarity_dictionary`
* **機能:** 極性辞書データのメモリ展開および高速検索（データリポジトリ）。
* **クラス:** `PolarityDictionary`
  * **`__init__(self, dict_dir: str)`**: 指定ディレクトリ内の辞書ファイル群を読み込み、内部ハッシュテーブル（`dict`）を構築する。ファイルの読み込みには `load_input_data.load_data` を使用すること。
  * **`get_polarity(self, word: str) -> str | None`**: 単語をキーとして極性ラベル（`"p"`, `"n"`, `"e"` など）を返す。
  * **コーナーケース:** 単語が辞書に存在しない場合、または入力が空文字の場合は例外（`KeyError`）を送出せず、必ず `None` を返すこと。

### 5.4. `my_library.classifier.predict_polarity`
* **機能:** トークン列と辞書を用いた極性判定（コアビジネスロジック）。
* **関数:** `predict(tokens: list[str], dictionary: PolarityDictionary) -> str`
* **仕様:**
  * 単語の出現頻度に基づくシンプルなスコアリングアルゴリズム。
  * **戻り値:** `"positive"`, `"negative"`, `"neutral"` のいずれかの文字列を厳密に返すこと。
  * **コーナーケース:** トークンリストが空 `[]` の場合、全トークンの極性が `None` の場合、あるいはスコアが拮抗した場合は、安全に `"neutral"` を返すこと。

### 5.5. `my_library.manage_output`
* **機能:** 評価結果の標準出力およびファイルへの永続化。
* **関数:** `output_result(raw_sentence: str, prediction: str, output_file: str = "data/processed_data.txt") -> None`
* **仕様:**
  * 標準出力に対して、視認性の高いフォーマット（例: `[POSITIVE] 該当テキスト`）で出力する。
  * `output_file` を追記モード（`a`）で開き、機械可読な形式（CSV等）で結果を1行書き込む。
  * **コーナーケース:** `raw_sentence` が空文字の場合でもプロセスを異常終了させず、規定のフォーマット処理を実行すること。

### 5.6. `my_library.classifier.__init__` (Facade)
* **機能:** 分類器パッケージの外部向けインターフェース。
* **クラス:** `SentimentClassifier`
  * **`__init__(self, dict_dir: str)`**: 内部で `PolarityDictionary` をインスタンス化し、保持する。
  * **`predict(self, tokens: list[str]) -> str`**: 内部状態（辞書インスタンス）と引数 `tokens` を `predict_polarity.predict` に委譲し、結果を返却する。本クラス内に固有の演算ロジックは実装しない。

---

## 6. テスト実装要件

本システムは高い品質要件を満たすため、各実装者は `pytest` を用いたユニットテストを記述すること。すべてのテストケースは異常系・境界値を網羅する必要がある。

### 6.1. `test_load_input_data.py`
* **検証項目:**
  * 正常なテキストファイルが正しくリスト化されること。
  * 空行や空白のみの行が適切に除外されること。
  * 末尾の改行コード（`\n`）が除去されていること。
  * 存在しないパスを指定した際に `FileNotFoundError` が送出されること。

### 6.2. `test_tokenizer.py`
* **検証項目:**
  * 標準的な日本語テキストが単語のリスト（`list[str]`）に分割されること（※Tokenオブジェクトのまま返していないかの確認）。
  * 記号や助詞が欠落せずに出力に含まれること。
  * 入力が空文字 `""` またはスペースのみの場合、エラーなく `[]` が返却されること。

### 6.3. `test_polarity_dictionary.py`
* **検証項目:**
  * ダミーのテキストファイルを読み込ませ、先頭と末尾の要素が正しくパースされ、辞書が構築されること。
  * `get_polarity` メソッドに対し、登録済みの単語を与えた際に正しい極性が返却されること。
  * 未登録の単語、および空文字 `""` を与えた際に、例外なく `None` が返却されること。

### 6.4. `test_predict_polarity.py`
* **検証方針:** 実環境のテキストファイルに依存させず、依存性の注入（DI）を利用して辞書オブジェクトをMock化（スタブ化）してテストすること。
* **検証項目:**
  * ポジティブ・ネガティブの基本スコアリングが正確に機能すること。
  * 入力トークンが空リスト `[]` の場合、結果が `"neutral"` になること。
* **Mock実装例:**
  ```python
  class MockDictionary:
      def get_polarity(self, word):
          return {"良い": "p", "悪い": "n"}.get(word, None)
  
  def test_predict_positive():
      mock_dict = MockDictionary()
      result = predict(["良い", "素晴らしい"], mock_dict)
      assert result == "positive"
  ```

### 6.5. `test_manage_output.py`
* **検証項目:**
  * `capsys` フィクスチャを利用し、標準出力が規定のフォーマットに合致していること。
  * 指定したファイル（テスト用の一時ファイル等を利用）に結果が正しく追記されること。
  * 空文字を渡しても例外が発生しないこと。

---

## 7. 実装上の注意点と具体例

### 7.1. `manage_output.output_result` の出力フォーマット詳細

#### 標準出力（コンソール出力）
* **形式:** `[極性ラベル] 元のテキスト`
* **極性ラベル:** `POSITIVE`、`NEGATIVE`、`NEUTRAL` のいずれか（大文字）
* **具体例:**
  ```
  [POSITIVE] 朝の空がきれいで、気持ちよく一日を始められた。
  [NEGATIVE] 寝坊して電車に乗り遅れ、朝から気分が沈んだ。
  [NEUTRAL] 朝食にはトーストとヨーグルトを食べた。
  ```
* **複数行入力時:** 1行ずつ同じフォーマットで出力

#### ファイル出力（`data/processed_data.txt`）
* **形式:** CSV形式（カンマ区切り）
* **列構成:** `元のテキスト,極性（小文字）`
* **具体例:**
  ```
  朝の空がきれいで、気持ちよく一日を始められた。,positive
  寝坊して電車に乗り遅れ、朝から気分が沈んだ。,negative
  朝食にはトーストとヨーグルトを食べた。,neutral
  ```
* **エンコーディング:** UTF-8
* **改行コード:** LF（Unix形式）
* **テキストにカンマが含まれる場合:** ダブルクォートで囲む
  * 例: `"朝, 昼, 晩のご飯",positive`
* **操作:** 追記モード（`a`）で開く

### 7.2. `janome` ライブラリの具体的な使用方法

#### 基本的な形態素解析
```python
from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()
sentence = "これはテストです。"
tokens = [token.surface for token in tokenizer.tokenize(sentence)]
print(tokens)  # 出力: ['これ', 'は', 'テスト', 'です', '。']
```

#### 重要なポイント
* `token.surface` は単語の表層形（見た目そのまま）を取得
* 品詞情報は `token.part_of_speech` で取得可能
* **仕様書で明記したとおり、助詞や記号の除外は一切行わない** ← ドメインロジック層で判定するため
* 返り値は必ず `list[str]` であること（Token オブジェクトのまま返さない）

### 7.3. 極性辞書ファイルのパース戦略

#### 辞書ファイルの形式再確認
東北大学評価極性辞書の例：
```
二度寝	～する(行為)	客観	12345678910	n
二日酔い	～である・になる(状態)	客観	n
賑やか	～である・になる(評価・感情)	主観	p
```

#### 実装時のパース戦略
```python
def parse_dictionary_line(line: str) -> tuple[str, str | None]:
    """
    例：
    'かわいい\t～である・になる(評価・感情)\t主観\tp'
    → ('かわいい', 'p')
    """
    parts = line.split('\t')
    if len(parts) < 2:
        return None, None  # フォーマット異常の行はスキップ
    
    word = parts[0]           # 先頭の要素（単語）
    polarity = parts[-1]      # 末尾の要素（極性ラベル）
    
    return word, polarity if polarity in ['p', 'n', 'e'] else None
```

#### 複数の辞書ファイルを使用する場合
```python
class PolarityDictionary:
    def __init__(self, dict_dir: str):
        self.word_polarity = {}  # {単語: 極性}
        
        # dictionary1.txt と dictionary2.txt を読み込む
        for filename in ['dictionary1.txt', 'dictionary2.txt']:
            filepath = os.path.join(dict_dir, filename)
            for line in load_input_data.load_data(filepath):
                word, polarity = parse_dictionary_line(line)
                if word and polarity:
                    # 同じ単語が両方の辞書に存在する場合は
                    # dictionary1を優先するか、新しい値で上書きするか
                    # グループで判断してください
                    self.word_polarity[word] = polarity
```

### 7.4. テスト用ダミーデータの作成

#### ダミー辞書ファイルの例
`tests/data/dummy_dictionary.txt` を作成：
```
良い	~である	p
悪い	~である	n
普通	~である	e
嬉しい	~である	p
悲しい	~である	n
退屈	~である	n
楽しい	~である	p
つまらない	~である	n
```

#### テストコード内での使用例
```python
import tempfile
import os
from my_library.classifier import PolarityDictionary

def test_polarity_dictionary():
    # 一時ディレクトリ作成
    with tempfile.TemporaryDirectory() as tmpdir:
        # ダミーファイルを作成
        dict_file = os.path.join(tmpdir, 'test_dict.txt')
        with open(dict_file, 'w', encoding='utf-8') as f:
            f.write('良い\t~である\tp\n')
            f.write('悪い\t~である\tn\n')
        
        # テスト実行
        dictionary = PolarityDictionary(tmpdir)
        assert dictionary.get_polarity('良い') == 'p'
        assert dictionary.get_polarity('悪い') == 'n'
        assert dictionary.get_polarity('存在しない') is None
```

### 7.5. `predict_polarity` の実装ガイドライン

#### 基本的なスコアリング戦略
```python
def predict(tokens: list[str], dictionary: PolarityDictionary) -> str:
    """
    推奨される実装方針：
    1. 各トークンについて極性を検索
    2. ポジティブスコア、ネガティブスコアを計算
    3. 否定語の影響を考慮（オプション）
    4. スコアに基づいて分類
    """
    positive_count = 0
    negative_count = 0
    
    for token in tokens:
        polarity = dictionary.get_polarity(token)
        if polarity == 'p':
            positive_count += 1
        elif polarity == 'n':
            negative_count += 1
    
    # スコアに基づいて判定
    if positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"  # 同数またはスコア0の場合
```

### 7.6. エラーハンドリングの一般原則

| 状況 | 推奨される動作 | 例外 |
|------|---------------|------|
| ファイルが見つからない | `FileNotFoundError` を送出 | 仕様通り |
| 辞書ファイルのフォーマット異常（一部行） | 問題行をスキップ、ログに記録 | 全行が異常な場合は例外 |
| 辞書に単語がない | `None` を返す | 例外にしない |
| 入力テキストが空 | エラー通知でなく安全に処理 | 処理を続行 |
| トークン化結果が空 | `"neutral"` を返す | 例外にしない |

#### 推奨されるロギング戦略
```python
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

def load_dictionary(dict_dir):
    """ロギング付きの辞書読み込み"""
    valid_entries = 0
    invalid_entries = 0
    
    for line in load_input_data.load_data(filepath):
        word, polarity = parse_dictionary_line(line)
        if word and polarity:
            valid_entries += 1
        else:
            invalid_entries += 1
            logger.warning(f"Skipped invalid dictionary entry: {line}")
    
    logger.info(f"Dictionary loaded: {valid_entries} valid, {invalid_entries} skipped")
```

### 7.7. 実装の推奨順序

1. **第1段階（第1週）:**
   - `load_input_data.load_data` を実装・テスト
   - `tokenizer.tokenize` を実装・テスト
   
2. **第2段階（第1週後半）:**
   - `polarity_dictionary.PolarityDictionary` を実装・テスト
   - 極性辞書の読み込み確認
   
3. **第3段階（第2週前半）:**
   - `predict_polarity.predict` の基本形を実装・テスト
   - Mock オブジェクトを活用したテスト
   
4. **第4段階（第2週後半）:**
   - `manage_output.output_result` を実装・テスト
   - `main.py` で全モジュールを統合
   - エンドツーエンドテスト

### 7.8. よくある質問（FAQ）

**Q: 複数の辞書ファイルがある場合、優先度をどうつけるか？**  
A: グループで決定してください。以下のいずれかが考えられます：
- dictionary1を優先（上書きしない）
- 統計情報が豊富な辞書を優先
- スコアを合算して両方を活かす

**Q: テスト用の小さい辞書ファイルはどこに置く？**  
A: `tests/data/` ディレクトリを作成し、そこに置いてください。テストコードからは絶対パスで指定できるよう工夫してください。

**Q: 出力ファイルが既に存在する場合はどうする？**  
A: 追記モード（`a`）で開くので、既存データを保持します。テスト時は `setUp` で削除するか、テスト専用の出力ファイルを使用してください。