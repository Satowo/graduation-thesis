"""
CSVファイルの区切り文字を変換するユーティリティ

タブ区切りのCSVファイルをカンマ区切りに変換します。
"""
from pathlib import Path


def convert_tab_to_comma(input_path, output_path=None, overwrite=False):
    """
    タブ区切りのCSVファイルをカンマ区切りに変換する
    
    Args:
        input_path: 入力ファイルのパス（タブ区切りCSV）
        output_path: 出力ファイルのパス（Noneの場合は入力ファイルを上書き）
        overwrite: 出力ファイルが既に存在する場合に上書きするか（デフォルト: False）
    
    Returns:
        Path: 出力ファイルのパス
    
    Raises:
        FileNotFoundError: 入力ファイルが見つからない場合
        FileExistsError: 出力ファイルが既に存在し、overwrite=Falseの場合
    """
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path
    
    # 入力ファイルの存在確認
    if not input_path.exists():
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")
    
    # 出力ファイルの存在確認
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"出力ファイルが既に存在します: {output_path}\n"
            "上書きする場合は overwrite=True を指定してください。"
        )
    
    # ファイルを読み込んでタブをカンマに置換
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # タブをカンマに置換
    converted_content = content.replace('\t', ',')
    
    # 出力ディレクトリが存在しない場合は作成
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 変換した内容を書き込み
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(converted_content)
    
    print(f"変換完了: {input_path} -> {output_path}")
    return output_path


def convert_csv_delimiter(input_path, output_path=None, 
                         input_delimiter='\t', output_delimiter=',', 
                         overwrite=False):
    """
    汎用的なCSV区切り文字変換関数
    
    Args:
        input_path: 入力ファイルのパス
        output_path: 出力ファイルのパス（Noneの場合は入力ファイルを上書き）
        input_delimiter: 入力ファイルの区切り文字（デフォルト: '\t'）
        output_delimiter: 出力ファイルの区切り文字（デフォルト: ','）
        overwrite: 出力ファイルが既に存在する場合に上書きするか（デフォルト: False）
    
    Returns:
        Path: 出力ファイルのパス
    
    Raises:
        FileNotFoundError: 入力ファイルが見つからない場合
        FileExistsError: 出力ファイルが既に存在し、overwrite=Falseの場合
    """
    input_path = Path(input_path)
    output_path = Path(output_path) if output_path else input_path
    
    # 入力ファイルの存在確認
    if not input_path.exists():
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")
    
    # 出力ファイルの存在確認
    if output_path.exists() and not overwrite:
        raise FileExistsError(
            f"出力ファイルが既に存在します: {output_path}\n"
            "上書きする場合は overwrite=True を指定してください。"
        )
    
    # ファイルを読み込んで区切り文字を置換
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 区切り文字を置換
    converted_content = content.replace(input_delimiter, output_delimiter)
    
    # 出力ディレクトリが存在しない場合は作成
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 変換した内容を書き込み
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(converted_content)
    
    print(f"変換完了: {input_path} -> {output_path}")
    return output_path


def convert_all_csv_in_folder(folder_path, overwrite=False, 
                              input_delimiter='\t', output_delimiter=','):
    """
    フォルダ内のすべてのCSVファイルの区切り文字を変換する
    
    Args:
        folder_path: 対象フォルダのパス
        overwrite: 出力ファイルが既に存在する場合に上書きするか（デフォルト: False）
        input_delimiter: 入力ファイルの区切り文字（デフォルト: '\t'）
        output_delimiter: 出力ファイルの区切り文字（デフォルト: ','）
    
    Returns:
        list: 変換されたファイルのパスのリスト
    
    Raises:
        NotADirectoryError: 指定されたパスがディレクトリでない場合
    """
    folder_path = Path(folder_path)
    
    if not folder_path.is_dir():
        raise NotADirectoryError(f"指定されたパスはディレクトリではありません: {folder_path}")
    
    # CSVファイルを検索（.csv拡張子を持つファイル）
    csv_files = list(folder_path.glob("*.csv"))
    
    if not csv_files:
        print(f"フォルダ内にCSVファイルが見つかりませんでした: {folder_path}")
        return []
    
    print(f"見つかったCSVファイル: {len(csv_files)}個")
    print("-" * 50)
    
    converted_files = []
    for csv_file in csv_files:
        try:
            output_path = convert_csv_delimiter(
                csv_file, 
                output_path=None,  # 元のファイルを上書き
                input_delimiter=input_delimiter,
                output_delimiter=output_delimiter,
                overwrite=overwrite
            )
            converted_files.append(output_path)
        except Exception as e:
            print(f"エラー: {csv_file} の変換に失敗しました: {e}")
    
    print("-" * 50)
    print(f"変換完了: {len(converted_files)}/{len(csv_files)}個のファイル")
    return converted_files


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # スクリプトの場所を基準にプロジェクトルートを取得
    SCRIPT_DIR = Path(__file__).parent
    PROJECT_ROOT = SCRIPT_DIR.parent
    
    # コマンドライン引数からファイルパスまたはフォルダパスを取得
    if len(sys.argv) > 1:
        target_path = Path(sys.argv[1])
        if not target_path.is_absolute():
            target_path = PROJECT_ROOT / target_path
        
        # フォルダかファイルかを判定
        if target_path.is_dir():
            # フォルダ内のすべてのCSVファイルを変換
            print(f"フォルダ内のすべてのCSVファイルを変換します: {target_path}")
            convert_all_csv_in_folder(target_path, overwrite=True)
        elif target_path.is_file():
            # 単一ファイルを変換
            output_file = None
            if len(sys.argv) > 2:
                output_file = Path(sys.argv[2])
                if not output_file.is_absolute():
                    output_file = PROJECT_ROOT / output_file
            
            # タブ区切りをカンマ区切りに変換
            convert_tab_to_comma(target_path, output_file, overwrite=True)
        else:
            print(f"エラー: 指定されたパスが見つかりません: {target_path}")
            sys.exit(1)
    else:
        # デフォルトでcsvフォルダを処理
        csv_folder = PROJECT_ROOT / "csv"
        if csv_folder.exists() and csv_folder.is_dir():
            print(f"デフォルトでcsvフォルダ内のすべてのCSVファイルを変換します: {csv_folder}")
            convert_all_csv_in_folder(csv_folder, overwrite=True)
        else:
            print("使用方法:")
            print("  python convert_csv_delimiter.py                    # csvフォルダ内のすべてのCSVを変換")
            print("  python convert_csv_delimiter.py <フォルダパス>      # 指定フォルダ内のすべてのCSVを変換")
            print("  python convert_csv_delimiter.py <ファイルパス>     # 単一ファイルを変換")
            print("  python convert_csv_delimiter.py <入力ファイル> [出力ファイル]  # 単一ファイルを別名で保存")
            print("\n例:")
            print("  python convert_csv_delimiter.py")
            print("  python convert_csv_delimiter.py csv")
            print("  python convert_csv_delimiter.py csv/硫酸_Mn.csv")
