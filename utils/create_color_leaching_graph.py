import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# スクリプトの場所を基準にプロジェクトルートを取得
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

def create_leaching_graph(csv_path=None, output_path=None):
    """
    浸出率のグラフを作成する
    
    Args:
        csv_path: CSVファイルのパス（Noneの場合はデフォルトパスを使用）
        output_path: 出力ファイルのパス（Noneの場合はプロジェクトルートに保存）
    """
    # デフォルトパスの設定
    if csv_path is None:
        csv_path = PROJECT_ROOT / "csv" / "硫酸_Mn.csv"
    else:
        csv_path = Path(csv_path)
    
    if output_path is None:
        output_path = PROJECT_ROOT / "graphs" / "硫酸_Mn_color.png"
    else:
        output_path = Path(output_path)
    
    # CSVファイルの存在確認
    if not csv_path.exists():
        raise FileNotFoundError(f"CSVファイルが見つかりません: {csv_path}")
    
    # 1. データの読み込み
    df = pd.read_csv(csv_path)
    
    # x軸の値を取得（空行を除外）
    x_values = df['x'].dropna().values
    num_x = len(x_values)
    
    # y軸の値をリスト化
    y_all = df['y'].values
    
    # 軸ラベルの取得（CSVの特定のセルから取得）
    y_label = df.iloc[0, 1] # Leaching ratio
    x_label = df.iloc[1, 1] # time(min)
    
    # 2. グラフの基本設定（ルール7: 白背景）
    plt.rcParams['font.family'] = 'sans-serif' # ルール4,5: ゴシック体/Sans Serif推奨
    fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    # カラー版: 色の違いで区別する
    styles = [
        {'color': '#1f77b4', 'ls': '-',  'marker': 'o'}, # 青・実線・円
        {'color': '#d62728', 'ls': '-',  'marker': 's'}, # 赤・実線・四角
        {'color': '#2ca02c', 'ls': '-',  'marker': '^'}, # 緑・実線・三角
        {'color': '#ff7f0e', 'ls': '-',  'marker': 'D'}, # オレンジ・実線・ひし形
        {'color': '#9467bd', 'ls': '-',  'marker': 'v'}, # 紫・実線・逆三角
        {'color': '#8c564b', 'ls': '-',  'marker': 'x'}, # 茶色・実線・バツ
        {'color': '#e377c2', 'ls': '-',  'marker': '+'}, # ピンク・実線・プラス
        {'color': '#7f7f7f', 'ls': '-',  'marker': '*'}, # グレー・実線・星
        {'color': '#bcbd22', 'ls': '-',  'marker': 'p'}, # オリーブ・実線・五角形
        {'color': '#17becf', 'ls': '-',  'marker': 'h'}, # シアン・実線・六角形
    ]

    # 3. 各シリーズのプロット
    # シリーズラベルの取得（空行を除外）
    series_labels = df['series'].dropna().values

    # yの値を上から順にxの数分ずつ分割してプロット
    for i in range(len(series_labels)):
        start_idx = i * num_x
        end_idx = start_idx + num_x
        series_y = y_all[start_idx:end_idx]
        
        # 横軸0、縦軸0の点を先頭に追加
        x_plot = np.concatenate([[0], x_values])
        y_plot = np.concatenate([[0], series_y])
        
        # マイナスの値を0にクリップ
        y_plot = np.maximum(y_plot, 0)
        
        ax.plot(x_plot, y_plot, 
                label=series_labels[i],
                linewidth=1.5,      # ルール7: 折れ線は太め(1.5pt)
                markersize=6,
                **styles[i % len(styles)])

    # 4. 軸と目盛りの設定
    # ルール10: 軸ラベルの設定。単位を忘れずに記載。
    ax.set_xlabel(x_label, fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    
    # ルール31: 目盛りの数字は太字にしない
    ax.tick_params(axis='both', labelsize=12, width=0.5) # ルール7: 目盛り線は細く
    
    # 目盛りの位置を調整（原点で交差するように）
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    
    # 縦軸の範囲設定：マイナスの値は0にクリップされるため、常に0を下限とする
    ax.set_ylim(bottom=0)
    
    # 横軸の範囲設定：0を下限とする
    ax.set_xlim(left=0)
    
    # 軸を原点(0,0)に配置
    ax.spines['left'].set_position(('data', 0))
    ax.spines['bottom'].set_position(('data', 0))
    
    # 右側と上側の軸を非表示にする
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # 枠線の太さ設定（ルール7: 基準線は目盛り線より少し太く）
    for spine in ax.spines.values():
        spine.set_linewidth(0.8)

    # 5. 凡例の設定
    # ルール6: 凡例はグラフの上段に配置
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),
              ncol=3, frameon=False, fontsize=12)

    # 6. タイトルの配置（ルール8: 図のタイトルは図の下に書く）
    # タイトルはコード外（本文）で付けるのが一般的ですが、配置を確保するために余白を調整
    plt.tight_layout()
    
    # 保存（論文用なので高解像度pngまたはpdf/eps）
    output_path.parent.mkdir(parents=True, exist_ok=True)  # ディレクトリが存在しない場合は作成
    plt.savefig(str(output_path), bbox_inches='tight', dpi=300)
    plt.close()  # メモリリークを防ぐためにグラフを閉じる

    print(f"グラフを保存しました: {output_path}")
    print("図1 浸出率の経時変化") # ルール11: 体言止め、ルール8: 図の下にタイトル


def create_all_leaching_graphs(csv_folder=None, output_folder=None):
    """
    csvフォルダ内のすべてのCSVファイルからグラフを作成する
    
    Args:
        csv_folder: CSVファイルが格納されているフォルダのパス（Noneの場合はデフォルトでcsvフォルダ）
        output_folder: グラフの出力先フォルダ（Noneの場合はデフォルトでgraphsフォルダ）
    
    Returns:
        list: 作成されたグラフファイルのパスのリスト
    """
    if csv_folder is None:
        csv_folder = PROJECT_ROOT / "csv"
    else:
        csv_folder = Path(csv_folder)
    
    if output_folder is None:
        output_folder = PROJECT_ROOT / "graphs"
    else:
        output_folder = Path(output_folder)
    
    if not csv_folder.is_dir():
        raise NotADirectoryError(f"指定されたパスはディレクトリではありません: {csv_folder}")
    
    # CSVファイルを検索
    csv_files = list(csv_folder.glob("*.csv"))
    
    if not csv_files:
        print(f"フォルダ内にCSVファイルが見つかりませんでした: {csv_folder}")
        return []
    
    print(f"見つかったCSVファイル: {len(csv_files)}個")
    print("-" * 50)
    
    created_graphs = []
    for csv_file in csv_files:
        try:
            # 出力ファイル名を生成（CSVファイル名から拡張子を除いて_color.pngに変更）
            output_filename = csv_file.stem + "_color.png"
            output_path = output_folder / output_filename
            
            print(f"処理中: {csv_file.name}")
            create_leaching_graph(csv_file, output_path)
            created_graphs.append(output_path)
            print()
        except Exception as e:
            print(f"エラー: {csv_file.name} のグラフ作成に失敗しました: {e}")
            print()
    
    print("-" * 50)
    print(f"グラフ作成完了: {len(created_graphs)}/{len(csv_files)}個のファイル")
    return created_graphs


if __name__ == "__main__":
    # csvフォルダ内のすべてのCSVファイルからグラフを作成
    create_all_leaching_graphs()