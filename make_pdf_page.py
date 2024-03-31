
import json
from pdfrw import PdfReader, PdfWriter
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, portrait
from pdfrw import PdfReader, PdfWriter
from typing import Dict, Any

# 1ページ分のPDFを作成する関数
# writer: PdfWriterオブジェクト
# font_name: 使用するフォント名
# pdf_page: 元のPDFの1ページ
# data_page: OCR結果の1ページ
def make_page(writer: PdfWriter, font_name: str, pdf_page: Any, data_page: Dict[str, Any]) -> None:
    # 中間生成物ファイル名
    tmp_file = r"C:/progs/python/ocr/env/img/work.pdf"

    # OCR結果のjsonデータからページサイズを取得
    page_width = data_page["width"]
    page_height = data_page["height"]
    pagesize = (page_width * inch, page_height * inch)

    # ここで定義したpdfにOCR結果を重畳して、tmp_fileに保存する
    pdf = canvas.Canvas(tmp_file, pagesize = pagesize)

    # 既存のPDFページをオブジェクト化
    pp = pagexobj(pdf_page)
    # 既存のPDFページを描画
    pdf.doForm(makerl(pdf,pp))

    # フォント設定
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))
    pdf.setFont(font_name, 8)

    # テキスト書き込み
    for line_num, line in enumerate(data_page["lines"]):
        # テキスト始点座標
        (pos_x,pos_y) = (line["boundingBox"][6], line["boundingBox"][7])

        # テキストボックスサイズ
        box_width = line["boundingBox"][2]-line["boundingBox"][0]
        box_height = line["boundingBox"][7]-line["boundingBox"][1]

        # 色指定
        pdf.setFillColorRGB(1,1,1,0)
        # テキストボックスの枠線
        pdf.setStrokeColorRGB(1,0,0,1)

        # テキストボックス描画
        pdf.setStrokeColorRGB(0,1,0,1)
        pdf.rect(
            pos_x * inch, # ここでx方向の位置を調整する
            (page_height - pos_y) * inch, # ここでy方向の位置を調整する
            box_width * inch, # ここでx方向の位置を調整する
            box_height * inch, # ここでy方向の位置を調整する
            stroke = 1, # 枠線を描画する
            fill = 1 # 塗りつぶす
        )

        # 色指定
        pdf.setFillColorRGB(0,0,1,1) # 青色
        # テキスト番号表示
        pdf.drawString(
            (pos_x - 0.3) * inch, # ここでx方向の位置を調整する
            (page_height - pos_y + 0.2) * inch, # ここでy方向の位置を調整する
            "L:" + str(line_num)
        )

        # テキスト
        text = line["text"]
        # 色指定
        pdf.setFillColorRGB(1,0,0,1) # 赤色
        # テキストを描画する
        pdf.drawString(
            pos_x * inch,  # ここでx方向の位置を調整する
            (page_height - pos_y + box_height) * inch, # ここでy方向の位置を調整する
            text
        )

    pdf.showPage()
    pdf.save()

    # 中間生成のPDFファイルを読み込む
    with open(tmp_file, mode="rb") as f:
        pdf_reader = PdfReader(f)

    # 中間生成PDFをwriterに取り込む
    writer.addPage(pdf_reader.pages[0])
