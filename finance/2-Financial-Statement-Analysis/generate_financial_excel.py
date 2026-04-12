from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "financial_analysis_template_bilingual.xlsx"


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""


ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""


WORKBOOK = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Data" sheetId="1" r:id="rId1" state="hidden"/>
    <sheet name="English" sheetId="2" r:id="rId2"/>
    <sheet name="Japanese" sheetId="3" r:id="rId3"/>
  </sheets>
</workbook>
"""


WORKBOOK_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>
"""


STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <fonts count="2">
    <font><sz val="11"/><name val="Calibri"/></font>
    <font><b/><sz val="11"/><name val="Calibri"/></font>
  </fonts>
  <fills count="3">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="D9EAF7"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="1">
    <border><left/><right/><top/><bottom/><diagonal/></border>
  </borders>
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>
  <cellXfs count="4">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="4" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
    <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
    <xf numFmtId="10" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
  </cellXfs>
  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>
</styleSheet>
"""


APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Excel</Application>
</Properties>
"""


CORE = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-04-12T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-04-12T00:00:00Z</dcterms:modified>
</cp:coreProperties>
"""


INPUT_ROWS = {4, 5, 7, 8, 10, 14, 15}


def inline_string(text: str) -> str:
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<c t="inlineStr"><is><t>{safe}</t></is></c>'


def number_cell(value: float, style: int = 1) -> str:
    return f'<c s="{style}"><v>{value}</v></c>'


def formula_cell(formula: str, style: int = 1) -> str:
    return f'<c s="{style}"><f>{formula}</f></c>'


def col_letter(index: int) -> str:
    result = ""
    n = index
    while n:
        n, rem = divmod(n - 1, 26)
        result = chr(65 + rem) + result
    return result


def sheet_ref(sheet_name: str, cell_ref: str) -> str:
    return f"'{sheet_name}'!{cell_ref}"


def row_xml(index: int, cells: list[str]) -> str:
    refs = []
    for col_idx, cell in enumerate(cells, start=1):
        refs.append(cell.replace("<c ", f'<c r="{col_letter(col_idx)}{index}" ', 1))
    return f'<row r="{index}">{"".join(refs)}</row>'


def build_data_sheet() -> str:
    rows = [
        row_xml(1, [inline_string("Data"), inline_string("Source values and formulas")]),
        row_xml(3, [inline_string("Balance Sheet Inputs"), inline_string("Amount"), inline_string("Key Ratios"), inline_string("Formula Result")]),
        row_xml(4, [inline_string("Current Assets"), number_cell(0)]),
        row_xml(5, [inline_string("Non-current Assets"), number_cell(0)]),
        row_xml(6, [inline_string("Total Assets"), formula_cell("SUM(B4:B5)")]),
        row_xml(7, [inline_string("Current Liabilities"), number_cell(0)]),
        row_xml(8, [inline_string("Non-current Liabilities"), number_cell(0)]),
        row_xml(9, [inline_string("Total Liabilities"), formula_cell("SUM(B7:B8)")]),
        row_xml(10, [inline_string("Equity"), number_cell(0)]),
        row_xml(11, [inline_string("Check: Liabilities + Equity"), formula_cell("B9+B10")]),
        row_xml(13, [inline_string("Income Statement Inputs"), inline_string("Amount"), inline_string("Ratio"), inline_string("Formula Result")]),
        row_xml(14, [inline_string("Revenue"), number_cell(0)]),
        row_xml(15, [inline_string("Net Income"), number_cell(0)]),
        row_xml(17, [inline_string("ROE Analysis"), inline_string("Amount"), inline_string("Ratio"), inline_string("Formula Result")]),
        row_xml(18, [inline_string("ROE"), inline_string(""), inline_string("ROE"), formula_cell('IF(B10=0,"",B15/B10)', 3)]),
        row_xml(19, [inline_string("ROA"), inline_string(""), inline_string("ROA"), formula_cell('IF(B6=0,"",B15/B6)', 3)]),
        row_xml(20, [inline_string("Net Profit Margin"), inline_string(""), inline_string("Net Profit Margin"), formula_cell('IF(B14=0,"",B15/B14)', 3)]),
        row_xml(21, [inline_string("Current Ratio"), inline_string(""), inline_string("Current Ratio"), formula_cell('IF(B7=0,"",B4/B7)')]),
        row_xml(22, [inline_string("Debt Ratio"), inline_string(""), inline_string("Debt Ratio"), formula_cell('IF(B6=0,"",B9/B6)', 3)]),
        row_xml(23, [inline_string("Debt to Equity"), inline_string(""), inline_string("Debt to Equity"), formula_cell('IF(B10=0,"",B9/B10)')]),
        row_xml(24, [inline_string("Asset Turnover"), inline_string(""), inline_string("Asset Turnover"), formula_cell('IF(B6=0,"",B14/B6)')]),
        row_xml(25, [inline_string("Equity Multiplier"), inline_string(""), inline_string("Equity Multiplier"), formula_cell('IF(B10=0,"",B6/B10)')]),
        row_xml(26, [inline_string("DuPont Check"), inline_string(""), inline_string("ROE via DuPont"), formula_cell("E20*E24*E25", 3)]),
    ]
    return build_sheet_xml(rows)


def build_english_sheet(labels: dict[str, str]) -> str:
    rows = [
        row_xml(1, [inline_string(labels["title"]), inline_string(labels["subtitle"])]),
        row_xml(3, [inline_string(labels["section_balance"]), inline_string(labels["amount"]), inline_string(labels["key_ratio"]), inline_string(labels["formula_result"])]),
    ]

    label_rows = {
        4: labels["current_assets"],
        5: labels["non_current_assets"],
        6: labels["total_assets"],
        7: labels["current_liabilities"],
        8: labels["non_current_liabilities"],
        9: labels["total_liabilities"],
        10: labels["equity"],
        11: labels["check_balance"],
        13: labels["section_income"],
        14: labels["revenue"],
        15: labels["net_income"],
        17: labels["section_roe"],
        18: labels["roe_row"],
        19: labels["roa_row"],
        20: labels["margin_row"],
        21: labels["current_ratio_row"],
        22: labels["debt_ratio_row"],
        23: labels["debt_equity_row"],
        24: labels["asset_turnover_row"],
        25: labels["equity_multiplier_row"],
        26: labels["dupont_row"],
    }

    ratio_names = {
        13: labels["ratio"],
        18: labels["roe"],
        19: labels["roa"],
        20: labels["margin"],
        21: labels["current_ratio"],
        22: labels["debt_ratio"],
        23: labels["debt_equity"],
        24: labels["asset_turnover"],
        25: labels["equity_multiplier"],
        26: labels["dupont"],
    }

    for row in range(4, 27):
        if row == 12 or row == 16:
            continue
        cells = [inline_string(label_rows.get(row, ""))]
        if row in {13, 17}:
            cells.append(inline_string(labels["amount"]))
            cells.append(inline_string(labels["ratio"]))
            cells.append(inline_string(labels["formula_result"]))
        else:
            cells.append(formula_cell(sheet_ref("Data", f"B{row}")))
        if row >= 18:
            cells.append(inline_string(ratio_names.get(row, "")))
            cells.append(formula_cell(sheet_ref("Data", f"E{row}"), 3 if row in {18, 19, 20, 22, 26} else 1))
        elif row in {3, 13, 17}:
            pass
        rows.append(row_xml(row, cells))

    return build_sheet_xml(rows)


def build_japanese_sheet(labels: dict[str, str]) -> str:
    rows = [
        row_xml(1, [inline_string(labels["title"]), inline_string(labels["subtitle"])]),
        row_xml(3, [inline_string(labels["section_balance"]), inline_string(labels["amount"]), inline_string(labels["key_ratio"]), inline_string(labels["formula_result"])]),
    ]

    label_rows = {
        4: labels["current_assets"],
        5: labels["non_current_assets"],
        6: labels["total_assets"],
        7: labels["current_liabilities"],
        8: labels["non_current_liabilities"],
        9: labels["total_liabilities"],
        10: labels["equity"],
        11: labels["check_balance"],
        13: labels["section_income"],
        14: labels["revenue"],
        15: labels["net_income"],
        17: labels["section_roe"],
        18: labels["roe_row"],
        19: labels["roa_row"],
        20: labels["margin_row"],
        21: labels["current_ratio_row"],
        22: labels["debt_ratio_row"],
        23: labels["debt_equity_row"],
        24: labels["asset_turnover_row"],
        25: labels["equity_multiplier_row"],
        26: labels["dupont_row"],
    }

    ratio_names = {
        18: labels["roe"],
        19: labels["roa"],
        20: labels["margin"],
        21: labels["current_ratio"],
        22: labels["debt_ratio"],
        23: labels["debt_equity"],
        24: labels["asset_turnover"],
        25: labels["equity_multiplier"],
        26: labels["dupont"],
    }

    for row in range(4, 27):
        if row == 12 or row == 16:
            continue
        cells = [inline_string(label_rows.get(row, ""))]
        if row in {13, 17}:
            cells.append(inline_string(labels["amount"]))
            cells.append(inline_string(labels["ratio"]))
            cells.append(inline_string(labels["formula_result"]))
        else:
            cells.append(formula_cell(sheet_ref("Data", f"B{row}")))
        if row >= 18:
            cells.append(inline_string(ratio_names.get(row, "")))
            cells.append(formula_cell(sheet_ref("Data", f"E{row}"), 3 if row in {18, 19, 20, 22, 26} else 1))
        rows.append(row_xml(row, cells))

    return build_sheet_xml(rows)


def build_sheet_xml(rows: list[str]) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="A1:E26"/>
  <sheetViews><sheetView workbookViewId="0"/></sheetViews>
  <sheetFormatPr defaultRowHeight="15"/>
  <cols>
    <col min="1" max="1" width="28" customWidth="1"/>
    <col min="2" max="2" width="16" customWidth="1"/>
    <col min="3" max="3" width="20" customWidth="1"/>
    <col min="4" max="5" width="18" customWidth="1"/>
  </cols>
  <sheetData>
    {''.join(rows)}
  </sheetData>
</worksheet>
"""


def create_workbook() -> None:
    with ZipFile(OUTPUT_FILE, "w", compression=ZIP_DEFLATED) as workbook:
        workbook.writestr("[Content_Types].xml", CONTENT_TYPES)
        workbook.writestr("_rels/.rels", ROOT_RELS)
        workbook.writestr("docProps/app.xml", APP)
        workbook.writestr("docProps/core.xml", CORE)
        workbook.writestr("xl/workbook.xml", WORKBOOK)
        workbook.writestr("xl/_rels/workbook.xml.rels", WORKBOOK_RELS)
        workbook.writestr("xl/styles.xml", STYLES)
        workbook.writestr("xl/worksheets/sheet1.xml", build_data_sheet())
        workbook.writestr("xl/worksheets/sheet2.xml", build_english_sheet(EN_LABELS))
        workbook.writestr("xl/worksheets/sheet3.xml", build_japanese_sheet(JA_LABELS))


EN_LABELS = {
    "title": "Financial Statement Analysis Template",
    "subtitle": "Both language sheets are linked to the same hidden Data sheet and stay synchronized.",
    "section_balance": "Balance Sheet Inputs",
    "amount": "Amount",
    "key_ratio": "Key Ratios",
    "formula_result": "Formula Result",
    "current_assets": "Current Assets",
    "non_current_assets": "Non-current Assets",
    "total_assets": "Total Assets",
    "current_liabilities": "Current Liabilities",
    "non_current_liabilities": "Non-current Liabilities",
    "total_liabilities": "Total Liabilities",
    "equity": "Equity",
    "check_balance": "Check: Liabilities + Equity",
    "section_income": "Income Statement Inputs",
    "ratio": "Ratio",
    "revenue": "Revenue",
    "net_income": "Net Income",
    "section_roe": "ROE Analysis",
    "roe_row": "ROE",
    "roa_row": "ROA",
    "margin_row": "Net Profit Margin",
    "current_ratio_row": "Current Ratio",
    "debt_ratio_row": "Debt Ratio",
    "debt_equity_row": "Debt to Equity",
    "asset_turnover_row": "Asset Turnover",
    "equity_multiplier_row": "Equity Multiplier",
    "dupont_row": "DuPont Check",
    "roe": "ROE",
    "roa": "ROA",
    "margin": "Net Profit Margin",
    "current_ratio": "Current Ratio",
    "debt_ratio": "Debt Ratio",
    "debt_equity": "Debt to Equity",
    "asset_turnover": "Asset Turnover",
    "equity_multiplier": "Equity Multiplier",
    "dupont": "ROE via DuPont",
}


JA_LABELS = {
    "title": "財務諸表分析テンプレート",
    "subtitle": "両方の言語シートは同じ非表示のDataシートに連動し、数値と結果が同期されます。",
    "section_balance": "貸借対照表入力",
    "amount": "金額",
    "key_ratio": "主要指標",
    "formula_result": "計算結果",
    "current_assets": "流動資産",
    "non_current_assets": "固定資産",
    "total_assets": "総資産",
    "current_liabilities": "流動負債",
    "non_current_liabilities": "固定負債",
    "total_liabilities": "総負債",
    "equity": "自己資本",
    "check_balance": "確認: 負債 + 自己資本",
    "section_income": "損益計算書入力",
    "ratio": "指標",
    "revenue": "売上高",
    "net_income": "当期純利益",
    "section_roe": "ROE分析",
    "roe_row": "ROE",
    "roa_row": "ROA",
    "margin_row": "売上高純利益率",
    "current_ratio_row": "流動比率",
    "debt_ratio_row": "負債比率",
    "debt_equity_row": "D/Eレシオ",
    "asset_turnover_row": "総資産回転率",
    "equity_multiplier_row": "財務レバレッジ",
    "dupont_row": "デュポン確認",
    "roe": "ROE",
    "roa": "ROA",
    "margin": "売上高純利益率",
    "current_ratio": "流動比率",
    "debt_ratio": "負債比率",
    "debt_equity": "D/Eレシオ",
    "asset_turnover": "総資産回転率",
    "equity_multiplier": "財務レバレッジ",
    "dupont": "デュポン式ROE",
}


if __name__ == "__main__":
    create_workbook()
    print(f"Created: {OUTPUT_FILE}")
