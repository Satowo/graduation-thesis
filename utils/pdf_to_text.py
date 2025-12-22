#!/usr/bin/env python3
"""
PDFファイルをテキストファイルに変換するユーティリティ

papersフォルダ内のPDFファイルを読み込み、テキストを抽出して
paper_textsフォルダに保存します。
"""

import os
from pathlib import Path
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDFがインストールされていません。以下のコマンドでインストールしてください:")
    print("pip install pymupdf")
    sys.exit(1)


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    PDFファイルからテキストを抽出する
    
    Args:
        pdf_path: PDFファイルのパス
        
    Returns:
        抽出されたテキスト文字列
    """
    try:
        doc = fitz.open(pdf_path)
        text_content = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text_content.append(text)
        
        doc.close()
        return "\n".join(text_content)
    
    except Exception as e:
        print(f"エラー: {pdf_path} の処理中に問題が発生しました: {e}")
        return ""


def convert_pdf_to_text(pdf_path: str, output_dir: str) -> bool:
    """
    単一のPDFファイルをテキストファイルに変換する
    
    Args:
        pdf_path: 入力PDFファイルのパス
        output_dir: 出力ディレクトリのパス
        
    Returns:
        変換が成功した場合True
    """
    pdf_file = Path(pdf_path)
    if not pdf_file.exists():
        print(f"警告: ファイルが見つかりません: {pdf_path}")
        return False
    
    # テキストを抽出
    text_content = extract_text_from_pdf(str(pdf_file))
    
    if not text_content.strip():
        print(f"警告: {pdf_path} からテキストを抽出できませんでした")
        return False
    
    # 出力ファイル名を生成（拡張子を.txtに変更）
    output_file = Path(output_dir) / f"{pdf_file.stem}.txt"
    
    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)
    
    # テキストファイルに保存
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"✓ {pdf_file.name} -> {output_file.name}")
        return True
    except Exception as e:
        print(f"エラー: {output_file} の保存中に問題が発生しました: {e}")
        return False


def convert_all_pdfs_in_papers_folder(
    papers_dir: str = "papers",
    output_dir: str = "paper_texts"
) -> None:
    """
    papersフォルダ内のすべてのPDFファイルをテキストファイルに変換する
    
    Args:
        papers_dir: PDFファイルが格納されているディレクトリ（デフォルト: "papers"）
        output_dir: テキストファイルの出力先ディレクトリ（デフォルト: "paper_texts"）
    """
    # プロジェクトルートを取得（このスクリプトがutilsフォルダにあることを想定）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    papers_path = project_root / papers_dir
    output_path = project_root / output_dir
    
    if not papers_path.exists():
        print(f"エラー: {papers_path} が見つかりません")
        return
    
    # PDFファイルを検索
    pdf_files = list(papers_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"警告: {papers_path} にPDFファイルが見つかりませんでした")
        return
    
    print(f"見つかったPDFファイル数: {len(pdf_files)}")
    print(f"出力先: {output_path}\n")
    
    # 各PDFファイルを処理
    success_count = 0
    for pdf_file in sorted(pdf_files):
        if convert_pdf_to_text(str(pdf_file), str(output_path)):
            success_count += 1
    
    print(f"\n処理完了: {success_count}/{len(pdf_files)} ファイルが正常に変換されました")


if __name__ == "__main__":
    convert_all_pdfs_in_papers_folder()

