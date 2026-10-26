"""Genera el libro Excel de Cafetería Aurora con fórmulas vivas.

Uso:
    python scripts/build_workbook.py

Las únicas celdas escritas son los supuestos de ``Supuestos``, ``Productos``,
``Personal`` y ``Costos`` (más metadatos de ``Portada`` y selectores). Las
hojas de escenario y el resumen se construyen con fórmulas.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

from openpyxl import Workbook
from openpyxl.chart import BarChart, DoughnutChart, LineChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.model import load_model  # noqa: E402

MODEL_PATH = ROOT / "data" / "model.json"
WORKBOOK_PATH = ROOT / "docs" / "assets" / "Cafeteria-Aurora-Modelo-Financiero.xlsx"

MONTH_COLS = [get_column_letter(3 + index) for index in range(36)]
YEAR_COLS = ["AM", "AN", "AO"]
TOTAL_COL = "AP"
MONTH_NAMES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
SCENARIO_SHEETS = {
    "pessimistic": ("Pesimista", 1),
    "base": ("Base", 2),
    "optimistic": ("Optimista", 3),
}

CREAM = "F7F1E7"
PAPER = "FFFDF9"
ESPRESSO = "2B1D16"
INK = "1C1917"
TERRACOTTA = "C4623B"
SAGE = "7C8B6F"
SAGE_STRONG = "5E6B52"
GOLD = "C9A227"
GOLD_STRONG = "806410"
MUTED = "6F6259"
LINE = "E4D8C8"
INPUT_FILL = "FFF4D6"
INPUT_FONT = "1F4E79"
CHECK_GREEN = "E2EFDA"
CHECK_RED = "FCE4D6"
NEGATIVE = "A33A2B"
NEGATIVE_BG = "F8E7E2"

FMT_EUR = '#,##0 €'
FMT_EUR2 = '#,##0.00 €'
FMT_PCT = '0.0%'
FMT_PCT2 = '0.00%'
FMT_TICKETS = '0.0'
FMT_INDEX = '0.000'
FMT_DATE = 'dd/mm/yyyy'
FMT_MONTH = 'mmm-yy'
FMT_DSCR = '0.00"x"'
FMT_INT = '#,##0'

THIN = Side(style="thin", color=LINE)
MEDIUM = Side(style="medium", color=ESPRESSO)
BORDER_THIN = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
BORDER_TOP = Border(top=MEDIUM)


def font(size: int = 10, bold: bool = False, color: str = ESPRESSO, italic: bool = False, name: str = "Calibri") -> Font:
    return Font(name=name, size=size, bold=bold, color=color, italic=italic)


def fill(color: str) -> PatternFill:
    return PatternFill(fill_type="solid", fgColor=color)


def style_input(cell) -> None:
    cell.fill = fill(INPUT_FILL)
    cell.font = font(color=INPUT_FONT)
    cell.border = BORDER_THIN
    cell.alignment = Alignment(horizontal="right")


def style_calc(cell) -> None:
    cell.fill = fill(PAPER)
    cell.font = font(color=ESPRESSO)
    cell.border = Border()


def style_total(cell) -> None:
    cell.fill = fill(CREAM)
    cell.font = font(bold=True)
    cell.border = BORDER_TOP


def style_section(ws, row: int, title: str, last_col: str = "AP") -> None:
    ws.merge_cells(f"A{row}:{last_col}{row}")
    cell = ws[f"A{row}"]
    cell.value = title.upper()
    cell.fill = fill(TERRACOTTA)
    cell.font = font(bold=True, color=PAPER)
    cell.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 20
    for column in range(1, column_index_from_string(last_col) + 1):
        ws.cell(row=row, column=column).fill = fill(TERRACOTTA)


def style_table_header(ws, row: int, start_col: int = 1, end_col: int | None = None) -> None:
    end_col = end_col or ws.max_column
    for column in range(start_col, end_col + 1):
        cell = ws.cell(row=row, column=column)
        cell.fill = fill(ESPRESSO)
        cell.font = font(bold=True, color=PAPER)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER_THIN


def style_check(cell) -> None:
    cell.fill = fill(CHECK_GREEN)
    cell.font = font(bold=True, color=SAGE_STRONG)
    cell.border = BORDER_THIN


def page_setup(ws, landscape: bool = True, repeat_rows: str | None = None) -> None:
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    if repeat_rows:
        ws.print_title_rows = repeat_rows
    ws.oddHeader.center.text = "Cafetería Aurora — Modelo 2026–2028"
    ws.oddFooter.center.text = "Página &P de &N"
    ws.print_options.gridLines = False


def _set_widths(ws, widths: dict[str, float]) -> None:
    for column, width in widths.items():
        ws.column_dimensions[column].width = width


def _money(value: float) -> float:
    return round(float(value), 2)


class WorkbookBuilder:
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        self._names: dict[str, str] = {}

    # ----------------------------------------------------------------- helpers
    def _add_name(self, name: str, sheet: str, reference: str) -> None:
        full = f"{sheet}!{reference}"
        self._names[name] = full
        self.wb.defined_names.add(DefinedName(name, attr_text=full))

    def _write_label(self, ws, row: int, label: str, unit: str = "", *, section: bool = False) -> None:
        ws[f"A{row}"] = label
        ws[f"A{row}"].font = font(bold=bool(section))
        ws[f"A{row}"].alignment = Alignment(vertical="center")
        if unit:
            ws[f"B{row}"] = unit
            ws[f"B{row}"].font = font(size=9, color=MUTED, italic=True)
            ws[f"B{row}"].alignment = Alignment(horizontal="left")

    def _write_month_header(self, ws, row: int, label: str = "Concepto") -> None:
        ws[f"A{row}"] = label
        ws[f"B{row}"] = "Unidad"
        style_table_header(ws, row, 1, 42)
        for index, column in enumerate(MONTH_COLS):
            cell = ws[f"{column}{row}"]
            cell.value = MONTH_NAMES[index] if index < 12 else MONTH_NAMES[index % 12] + f" {index // 12 + 26}"
        for column in YEAR_COLS:
            ws[f"{column}{row}"] = f"Total {2026 + YEAR_COLS.index(column)}"
        ws[f"{TOTAL_COL}{row}"] = "Trienio"
        style_table_header(ws, row, 1, 42)

    def _row_formula(
        self,
        ws,
        row: int,
        label: str,
        unit: str,
        formula: str | Callable[[str, int], str],
        fmt: str,
        *,
        annual: str = "sum",
        total: str = "sum",
        bold: bool = False,
        style_inputs: bool = False,
    ) -> None:
        """Escribe una fila mensual y sus totales anuales.

        ``formula`` puede ser una plantilla con ``{c}``, ``{i}`` y ``{y}``.
        """
        self._write_label(ws, row, label, unit)
        for index, column in enumerate(MONTH_COLS):
            value = formula.format(c=column, i=index + 1, y=index // 12 + 1) if isinstance(formula, str) else formula(column, index + 1)
            cell = ws[f"{column}{row}"]
            cell.value = value
            style_calc(cell)
            cell.number_format = fmt
            cell.alignment = Alignment(horizontal="right")
            if bold:
                cell.font = font(bold=True)
        if annual != "none":
            for year_index, column in enumerate(YEAR_COLS):
                first = MONTH_COLS[year_index * 12]
                last = MONTH_COLS[year_index * 12 + 11]
                cell = ws[f"{column}{row}"]
                if annual == "sum":
                    cell.value = f"=SUM({first}{row}:{last}{row})"
                elif annual == "december":
                    cell.value = f"={last}{row}"
                elif annual == "margin":
                    numerator = {"AM": "AM", "AN": "AN", "AO": "AO"}[column]
                    cell.value = f"=IFERROR({numerator}{row - 16 if row in (33, 34, 35) else row}/{'AM' if column == 'AM' else 'AN' if column == 'AN' else 'AO'}15,0)"
                style_calc(cell)
                cell.number_format = fmt
                cell.alignment = Alignment(horizontal="right")
                if bold:
                    cell.font = font(bold=True)
        if total != "none":
            cell = ws[f"{TOTAL_COL}{row}"]
            if total == "sum":
                cell.value = f"=SUM(AM{row}:AO{row})"
            elif total == "last":
                cell.value = f"=AO{row}"
            style_calc(cell)
            cell.number_format = fmt
            cell.alignment = Alignment(horizontal="right")
            if bold:
                cell.font = font(bold=True)

    def _set_data_validation(self, ws, cell_range: str, formula1: str, formula2: str | None = None) -> None:
        validation = DataValidation(
            type="whole",
            operator="between" if formula2 is not None else "equal",
            formula1=formula1,
            formula2=formula2,
            allow_blank=False,
        )
        validation.error = "Selecciona un escenario entre 1 y 3."
        validation.errorTitle = "Selector no válido"
        validation.prompt = "1 = Pesimista, 2 = Base, 3 = Optimista"
        validation.promptTitle = "Escenario"
        ws.add_data_validation(validation)
        validation.add(cell_range)

    # ----------------------------------------------------------------- portada
    def build_portada(self) -> None:
        ws = self.wb.create_sheet("Portada")
        ws.sheet_properties.tabColor = ESPRESSO
        ws.sheet_view.showGridLines = False
        _set_widths(ws, {"A": 3, "B": 26, "C": 92, "D": 3})
        ws["B2"] = "Cafetería Aurora"
        ws["B2"].font = font(size=30, bold=True, color=ESPRESSO)
        ws["B3"] = "Modelo financiero 2026–2028"
        ws["B3"].font = font(size=17, bold=False, color=TERRACOTTA)
        ws["B4"] = "Café de especialidad · Zaragoza · EUR"
        ws["B4"].font = font(size=11, color=MUTED)

        ws["B6"] = "QUÉ ES ESTE LIBRO"
        ws["B6"].font = font(size=11, bold=True, color=TERRACOTTA)
        ws["B7"] = (
            "Un modelo mensual de 36 meses, tres escenarios (Pesimista, Base y Optimista), "
            "cuenta de resultados, caja, deuda, impuestos, punto de equilibrio y payback. "
            "Todas las celdas blancas son fórmulas: cambia una celda amarilla y el libro se recalcula."
        )
        ws["B7"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells("B7:C8")

        ws["B10"] = "CÓMO USARLO"
        ws["B10"].font = font(size=11, bold=True, color=TERRACOTTA)
        steps = [
            "1. Elige el escenario en Resumen B4 (1 Pesimista, 2 Base, 3 Optimista).",
            "2. Cambia solo las celdas amarillas de Supuestos, Productos, Personal y Costos.",
            "3. No edites celdas blancas: son fórmulas vivas.",
            "4. Revisa los checks verdes de Supuestos y de cada hoja de escenario.",
            "5. Descarga la versión web y la guía desde el README del repositorio.",
        ]
        for offset, text in enumerate(steps):
            ws[f"B{11 + offset}"] = text
            ws[f"B{11 + offset}"].font = font(size=10)
            ws[f"B{11 + offset}"].alignment = Alignment(vertical="center")

        ws["B17"] = "LEYENDA"
        ws["B17"].font = font(size=11, bold=True, color=TERRACOTTA)
        ws["B18"] = "Entrada editable"
        style_input(ws["B18"])
        ws["C18"] = "Celda amarilla: puedes cambiarla. Solo en las hojas de entrada y selectores."
        ws["B19"] = "Fórmula (no editar)"
        ws["B19"].fill = fill(PAPER)
        ws["B19"].border = BORDER_THIN
        ws["C19"] = "Celda blanca: se recalcula. Si la sobrescribes, rompes la trazabilidad."
        ws["B20"] = "Check"
        ws["B20"].value = "OK"
        style_check(ws["B20"])
        ws["C20"] = "Verde si cuadra; rojo si hay que revisar."
        for row in (18, 19, 20):
            ws[f"C{row}"].font = font(size=10, color=MUTED)

        ws["B22"] = "FUENTE DE VERDAD"
        ws["B22"].font = font(size=11, bold=True, color=TERRACOTTA)
        ws["B23"] = "data/model.json"
        ws["B23"].font = font(size=11, bold=True, color=ESPRESSO)
        ws["C23"] = "El contrato de supuestos. El libro, el sitio y los tests se generan desde él."
        ws["C23"].font = font(size=10, color=MUTED)

        ws["B25"] = "Versión"
        ws["B25"].font = font(bold=True)
        ws["C25"] = "1.0 · 25/10/2026"
        ws["B26"] = "Autor"
        ws["B26"].font = font(bold=True)
        ws["C26"] = "Cafetería Aurora · modelo educativo"
        ws["B27"] = "Aviso"
        ws["B27"].font = font(bold=True, color=NEGATIVE)
        ws["C27"] = "Este modelo es educativo. No es asesoramiento financiero, fiscal ni legal."
        ws["C27"].font = font(size=10, color=NEGATIVE)
        page_setup(ws, landscape=False)

    # ----------------------------------------------------------------- supuestos
    def build_supuestos(self) -> None:
        ws = self.wb.create_sheet("Supuestos")
        ws.sheet_properties.tabColor = SAGE
        _set_widths(ws, {"A": 44, "B": 15, "C": 12, **{get_column_letter(4 + i): 11 for i in range(9)}, "M": 11, "N": 11, "O": 12})
        ws.sheet_view.showGridLines = True
        ws["A1"] = "Supuestos"
        ws["A1"].font = font(size=18, bold=True)
        ws["A2"] = "Todo lo que se puede cambiar vive aquí. Las celdas amarillas son entradas; los checks, fórmulas."
        ws["A2"].font = font(size=10, color=MUTED)

        style_section(ws, 4, "Identidad y calendario", "O")
        identity = [
            ("Nombre", self.data["meta"]["name"], None),
            ("Moneda", self.data["meta"]["currency"], None),
            ("Inicio", self.data["calendar"]["start"], "date"),
            ("Meses", self.data["calendar"]["months"], "int"),
            ("Año base", self.data["calendar"]["years"][0], "int"),
            ("Modelo", "Mensual, 36 meses", None),
        ]
        for offset, (label, value, kind) in enumerate(identity, start=5):
            self._write_label(ws, offset, label)
            cell = ws[f"B{offset}"]
            cell.value = value
            if kind == "date":
                from datetime import date

                cell.value = date.fromisoformat(value)
                cell.number_format = FMT_DATE
            elif kind == "int":
                cell.number_format = FMT_INT
            style_input(cell)

        style_section(ws, 12, "Demanda", "O")
        demand = [
            ("Tickets/día en régimen", "tickets/día", self.data["calendar"]["baseTicketsPerDay"], FMT_TICKETS, True),
            ("Ítems por ticket", "ítems", self.data["calendar"]["itemsPerTicket"], "0.00", True),
            ("Días operativos al año", "días", None, FMT_INT, False),
        ]
        for offset, (label, unit, value, fmt, is_input) in enumerate(demand, start=13):
            self._write_label(ws, offset, label, unit)
            cell = ws[f"B{offset}"]
            if value is None:
                cell.value = "=SUM(C20:N20)"
                style_calc(cell)
            else:
                cell.value = value
                style_input(cell)
            cell.number_format = fmt

        style_section(ws, 17, "Estacionalidad, días operativos y rampa", "O")
        ws["A18"] = "Concepto"
        ws["B18"] = "Unidad"
        ws["O18"] = "Total"
        for index, column in enumerate([get_column_letter(3 + i) for i in range(12)]):
            ws[f"{column}18"] = MONTH_NAMES[index]
        style_table_header(ws, 18, 1, 15)
        rows = [
            ("Estacionalidad", "factor", self.data["calendar"]["seasonality"], FMT_INDEX, "=SUM(C19:N19)"),
            ("Días operativos", "días", self.data["calendar"]["openingDays"], FMT_INT, "=SUM(C20:N20)"),
            ("Rampa año 1", "factor", self.data["calendar"]["ramp"], FMT_INDEX, "=SUM(C21:N21)/12"),
        ]
        for offset, (label, unit, values, fmt, total) in enumerate(rows, start=19):
            self._write_label(ws, offset, label, unit)
            for index, value in enumerate(values):
                cell = ws[f"{get_column_letter(3 + index)}{offset}"]
                cell.value = value
                style_input(cell)
                cell.number_format = fmt
            ws[f"O{offset}"] = total
            style_calc(ws[f"O{offset}"])
            ws[f"O{offset}"].number_format = fmt
        ws["A22"] = "Nota: la estacionalidad suma 12,00 y los días 312. La rampa solo se aplica en 2026."
        ws["A22"].font = font(size=9, italic=True, color=MUTED)

        style_section(ws, 25, "Matriz de escenarios", "O")
        headers = ["#", "Variable", "Unidad", "Pesimista", "Base", "Optimista"]
        for index, value in enumerate(headers, start=1):
            ws.cell(row=26, column=index, value=value)
        style_table_header(ws, 26, 1, 6)
        scenario_rows = [
            ("Factor de demanda año 1", "×", "demandFactor", "0.00"),
            ("Crecimiento anual de demanda", "%", "demandGrowth", FMT_PCT),
            ("Crecimiento anual de precios", "%", "priceGrowth", FMT_PCT),
            ("Inflación anual de costes de producto", "%", "productCostInflation", FMT_PCT),
            ("Factor de personal", "×", "personnelFactor", "0.00"),
            ("Factor de alquiler", "×", "rentFactor", "0.00"),
            ("Inflación de suministros y servicios", "%", "servicesInflation", FMT_PCT),
            ("Marketing variable", "% ingresos", "marketingPct", FMT_PCT),
            ("Factor de otros gastos", "×", "otherOpexFactor", "0.00"),
            ("Crecimiento de otros gastos", "%", "otherOpexGrowth", FMT_PCT),
        ]
        for row, (label, unit, key, fmt) in enumerate(scenario_rows, start=27):
            ws[f"A{row}"] = row - 26
            ws[f"A{row}"].font = font(color=MUTED)
            ws[f"A{row}"].alignment = Alignment(horizontal="center")
            ws[f"B{row}"] = label
            ws[f"B{row}"].font = font()
            ws[f"C{row}"] = unit
            ws[f"C{row}"].font = font(size=9, color=MUTED, italic=True)
            for column, scenario_key in zip(("D", "E", "F"), ("pessimistic", "base", "optimistic")):
                cell = ws[f"{column}{row}"]
                cell.value = self.data["scenarios"][scenario_key][key]
                style_input(cell)
                cell.number_format = fmt
        ws["A37"] = "Excepción intencional: marketing variable es más bajo en Pesimista (2 %) porque es una respuesta de gestión, no un coste externo."
        ws["A37"].font = font(size=9, italic=True, color=MUTED)

        style_section(ws, 40, "Financiación y caja inicial", "O")
        financing_rows = [
            ("Equity aportado", "€", self.data["financing"]["equity"], FMT_EUR, True),
            ("Préstamo", "€", self.data["financing"]["loanAmount"], FMT_EUR, True),
            ("Tipo nominal anual", "%", self.data["financing"]["loanRate"], FMT_PCT, True),
            ("Plazo", "meses", self.data["financing"]["loanMonths"], FMT_INT, True),
            ("Caja de apertura", "€", self.data["financing"]["openingCash"], FMT_EUR, True),
            ("Stock inicial (capital circulante t0)", "€", self.data["financing"]["initialStock"], FMT_EUR, True),
            ("Caja mínima de política", "€", self.data["financing"]["minimumCash"], FMT_EUR, True),
            ("Cuota mensual del préstamo", "€", None, FMT_EUR2, False),
        ]
        for offset, (label, unit, value, fmt, is_input) in enumerate(financing_rows, start=41):
            self._write_label(ws, offset, label, unit)
            cell = ws[f"B{offset}"]
            if value is None:
                cell.value = "=PMT(B43/12,B44,-B42)"
                style_calc(cell)
            else:
                cell.value = value
                style_input(cell)
            cell.number_format = fmt
        ws["A49"] = "La caja de apertura y el stock son usos financiados con equity y deuda; no son ingresos."
        ws["A49"].font = font(size=9, italic=True, color=MUTED)

        style_section(ws, 52, "Fiscalidad y capital circulante", "O")
        tax_rows = [
            ("Tipo de sociedades", "%", self.data["tax"]["corporateRate"], FMT_PCT, True),
            ("Días de inventario", "días", self.data["workingCapital"]["inventoryDays"], FMT_INT, True),
            ("Días de proveedor", "días", self.data["workingCapital"]["payableDays"], FMT_INT, True),
            ("Días de cobro", "días", self.data["workingCapital"]["receivableDays"], FMT_INT, True),
        ]
        for offset, (label, unit, value, fmt, is_input) in enumerate(tax_rows, start=53):
            self._write_label(ws, offset, label, unit)
            cell = ws[f"B{offset}"]
            cell.value = value
            style_input(cell)
            cell.number_format = fmt
        ws["A57"] = "Pérdidas compensables sin límite por ser pyme (<1 M€). Provisión mensual = cuota anual / 12."
        ws["A57"].font = font(size=9, italic=True, color=MUTED)

        style_section(ws, 60, "Crecimientos estructurales", "O")
        growth = [
            ("Crecimiento anual del alquiler", "%", self.data["fixedCosts"]["rentGrowth"], FMT_PCT),
            ("Crecimiento anual del marketing fijo", "%", self.data["fixedCosts"]["fixedMarketingGrowth"], FMT_PCT),
        ]
        for offset, (label, unit, value, fmt) in enumerate(growth, start=61):
            self._write_label(ws, offset, label, unit)
            cell = ws[f"B{offset}"]
            cell.value = value
            style_input(cell)
            cell.number_format = fmt
        ws["A63"] = "La inflación de precios, costes y servicios vive en la matriz de escenarios; aquí solo los crecimientos estructurales."
        ws["A63"].font = font(size=9, italic=True, color=MUTED)

        style_section(ws, 65, "Controles de integridad", "O")
        ws["A66"] = "Check"
        ws["B66"] = "Valor"
        ws["C66"] = "Estado"
        style_table_header(ws, 66, 1, 3)
        checks = [
            (67, "Mix de producto (debe ser 100 %)", "=SUM(Productos!H5:H12)", FMT_PCT, '=IF(ABS(B67-1)<0.0001,"OK","Revisar")'),
            (68, "Estacionalidad (debe ser 12,00)", "=SUM(C19:N19)", "0.00", '=IF(ABS(B68-12)<0.0001,"OK","Revisar")'),
            (69, "Días operativos (deben ser 312)", "=SUM(C20:N20)", FMT_INT, '=IF(B69=312,"OK","Revisar")'),
            (70, "Capex inicial (debe ser 132.000 €)", "=Costos!B21", FMT_EUR, '=IF(B70=132000,"OK","Revisar")'),
            (71, "Fuentes = usos", "=B41+B42", FMT_EUR, '=IF(B71=Costos!B30,"OK","Revisar")'),
            (72, "Orden de escenarios (demanda y precio)", '=IF(AND(D27<E27,E27<F27,D28<E28,E28<F28,D29<E29,E29<F29),"OK","Revisar orden")', "@", None),
            (73, "Orden de costes (inverso)", '=IF(AND(D30>E30,E30>F30,D31>E31,E31>F31,D32>E32,E32>F32,D34>E34,E34>F34,D35>E35,E35>F35,D36>E36,E36>F36),"OK","Revisar orden")', "@", None),
        ]
        for row, label, formula, fmt, status in checks:
            ws[f"A{row}"] = label
            ws[f"A{row}"].font = font()
            ws[f"B{row}"] = formula
            style_calc(ws[f"B{row}"])
            if fmt != "@":
                ws[f"B{row}"].number_format = fmt
            if status:
                ws[f"C{row}"] = status
                style_check(ws[f"C{row}"])
        ws["A75"] = "Si algún check dice «Revisar», no uses las cifras: corrige la entrada."
        ws["A75"].font = font(size=9, italic=True, color=MUTED)
        ws["A75"].fill = fill(CHECK_GREEN)
        page_setup(ws, landscape=False)

        # Nombres definidos
        self._add_name("BaseTicketsDay", "Supuestos", "$B$13")
        self._add_name("ItemsPerTicket", "Supuestos", "$B$14")
        self._add_name("Seasonality", "Supuestos", "$C$19:$N$19")
        self._add_name("OpeningDays", "Supuestos", "$C$20:$N$20")
        self._add_name("Ramp", "Supuestos", "$C$21:$N$21")
        self._add_name("ScenarioMatrix", "Supuestos", "$D$27:$F$36")
        self._add_name("Equity", "Supuestos", "$B$41")
        self._add_name("LoanAmount", "Supuestos", "$B$42")
        self._add_name("LoanRate", "Supuestos", "$B$43")
        self._add_name("LoanMonths", "Supuestos", "$B$44")
        self._add_name("OpeningCash", "Supuestos", "$B$45")
        self._add_name("WC0", "Supuestos", "$B$46")
        self._add_name("MinCash", "Supuestos", "$B$47")
        self._add_name("LoanPayment", "Supuestos", "$B$48")
        self._add_name("TaxRate", "Supuestos", "$B$53")
        self._add_name("InventoryDays", "Supuestos", "$B$54")
        self._add_name("PayableDays", "Supuestos", "$B$55")
        self._add_name("ReceivableDays", "Supuestos", "$B$56")
        self._add_name("RentGrowth", "Supuestos", "$B$61")
        self._add_name("FixedMarketingGrowth", "Supuestos", "$B$62")

    # ----------------------------------------------------------------- productos
    def build_productos(self) -> None:
        ws = self.wb.create_sheet("Productos")
        ws.sheet_properties.tabColor = SAGE
        _set_widths(ws, {"A": 5, "B": 24, "C": 18, "D": 10, "E": 8, "F": 12, "G": 12, "H": 8, "I": 8, "J": 13, "K": 13, "L": 11, "M": 13, "N": 10})
        ws["A1"] = "Productos"
        ws["A1"].font = font(size=18, bold=True)
        ws["A2"] = "PVP con IVA en la carta; precio neto y coste ajustado por merma en el modelo."
        ws["A2"].font = font(size=10, color=MUTED)
        headers = ["#", "Producto", "Categoría", "PVP", "IVA", "Precio neto", "Coste unitario", "Mix", "Merma", "Coste ajustado", "Margen unitario", "Margen %", "Contribución", "Check PVP"]
        for index, value in enumerate(headers, start=1):
            ws.cell(row=4, column=index, value=value)
        style_table_header(ws, 4, 1, 14)
        for offset, product in enumerate(self.data["products"], start=5):
            ws[f"A{offset}"] = offset - 4
            ws[f"A{offset}"].font = font(color=MUTED)
            ws[f"B{offset}"] = product["name"]
            ws[f"C{offset}"] = product["category"]
            ws[f"D{offset}"] = product["pvp"]
            ws[f"E{offset}"] = product["vat"]
            ws[f"F{offset}"] = f"=D{offset}/(1+E{offset})"
            ws[f"G{offset}"] = product["unitCost"]
            ws[f"H{offset}"] = product["mix"]
            ws[f"I{offset}"] = product["waste"]
            ws[f"J{offset}"] = f"=G{offset}/(1-I{offset})"
            ws[f"K{offset}"] = f"=F{offset}-J{offset}"
            ws[f"L{offset}"] = f"=IFERROR(K{offset}/F{offset},0)"
            ws[f"M{offset}"] = f"=F{offset}*H{offset}"
            ws[f"N{offset}"] = f"=IF(F{offset}>J{offset},1,0)"
            for column in ("D", "G", "H", "I"):
                style_input(ws[f"{column}{offset}"])
            for column in ("F", "J", "K", "L", "M", "N"):
                style_calc(ws[f"{column}{offset}"])
            ws[f"D{offset}"].number_format = FMT_EUR2
            ws[f"E{offset}"].number_format = FMT_PCT
            ws[f"F{offset}"].number_format = "0.0000 €"
            ws[f"G{offset}"].number_format = FMT_EUR2
            ws[f"H{offset}"].number_format = FMT_PCT
            ws[f"I{offset}"].number_format = FMT_PCT
            ws[f"J{offset}"].number_format = "0.0000 €"
            ws[f"K{offset}"].number_format = "0.0000 €"
            ws[f"L{offset}"].number_format = FMT_PCT
            ws[f"M{offset}"].number_format = "0.0000 €"
            ws[f"N{offset}"].number_format = "0"
        ws["B13"] = "Total / ponderado"
        ws["B13"].font = font(bold=True)
        formulas = {
            "D": "=SUMPRODUCT(D5:D12,H5:H12)",
            "E": '=""',
            "F": "=SUMPRODUCT(F5:F12,H5:H12)",
            "G": '=""',
            "H": "=SUM(H5:H12)",
            "I": '=""',
            "J": "=SUMPRODUCT(J5:J12,H5:H12)",
            "K": "=F13-J13",
            "L": "=IFERROR(K13/F13,0)",
            "M": "=SUM(M5:M12)",
            "N": "=SUM(N5:N12)",
        }
        for column, value in formulas.items():
            ws[f"{column}13"] = value
            style_total(ws[f"{column}13"])
        ws["D13"].number_format = FMT_EUR2
        ws["F13"].number_format = "0.0000 €"
        ws["H13"].number_format = FMT_PCT
        ws["J13"].number_format = "0.0000 €"
        ws["K13"].number_format = "0.0000 €"
        ws["L13"].number_format = FMT_PCT
        ws["M13"].number_format = "0.0000 €"
        ws["N13"].number_format = "0"
        ws["A14"] = "Check"
        ws["B14"] = "Mix 100 %"
        ws["C14"] = '=IF(ABS(H13-1)<0.0001,"OK","Revisar")'
        ws["D14"] = "PVP > coste"
        ws["E14"] = '=IF(N13=8,"OK","Revisar")'
        style_check(ws["C14"])
        style_check(ws["E14"])
        ws["A15"] = "La merma se aplica al coste, nunca al precio. El mix se mantiene constante en los tres años."
        ws["A15"].font = font(size=9, italic=True, color=MUTED)
        page_setup(ws, landscape=True)
        for name, reference in {
            "ProductPVP": "$D$5:$D$12",
            "ProductVAT": "$E$5:$E$12",
            "ProductNetPrice": "$F$5:$F$12",
            "ProductCost": "$G$5:$G$12",
            "ProductMix": "$H$5:$H$12",
            "ProductWaste": "$I$5:$I$12",
            "ProductCostAdj": "$J$5:$J$12",
            "ProductUnitMargin": "$K$5:$K$12",
            "WeightedNetPrice": "$F$13",
            "WeightedCostAdj": "$J$13",
        }.items():
            self._add_name(name, "Productos", reference)

    # ----------------------------------------------------------------- personal
    def build_personal(self) -> None:
        ws = self.wb.create_sheet("Personal")
        ws.sheet_properties.tabColor = SAGE
        _set_widths(ws, {"A": 26, "B": 16, "C": 12, "D": 12, "E": 12, "F": 15, "G": 15, "H": 15})
        ws["A1"] = "Personal"
        ws["A1"].font = font(size=18, bold=True)
        ws["A2"] = "Coste empresa = salario bruto × FTE × (1 + cotización) × (1 + crecimiento)^(año−1)."
        ws["A2"].font = font(size=10, color=MUTED)
        headers = ["Rol", "Salario bruto anual", "FTE 2026", "FTE 2027", "FTE 2028", "Coste 2026", "Coste 2027", "Coste 2028"]
        for index, value in enumerate(headers, start=1):
            ws.cell(row=4, column=index, value=value)
        style_table_header(ws, 4, 1, 8)
        for offset, role in enumerate(self.data["staff"]["roles"], start=5):
            ws[f"A{offset}"] = role["name"]
            ws[f"B{offset}"] = role["grossSalary"]
            style_input(ws[f"B{offset}"])
            ws[f"B{offset}"].number_format = FMT_EUR
            for column, year in zip(("C", "D", "E"), range(3)):
                ws[f"{column}{offset}"] = role["fte"][year]
                style_input(ws[f"{column}{offset}"])
                ws[f"{column}{offset}"].number_format = "0.0"
            ws[f"F{offset}"] = f"=B{offset}*C{offset}*(1+$B$11)"
            ws[f"G{offset}"] = f"=B{offset}*(1+$B$12)*D{offset}*(1+$B$11)"
            ws[f"H{offset}"] = f"=B{offset}*(1+$B$12)^2*E{offset}*(1+$B$11)"
            for column in ("F", "G", "H"):
                style_calc(ws[f"{column}{offset}"])
                ws[f"{column}{offset}"].number_format = FMT_EUR
        ws["A9"] = "Total"
        style_total(ws["A9"])
        for column in ("C", "D", "E"):
            ws[f"{column}9"] = f"=SUM({column}5:{column}8)"
            style_total(ws[f"{column}9"])
            ws[f"{column}9"].number_format = "0.0"
        for column in ("F", "G", "H"):
            ws[f"{column}9"] = f"=SUM({column}5:{column}8)"
            style_total(ws[f"{column}9"])
            ws[f"{column}9"].number_format = FMT_EUR
        ws["A11"] = "Cotización empresarial"
        ws["B11"] = self.data["staff"]["employerSocialSecurity"]
        style_input(ws["B11"])
        ws["B11"].number_format = FMT_PCT
        ws["A12"] = "Crecimiento salarial"
        ws["B12"] = self.data["staff"]["salaryGrowth"]
        style_input(ws["B12"])
        ws["B12"].number_format = FMT_PCT
        ws["A13"] = "El barista pasa de 1,0 a 1,5 FTE en 2027. No se modelan horas extras, bajas ni bonificaciones."
        ws["A13"].font = font(size=9, italic=True, color=MUTED)
        page_setup(ws, landscape=False)
        for name, reference in {
            "StaffSalary": "$B$5:$B$8",
            "StaffFTE_Y1": "$C$5:$C$8",
            "StaffFTE_Y2": "$D$5:$D$8",
            "StaffFTE_Y3": "$E$5:$E$8",
            "StaffCostByYear": "$F$9:$H$9",
            "EmployerSS": "$B$11",
            "SalaryGrowth": "$B$12",
        }.items():
            self._add_name(name, "Personal", reference)

    # ----------------------------------------------------------------- costos
    def build_costos(self) -> None:
        ws = self.wb.create_sheet("Costos")
        ws.sheet_properties.tabColor = SAGE
        _set_widths(ws, {"A": 32, "B": 16, "C": 16, "D": 34, "E": 20})
        ws["A1"] = "Costos"
        ws["A1"].font = font(size=18, bold=True)
        ws["A2"] = "Costes fijos, capex, mantenimiento y cuadre de fuentes y usos."
        ws["A2"].font = font(size=10, color=MUTED)

        style_section(ws, 4, "Costes fijos", "E")
        for index, value in enumerate(["Concepto", "€/mes año 1", "€/año año 1", "Indexación", "Nota"], start=1):
            ws.cell(row=5, column=index, value=value)
        style_table_header(ws, 5, 1, 5)
        fixed = [
            ("Alquiler", self.data["fixedCosts"]["rent"], "2,0 % anual × factor de alquiler", "92 m² a 20,65 €/m²/mes"),
            ("Suministros", self.data["fixedCosts"]["utilities"], "Inflación de servicios del escenario", "Luz, gas, agua y residuos"),
            ("Servicios fijos", self.data["fixedCosts"]["fixedServices"], "Inflación de servicios del escenario", "Internet, TPV, software, seguro, gestoría y alarma"),
            ("Marketing fijo", self.data["fixedCosts"]["fixedMarketing"], "2,5 % anual", "Contenido, fotografía e impresos"),
            ("Otros gastos", self.data["fixedCosts"]["other"], "Crecimiento de otros × factor", "Limpieza, mantenimiento, formación, banca y comisiones"),
        ]
        for offset, (label, value, indexation, note) in enumerate(fixed, start=6):
            ws[f"A{offset}"] = label
            ws[f"B{offset}"] = value
            style_input(ws[f"B{offset}"])
            ws[f"B{offset}"].number_format = FMT_EUR
            ws[f"C{offset}"] = f"=B{offset}*12"
            style_calc(ws[f"C{offset}"])
            ws[f"C{offset}"].number_format = FMT_EUR
            ws[f"D{offset}"] = indexation
            ws[f"D{offset}"].font = font(size=9, color=MUTED)
            ws[f"E{offset}"] = note
            ws[f"E{offset}"].font = font(size=9, color=MUTED)
        ws["A11"] = "Total"
        style_total(ws["A11"])
        for column in ("B", "C"):
            ws[f"{column}11"] = f"=SUM({column}6:{column}10)"
            style_total(ws[f"{column}11"])
            ws[f"{column}11"].number_format = FMT_EUR

        style_section(ws, 13, "Capex inicial", "E")
        for index, value in enumerate(["Activo", "Importe", "Vida útil", "Amortización anual", "Amortización mensual"], start=1):
            ws.cell(row=14, column=index, value=value)
        style_table_header(ws, 14, 1, 5)
        for offset, item in enumerate(self.data["capex"]["items"], start=15):
            ws[f"A{offset}"] = item["name"]
            ws[f"B{offset}"] = item["amount"]
            style_input(ws[f"B{offset}"])
            ws[f"B{offset}"].number_format = FMT_EUR
            ws[f"C{offset}"] = item["lifeYears"]
            style_input(ws[f"C{offset}"])
            ws[f"C{offset}"].number_format = "0"
            ws[f"D{offset}"] = f"=B{offset}/C{offset}"
            style_calc(ws[f"D{offset}"])
            ws[f"D{offset}"].number_format = FMT_EUR
            ws[f"E{offset}"] = f"=D{offset}/12"
            style_calc(ws[f"E{offset}"])
            ws[f"E{offset}"].number_format = FMT_EUR2
        ws["A21"] = "Total"
        style_total(ws["A21"])
        for column in ("B", "D", "E"):
            ws[f"{column}21"] = f"=SUM({column}15:{column}20)"
            style_total(ws[f"{column}21"])
            ws[f"{column}21"].number_format = FMT_EUR2 if column == "E" else FMT_EUR
        style_section(ws, 23, "Capex de mantenimiento", "E")
        ws["A24"] = "Capex de mantenimiento"
        ws["B24"] = self.data["capex"]["maintenancePct"]
        style_input(ws["B24"])
        ws["B24"].number_format = FMT_PCT
        ws["C24"] = "de ingresos netos, salida de caja de inversión"
        ws["C24"].font = font(size=9, color=MUTED)

        style_section(ws, 26, "Cuadre de fuentes y usos", "E")
        ws["A27"] = "Concepto"
        ws["B27"] = "Importe"
        style_table_header(ws, 27, 1, 2)
        ws["A28"] = "Capex inicial"
        ws["B28"] = "=B21"
        ws["A29"] = "Stock inicial"
        ws["B29"] = "=Supuestos!B46"
        ws["A30"] = "Total usos (capex + stock + caja)"
        ws["B30"] = "=B21+Supuestos!B46+Supuestos!B45"
        ws["A31"] = "Total fuentes (equity + deuda)"
        ws["B31"] = "=Supuestos!B41+Supuestos!B42"
        ws["A32"] = "Check"
        ws["B32"] = '=IF(B30=B31,"OK","Revisar")'
        for row in (28, 29, 30, 31):
            style_calc(ws[f"B{row}"])
            ws[f"B{row}"].number_format = FMT_EUR
        style_total(ws["A30"])
        style_total(ws["B30"])
        style_total(ws["A31"])
        style_total(ws["B31"])
        style_check(ws["B32"])
        ws["A34"] = "La caja de apertura es un uso, no un ingreso. El capex de mantenimiento no genera una capa adicional de amortización."
        ws["A34"].font = font(size=9, italic=True, color=MUTED)
        page_setup(ws, landscape=False)
        for name, reference in {
            "RentMonth": "$B$6",
            "UtilitiesMonth": "$B$7",
            "FixedServicesMonth": "$B$8",
            "FixedMarketingMonth": "$B$9",
            "OtherOpexMonth": "$B$10",
            "CapexAmount": "$B$15:$B$20",
            "CapexLife": "$C$15:$C$20",
            "TotalCapex": "$B$21",
            "MonthlyDepreciation": "$E$21",
            "MaintenanceCapexPct": "$B$24",
        }.items():
            self._add_name(name, "Costos", reference)

    # ----------------------------------------------------------------- escenario
    def build_scenario(self, key: str) -> None:
        sheet_name, selector = SCENARIO_SHEETS[key]
        ws = self.wb.create_sheet(sheet_name)
        ws.sheet_properties.tabColor = {"pessimistic": NEGATIVE, "base": TERRACOTTA, "optimistic": SAGE_STRONG}[key]
        _set_widths(ws, {"A": 44, "B": 14, **{column: 11 for column in MONTH_COLS}, **{column: 13 for column in YEAR_COLS}, "AP": 13})
        ws.sheet_view.zoomScale = 85
        ws.sheet_view.showGridLines = True

        ws["A1"] = f"Cafetería Aurora — Escenario {sheet_name}"
        ws["A1"].font = font(size=16, bold=True)
        ws["A2"] = "EUR, sin IVA. Solo se editan las hojas de entrada."
        ws["A2"].font = font(size=10, color=MUTED)
        ws["A3"] = "Selector (1/2/3):"
        ws["B3"] = selector
        style_input(ws["B3"])
        ws["C3"] = "1 = Pesimista · 2 = Base · 3 = Optimista"
        ws["C3"].font = font(size=9, color=MUTED)
        self._set_data_validation(ws, "B3", "1", "3")
        ws["A4"] = "Escenario:"
        ws["B4"] = '=CHOOSE(B3,"Pesimista","Base","Optimista")'
        style_calc(ws["B4"])
        ws["B4"].font = font(bold=True, color=TERRACOTTA)
        ws["C4"] = "Cambia el selector para ver el mismo modelo con los supuestos de otro escenario."
        ws["C4"].font = font(size=9, color=MUTED)

        # Tiempo
        ws["A5"] = "Índice de mes"
        ws["B5"] = "mes"
        ws["C5"] = 1
        style_input(ws["C5"])
        for index in range(1, 36):
            column = MONTH_COLS[index]
            previous = MONTH_COLS[index - 1]
            ws[f"{column}5"] = f"={previous}5+1"
            style_calc(ws[f"{column}5"])
        ws["A6"] = "Fecha"
        ws["B6"] = "fecha"
        ws["C6"] = "=DATE(2026,1,1)"
        style_calc(ws["C6"])
        ws["C6"].number_format = FMT_DATE
        for index in range(1, 36):
            column = MONTH_COLS[index]
            previous = MONTH_COLS[index - 1]
            ws[f"{column}6"] = f"=EDATE({previous}6,1)"
            style_calc(ws[f"{column}6"])
            ws[f"{column}6"].number_format = FMT_MONTH
        ws["A7"] = "Año"
        ws["B7"] = "1–3"
        ws["A8"] = "Mes"
        ws["B8"] = "1–12"
        ws["A9"] = "Días operativos"
        ws["B9"] = "días"
        for index, column in enumerate(MONTH_COLS):
            ws[f"{column}7"] = f"=ROUNDUP({column}5/12,0)"
            style_calc(ws[f"{column}7"])
            ws[f"{column}8"] = f"=MOD({column}5-1,12)+1"
            style_calc(ws[f"{column}8"])
            ws[f"{column}9"] = f"=INDEX(OpeningDays,1,{column}8)"
            style_calc(ws[f"{column}9"])
            ws[f"{column}9"].number_format = FMT_INT
        for row in (5, 6, 7, 8, 9):
            ws[f"A{row}"].font = font(bold=True)
            ws[f"B{row}"].font = font(size=9, color=MUTED, italic=True)
        for year_index, column in enumerate(YEAR_COLS):
            first = MONTH_COLS[year_index * 12]
            last = MONTH_COLS[year_index * 12 + 11]
            ws[f"{column}9"] = f"=SUM({first}9:{last}9)"
            style_calc(ws[f"{column}9"])
            ws[f"{column}9"].number_format = FMT_INT
        ws[f"{TOTAL_COL}9"] = "=SUM(AM9:AO9)"
        style_calc(ws[f"{TOTAL_COL}9"])
        ws[f"{TOTAL_COL}9"].number_format = FMT_INT

        # P&L
        style_section(ws, 11, "Cuenta de resultados", "AP")
        self._row_formula(ws, 12, "Tickets/día", "tickets/día", "=BaseTicketsDay*INDEX(ScenarioMatrix,1,$B$3)*(1+INDEX(ScenarioMatrix,2,$B$3))^({y}-1)*INDEX(Seasonality,1,{c}8)*IF({y}=1,INDEX(Ramp,1,{c}8),1)", FMT_TICKETS)
        self._row_formula(ws, 13, "Tickets", "tickets", "={c}12*{c}9", FMT_INT)
        self._row_formula(ws, 14, "Ítems vendidos", "ítems", "={c}13*ItemsPerTicket", FMT_INT)
        self._row_formula(ws, 15, "Ingresos netos", "€", "={c}14*WeightedNetPrice*(1+INDEX(ScenarioMatrix,3,$B$3))^({y}-1)", FMT_EUR, bold=True)
        self._row_formula(ws, 16, "COGS", "€", "={c}14*WeightedCostAdj*(1+INDEX(ScenarioMatrix,4,$B$3))^({y}-1)", FMT_EUR)
        self._row_formula(ws, 17, "Margen bruto", "€", "={c}15-{c}16", FMT_EUR, bold=True)
        self._row_formula(ws, 18, "Personal", "€", "=INDEX(StaffCostByYear,1,{c}7)*INDEX(ScenarioMatrix,5,$B$3)/12", FMT_EUR)
        self._row_formula(ws, 19, "Alquiler", "€", "=RentMonth*INDEX(ScenarioMatrix,6,$B$3)*(1+RentGrowth)^({c}7-1)", FMT_EUR)
        self._row_formula(ws, 20, "Suministros", "€", "=UtilitiesMonth*(1+INDEX(ScenarioMatrix,7,$B$3))^({c}7-1)", FMT_EUR)
        self._row_formula(ws, 21, "Servicios fijos", "€", "=FixedServicesMonth*(1+INDEX(ScenarioMatrix,7,$B$3))^({c}7-1)", FMT_EUR)
        self._row_formula(ws, 22, "Marketing fijo", "€", "=FixedMarketingMonth*(1+FixedMarketingGrowth)^({c}7-1)", FMT_EUR)
        self._row_formula(ws, 23, "Marketing variable", "€", "=INDEX(ScenarioMatrix,8,$B$3)*{c}15", FMT_EUR)
        self._row_formula(ws, 24, "Otros gastos", "€", "=OtherOpexMonth*INDEX(ScenarioMatrix,9,$B$3)*(1+INDEX(ScenarioMatrix,10,$B$3))^({c}7-1)", FMT_EUR)
        self._row_formula(ws, 25, "Total opex + personal", "€", "=SUM({c}18:{c}24)", FMT_EUR, bold=True)
        self._row_formula(ws, 26, "EBITDA", "€", "={c}17-{c}25", FMT_EUR, bold=True)
        self._row_formula(ws, 27, "Amortización", "€", "=MonthlyDepreciation", FMT_EUR)
        self._row_formula(ws, 28, "EBIT", "€", "={c}26-{c}27", FMT_EUR, bold=True)
        self._row_formula(ws, 29, "Intereses", "€", "={c}53", FMT_EUR)
        self._row_formula(ws, 30, "EBT", "€", "={c}28-{c}29", FMT_EUR, bold=True)
        self._row_formula(ws, 31, "Impuestos", "€", "=IF({c}7=1,$B$63/12,IF({c}7=2,$C$63/12,$D$63/12))", FMT_EUR)
        self._row_formula(ws, 32, "Beneficio neto", "€", "={c}30-{c}31", FMT_EUR, bold=True)

        # Margin rows need custom annual ratio, not sum.
        for row, label, numerator_row in ((33, "Margen bruto %", 17), (34, "Margen EBITDA %", 26), (35, "Margen neto %", 32)):
            self._write_label(ws, row, label, "%")
            for column in MONTH_COLS:
                ws[f"{column}{row}"] = f"=IFERROR({column}{numerator_row}/{column}15,0)"
                style_calc(ws[f"{column}{row}"])
                ws[f"{column}{row}"].number_format = FMT_PCT
            for year_index, column in enumerate(YEAR_COLS):
                first = MONTH_COLS[year_index * 12]
                last = MONTH_COLS[year_index * 12 + 11]
                ws[f"{column}{row}"] = f"=IFERROR({column}{numerator_row}/{column}15,0)"
                style_calc(ws[f"{column}{row}"])
                ws[f"{column}{row}"].number_format = FMT_PCT
            ws[f"{TOTAL_COL}{row}"] = f"=IFERROR({TOTAL_COL}{numerator_row}/{TOTAL_COL}15,0)"
            style_calc(ws[f"{TOTAL_COL}{row}"])
            ws[f"{TOTAL_COL}{row}"].number_format = FMT_PCT

        # Checks P&L
        self._write_label(ws, 36, "Check P&L (debe ser 0)", "€")
        for column in MONTH_COLS:
            ws[f"{column}36"] = f"={column}17-{column}25-{column}26"
            style_calc(ws[f"{column}36"])
        for column in YEAR_COLS:
            ws[f"{column}36"] = f"={column}17-{column}25-{column}26"
            style_calc(ws[f"{column}36"])
        ws["AP36"] = "=SUM(AM36:AO36)"
        style_calc(ws["AP36"])

        # Cash
        style_section(ws, 37, "Caja", "AP")
        self._row_formula(ws, 38, "Caja inicial", "€", "=OpeningCash" if False else lambda c, i: "=OpeningCash" if i == 1 else f"={MONTH_COLS[i - 2]}48", FMT_EUR, annual="december", total="last")
        self._row_formula(ws, 39, "Capital circulante", "€", "={c}16*(InventoryDays-PayableDays)/365", FMT_EUR, annual="december", total="last")
        self._row_formula(ws, 40, "Δ capital circulante", "€", lambda c, i: f"={c}39-WC0" if i == 1 else f"={c}39-{MONTH_COLS[i - 2]}39", FMT_EUR)
        self._row_formula(ws, 41, "Capex de mantenimiento", "€", "={c}15*MaintenanceCapexPct", FMT_EUR)
        self._row_formula(ws, 42, "Impuesto teórico sin deuda", "€", "=IF({c}7=1,$B$68/12,IF({c}7=2,$C$68/12,$D$68/12))", FMT_EUR)
        self._row_formula(ws, 43, "FCFF", "€", "={c}26-{c}42-{c}41-{c}40", FMT_EUR, bold=True)
        self._row_formula(ws, 44, "Intereses", "€", "={c}53", FMT_EUR)
        self._row_formula(ws, 45, "Escudo fiscal", "€", "={c}42-{c}31", FMT_EUR)
        self._row_formula(ws, 46, "Principal", "€", "={c}54", FMT_EUR)
        self._row_formula(ws, 47, "FCFE", "€", "={c}43-{c}44+{c}45-{c}46", FMT_EUR, bold=True)
        self._row_formula(ws, 48, "Caja final", "€", "={c}38+{c}47", FMT_EUR, bold=True, annual="december", total="last")
        self._row_formula(ws, 49, "Check caja mínima", "texto", '=IF({c}48<MinCash,"Alerta","OK")', "@", annual="none", total="none")
        self._row_formula(ws, 50, "Check caja (debe ser 0)", "€", "={c}38+{c}47-{c}48", FMT_EUR)

        # Debt
        style_section(ws, 51, "Calendario de deuda", "AP")
        self._row_formula(ws, 52, "Deuda inicial", "€", lambda c, i: "=LoanAmount" if i == 1 else f"={MONTH_COLS[i - 2]}55", FMT_EUR, annual="december", total="last")
        self._row_formula(ws, 53, "Intereses", "€", "={c}52*LoanRate/12", FMT_EUR)
        self._row_formula(ws, 54, "Principal", "€", "=MIN(LoanPayment-{c}53,{c}52)", FMT_EUR)
        self._row_formula(ws, 55, "Deuda final", "€", "={c}52-{c}54", FMT_EUR, bold=True, annual="december", total="last")
        self._row_formula(ws, 56, "Cuota", "€", "=LoanPayment", FMT_EUR)
        self._row_formula(ws, 57, "DSCR", "×", "=IFERROR(({c}26-{c}31)/({c}53+{c}54),0)", FMT_DSCR, annual="none", total="none")
        for year_index, column in enumerate(YEAR_COLS):
            first = MONTH_COLS[year_index * 12]
            last = MONTH_COLS[year_index * 12 + 11]
            ws[f"{column}57"] = f"=IFERROR(({column}26-{column}31)/({column}53+{column}54),0)"
            style_calc(ws[f"{column}57"])
            ws[f"{column}57"].number_format = FMT_DSCR
        ws[f"{TOTAL_COL}57"] = "=IFERROR((AP26-AP31)/(AP53+AP54),0)"
        style_calc(ws[f"{TOTAL_COL}57"])
        ws[f"{TOTAL_COL}57"].number_format = FMT_DSCR

        # Impuesto anual
        style_section(ws, 58, "Impuesto anual y pérdidas compensables", "D")
        ws["A59"] = "Concepto"
        ws["B59"] = "2026"
        ws["C59"] = "2027"
        ws["D59"] = "2028"
        style_table_header(ws, 59, 1, 4)
        tax_rows = [
            (60, "EBT anual", ["=AM30", "=AN30", "=AO30"], FMT_EUR),
            (61, "Pérdidas inicio (con deuda)", [0, "=B64", "=C64"], FMT_EUR),
            (62, "Base imponible", ["=MAX(0,B60-B61)", "=MAX(0,C60-C61)", "=MAX(0,D60-D61)"], FMT_EUR),
            (63, "Cuota", ["=B62*TaxRate", "=C62*TaxRate", "=D62*TaxRate"], FMT_EUR),
            (64, "Pérdidas fin", ["=B61-MIN(B61,MAX(0,B60))+MAX(0,-B60)", "=C61-MIN(C61,MAX(0,C60))+MAX(0,-C60)", "=D61-MIN(D61,MAX(0,D60))+MAX(0,-D60)"], FMT_EUR),
            (65, "EBIT anual", ["=AM28", "=AN28", "=AO28"], FMT_EUR),
            (66, "Pérdidas inicio (sin deuda)", [0, "=B69", "=C69"], FMT_EUR),
            (67, "Base imponible sin deuda", ["=MAX(0,B65-B66)", "=MAX(0,C65-C66)", "=MAX(0,D65-D66)"], FMT_EUR),
            (68, "Cuota sin deuda", ["=B67*TaxRate", "=C67*TaxRate", "=D67*TaxRate"], FMT_EUR),
            (69, "Pérdidas fin (sin deuda)", ["=B66-MIN(B66,MAX(0,B65))+MAX(0,-B65)", "=C66-MIN(C66,MAX(0,C65))+MAX(0,-C65)", "=D66-MIN(D66,MAX(0,D65))+MAX(0,-D65)"], FMT_EUR),
            (70, "Escudo fiscal", ["=B68-B63", "=C68-C63", "=D68-D63"], FMT_EUR),
        ]
        for row, label, formulas, fmt in tax_rows:
            ws[f"A{row}"] = label
            ws[f"A{row}"].font = font()
            for column, formula in zip(("B", "C", "D"), formulas):
                ws[f"{column}{row}"] = formula
                style_calc(ws[f"{column}{row}"])
                ws[f"{column}{row}"].number_format = fmt
        ws["E59"] = "La cuota mensual de la fila 31 es la cuota anual / 12."
        ws["E59"].font = font(size=9, italic=True, color=MUTED)

        # Resumen anual
        style_section(ws, 74, "Resumen anual", "AP")
        headers = ["Métrica", "2026", "2027", "2028", "3 años"]
        for index, value in enumerate(headers, start=1):
            ws.cell(row=75, column=index, value=value)
        style_table_header(ws, 75, 1, 5)
        summary_rows = [
            (76, "Ingresos netos", ["=AM15", "=AN15", "=AO15"], FMT_EUR),
            (77, "COGS", ["=AM16", "=AN16", "=AO16"], FMT_EUR),
            (78, "Margen bruto", ["=AM17", "=AN17", "=AO17"], FMT_EUR),
            (79, "Personal", ["=AM18", "=AN18", "=AO18"], FMT_EUR),
            (80, "Alquiler", ["=AM19", "=AN19", "=AO19"], FMT_EUR),
            (81, "Suministros", ["=AM20", "=AN20", "=AO20"], FMT_EUR),
            (82, "Servicios fijos", ["=AM21", "=AN21", "=AO21"], FMT_EUR),
            (83, "Marketing fijo", ["=AM22", "=AN22", "=AO22"], FMT_EUR),
            (84, "Marketing variable", ["=AM23", "=AN23", "=AO23"], FMT_EUR),
            (85, "Otros gastos", ["=AM24", "=AN24", "=AO24"], FMT_EUR),
            (86, "EBITDA", ["=AM26", "=AN26", "=AO26"], FMT_EUR),
            (87, "Amortización", ["=AM27", "=AN27", "=AO27"], FMT_EUR),
            (88, "EBIT", ["=AM28", "=AN28", "=AO28"], FMT_EUR),
            (89, "Intereses", ["=AM29", "=AN29", "=AO29"], FMT_EUR),
            (90, "EBT", ["=AM30", "=AN30", "=AO30"], FMT_EUR),
            (91, "Impuestos", ["=AM31", "=AN31", "=AO31"], FMT_EUR),
            (92, "Beneficio neto", ["=AM32", "=AN32", "=AO32"], FMT_EUR),
            (93, "CFO", ["=B92+B87-AM40", "=C92+C87-AN40", "=D92+D87-AO40"], FMT_EUR),
            (94, "Capex mantenimiento", ["=AM41", "=AN41", "=AO41"], FMT_EUR),
            (95, "FCFF", ["=AM43", "=AN43", "=AO43"], FMT_EUR),
            (96, "Principal", ["=AM46", "=AN46", "=AO46"], FMT_EUR),
            (97, "FCFE", ["=AM47", "=AN47", "=AO47"], FMT_EUR),
            (98, "Caja final", ["=N48", "=Z48", "=AL48"], FMT_EUR),
            (99, "Tickets/día", ["=AM13/AM9", "=AN13/AN9", "=AO13/AO9"], FMT_TICKETS),
            (100, "Ticket medio neto", ["=B76/AM13", "=C76/AN13", "=D76/AO13"], FMT_EUR2),
            (101, "Ticket medio con IVA", ["=B100*1.1", "=C100*1.1", "=D100*1.1"], FMT_EUR2),
            (102, "Punto de equilibrio EBITDA", ["=(B79+B80+B81+B82+B83+B85)/((B76-B77-B84)/AM13)/AM9", "=(C79+C80+C81+C82+C83+C85)/((C76-C77-C84)/AN13)/AN9", "=(D79+D80+D81+D82+D83+D85)/((D76-D77-D84)/AO13)/AO9"], FMT_TICKETS),
            (103, "Punto de equilibrio total", ["=(B79+B80+B81+B82+B83+B85+B87+B89)/((B76-B77-B84)/AM13)/AM9", "=(C79+C80+C81+C82+C83+C85+C87+C89)/((C76-C77-C84)/AN13)/AN9", "=(D79+D80+D81+D82+D83+D85+D87+D89)/((D76-D77-D84)/AO13)/AO9"], FMT_TICKETS),
            (104, "Margen de seguridad", ["=(B99-B103)/B99", "=(C99-C103)/C99", "=(D99-D103)/D99"], FMT_PCT),
            (105, "DSCR", ["=(B86-B91)/(B89+B96)", "=(C86-C91)/(C89+C96)", "=(D86-D91)/(D89+D96)"], FMT_DSCR),
        ]
        for row, label, formulas, fmt in summary_rows:
            ws[f"A{row}"] = label
            ws[f"A{row}"].font = font()
            for column, formula in zip(("B", "C", "D"), formulas):
                ws[f"{column}{row}"] = formula
                style_calc(ws[f"{column}{row}"])
                ws[f"{column}{row}"].number_format = fmt
            if row not in (99, 100, 101, 102, 103, 104, 105):
                ws[f"E{row}"] = f"=SUM(B{row}:D{row})"
                style_calc(ws[f"E{row}"])
                ws[f"E{row}"].number_format = fmt
        ws["E98"] = "=D98"
        style_calc(ws["E98"])
        ws["E98"].number_format = FMT_EUR
        ws["E99"] = "=SUM(B99:D99)/3"
        style_calc(ws["E99"])
        ws["E99"].number_format = FMT_TICKETS
        ws["E100"] = "=E76/SUM(AM13:AO13)"
        style_calc(ws["E100"])
        ws["E100"].number_format = FMT_EUR2
        ws["E101"] = "=E100*1.1"
        style_calc(ws["E101"])
        ws["E101"].number_format = FMT_EUR2
        ws["A106"] = "Cash-on-cash"
        ws["B106"] = "=AL110/Equity"
        style_calc(ws["B106"])
        ws["B106"].number_format = FMT_PCT
        ws["C106"] = "FCFE acumulado a 36 meses / equity"
        ws["C106"].font = font(size=9, italic=True, color=MUTED)
        ws["A107"] = "Margen de seguridad = (tickets/día previstos − BE total) / tickets/día previstos."
        ws["A107"].font = font(size=9, italic=True, color=MUTED)

        # Payback
        style_section(ws, 108, "Payback", "AP")
        self._write_label(ws, 109, "FCFF acumulado", "€")
        self._write_label(ws, 110, "FCFE acumulado", "€")
        self._write_label(ws, 111, "Flag payback proyecto", "mes")
        self._write_label(ws, 112, "Flag payback equity", "mes")
        for index, column in enumerate(MONTH_COLS):
            if index == 0:
                ws[f"{column}109"] = f"={column}43"
                ws[f"{column}110"] = f"={column}47"
            else:
                previous = MONTH_COLS[index - 1]
                ws[f"{column}109"] = f"={previous}109+{column}43"
                ws[f"{column}110"] = f"={previous}110+{column}47"
            style_calc(ws[f"{column}109"])
            style_calc(ws[f"{column}110"])
            ws[f"{column}109"].number_format = FMT_EUR
            ws[f"{column}110"].number_format = FMT_EUR
            ws[f"{column}111"] = f"=IF({column}109>=TotalCapex+WC0,{column}5,999)"
            ws[f"{column}112"] = f"=IF({column}110>=Equity,{column}5,999)"
            style_calc(ws[f"{column}111"])
            style_calc(ws[f"{column}112"])
        ws["A113"] = "Payback proyecto (meses)"
        ws["B113"] = '=IF(MIN(C111:AL111)=999,">36",MIN(C111:AL111))'
        style_calc(ws["B113"])
        ws["B113"].font = font(bold=True)
        ws["A114"] = "Payback equity (meses)"
        ws["B114"] = '=IF(MIN(C112:AL112)=999,">36",MIN(C112:AL112))'
        style_calc(ws["B114"])
        ws["B114"].font = font(bold=True)
        ws["C113"] = "Recuperación del proyecto: capex 132.000 € + capital circulante inicial 6.500 €."
        ws["C114"] = "Recuperación del accionista: equity aportado 90.000 €."
        for cell in ("C113", "C114"):
            ws[cell].font = font(size=9, italic=True, color=MUTED)

        # Productos por año
        style_section(ws, 116, "Rentabilidad por producto", "AP")
        product_ranges = [(117, 118, 126, 0), (128, 129, 137, 1), (139, 140, 148, 2)]
        for header_row, first_row, total_row, year_index in product_ranges:
            ws[f"A{header_row}"] = f"Producto — {2026 + year_index}"
            ws[f"B{header_row}"] = "Unidades"
            ws[f"C{header_row}"] = "Ingresos"
            ws[f"D{header_row}"] = "COGS"
            ws[f"E{header_row}"] = "Margen bruto"
            ws[f"F{header_row}"] = "Margen %"
            style_table_header(ws, header_row, 1, 6)
            annual_col = YEAR_COLS[year_index]
            for offset, product in enumerate(self.data["products"]):
                row = first_row + offset
                product_row = 5 + offset
                ws[f"A{row}"] = product["name"]
                ws[f"B{row}"] = f"=${annual_col}$14*Productos!$H{product_row}"
                exp = "" if year_index == 0 else f"^{year_index}"
                ws[f"C{row}"] = f"=B{row}*Productos!$F{product_row}*(1+INDEX(ScenarioMatrix,3,$B$3)){exp}" if year_index else f"=B{row}*Productos!$F{product_row}"
                ws[f"D{row}"] = f"=B{row}*Productos!$J{product_row}*(1+INDEX(ScenarioMatrix,4,$B$3)){exp}" if year_index else f"=B{row}*Productos!$J{product_row}"
                ws[f"E{row}"] = f"=C{row}-D{row}"
                ws[f"F{row}"] = f"=IFERROR(E{row}/C{row},0)"
                for column in ("B", "C", "D", "E", "F"):
                    style_calc(ws[f"{column}{row}"])
                ws[f"B{row}"].number_format = FMT_INT
                ws[f"C{row}"].number_format = FMT_EUR
                ws[f"D{row}"].number_format = FMT_EUR
                ws[f"E{row}"].number_format = FMT_EUR
                ws[f"F{row}"].number_format = FMT_PCT
            ws[f"A{total_row}"] = "Total"
            for column in ("B", "C", "D", "E"):
                ws[f"{column}{total_row}"] = f"=SUM({column}{first_row}:{column}{first_row + 7})"
                style_total(ws[f"{column}{total_row}"])
                ws[f"{column}{total_row}"].number_format = FMT_INT if column == "B" else FMT_EUR
            ws[f"F{total_row}"] = f"=IFERROR(E{total_row}/C{total_row},0)"
            style_total(ws[f"F{total_row}"])
            ws[f"F{total_row}"].number_format = FMT_PCT

        ws["A149"] = "Check producto 2028 vs P&L"
        ws["C149"] = "=C148-AO15"
        ws["D149"] = "=D148-AO16"
        ws["E149"] = '=IF(AND(ABS(C149)<1,ABS(D149)<1),"OK","Revisar")'
        style_calc(ws["C149"])
        style_calc(ws["D149"])
        style_check(ws["E149"])
        ws["A150"] = "Check producto 2026 vs P&L"
        ws["C150"] = "=C126-AM15"
        ws["D150"] = "=D126-AM16"
        ws["E150"] = '=IF(AND(ABS(C150)<1,ABS(D150)<1),"OK","Revisar")'
        style_calc(ws["C150"])
        style_calc(ws["D150"])
        style_check(ws["E150"])
        ws["A151"] = "Check producto 2027 vs P&L"
        ws["C151"] = "=C137-AN15"
        ws["D151"] = "=D137-AN16"
        ws["E151"] = '=IF(AND(ABS(C151)<1,ABS(D151)<1),"OK","Revisar")'
        style_calc(ws["C151"])
        style_calc(ws["D151"])
        style_check(ws["E151"])

        # BE mensual auxiliar
        style_section(ws, 153, "Punto de equilibrio mensual (auxiliar)", "AP")
        self._row_formula(ws, 154, "BE EBITDA mensual", "tickets/día", "=({c}18+{c}19+{c}20+{c}21+{c}22+{c}24)/(({c}15-{c}16-{c}23)/{c}13)/{c}9", FMT_TICKETS, annual="none", total="none")
        self._row_formula(ws, 155, "BE total mensual", "tickets/día", "=({c}18+{c}19+{c}20+{c}21+{c}22+{c}24+{c}27+{c}29)/(({c}15-{c}16-{c}23)/{c}13)/{c}9", FMT_TICKETS, annual="none", total="none")
        self._row_formula(ws, 156, "Margen de seguridad mensual", "%", "=IFERROR(({c}12-{c}155)/{c}12,0)", FMT_PCT, annual="none", total="none")

        # Formato condicional
        ws.conditional_formatting.add("C49:AL49", CellIsRule(operator="equal", formula=['"Alerta"'], fill=fill(NEGATIVE_BG), font=font(color=NEGATIVE, bold=True)))
        ws.conditional_formatting.add("C26:AL26", CellIsRule(operator="lessThan", formula=["0"], fill=fill("FCE9D9")))
        ws.conditional_formatting.add("C32:AL32", CellIsRule(operator="lessThan", formula=["0"], fill=fill(NEGATIVE_BG)))
        ws.conditional_formatting.add("C33:AL33", CellIsRule(operator="lessThan", formula=["0.6"], fill=fill("FCE9D9")))
        ws.conditional_formatting.add("C34:AL34", CellIsRule(operator="lessThan", formula=["0.1"], fill=fill("FCE9D9")))

        ws.freeze_panes = "C10"
        page_setup(ws, landscape=True, repeat_rows="1:9")
        ws.print_title_cols = "A:B"

    # ----------------------------------------------------------------- build
    def build(self, path: Path) -> Path:
        self.build_portada()
        self.build_supuestos()
        self.build_productos()
        self.build_personal()
        self.build_costos()
        for key in SCENARIO_SHEETS:
            self.build_scenario(key)

        self.wb.calculation.fullCalcOnLoad = True
        self.wb.calculation.forceFullCalc = True
        self.wb.calculation.calcMode = "auto"
        self.wb.active = 0
        path.parent.mkdir(parents=True, exist_ok=True)
        self.wb.save(path)
        return path


def build_workbook(model_path: str | Path = MODEL_PATH, output: str | Path = WORKBOOK_PATH) -> Path:
    data = load_model(model_path)
    builder = WorkbookBuilder(data)
    return builder.build(Path(output))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Genera el libro Excel de Cafetería Aurora")
    parser.add_argument("--model", default=str(MODEL_PATH))
    parser.add_argument("--output", default=str(WORKBOOK_PATH))
    args = parser.parse_args(argv)
    path = build_workbook(args.model, args.output)
    print(f"Libro generado: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
