"""
main.py
  - バッチ処理モードと対話型どっちも行けるようにする

実行方法：
  $ python src/main.py data/data.txt    # バッチ処理
  $ python src/main.py                  # 対話型
"""

import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_library import load_input_data, tokenizer, manage_output
from my_library.classifier import SentimentClassifier


def main():
    """メイン処理
    - コマンドライン引数があればバッチ処理、なければ対話型
    """
    # 極性分類器を初期化
    classifier = SentimentClassifier("data")
    
    if len(sys.argv) > 1:
        # バッチ処理モード
        batch_process(sys.argv[1], classifier)
    else:
        # 対話型モード
        interactive_mode(classifier)


def batch_process(file_path: str, classifier: SentimentClassifier) -> None:
    """
    ファイルから複数行を読み込み、極性を分類する。
    """
    try:
        sentences = load_input_data.load_data(file_path)
    except FileNotFoundError as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)
    
    for sentence in sentences:
        # トークン化
        tokens = tokenizer.tokenize(sentence)
        
        # 極性予測
        prediction = classifier.predict(tokens)
        
        # 出力
        manage_output.output_result(sentence, prediction)


def interactive_mode(classifier: SentimentClassifier) -> None:
    """
    対話型モード：標準入力から1行ずつ入力を受け付ける。
    """
    print("テキスト感情極性分類")
    print("テキストを入力してください。（終了するには Ctrl+D または exit を入力）")
    print()
    
    try:
        while True:
            user_input = input("> ").strip()
            
            if user_input.lower() == "exit" or user_input == "":
                continue
            
            # トークン化
            tokens = tokenizer.tokenize(user_input)
            
            # 極性予測
            prediction = classifier.predict(tokens)
            
            # 出力
            manage_output.output_result(user_input, prediction)
    except EOFError:
        print("\nシステムを終了します。")
        sys.exit(0)
    except KeyboardInterrupt:
        print("\n\nシステムを終了します。")
        sys.exit(0)


if __name__ == "__main__":
    main()

