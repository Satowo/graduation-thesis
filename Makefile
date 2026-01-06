# 変数定義
MD_FILES = $(sort $(wildcard src/*.md))
OUTPUT_DIR = output
TEMPLATE = templates/reference.docx
# BIB_FILE = bib/references.bib
OUTPUT_NAME = graduation_thesis.docx

# 実行コマンド
PANDOC = pandoc
FLAGS = --reference-doc=$(TEMPLATE) \
        --filter pandoc-crossref \
        --citeproc \
        --toc \
		--toc-depth=3 \
		-M toc-title="目次" \
        -M reference-section-title="参考文献" \
        -M figureTitle="図" \
        -M tableTitle="表"

# デフォルトのターゲット
all: $(OUTPUT_NAME)

# docx生成
$(OUTPUT_NAME): $(MD_FILES)
	@mkdir -p $(OUTPUT_DIR)
	$(PANDOC) $(MD_FILES) $(FLAGS) -o $(OUTPUT_DIR)/$@
	@echo "---------------------------------------"
	@echo "変換完了: $(OUTPUT_DIR)/$(OUTPUT_NAME)"
	@echo "---------------------------------------"

# 掃除用コマンド
clean:
	rm -rf $(OUTPUT_DIR)/*

# 論文文字起こしコマンド
paper:
	source venv/bin/activate && python utils/pdf_to_text.py && deactivate

# グラフ作成コマンド
graph:
	source venv/bin/activate && python utils/convert_csv_delimiter.py && python utils/create_leaching_graph.py && deactivate

# CSV区切り文字変換コマンド（csvフォルダ内のすべてのCSVファイルをカンマ区切りに変換）
convert_csv:
	source venv/bin/activate && python utils/convert_csv_delimiter.py && deactivate