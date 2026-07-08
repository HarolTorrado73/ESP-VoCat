#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 generar_manual.py
================================================================================
 Generador de plantilla PDF profesional tipo libro técnico.
 Utiliza exclusivamente ReportLab (Platypus + Canvas).

 Ejecución:
     python generar_manual.py

 Salida:
     Manual_Tecnico.pdf

 Autor  : [EDITAR] Tu Nombre
 Versión: 1.0.0
 Fecha  : Julio 2026
================================================================================
"""

# ==============================================================================
# IMPORTS
# ==============================================================================
import os
import sys
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import Flowable


# ==============================================================================
# CONFIGURACIÓN GLOBAL DEL DOCUMENTO
#   → Modifica estas constantes para personalizar la plantilla.
# ==============================================================================

# --- Metadatos del documento (aparecen en propiedades del PDF) ---
DOC_TITLE    = "Manual Técnico ESP-VoCat"
DOC_SUBTITLE = "Sistema de Voz y Control para Mascotas con ESP32"
DOC_AUTHOR   = "[EDITAR] Nombre del Autor"
DOC_VERSION  = "1.0.0"
_MESES_ES = [
  "enero", "febrero", "marzo", "abril", "mayo", "junio",
  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
_now = datetime.now()
DOC_DATE = f"{_now.day} de {_MESES_ES[_now.month - 1]} de {_now.year}"
DOC_SUBJECT  = "Documentación técnica del proyecto ESP-VoCat"
DOC_KEYWORDS = "ESP32, UART, sensores, motor paso a paso, IoT, firmware"

# --- Archivo de salida ---
OUTPUT_FILE = "Manual_Tecnico.pdf"

# --- Dimensiones de página ---
PAGE_WIDTH, PAGE_HEIGHT = A4          # 210 × 297 mm

# --- Márgenes profesionales ---
MARGIN_LEFT   = 2.5 * cm
MARGIN_RIGHT  = 2.5 * cm
MARGIN_TOP    = 3.0 * cm
MARGIN_BOTTOM = 2.5 * cm

# Área útil de contenido
CONTENT_WIDTH  = PAGE_WIDTH  - MARGIN_LEFT - MARGIN_RIGHT
CONTENT_HEIGHT = PAGE_HEIGHT - MARGIN_TOP  - MARGIN_BOTTOM


# ==============================================================================
# PALETA DE COLORES
#   → Colores sobrios para un aspecto técnico profesional.
# ==============================================================================
COLOR_PRIMARY    = colors.HexColor("#1A3A5C")   # Azul oscuro – títulos
COLOR_SECONDARY  = colors.HexColor("#2C6E9E")   # Azul medio  – subtítulos
COLOR_ACCENT     = colors.HexColor("#4A90D9")   # Azul claro  – acentos
COLOR_TEXT       = colors.HexColor("#2D2D2D")   # Gris oscuro – cuerpo
COLOR_LIGHT_TEXT = colors.HexColor("#666666")   # Gris medio  – pies de figura
COLOR_BORDER     = colors.HexColor("#B0BEC5")   # Gris claro  – bordes
COLOR_BG_LIGHT   = colors.HexColor("#F5F7FA")   # Fondo suave
COLOR_WHITE      = colors.white

# Colores de los cuadros informativos
COLOR_NOTE_BG      = colors.HexColor("#E8F4FD")   # Azul muy claro
COLOR_NOTE_BORDER  = colors.HexColor("#2196F3")   # Azul
COLOR_WARN_BG      = colors.HexColor("#FFF3E0")   # Naranja claro
COLOR_WARN_BORDER  = colors.HexColor("#FF9800")   # Naranja
COLOR_TIP_BG       = colors.HexColor("#E8F5E9")   # Verde claro
COLOR_TIP_BORDER   = colors.HexColor("#4CAF50")   # Verde

# Colores de tablas
COLOR_TABLE_HEADER = colors.HexColor("#1A3A5C")
COLOR_TABLE_ALT    = colors.HexColor("#EEF2F7")
COLOR_TABLE_BORDER = colors.HexColor("#90A4AE")


# ==============================================================================
# TIPOGRAFÍA
#   → Helvetica es la fuente estándar de ReportLab (no requiere registro).
# ==============================================================================
FONT_REGULAR = "Helvetica"
FONT_BOLD    = "Helvetica-Bold"
FONT_ITALIC  = "Helvetica-Oblique"
FONT_MONO    = "Courier"


# ==============================================================================
# CONTADOR GLOBAL DE FIGURAS
#   → Se incrementa automáticamente al crear cada placeholder de imagen.
# ==============================================================================
_figure_counter = 0


def next_figure_number():
    """Devuelve el siguiente número de figura y lo incrementa."""
    global _figure_counter
    _figure_counter += 1
    return _figure_counter


# ==============================================================================
# CLASE: ImagePlaceholder
#   → Caja con borde para insertar imágenes posteriormente.
#   → Reemplaza el contenido de esta clase por un Image() de ReportLab
#     cuando tengas la imagen lista.
# ==============================================================================
class ImagePlaceholder(Flowable):
  """
  Dibuja una caja rectangular con borde punteado y texto centrado.
  Úsala como marcador de posición para imágenes futuras.

  Parámetros:
      width, height : dimensiones de la caja
      label         : texto principal dentro de la caja
      sublabel      : texto secundario (instrucción)
  """

  def __init__(self, width, height, label="ESPACIO PARA IMAGEN",
               sublabel="Reemplazar por Imagen del Capítulo"):
    Flowable.__init__(self)
    self.width  = width
    self.height = height
    self.label  = label
    self.sublabel = sublabel

  def draw(self):
    canv = self.canv
    # Borde exterior
    canv.setStrokeColor(COLOR_BORDER)
    canv.setLineWidth(1.2)
    canv.setDash(6, 3)
    canv.rect(0, 0, self.width, self.height, stroke=1, fill=0)
    canv.setDash()  # Restaurar línea continua

    # Fondo suave
    canv.setFillColor(COLOR_BG_LIGHT)
    canv.rect(2, 2, self.width - 4, self.height - 4, stroke=0, fill=1)

    # Texto principal
    canv.setFillColor(COLOR_LIGHT_TEXT)
    canv.setFont(FONT_BOLD, 11)
    canv.drawCentredString(self.width / 2, self.height / 2 + 8, self.label)

    # Texto secundario
    canv.setFont(FONT_ITALIC, 9)
    canv.drawCentredString(self.width / 2, self.height / 2 - 10, self.sublabel)


# ==============================================================================
# CLASE: CoverImagePlaceholder
#   → Caja grande para la portada (reemplazar por imagen de portada).
# ==============================================================================
class CoverImagePlaceholder(Flowable):
  """Marcador de posición grande para la imagen de portada."""

  def __init__(self, width, height):
    Flowable.__init__(self)
    self.width  = width
    self.height = height

  def draw(self):
    canv = self.canv
    canv.setStrokeColor(COLOR_ACCENT)
    canv.setLineWidth(2)
    canv.setDash(8, 4)
    canv.rect(0, 0, self.width, self.height, stroke=1, fill=0)
    canv.setDash()

    canv.setFillColor(colors.HexColor("#EBF2FA"))
    canv.rect(3, 3, self.width - 6, self.height - 6, stroke=0, fill=1)

    canv.setFillColor(COLOR_SECONDARY)
    canv.setFont(FONT_BOLD, 16)
    canv.drawCentredString(self.width / 2, self.height / 2 + 6,
                           "ESPACIO PARA PORTADA")
    canv.setFont(FONT_ITALIC, 10)
    canv.setFillColor(COLOR_LIGHT_TEXT)
    canv.drawCentredString(self.width / 2, self.height / 2 - 14,
                           "Reemplazar por imagen de portada")


# ==============================================================================
# CLASE: CalloutBox
#   → Cuadros informativos: Nota, Advertencia, Consejo.
# ==============================================================================
class CalloutBox(Flowable):
  """
  Cuadro informativo con icono, título y cuerpo de texto.

  Parámetros:
      width, height : dimensiones
      title         : "Nota" | "Advertencia" | "Consejo"
      body          : texto del cuadro
      bg_color      : color de fondo
      border_color  : color del borde izquierdo
      icon          : símbolo unicode
  """

  def __init__(self, width, title, body, bg_color, border_color, icon="ℹ"):
    Flowable.__init__(self)
    self.box_width    = width
    self.title        = title
    self.body         = body
    self.bg_color     = bg_color
    self.border_color = border_color
    self.icon         = icon
    # Calcular altura dinámicamente según longitud del texto
    lines = max(2, len(body) // 80 + 1)
    self.height = 1.2 * cm + lines * 0.45 * cm

  def draw(self):
    canv = self.canv
    h = self.height
    w = self.box_width

    # Fondo
    canv.setFillColor(self.bg_color)
    canv.roundRect(0, 0, w, h, 4, stroke=0, fill=1)

    # Barra lateral de color
    canv.setFillColor(self.border_color)
    canv.rect(0, 0, 5, h, stroke=0, fill=1)

    # Título
    canv.setFillColor(self.border_color)
    canv.setFont(FONT_BOLD, 10)
    canv.drawString(14, h - 16, f"{self.icon}  {self.title}")

    # Cuerpo
    canv.setFillColor(COLOR_TEXT)
    canv.setFont(FONT_REGULAR, 9)
    # Dividir texto en líneas de ~90 caracteres
    words = self.body.split()
    line, lines_out = "", []
    for word in words:
      if len(line) + len(word) + 1 <= 90:
        line = (line + " " + word).strip()
      else:
        lines_out.append(line)
        line = word
    if line:
      lines_out.append(line)

    y = h - 30
    for ln in lines_out:
      canv.drawString(14, y, ln)
      y -= 13


# ==============================================================================
# CLASE: HorizontalRule
#   → Línea horizontal decorativa.
# ==============================================================================
class HorizontalRule(Flowable):
  """Línea horizontal de ancho configurable."""

  def __init__(self, width, thickness=0.5, color=COLOR_BORDER):
    Flowable.__init__(self)
    self.width     = width
    self.thickness = thickness
    self.color     = color
    self.height    = thickness + 4

  def draw(self):
    self.canv.setStrokeColor(self.color)
    self.canv.setLineWidth(self.thickness)
    self.canv.line(0, 2, self.width, 2)


# ==============================================================================
# CLASE: TOCItem
#   → Entrada del índice con puntos de relleno y número de página.
# ==============================================================================
class TOCItem(Flowable):
  """
  Línea del índice:  "1. Introducción .............. 5"
  """

  def __init__(self, number, title, page_num, width):
    Flowable.__init__(self)
    self.number   = number
    self.title    = title
    self.page_num = page_num
    self.width    = width
    self.height   = 18

  def draw(self):
    canv = self.canv
    left_text  = f"{self.number}. {self.title}"
    right_text = str(self.page_num)

    canv.setFont(FONT_REGULAR, 11)
    canv.setFillColor(COLOR_TEXT)
    canv.drawString(0, 4, left_text)

    canv.setFont(FONT_REGULAR, 11)
    text_width = canv.stringWidth(left_text, FONT_REGULAR, 11)
    page_width = canv.stringWidth(right_text, FONT_REGULAR, 11)
    dot_start = text_width + 8
    dot_end   = self.width - page_width - 4

    # Puntos de relleno
    canv.setFont(FONT_REGULAR, 8)
    canv.setFillColor(COLOR_LIGHT_TEXT)
    x = dot_start
    while x < dot_end:
      canv.drawString(x, 5, ".")
      x += 5

    # Número de página
    canv.setFont(FONT_REGULAR, 11)
    canv.setFillColor(COLOR_TEXT)
    canv.drawRightString(self.width, 4, right_text)


# ==============================================================================
# ESTILOS DE PÁRRAFO
#   → Centraliza todos los estilos tipográficos del documento.
# ==============================================================================
def build_styles():
  """
  Crea y devuelve un diccionario con todos los estilos del manual.
  Modifica tamaños, colores y espaciados aquí.
  """
  base = getSampleStyleSheet()

  styles = {}

  # --- Título principal (portada) ---
  styles["CoverTitle"] = ParagraphStyle(
    name="CoverTitle",
    fontName=FONT_BOLD,
    fontSize=28,
    leading=34,
    textColor=COLOR_PRIMARY,
    alignment=TA_CENTER,
    spaceAfter=12,
  )

  # --- Subtítulo (portada) ---
  styles["CoverSubtitle"] = ParagraphStyle(
    name="CoverSubtitle",
    fontName=FONT_REGULAR,
    fontSize=14,
    leading=18,
    textColor=COLOR_SECONDARY,
    alignment=TA_CENTER,
    spaceAfter=8,
  )

  # --- Metadatos de portada ---
  styles["CoverMeta"] = ParagraphStyle(
    name="CoverMeta",
    fontName=FONT_REGULAR,
    fontSize=11,
    leading=16,
    textColor=COLOR_LIGHT_TEXT,
    alignment=TA_CENTER,
    spaceAfter=4,
  )

  # --- Título de capítulo ---
  styles["ChapterTitle"] = ParagraphStyle(
    name="ChapterTitle",
    fontName=FONT_BOLD,
    fontSize=22,
    leading=28,
    textColor=COLOR_PRIMARY,
    spaceBefore=0,
    spaceAfter=16,
    borderWidth=0,
    borderPadding=0,
  )

  # --- Subcapítulo ---
  styles["SectionTitle"] = ParagraphStyle(
    name="SectionTitle",
    fontName=FONT_BOLD,
    fontSize=14,
    leading=18,
    textColor=COLOR_SECONDARY,
    spaceBefore=14,
    spaceAfter=8,
  )

  # --- Sub-subcapítulo ---
  styles["SubSectionTitle"] = ParagraphStyle(
    name="SubSectionTitle",
    fontName=FONT_BOLD,
    fontSize=12,
    leading=16,
    textColor=COLOR_ACCENT,
    spaceBefore=10,
    spaceAfter=6,
  )

  # --- Texto normal ---
  styles["BodyText"] = ParagraphStyle(
    name="BodyText",
    fontName=FONT_REGULAR,
    fontSize=10.5,
    leading=15,
    textColor=COLOR_TEXT,
    alignment=TA_JUSTIFY,
    spaceBefore=4,
    spaceAfter=8,
  )

  # --- Pie de figura ---
  styles["FigureCaption"] = ParagraphStyle(
    name="FigureCaption",
    fontName=FONT_ITALIC,
    fontSize=9,
    leading=12,
    textColor=COLOR_LIGHT_TEXT,
    alignment=TA_CENTER,
    spaceBefore=4,
    spaceAfter=16,
  )

  # --- Código / monospace ---
  styles["Code"] = ParagraphStyle(
    name="Code",
    fontName=FONT_MONO,
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#1B5E20"),
    backColor=colors.HexColor("#F1F8E9"),
    borderWidth=0.5,
    borderColor=colors.HexColor("#C8E6C9"),
    borderPadding=6,
    spaceBefore=6,
    spaceAfter=10,
    leftIndent=10,
  )

  # --- Título de tabla ---
  styles["TableTitle"] = ParagraphStyle(
    name="TableTitle",
    fontName=FONT_BOLD,
    fontSize=11,
    leading=14,
    textColor=COLOR_PRIMARY,
    spaceBefore=12,
    spaceAfter=6,
  )

  # --- Índice: título de sección ---
  styles["TOCTitle"] = ParagraphStyle(
    name="TOCTitle",
    fontName=FONT_BOLD,
    fontSize=20,
    leading=26,
    textColor=COLOR_PRIMARY,
    alignment=TA_CENTER,
    spaceAfter=24,
  )

  # --- Encabezado de página ---
  styles["Header"] = ParagraphStyle(
    name="Header",
    fontName=FONT_ITALIC,
    fontSize=8,
    textColor=COLOR_LIGHT_TEXT,
    alignment=TA_RIGHT,
  )

  # --- Pie de página ---
  styles["Footer"] = ParagraphStyle(
    name="Footer",
    fontName=FONT_REGULAR,
    fontSize=8,
    textColor=COLOR_LIGHT_TEXT,
    alignment=TA_CENTER,
  )

  return styles


# ==============================================================================
# CALLBACKS DE PÁGINA (encabezado y pie)
# ==============================================================================

def _draw_header_footer(canv, doc, is_cover=False):
  """
  Dibuja encabezado y pie de página en cada hoja.
  No se dibuja en la portada (is_cover=True).
  """
  canv.saveState()

  if not is_cover:
    # --- Encabezado ---
    canv.setFont(FONT_ITALIC, 8)
    canv.setFillColor(COLOR_LIGHT_TEXT)
    canv.drawString(MARGIN_LEFT, PAGE_HEIGHT - 1.6 * cm, DOC_TITLE)
    canv.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 1.6 * cm,
                         DOC_AUTHOR)
    # Línea bajo el encabezado
    canv.setStrokeColor(COLOR_BORDER)
    canv.setLineWidth(0.4)
    canv.line(MARGIN_LEFT, PAGE_HEIGHT - 1.8 * cm,
              PAGE_WIDTH - MARGIN_RIGHT, PAGE_HEIGHT - 1.8 * cm)

    # --- Pie de página ---
    canv.setFont(FONT_REGULAR, 8)
    canv.setFillColor(COLOR_LIGHT_TEXT)
    page_num = canv.getPageNumber()
    canv.drawCentredString(PAGE_WIDTH / 2, 1.2 * cm, f"— {page_num} —")
    canv.drawString(MARGIN_LEFT, 1.2 * cm, DOC_VERSION)
    canv.drawRightString(PAGE_WIDTH - MARGIN_RIGHT, 1.2 * cm, DOC_DATE)

    # Línea sobre el pie
    canv.setStrokeColor(COLOR_BORDER)
    canv.setLineWidth(0.4)
    canv.line(MARGIN_LEFT, 1.5 * cm,
              PAGE_WIDTH - MARGIN_RIGHT, 1.5 * cm)

  canv.restoreState()


def on_first_page(canv, doc):
  """Callback para la primera página (portada, sin encabezado)."""
  _draw_header_footer(canv, doc, is_cover=True)


def on_later_pages(canv, doc):
  """Callback para el resto de páginas."""
  _draw_header_footer(canv, doc, is_cover=False)


# ==============================================================================
# FUNCIONES AUXILIARES DE CONSTRUCCIÓN
# ==============================================================================

def make_callout_note(text, width):
  """Crea un cuadro de Nota."""
  return CalloutBox(width, "Nota", text,
                    COLOR_NOTE_BG, COLOR_NOTE_BORDER, icon="ℹ")


def make_callout_warning(text, width):
  """Crea un cuadro de Advertencia."""
  return CalloutBox(width, "Advertencia", text,
                    COLOR_WARN_BG, COLOR_WARN_BORDER, icon="⚠")


def make_callout_tip(text, width):
  """Crea un cuadro de Consejo."""
  return CalloutBox(width, "Consejo", text,
                    COLOR_TIP_BG, COLOR_TIP_BORDER, icon="✔")


def make_image_block(width, figure_desc, chapter_label=""):
  """
  Devuelve una lista de flowables: placeholder + pie de figura.
  Incrementa el contador global de figuras.
  """
  fig_num = next_figure_number()
  placeholder = ImagePlaceholder(
    width=width,
    height=7.5 * cm,
    label="ESPACIO PARA IMAGEN",
    sublabel=f"Reemplazar por Imagen del Capítulo{f' — {chapter_label}' if chapter_label else ''}",
  )
  caption = Paragraph(
    f"<b>Figura {fig_num}.</b> {figure_desc}",
    _STYLES["FigureCaption"],
  )
  return [placeholder, caption]


def make_table(title, headers, rows, col_widths=None):
  """
  Crea una tabla profesional con encabezado coloreado y filas alternas.

  Parámetros:
      title     : título sobre la tabla
      headers   : lista de strings (encabezados de columna)
      rows      : lista de listas (filas de datos)
      col_widths: anchos de columna (opcional, se calculan automáticamente)
  """
  elements = []
  elements.append(Paragraph(title, _STYLES["TableTitle"]))

  num_cols = len(headers)
  if col_widths is None:
    col_widths = [CONTENT_WIDTH / num_cols] * num_cols

  # Construir datos: encabezado + filas
  table_data = [headers] + rows

  tbl = Table(table_data, colWidths=col_widths, repeatRows=1)
  tbl.setStyle(TableStyle([
    # Encabezado
    ("BACKGROUND",    (0, 0), (-1, 0),  COLOR_TABLE_HEADER),
    ("TEXTCOLOR",     (0, 0), (-1, 0),  COLOR_WHITE),
    ("FONTNAME",      (0, 0), (-1, 0),  FONT_BOLD),
    ("FONTSIZE",      (0, 0), (-1, 0),  9),
    ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
    ("BOTTOMPADDING", (0, 0), (-1, 0),  8),
    ("TOPPADDING",    (0, 0), (-1, 0),  8),
    # Cuerpo
    ("FONTNAME",      (0, 1), (-1, -1), FONT_REGULAR),
    ("FONTSIZE",      (0, 1), (-1, -1), 9),
    ("ALIGN",         (0, 1), (-1, -1), "LEFT"),
    ("TOPPADDING",    (0, 1), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
    ("LEFTPADDING",   (0, 0), (-1, -1), 8),
    ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    # Filas alternas
    ("ROWBACKGROUNDS", (0, 1), (-1, -1),
     [COLOR_WHITE, COLOR_TABLE_ALT]),
    # Bordes
    ("GRID",          (0, 0), (-1, -1), 0.4, COLOR_TABLE_BORDER),
    ("BOX",           (0, 0), (-1, -1), 0.8, COLOR_TABLE_HEADER),
  ]))

  elements.append(tbl)
  elements.append(Spacer(1, 12))
  return elements


def make_chapter(number, title, body_text, figure_desc,
                 note_text, warn_text, tip_text,
                 extra_elements=None, chapter_label=""):
  """
  Construye el contenido completo de un capítulo.

  Parámetros:
      number          : número del capítulo (int)
      title           : título del capítulo
      body_text       : párrafo de ejemplo
      figure_desc     : descripción de la figura
      note_text       : texto del cuadro Nota
      warn_text       : texto del cuadro Advertencia
      tip_text        : texto del cuadro Consejo
      extra_elements  : lista adicional de flowables (tablas, código, etc.)
      chapter_label   : etiqueta para el placeholder de imagen
  """
  elements = []

  # Salto de página antes de cada capítulo
  elements.append(PageBreak())

  # Título del capítulo con número
  elements.append(Paragraph(
    f"Capítulo {number}<br/>{title}",
    _STYLES["ChapterTitle"],
  ))
  elements.append(HorizontalRule(CONTENT_WIDTH, thickness=1.5,
                                  color=COLOR_ACCENT))
  elements.append(Spacer(1, 10))

  # Párrafo de ejemplo
  elements.append(Paragraph(body_text, _STYLES["BodyText"]))

  # Placeholder de imagen + pie de figura
  elements.extend(make_image_block(CONTENT_WIDTH, figure_desc, chapter_label))

  elements.append(Spacer(1, 6))

  # Cuadros informativos
  elements.append(make_callout_note(note_text, CONTENT_WIDTH))
  elements.append(Spacer(1, 6))
  elements.append(make_callout_warning(warn_text, CONTENT_WIDTH))
  elements.append(Spacer(1, 6))
  elements.append(make_callout_tip(tip_text, CONTENT_WIDTH))

  # Elementos adicionales (tablas, código, subsecciones…)
  if extra_elements:
    elements.append(Spacer(1, 10))
    elements.extend(extra_elements)

  return elements


# ==============================================================================
# DEFINICIÓN DE CAPÍTULOS
#   → Edita los textos de cada capítulo en esta sección.
# ==============================================================================

def get_chapters_content():
  """
  Devuelve la lista de capítulos con su contenido.
  Cada capítulo es un dict con las claves necesarias para make_chapter().
  """
  chapters = [

    # ------------------------------------------------------------------
    # CAPÍTULO 1 – Introducción
    # ------------------------------------------------------------------
    {
      "number": 1,
      "title": "Introducción",
      "body": (
        "[EDITAR] Escriba aquí una introducción general al proyecto ESP-VoCat. "
        "Describa el propósito del sistema, el contexto en el que se desarrolló "
        "y una visión general de sus capacidades. Incluya el problema que resuelve "
        "y el público objetivo de este manual técnico."
      ),
      "figure_desc": "[EDITAR] Diagrama general del sistema ESP-VoCat mostrando los componentes principales.",
      "note": "[EDITAR] Este manual está dirigido a ingenieros y técnicos con conocimientos básicos de electrónica y programación embebida.",
      "warn": "[EDITAR] No alimente el sistema con tensiones superiores a las especificadas en la hoja de datos del ESP32.",
      "tip": "[EDITAR] Lea completamente este manual antes de comenzar el ensamblaje del hardware.",
      "label": "Introducción",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 2 – Objetivos
    # ------------------------------------------------------------------
    {
      "number": 2,
      "title": "Objetivos",
      "body": (
        "[EDITAR] Defina los objetivos generales y específicos del proyecto. "
        "Los objetivos generales describen el propósito global; los específicos "
        "detallan cada meta técnica alcanzable y medible del sistema ESP-VoCat."
      ),
      "figure_desc": "[EDITAR] Mapa de objetivos del proyecto con indicadores de cumplimiento.",
      "note": "[EDITAR] Los objetivos específicos deben ser SMART: Específicos, Medibles, Alcanzables, Relevantes y Temporales.",
      "warn": "[EDITAR] Modificar los objetivos durante el desarrollo puede afectar la arquitectura ya implementada.",
      "tip": "[EDITAR] Revise los objetivos al finalizar cada fase del proyecto para validar el progreso.",
      "label": "Objetivos",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 3 – Arquitectura General
    # ------------------------------------------------------------------
    {
      "number": 3,
      "title": "Arquitectura General",
      "body": (
        "[EDITAR] Describa la arquitectura de alto nivel del sistema. "
        "Incluya los bloques funcionales principales: capa de sensores, capa de "
        "procesamiento (ESP32), capa de actuadores y capa de comunicación. "
        "Explique cómo interactúan entre sí."
      ),
      "figure_desc": "[EDITAR] Diagrama de bloques de la arquitectura general del sistema.",
      "note": "[EDITAR] La arquitectura sigue un modelo de capas desacopladas para facilitar el mantenimiento.",
      "warn": "[EDITAR] Cambios en la arquitectura de comunicación requieren actualizar tanto firmware como software host.",
      "tip": "[EDITAR] Use diagramas UML o de bloques para documentar la arquitectura de forma clara.",
      "label": "Arquitectura",
      "extra": [
        Paragraph("3.1 Diagrama de Bloques", _STYLES["SectionTitle"]),
        Paragraph(
          "[EDITAR] Describa cada bloque del diagrama: entrada de sensores, "
          "procesamiento central, salida de actuadores y módulo de comunicación.",
          _STYLES["BodyText"],
        ),
        Paragraph("3.2 Flujo de Datos", _STYLES["SectionTitle"]),
        Paragraph(
          "[EDITAR] Explique el flujo de datos desde la captura del sensor "
          "hasta la respuesta del actuador, incluyendo tiempos de latencia.",
          _STYLES["BodyText"],
        ),
      ],
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 4 – Hardware
    # ------------------------------------------------------------------
    {
      "number": 4,
      "title": "Hardware",
      "body": (
        "[EDITAR] Documente todos los componentes electrónicos del sistema: "
        "microcontrolador ESP32, sensores, drivers de motor, reguladores de "
        "tensión y conectores. Incluya referencias y hojas de datos."
      ),
      "figure_desc": "[EDITAR] Esquema eléctrico completo del circuito ESP-VoCat.",
      "note": "[EDITAR] Todos los componentes deben ser de grado industrial o comercial según el entorno de operación.",
      "warn": "[EDITAR] Verifique la polaridad de todos los condensadores electrolíticos antes de energizar el circuito.",
      "tip": "[EDITAR] Mantenga un inventario actualizado de componentes con sus números de parte.",
      "label": "Hardware",
      "extra": _make_gpio_table(),
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 5 – Firmware
    # ------------------------------------------------------------------
    {
      "number": 5,
      "title": "Firmware",
      "body": (
        "[EDITAR] Describa el firmware del ESP32: entorno de desarrollo "
        "(Arduino IDE / ESP-IDF / PlatformIO), estructura del código, "
        "tareas principales y ciclo de ejecución del sistema."
      ),
      "figure_desc": "[EDITAR] Diagrama de flujo del firmware principal (loop y tareas FreeRTOS).",
      "note": "[EDITAR] El firmware está desarrollado para ESP-IDF v5.x. Verifique compatibilidad con su versión.",
      "warn": "[EDITAR] No actualice el firmware durante una operación crítica del sistema.",
      "tip": "[EDITAR] Use control de versiones (Git) para gestionar las revisiones del firmware.",
      "label": "Firmware",
      "extra": [
        Paragraph("5.1 Estructura del Código", _STYLES["SectionTitle"]),
        Paragraph(
          "[EDITAR] Describa la organización de carpetas y módulos del firmware.",
          _STYLES["BodyText"],
        ),
        Paragraph(
          "// [EDITAR] Ejemplo de configuración inicial<br/>"
          "#include &lt;Arduino.h&gt;<br/>"
          "#define UART_BAUD 115200<br/>"
          "#define STEP_PIN  GPIO_NUM_18<br/>"
          "void setup() { Serial.begin(UART_BAUD); }",
          _STYLES["Code"],
        ),
      ],
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 6 – Comunicación UART
    # ------------------------------------------------------------------
    {
      "number": 6,
      "title": "Comunicación UART",
      "body": (
        "[EDITAR] Documente el protocolo de comunicación UART entre el ESP32 "
        "y los módulos periféricos. Incluya baudrate, formato de trama, "
        "comandos disponibles y ejemplos de intercambio de mensajes."
      ),
      "figure_desc": "[EDITAR] Diagrama de temporización de tramas UART.",
      "note": "[EDITAR] El baudrate por defecto es 115200 bps, 8N1 (8 bits, sin paridad, 1 bit de stop).",
      "warn": "[EDITAR] Conectar TX a TX y RX a RX directamente dañará los pines. Use cruce TX↔RX.",
      "tip": "[EDITAR] Use un analizador lógico o monitor serial para depurar la comunicación UART.",
      "label": "UART",
      "extra": _make_protocol_table(),
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 7 – Sensores
    # ------------------------------------------------------------------
    {
      "number": 7,
      "title": "Sensores",
      "body": (
        "[EDITAR] Describa cada sensor utilizado en el sistema: tipo, "
        "principio de funcionamiento, rango de medición, precisión, "
        "interfaz de conexión y pin GPIO asignado."
      ),
      "figure_desc": "[EDITAR] Diagrama de conexión de sensores al ESP32.",
      "note": "[EDITAR] Los sensores analógicos requieren conversión ADC de 12 bits del ESP32.",
      "warn": "[EDITAR] No exceda el voltaje máximo de entrada de los sensores (típicamente 3.3 V).",
      "tip": "[EDITAR] Implemente filtrado digital (media móvil) para reducir ruido en lecturas analógicas.",
      "label": "Sensores",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 8 – Motor Paso a Paso
    # ------------------------------------------------------------------
    {
      "number": 8,
      "title": "Motor Paso a Paso",
      "body": (
        "[EDITAR] Documente el motor paso a paso: modelo, torque, "
        "corriente nominal, driver utilizado (A4988/DRV8825/TMC2208), "
        "configuración de microstepping y secuencia de control."
      ),
      "figure_desc": "[EDITAR] Esquema de conexión del driver de motor paso a paso.",
      "note": "[EDITAR] Ajuste la corriente del driver con un multímetro antes de conectar el motor.",
      "warn": "[EDITAR] Un driver mal configurado puede sobrecalentar y dañar el motor permanentemente.",
      "tip": "[EDITAR] Use microstepping 1/16 para operación silenciosa y mayor resolución angular.",
      "label": "Motor",
      "extra": _make_specs_table(),
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 9 – Diseño Mecánico
    # ------------------------------------------------------------------
    {
      "number": 9,
      "title": "Diseño Mecánico",
      "body": (
        "[EDITAR] Presente el diseño mecánico del sistema: materiales, "
        "dimensiones, tolerancias, método de fabricación (impresión 3D, "
        "corte CNC, etc.) y ensamblajes críticos."
      ),
      "figure_desc": "[EDITAR] Plano o render 3D del diseño mecánico completo.",
      "note": "[EDITAR] Los archivos CAD originales están disponibles en el repositorio del proyecto.",
      "warn": "[EDITAR] Respete las tolerancias indicadas en los planos para garantizar el correcto ensamblaje.",
      "tip": "[EDITAR] Imprima piezas de prueba antes de fabricar el lote completo.",
      "label": "Diseño Mecánico",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 10 – Ensamblaje
    # ------------------------------------------------------------------
    {
      "number": 10,
      "title": "Ensamblaje",
      "body": (
        "[EDITAR] Proporcione instrucciones paso a paso para el ensamblaje "
        "del sistema. Incluya el orden recomendado, herramientas necesarias "
        "y verificaciones intermedias."
      ),
      "figure_desc": "[EDITAR] Secuencia fotográfica del proceso de ensamblaje.",
      "note": "[EDITAR] Realice el ensamblaje en una superficie antiestática para proteger los componentes.",
      "warn": "[EDITAR] No aplique torque excesivo en tornillos de montaje de la PCB.",
      "tip": "[EDITAR] Fotografíe cada etapa del ensamblaje para facilitar el mantenimiento futuro.",
      "label": "Ensamblaje",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 11 – Calibración
    # ------------------------------------------------------------------
    {
      "number": 11,
      "title": "Calibración",
      "body": (
        "[EDITAR] Describa los procedimientos de calibración del sistema: "
        "sensores, motor, comunicación y parámetros de operación. "
        "Incluya valores de referencia y criterios de aceptación."
      ),
      "figure_desc": "[EDITAR] Gráfica de calibración de sensores con curva de respuesta.",
      "note": "[EDITAR] La calibración debe realizarse a temperatura ambiente (20-25 °C).",
      "warn": "[EDITAR] Una calibración incorrecta producirá lecturas erróneas y comportamiento impredecible.",
      "tip": "[EDITAR] Documente los valores de calibración en la EEPROM del ESP32 para persistencia.",
      "label": "Calibración",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 12 – Lista de Materiales
    # ------------------------------------------------------------------
    {
      "number": 12,
      "title": "Lista de Materiales",
      "body": (
        "[EDITAR] Presente la lista completa de materiales (BOM) necesarios "
        "para construir el sistema. Incluya cantidad, descripción, "
        "número de parte y proveedor sugerido."
      ),
      "figure_desc": "[EDITAR] Fotografía de todos los componentes organizados.",
      "note": "[EDITAR] Verifique la disponibilidad de componentes antes de iniciar la compra.",
      "warn": "[EDITAR] No sustituya componentes críticos sin verificar compatibilidad eléctrica y mecánica.",
      "tip": "[EDITAR] Compre un 10% adicional de componentes pasivos (resistencias, condensadores) como repuesto.",
      "label": "BOM",
      "extra": _make_bom_table(),
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 13 – Pruebas
    # ------------------------------------------------------------------
    {
      "number": 13,
      "title": "Pruebas",
      "body": (
        "[EDITAR] Documente el plan de pruebas del sistema: pruebas unitarias "
        "de cada módulo, pruebas de integración y pruebas de aceptación. "
        "Incluya procedimientos, resultados esperados y criterios de pase/fallo."
      ),
      "figure_desc": "[EDITAR] Banco de pruebas con el sistema en operación.",
      "note": "[EDITAR] Registre todos los resultados de prueba en una hoja de cálculo para trazabilidad.",
      "warn": "[EDITAR] No omita las pruebas de estrés térmico si el sistema operará en ambientes extremos.",
      "tip": "[EDITAR] Automatice las pruebas repetitivas con scripts de Python y pytest.",
      "label": "Pruebas",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 14 – Problemas Frecuentes
    # ------------------------------------------------------------------
    {
      "number": 14,
      "title": "Problemas Frecuentes",
      "body": (
        "[EDITAR] Liste los problemas más comunes encontrados durante el "
        "desarrollo y operación del sistema, junto con sus causas probables "
        "y soluciones verificadas."
      ),
      "figure_desc": "[EDITAR] Tabla de diagnóstico de fallos con árbol de decisión.",
      "note": "[EDITAR] Consulte este capítulo antes de contactar al soporte técnico.",
      "warn": "[EDITAR] Algunas soluciones requieren reprogramar el firmware. Haga backup antes.",
      "tip": "[EDITAR] Mantenga un log de errores en el ESP32 para facilitar el diagnóstico remoto.",
      "label": "Problemas",
      "extra": _make_troubleshooting_table(),
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 15 – Mejoras Futuras
    # ------------------------------------------------------------------
    {
      "number": 15,
      "title": "Mejoras Futuras",
      "body": (
        "[EDITAR] Describa las mejoras planificadas para futuras versiones "
        "del sistema: nuevas funcionalidades, optimizaciones de rendimiento, "
        "reducción de costos y escalabilidad."
      ),
      "figure_desc": "[EDITAR] Roadmap de desarrollo con hitos y fechas estimadas.",
      "note": "[EDITAR] Las mejoras están priorizadas según impacto y esfuerzo de implementación.",
      "warn": "[EDITAR] Algunas mejoras propuestas pueden requerir rediseño de hardware.",
      "tip": "[EDITAR] Solicite retroalimentación de usuarios para priorizar las mejoras más valoradas.",
      "label": "Mejoras",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 16 – Conclusiones
    # ------------------------------------------------------------------
    {
      "number": 16,
      "title": "Conclusiones",
      "body": (
        "[EDITAR] Redacte las conclusiones del proyecto: objetivos alcanzados, "
        "lecciones aprendidas, limitaciones identificadas y el impacto "
        "del sistema ESP-VoCat en su contexto de aplicación."
      ),
      "figure_desc": "[EDITAR] Resumen visual de logros y métricas del proyecto.",
      "note": "[EDITAR] Las conclusiones deben estar respaldadas por los datos de las pruebas del Capítulo 13.",
      "warn": "[EDITAR] Evite conclusiones no sustentadas por evidencia experimental.",
      "tip": "[EDITAR] Incluya métricas cuantitativas (tiempo de respuesta, precisión, consumo) en las conclusiones.",
      "label": "Conclusiones",
    },

    # ------------------------------------------------------------------
    # CAPÍTULO 17 – Bibliografía
    # ------------------------------------------------------------------
    {
      "number": 17,
      "title": "Bibliografía",
      "body": (
        "[EDITAR] Liste todas las referencias bibliográficas utilizadas: "
        "hojas de datos, libros, artículos, documentación oficial y "
        "recursos en línea. Use formato IEEE o APA según preferencia."
      ),
      "figure_desc": "[EDITAR] No aplica — este capítulo es solo texto bibliográfico.",
      "note": "[EDITAR] Formato sugerido: [N] Autor, «Título», Editorial, Año.",
      "warn": "[EDITAR] Verifique que todos los enlaces web estén activos al momento de publicar.",
      "tip": "[EDITAR] Use un gestor bibliográfico (Zotero, Mendeley) para mantener las referencias organizadas.",
      "label": "Bibliografía",
      "extra": [
        Paragraph("Referencias", _STYLES["SectionTitle"]),
        Paragraph(
          "[1] [EDITAR] Espressif Systems, «ESP32 Series Datasheet», "
          "Versión 3.9, 2023.<br/>"
          "[2] [EDITAR] Texas Instruments, «A4988 Stepper Motor Driver Carrier», "
          "Hoja de datos, 2019.<br/>"
          "[3] [EDITAR] Autor, «Título del libro técnico», Editorial, Año.<br/>"
          "[4] [EDITAR] Autor, «Artículo o paper», Revista, Vol., pp., Año.<br/>"
          "[5] [EDITAR] Nombre del recurso web, URL, fecha de consulta.",
          _STYLES["BodyText"],
        ),
      ],
    },

  ]  # fin chapters
  return chapters


# ==============================================================================
# TABLAS DE EJEMPLO
#   → Edita los datos de cada tabla según tu proyecto.
# ==============================================================================

def _make_gpio_table():
  """Tabla de asignación de pines GPIO del ESP32."""
  headers = ["GPIO", "Función", "Dirección", "Módulo", "Notas"]
  rows = [
    ["GPIO 2",  "[EDITAR] LED estado",    "Salida", "On-board",  "Active HIGH"],
    ["GPIO 4",  "[EDITAR] Sensor trigger", "Salida", "Ultrasonic", "10 µs pulse"],
    ["GPIO 5",  "[EDITAR] STEP",          "Salida", "Motor",      "Pulso paso"],
    ["GPIO 12", "[EDITAR] DIR",           "Salida", "Motor",      "0=CW, 1=CCW"],
    ["GPIO 13", "[EDITAR] ENABLE",        "Salida", "Motor",      "Active LOW"],
    ["GPIO 16", "[EDITAR] UART RX",       "Entrada","Comms",      "115200 bps"],
    ["GPIO 17", "[EDITAR] UART TX",       "Salida", "Comms",      "115200 bps"],
    ["GPIO 34", "[EDITAR] ADC sensor",    "Entrada","Sensor",     "Solo input"],
    ["GPIO 35", "[EDITAR] ADC sensor 2",  "Entrada","Sensor",     "Solo input"],
  ]
  cw = [1.5*cm, 3.5*cm, 2*cm, 2.5*cm, CONTENT_WIDTH - 9.5*cm]
  return make_table("Tabla 4.1 – Asignación de Pines GPIO", headers, rows, cw)


def _make_protocol_table():
  """Tabla de comandos del protocolo UART."""
  headers = ["Comando", "Dirección", "Formato", "Descripción", "Respuesta"]
  rows = [
    ["PING",    "Host→ESP", "PING\\n",        "[EDITAR] Verificar conexión",  "PONG\\n"],
    ["GET_ADC", "Host→ESP", "GET_ADC,<ch>\\n", "[EDITAR] Leer canal ADC",      "<valor>\\n"],
    ["SET_PWM", "Host→ESP", "SET_PWM,<ch>,<d>\\n", "[EDITAR] Configurar PWM", "OK\\n"],
    ["MOVE",    "Host→ESP", "MOVE,<pasos>\\n", "[EDITAR] Mover motor",        "DONE\\n"],
    ["STOP",    "Host→ESP", "STOP\\n",         "[EDITAR] Detener motor",       "OK\\n"],
    ["STATUS",  "Host→ESP", "STATUS\\n",      "[EDITAR] Estado del sistema",  "<json>\\n"],
    ["RESET",   "Host→ESP", "RESET\\n",        "[EDITAR] Reiniciar ESP32",     "—"],
    ["CAL",     "Host→ESP", "CAL,<sensor>\\n", "[EDITAR] Calibrar sensor",    "OK\\n"],
  ]
  cw = [2*cm, 2.2*cm, 3.5*cm, 4.5*cm, CONTENT_WIDTH - 12.2*cm]
  return make_table("Tabla 6.1 – Comandos del Protocolo UART", headers, rows, cw)


def _make_specs_table():
  """Tabla de especificaciones técnicas del motor."""
  headers = ["Parámetro", "Valor", "Unidad", "Condición"]
  rows = [
    ["Modelo",           "[EDITAR] NEMA 17",   "—",    "—"],
    ["Pasos/revolución", "[EDITAR] 200",       "steps", "Full step"],
    ["Torque nominal",   "[EDITAR] 0.45",      "N·m",  "—"],
    ["Corriente/ fase",  "[EDITAR] 1.7",       "A",    "—"],
    ["Voltaje",          "[EDITAR] 12",        "V DC", "—"],
    ["Driver",           "[EDITAR] A4988",     "—",    "—"],
    ["Microstepping",    "[EDITAR] 1/16",      "—",    "MS1=H MS2=H MS3=H"],
    ["Vel. máxima",      "[EDITAR] 1000",      "steps/s", "—"],
  ]
  cw = [3.5*cm, 3*cm, 2*cm, CONTENT_WIDTH - 8.5*cm]
  return make_table("Tabla 8.1 – Especificaciones del Motor Paso a Paso", headers, rows, cw)


def _make_bom_table():
  """Tabla de lista de materiales (BOM)."""
  headers = ["#", "Cant.", "Descripción", "Ref./Parte", "Proveedor"]
  rows = [
    ["1",  "1", "[EDITAR] ESP32-WROOM-32",    "ESP32-WROOM-32D", "[EDITAR]"],
    ["2",  "1", "[EDITAR] Driver A4988",       "A4988",           "[EDITAR]"],
    ["3",  "1", "[EDITAR] Motor NEMA 17",      "17HS19-2004S",    "[EDITAR]"],
    ["4",  "2", "[EDITAR] Sensor HC-SR04",     "HC-SR04",         "[EDITAR]"],
    ["5",  "1", "[EDITAR] Regulador 3.3V",     "AMS1117-3.3",     "[EDITAR]"],
    ["6",  "5", "[EDITAR] Resistencia 10kΩ",   "RC0603FR-0710KL", "[EDITAR]"],
    ["7",  "3", "[EDITAR] Condensador 100nF",  "CL10B104KB8NNNC", "[EDITAR]"],
    ["8",  "1", "[EDITAR] Fuente 12V 2A",      "GST25A12-P1J",    "[EDITAR]"],
    ["9",  "1", "[EDITAR] PCB personalizada",  "ESP-VOCAT-PCB",   "[EDITAR]"],
    ["10", "—", "[EDITAR] Tornillería M3",       "DIN 912",         "[EDITAR]"],
  ]
  cw = [0.8*cm, 1*cm, 5*cm, 3.5*cm, CONTENT_WIDTH - 10.3*cm]
  return make_table("Tabla 12.1 – Lista de Materiales (BOM)", headers, rows, cw)


def _make_troubleshooting_table():
  """Tabla de problemas frecuentes y soluciones."""
  headers = ["#", "Síntoma", "Causa Probable", "Solución"]
  rows = [
    ["1", "[EDITAR] Motor no gira",         "[EDITAR] Driver sin enable",    "[EDITAR] Verificar pin ENABLE"],
    ["2", "[EDITAR] UART sin respuesta",    "[EDITAR] Baudrate incorrecto",   "[EDITAR] Configurar 115200 bps"],
    ["3", "[EDITAR] Lecturas ADC erráticas","[EDITAR] Ruido en línea",       "[EDITAR] Agregar capacitor 100nF"],
    ["4", "[EDITAR] ESP32 no arranca",      "[EDITAR] Fuente insuficiente",   "[EDITAR] Usar fuente ≥ 1A"],
    ["5", "[EDITAR] Motor se calienta",     "[EDITAR] Corriente excesiva",  "[EDITAR] Ajustar pot. del driver"],
    ["6", "[EDITAR] Sensor siempre 0",     "[EDITAR] Cable desconectado",    "[EDITAR] Verificar conexión GPIO"],
  ]
  cw = [0.8*cm, 3.5*cm, 4*cm, CONTENT_WIDTH - 8.3*cm]
  return make_table("Tabla 14.1 – Problemas Frecuentes y Soluciones", headers, rows, cw)


# ==============================================================================
# CONSTRUCCIÓN DE LA PORTADA
# ==============================================================================

def build_cover():
  """Genera los flowables de la página de portada."""
  elements = []

  elements.append(Spacer(1, 3 * cm))

  # Título principal
  elements.append(Paragraph(DOC_TITLE, _STYLES["CoverTitle"]))
  elements.append(Spacer(1, 6))
  elements.append(Paragraph(DOC_SUBTITLE, _STYLES["CoverSubtitle"]))
  elements.append(Spacer(1, 1.5 * cm))

  # Caja grande para imagen de portada
  elements.append(CoverImagePlaceholder(
    width=CONTENT_WIDTH,
    height=9 * cm,
  ))
  elements.append(Spacer(1, 1.5 * cm))

  # Metadatos
  elements.append(Paragraph(f"<b>Autor:</b> {DOC_AUTHOR}", _STYLES["CoverMeta"]))
  elements.append(Paragraph(f"<b>Versión:</b> {DOC_VERSION}", _STYLES["CoverMeta"]))
  elements.append(Paragraph(f"<b>Fecha:</b> {DOC_DATE}", _STYLES["CoverMeta"]))

  elements.append(Spacer(1, 1 * cm))
  elements.append(HorizontalRule(CONTENT_WIDTH, thickness=1, color=COLOR_ACCENT))

  return elements


# ==============================================================================
# CONSTRUCCIÓN DEL ÍNDICE
# ==============================================================================

# Lista de capítulos para el índice (título y número de página estimado)
# [EDITAR] Actualice los números de página después de generar el PDF
#          si necesita un índice con páginas exactas.
TOC_ENTRIES = [
  (1,  "Introducción",           3),
  (2,  "Objetivos",              4),
  (3,  "Arquitectura General",   5),
  (4,  "Hardware",               6),
  (5,  "Firmware",               7),
  (6,  "Comunicación UART",      8),
  (7,  "Sensores",               9),
  (8,  "Motor Paso a Paso",     10),
  (9,  "Diseño Mecánico",       11),
  (10, "Ensamblaje",            12),
  (11, "Calibración",           13),
  (12, "Lista de Materiales",   14),
  (13, "Pruebas",               15),
  (14, "Problemas Frecuentes",  16),
  (15, "Mejoras Futuras",       17),
  (16, "Conclusiones",          18),
  (17, "Bibliografía",          19),
]


def build_toc():
  """Genera la página de índice."""
  elements = []

  elements.append(PageBreak())
  elements.append(Paragraph("Índice General", _STYLES["TOCTitle"]))
  elements.append(Spacer(1, 12))

  for number, title, page in TOC_ENTRIES:
    elements.append(TOCItem(number, title, page, CONTENT_WIDTH))
    elements.append(Spacer(1, 4))

  return elements


# ==============================================================================
# CONSTRUCCIÓN DE TODOS LOS CAPÍTULOS
# ==============================================================================

def build_all_chapters():
  """Itera sobre la definición de capítulos y construye su contenido."""
  elements = []
  chapters = get_chapters_content()

  for ch in chapters:
    elements.extend(make_chapter(
      number=ch["number"],
      title=ch["title"],
      body_text=ch["body"],
      figure_desc=ch["figure_desc"],
      note_text=ch["note"],
      warn_text=ch["warn"],
      tip_text=ch["tip"],
      extra_elements=ch.get("extra"),
      chapter_label=ch.get("label", ""),
    ))

  return elements


# ==============================================================================
# PÁGINA FINAL (contraportada / espacio reservado)
# ==============================================================================

def build_back_cover():
  """Genera una página final con espacio para contraportada."""
  elements = []
  elements.append(PageBreak())
  elements.append(Spacer(1, 6 * cm))
  elements.append(Paragraph(
    "— Fin del Documento —",
    _STYLES["CoverSubtitle"],
  ))
  elements.append(Spacer(1, 1 * cm))
  elements.append(CoverImagePlaceholder(
    width=CONTENT_WIDTH * 0.6,
    height=5 * cm,
  ))
  elements.append(Spacer(1, 1 * cm))
  elements.append(Paragraph(
    f"{DOC_TITLE} · {DOC_VERSION} · {DOC_DATE}",
    _STYLES["CoverMeta"],
  ))
  elements.append(Paragraph(
  "[EDITAR] Información de contacto, licencia o datos de la institución.",
    _STYLES["CoverMeta"],
  ))
  return elements


# ==============================================================================
# VARIABLE GLOBAL DE ESTILOS (se inicializa en main)
# ==============================================================================
_STYLES = {}


# ==============================================================================
# FUNCIÓN PRINCIPAL
# ==============================================================================

def main():
  """
  Punto de entrada del script.
  Construye y genera el PDF completo.
  """
  global _STYLES

  print("=" * 60)
  print("  Generador de Manual Técnico — ESP-VoCat")
  print("=" * 60)
  print(f"  Título  : {DOC_TITLE}")
  print(f"  Autor   : {DOC_AUTHOR}")
  print(f"  Versión : {DOC_VERSION}")
  print(f"  Fecha   : {DOC_DATE}")
  print(f"  Salida  : {OUTPUT_FILE}")
  print("-" * 60)

  # --- Inicializar estilos ---
  _STYLES.update(build_styles())

  # --- Crear documento ---
  doc = BaseDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=MARGIN_LEFT,
    rightMargin=MARGIN_RIGHT,
    topMargin=MARGIN_TOP,
    bottomMargin=MARGIN_BOTTOM,
    title=DOC_TITLE,
    author=DOC_AUTHOR,
    subject=DOC_SUBJECT,
    keywords=DOC_KEYWORDS,
  )

  # --- Frame y plantillas de página ---
  frame = Frame(
    MARGIN_LEFT, MARGIN_BOTTOM,
    CONTENT_WIDTH, CONTENT_HEIGHT,
    id="main_frame",
  )

  template_cover = PageTemplate(
    id="cover",
    frames=[frame],
    onPage=on_first_page,
  )
  template_normal = PageTemplate(
    id="normal",
    frames=[frame],
    onPage=on_later_pages,
  )

  doc.addPageTemplates([template_cover, template_normal])

  # --- Ensamblar contenido ---
  story = []

  # Portada
  story.extend(build_cover())

  # Cambiar a plantilla normal después de la portada
  story.append(NextPageTemplate("normal"))

  # Índice
  story.extend(build_toc())

  # Capítulos (1 – 17)
  story.extend(build_all_chapters())

  # Contraportada
  story.extend(build_back_cover())

  # --- Generar PDF ---
  print("  Generando PDF...")
  try:
    doc.build(story)
    file_size = os.path.getsize(OUTPUT_FILE)
    print(f"  [OK] PDF generado exitosamente: {OUTPUT_FILE}")
    print(f"  [OK] Tamano: {file_size / 1024:.1f} KB")
    print(f"  [OK] Figuras: {_figure_counter}")
    print(f"  [OK] Capitulos: {len(get_chapters_content())}")
    print("=" * 60)
    print("  Edite generar_manual.py para personalizar el contenido.")
    print("=" * 60)
  except Exception as exc:
    print(f"  [ERROR] Error al generar el PDF: {exc}", file=sys.stderr)
    sys.exit(1)


# ==============================================================================
# PUNTO DE ENTRADA
# ==============================================================================
if __name__ == "__main__":
  main()
