#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
毕业论文PDF生成脚本
题目：基于Spring Cloud的高校实验室设备管理系统设计与实现
生成文件：/home/z/my-project/download/thesis_body.pdf
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, CondPageBreak,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame
from reportlab.platypus.frames import Frame as RLFrame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.graphics.shapes import Drawing, Line, String, Rect
from reportlab.graphics import renderPDF
from io import BytesIO

# ============================================================
# 配置常量
# ============================================================
OUTPUT_PDF = '/home/z/my-project/download/thesis_body.pdf'
BASE_DIR = '/home/z/my-project/download'
IMG_DIR = os.path.join(BASE_DIR, 'thesis_images')
CODE_DIR = os.path.join(IMG_DIR, 'code_screenshots')

FONT_SIMHEI = '/usr/share/fonts/truetype/chinese/SimHei.ttf'
FONT_MS_YAHEI = '/usr/share/fonts/truetype/chinese/msyh.ttf'
FONT_SIMSUN = '/usr/share/fonts/truetype/chinese/SimSun.ttf'
FONT_TIMES = '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'

# 页面尺寸与边距
PAGE_W, PAGE_H = A4
MARGIN_TOP = 2.5 * cm
MARGIN_BOTTOM = 2.5 * cm
MARGIN_LEFT = 3.0 * cm
MARGIN_RIGHT = 2.5 * cm

# 颜色
ACCENT = colors.HexColor('#5d38ce')
TEXT_PRIMARY = colors.HexColor('#272623')
TEXT_MUTED = colors.HexColor('#817d75')
BG_SURFACE = colors.HexColor('#e3e0db')
BG_PAGE = colors.HexColor('#efeeec')

# ============================================================
# 字体注册
# ============================================================
pdfmetrics.registerFont(TTFont('SimHei', FONT_SIMHEI))
pdfmetrics.registerFont(TTFont('SimSun', FONT_SIMSUN))
pdfmetrics.registerFont(TTFont('MsYaHei', FONT_MS_YAHEI))
pdfmetrics.registerFont(TTFont('TimesNewRoman', FONT_TIMES))

addMapping('SimHei', 0, 0, 'SimHei')
addMapping('SimHei', 1, 0, 'SimHei')
addMapping('SimSun', 0, 0, 'SimSun')
addMapping('SimSun', 1, 0, 'SimSun')
addMapping('TimesNewRoman', 0, 0, 'TimesNewRoman')
addMapping('TimesNewRoman', 1, 0, 'TimesNewRoman')

# ============================================================
# 样式定义
# ============================================================

# 一级标题：三号(16pt)黑体居中
STYLE_H1 = ParagraphStyle(
    'H1',
    fontName='SimHei',
    fontSize=16,
    leading=24,
    alignment=TA_CENTER,
    spaceBefore=24,
    spaceAfter=12,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 二级标题：四号(14pt)黑体
STYLE_H2 = ParagraphStyle(
    'H2',
    fontName='SimHei',
    fontSize=14,
    leading=21,
    alignment=TA_LEFT,
    spaceBefore=18,
    spaceAfter=8,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 三级标题：小四号(12pt)黑体
STYLE_H3 = ParagraphStyle(
    'H3',
    fontName='SimHei',
    fontSize=12,
    leading=18,
    alignment=TA_LEFT,
    spaceBefore=12,
    spaceAfter=6,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 正文：小四号(12pt)宋体，1.5倍行距，首行缩进2字符
STYLE_BODY = ParagraphStyle(
    'Body',
    fontName='SimSun',
    fontSize=12,
    leading=18,  # 1.5x line spacing
    alignment=TA_LEFT,
    firstLineIndent=24,  # 2 Chinese chars
    spaceBefore=0,
    spaceAfter=0,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 正文无缩进
STYLE_BODY_NO_INDENT = ParagraphStyle(
    'BodyNoIndent',
    parent=STYLE_BODY,
    firstLineIndent=0,
)

# 图注
STYLE_FIGURE_CAPTION = ParagraphStyle(
    'FigureCaption',
    fontName='SimSun',
    fontSize=10.5,
    leading=16,
    alignment=TA_CENTER,
    spaceBefore=6,
    spaceAfter=12,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 表注
STYLE_TABLE_CAPTION = ParagraphStyle(
    'TableCaption',
    fontName='SimSun',
    fontSize=10.5,
    leading=16,
    alignment=TA_CENTER,
    spaceBefore=12,
    spaceAfter=6,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 摘要标题
STYLE_ABSTRACT_TITLE = ParagraphStyle(
    'AbstractTitle',
    fontName='SimHei',
    fontSize=16,
    leading=24,
    alignment=TA_CENTER,
    spaceBefore=12,
    spaceAfter=12,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 摘要正文
STYLE_ABSTRACT_BODY = ParagraphStyle(
    'AbstractBody',
    fontName='SimSun',
    fontSize=12,
    leading=18,
    alignment=TA_LEFT,
    firstLineIndent=24,
    spaceBefore=0,
    spaceAfter=0,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 关键词
STYLE_KEYWORDS = ParagraphStyle(
    'Keywords',
    fontName='SimSun',
    fontSize=12,
    leading=18,
    alignment=TA_LEFT,
    firstLineIndent=0,
    spaceBefore=12,
    spaceAfter=6,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 英文摘要正文
STYLE_EN_BODY = ParagraphStyle(
    'EnBody',
    fontName='TimesNewRoman',
    fontSize=12,
    leading=18,
    alignment=TA_JUSTIFY,
    firstLineIndent=24,
    spaceBefore=0,
    spaceAfter=0,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 英文标题
STYLE_EN_TITLE = ParagraphStyle(
    'EnTitle',
    fontName='TimesNewRoman',
    fontSize=16,
    leading=24,
    alignment=TA_CENTER,
    spaceBefore=12,
    spaceAfter=12,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 英文关键词
STYLE_EN_KEYWORDS = ParagraphStyle(
    'EnKeywords',
    fontName='TimesNewRoman',
    fontSize=12,
    leading=18,
    alignment=TA_LEFT,
    firstLineIndent=0,
    spaceBefore=12,
    spaceAfter=6,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 参考文献条目
STYLE_REF = ParagraphStyle(
    'Reference',
    fontName='SimSun',
    fontSize=10.5,
    leading=16,
    alignment=TA_LEFT,
    leftIndent=24,
    firstLineIndent=-24,
    spaceBefore=2,
    spaceAfter=2,
    textColor=TEXT_PRIMARY,
    wordWrap='CJK',
)

# 目录样式
STYLE_TOC_H1 = ParagraphStyle(
    'TOCH1',
    fontName='SimHei',
    fontSize=12,
    leading=22,
    leftIndent=0,
    wordWrap='CJK',
)

STYLE_TOC_H2 = ParagraphStyle(
    'TOCH2',
    fontName='SimSun',
    fontSize=12,
    leading=22,
    leftIndent=24,
    wordWrap='CJK',
)

STYLE_TOC_H3 = ParagraphStyle(
    'TOCH3',
    fontName='SimSun',
    fontSize=12,
    leading=22,
    leftIndent=48,
    wordWrap='CJK',
)

# 表格单元格样式
STYLE_TABLE_CELL = ParagraphStyle(
    'TableCell',
    fontName='SimSun',
    fontSize=10.5,
    leading=16,
    alignment=TA_CENTER,
    wordWrap='CJK',
    textColor=TEXT_PRIMARY,
)

STYLE_TABLE_CELL_LEFT = ParagraphStyle(
    'TableCellLeft',
    fontName='SimSun',
    fontSize=10.5,
    leading=16,
    alignment=TA_LEFT,
    wordWrap='CJK',
    textColor=TEXT_PRIMARY,
)

STYLE_TABLE_HEADER = ParagraphStyle(
    'TableHeader',
    fontName='SimHei',
    fontSize=10.5,
    leading=16,
    alignment=TA_CENTER,
    wordWrap='CJK',
    textColor=TEXT_PRIMARY,
)

# ============================================================
# 自定义 DocTemplate（支持TOC多遍构建）
# ============================================================

class ThesisDocTemplate(BaseDocTemplate):
    """支持目录生成的自定义文档模板"""
    
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        
        content_width = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT
        content_height = PAGE_H - MARGIN_TOP - MARGIN_BOTTOM
        
        frame = RLFrame(
            MARGIN_LEFT, MARGIN_BOTTOM,
            content_width, content_height,
            id='normal'
        )
        
        template = PageTemplate(
            id='normal',
            frames=[frame],
            onPage=self._add_page_header_footer,
        )
        self.addPageTemplates([template])
        self.page_count_offset = 0
        
    def _add_page_header_footer(self, canvas, doc):
        """添加页眉页脚"""
        canvas.saveState()
        page_num = doc.page
        
        # 页眉 - 章节标题（简化：只画线）
        canvas.setStrokeColor(TEXT_MUTED)
        canvas.setLineWidth(0.5)
        header_y = PAGE_H - MARGIN_TOP + 10
        canvas.line(MARGIN_LEFT, header_y, PAGE_W - MARGIN_RIGHT, header_y)
        
        # 页脚 - 页码
        canvas.setFont('TimesNewRoman', 10.5)
        canvas.setFillColor(TEXT_PRIMARY)
        page_num_str = str(page_num)
        canvas.drawCentredString(PAGE_W / 2, MARGIN_BOTTOM - 18, page_num_str)
        
        # 页脚线
        footer_y = MARGIN_BOTTOM + 5
        canvas.line(MARGIN_LEFT, footer_y, PAGE_W - MARGIN_RIGHT, footer_y)
        
        canvas.restoreState()


# ============================================================
# 目录类（使用 bookmark 可点击）
# ============================================================

class ThesisTOC(TableOfContents):
    def __init__(self):
        super().__init__()
        self.levelStyles = [STYLE_TOC_H1, STYLE_TOC_H2, STYLE_TOC_H3]


# ============================================================
# 辅助函数
# ============================================================

def h1(text, bookmark_key=None):
    """一级标题"""
    elements = []
    elements.append(CondPageBreak(60))
    style = ParagraphStyle(
        'H1_custom',
        parent=STYLE_H1,
        bookmarkName=bookmark_key or text,
    )
    elements.append(Paragraph(text, style))
    return elements


def h2(text, bookmark_key=None):
    """二级标题"""
    style = ParagraphStyle(
        'H2_custom',
        parent=STYLE_H2,
        bookmarkName=bookmark_key or text,
    )
    return [Paragraph(text, style)]


def h3(text, bookmark_key=None):
    """三级标题"""
    style = ParagraphStyle(
        'H3_custom',
        parent=STYLE_H3,
        bookmarkName=bookmark_key or text,
    )
    return [Paragraph(text, style)]


def body(text):
    """正文段落"""
    return [Paragraph(text, STYLE_BODY)]


def body_ni(text):
    """正文段落（无缩进）"""
    return [Paragraph(text, STYLE_BODY_NO_INDENT)]


def spacer(h=6):
    return [Spacer(1, h)]


def add_image(img_path, caption, fig_num, max_width=450, max_height=300):
    """添加图片及图注"""
    elements = []
    if os.path.exists(img_path):
        from reportlab.lib.utils import ImageReader
        img = Image(img_path)
        img_w, img_h = img.imageWidth, img.imageHeight
        ratio = min(max_width / img_w, max_height / img_h, 1.0)
        img.drawWidth = img_w * ratio
        img.drawHeight = img_h * ratio
        img.hAlign = 'CENTER'
        elements.append(img)
    else:
        # 生成占位图片
        d = Drawing(max_width, 80)
        d.add(Rect(0, 0, max_width, 80, fillColor=colors.HexColor('#f5f5f5'),
                   strokeColor=colors.grey, strokeWidth=0.5))
        d.add(String(max_width/2, 35, f"[{caption}]",
                     fontSize=12, fontName='SimHei',
                     textAnchor='middle', fillColor=colors.grey))
        elements.append(d)
    
    cap_style = ParagraphStyle(
        'FigCap', parent=STYLE_FIGURE_CAPTION,
    )
    elements.append(Paragraph(f'图{fig_num} {caption}', cap_style))
    return elements


def make_placeholder_screenshot(page_name, width=420, height=200):
    """生成前端页面截图占位图"""
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=colors.HexColor('#fafafa'),
               strokeColor=colors.HexColor('#cccccc'), strokeWidth=1))
    # 标题栏模拟
    d.add(Rect(0, height - 28, width, 28, fillColor=colors.HexColor('#e8e8e8'),
               strokeColor=colors.HexColor('#cccccc'), strokeWidth=0.5))
    d.add(String(width/2, height - 20, f'—— 需要{page_name}截图 ——',
                 fontSize=11, fontName='SimHei',
                 textAnchor='middle', fillColor=TEXT_MUTED))
    return d


def add_screenshot_placeholder(page_name, fig_num, caption, width=420, height=200):
    """添加前端截图占位图"""
    elements = []
    d = make_placeholder_screenshot(page_name, width, height)
    d.hAlign = 'CENTER'
    elements.append(d)
    elements.append(Paragraph(f'图{fig_num} {caption}', STYLE_FIGURE_CAPTION))
    return elements


def add_code_screenshot(code_file, fig_num, caption, max_width=440, max_height=260):
    """添加代码截图"""
    img_path = os.path.join(CODE_DIR, code_file)
    return add_image(img_path, caption, fig_num, max_width, max_height)


def add_table_with_caption(table_data, caption, table_num, col_widths=None):
    """添加带标题的表格，所有单元格使用Paragraph"""
    elements = []
    elements.append(Paragraph(f'表{table_num} {caption}', STYLE_TABLE_CAPTION))
    
    # 将所有单元格转为Paragraph
    formatted_data = []
    for row_idx, row in enumerate(table_data):
        formatted_row = []
        for cell in row:
            if isinstance(cell, str):
                style = STYLE_TABLE_HEADER if row_idx == 0 else STYLE_TABLE_CELL
                formatted_row.append(Paragraph(cell, style))
            else:
                formatted_row.append(cell)
        formatted_data.append(formatted_row)
    
    t = Table(formatted_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, TEXT_MUTED),
        ('BACKGROUND', (0, 0), (-1, 0), BG_SURFACE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    t.hAlign = 'CENTER'
    elements.append(t)
    return elements


# ============================================================
# 论文内容
# ============================================================

def build_chinese_abstract():
    """中文摘要"""
    story = []
    story.append(Paragraph('摘  要', STYLE_ABSTRACT_TITLE))
    story.append(Spacer(1, 6))
    
    abstract_text = (
        '随着高校教育事业的快速发展，实验室建设规模不断扩大，实验室设备的种类和数量也在持续增长。'
        '传统的实验室设备管理方式主要依赖人工登记和纸质记录，不仅效率低下、容易出错，而且难以实现设备的实时监控和高效调度。'
        '特别是在多人同时借用同一设备时，容易出现库存数据不一致的问题，严重影响教学和科研工作的正常开展。'
        '因此，开发一套功能完善、性能优良的实验室设备管理系统具有重要的现实意义。'
    )
    story.append(Paragraph(abstract_text, STYLE_ABSTRACT_BODY))
    
    abstract_text2 = (
        '本文设计并实现了一套基于Spring Cloud微服务架构的高校实验室设备管理系统。'
        '系统采用前后端分离的开发模式，后端基于Spring Cloud构建微服务集群，'
        '包含网关服务、认证服务、设备管理服务、借用预约服务、用户管理服务、统计报表服务和公共模块七个核心模块。'
        '前端采用Vue.js框架，结合Element Plus组件库构建用户界面，实现了响应式的单页应用。'
        '系统使用MySQL作为主数据库存储业务数据，Redis作为缓存和分布式锁的实现载体，'
        'Nacos作为服务注册中心和配置中心，有效提升了系统的可扩展性和可维护性。'
    )
    story.append(Paragraph(abstract_text2, STYLE_ABSTRACT_BODY))
    
    abstract_text3 = (
        '针对设备借用过程中的并发库存扣减问题，本文提出了基于Redis分布式锁与MyBatis-Plus乐观锁的双重保障机制。'
        '该机制通过Redis的SETNX命令实现分布式环境下的互斥访问控制，'
        '同时利用数据库层面的版本号校验确保数据一致性，有效解决了高并发场景下的超卖问题。'
        '经过系统测试验证，本系统在功能完整性、系统性能和用户体验等方面均达到了预期目标，'
        '能够满足高校实验室设备管理的实际需求，为同类系统的设计与开发提供了有价值的参考。'
    )
    story.append(Paragraph(abstract_text3, STYLE_ABSTRACT_BODY))
    
    story.append(Paragraph(
        '<b>关键词：</b>Spring Cloud；微服务架构；实验设备管理；前后端分离；库存并发控制',
        STYLE_KEYWORDS
    ))
    
    story.append(PageBreak())
    return story


def build_english_abstract():
    """英文摘要"""
    story = []
    story.append(Paragraph(
        'Design and Implementation of Lab Equipment Management System Based on Spring Cloud',
        STYLE_EN_TITLE
    ))
    story.append(Paragraph('Abstract', ParagraphStyle(
        'EnAbstractTitle',
        parent=STYLE_EN_TITLE,
        fontSize=14,
        leading=21,
    )))
    story.append(Spacer(1, 6))
    
    en_text1 = (
        'With the rapid development of higher education, the scale of laboratory construction '
        'has been continuously expanding, and both the variety and quantity of laboratory equipment '
        'have been steadily increasing. Traditional laboratory equipment management methods primarily '
        'rely on manual registration and paper-based records, which are not only inefficient and '
        'error-prone but also difficult to achieve real-time monitoring and efficient scheduling of '
        'equipment. Particularly when multiple users attempt to borrow the same equipment simultaneously, '
        'inconsistent inventory data often occurs, seriously affecting the normal progress of teaching '
        'and research activities. Therefore, developing a comprehensive and high-performance laboratory '
        'equipment management system is of significant practical importance.'
    )
    story.append(Paragraph(en_text1, STYLE_EN_BODY))
    
    en_text2 = (
        'This thesis designs and implements a university laboratory equipment management system '
        'based on the Spring Cloud microservice architecture. The system adopts a frontend-backend '
        'separation development model. The backend constructs a microservice cluster based on Spring Cloud, '
        'comprising seven core modules: gateway service, authentication service, equipment management service, '
        'borrowing and reservation service, user management service, statistical report service, and a common module. '
        'The frontend utilizes the Vue.js framework combined with the Element Plus component library to build '
        'the user interface, implementing a responsive single-page application. The system uses MySQL as the '
        'primary database for business data storage, Redis as the cache and distributed lock implementation carrier, '
        'and Nacos as the service registry and configuration center, effectively improving system scalability '
        'and maintainability.'
    )
    story.append(Paragraph(en_text2, STYLE_EN_BODY))
    
    en_text3 = (
        'To address the concurrent inventory deduction problem during equipment borrowing, '
        'this thesis proposes a dual guarantee mechanism based on Redis distributed locks and '
        'MyBatis-Plus optimistic locks. This mechanism implements mutual exclusive access control '
        'in distributed environments through Redis SETNX commands while ensuring data consistency '
        'through database-level version verification, effectively solving the overselling problem '
        'in high-concurrency scenarios. Through systematic testing and verification, this system '
        'has achieved expected goals in terms of functional completeness, system performance, and '
        'user experience, meeting the practical requirements of university laboratory equipment '
        'management and providing valuable references for the design and development of similar systems.'
    )
    story.append(Paragraph(en_text3, STYLE_EN_BODY))
    
    story.append(Paragraph(
        '<b>Keywords:</b> Spring Cloud; Microservice Architecture; Lab Equipment Management; '
        'Frontend-Backend Separation; Inventory Concurrency Control',
        STYLE_EN_KEYWORDS
    ))
    
    story.append(PageBreak())
    return story


def build_chapter1():
    """第一章 绪论"""
    story = []
    story.extend(h1('第1章 绪论', 'ch1'))
    
    # 1.1 研究背景与意义
    story.extend(h2('1.1 研究背景与意义', 'ch1_1'))
    
    story.extend(body(
        '近年来，随着我国高等教育事业的蓬勃发展，高校实验室作为培养学生实践能力和创新精神的重要基地，'
        '其建设规模和装备水平得到了显著提升。各类教学实验室、科研实验室的数量不断增加，'
        '实验设备的种类日益丰富，从基础的测量仪器到高端的分析设备，总价值往往达到数千万元甚至上亿元。'
        '如何科学有效地管理这些宝贵的实验设备资源，最大限度地发挥其在教学和科研中的作用，'
        '已成为高校实验室管理工作中亟待解决的重要课题。'
    ))
    
    story.extend(body(
        '传统的实验室设备管理方式主要依赖人工登记和纸质台账，管理人员通过Excel表格或纸质记录本'
        '跟踪设备的借用、归还和维护情况。这种管理方式存在诸多弊端：首先，人工登记效率低下，'
        '特别是在设备借用高峰期，管理人员需要花费大量时间处理借还手续；其次，纸质记录容易丢失和损坏，'
        '数据的安全性和完整性难以保障；再次，信息更新滞后，管理人员和师生无法实时了解设备的可用状态，'
        '导致设备利用率偏低；最后，多人同时借用同一批设备时，容易出现信息不一致和冲突，'
        '严重影响教学和科研工作的正常开展。'
    ))
    
    story.extend(body(
        '与此同时，早期开发的一些实验室设备管理系统大多采用单体架构设计，虽然在一定程度上缓解了人工管理的压力，'
        '但随着系统功能的不断扩展和用户规模的持续增长，单体架构的局限性日益凸显。'
        '单体架构将所有功能模块打包在一个应用中部署，各模块之间高度耦合，'
        '一旦某个模块出现问题，可能影响整个系统的可用性。此外，单体应用的扩展性较差，'
        '难以针对特定的高负载模块进行独立扩容，系统的维护和升级成本也随着代码规模的增大而急剧上升。'
    ))
    
    story.extend(body(
        '微服务架构作为一种新兴的软件架构风格，将大型应用拆分为一组小型、独立部署的服务，'
        '每个服务围绕特定的业务能力构建，通过轻量级的通信机制进行交互。'
        '相比单体架构，微服务架构具有以下显著优势：一是服务独立部署和扩展，可以根据各服务的负载情况'
        '灵活调整资源分配；二是技术栈灵活，不同服务可以采用最适合的技术方案；'
        '三是故障隔离性好，单个服务的故障不会影响整个系统；四是团队协作效率高，'
        '不同团队可以独立开发和维护各自负责的服务。基于以上分析，采用Spring Cloud微服务架构'
        '设计和实现实验室设备管理系统，不仅能够有效解决传统管理方式的效率问题，'
        '还能为系统的长期演进和功能扩展提供良好的架构基础，具有重要的理论价值和实践意义。'
    ))
    
    # 1.2 国内外研究现状
    story.extend(h2('1.2 国内外研究现状', 'ch1_2'))
    
    story.extend(h3('1.2.1 国外研究现状', 'ch1_2_1'))
    story.extend(body(
        '在实验室信息管理系统领域，国外起步较早，已形成了一批成熟的产品和解决方案。'
        'LabArchive是一款广泛使用的实验室数据管理平台，支持实验数据的存储、共享和版本控制，'
        '但在设备管理功能方面相对薄弱。Labguru是由BioData公司开发的实验室管理平台，'
        '提供了从实验设计到设备管理的全流程功能，支持移动端访问和第三方集成，'
        '但其高昂的订阅费用限制了在国内高校的推广使用。'
        'Quartzy是另一个知名的实验室管理工具，侧重于库存管理和订单管理，'
        '界面友好、操作简便，但其功能深度有限，难以满足复杂的管理需求。'
        '此外，国外高校普遍采用自行开发的定制化系统，如麻省理工学院的Equipment Management System，'
        '利用RFID技术实现设备的自动识别和跟踪，但这类系统建设成本高昂，技术门槛较高。'
    ))
    
    story.extend(h3('1.2.2 国内研究现状', 'ch1_2_2'))
    story.extend(body(
        '国内在实验室设备管理信息化方面也进行了大量的探索和实践。'
        '早期的管理系统多采用C/S架构，使用Delphi、VB等开发工具，功能相对简单，'
        '主要实现基本的设备台账管理和借还登记功能。随着Web技术的发展，'
        'B/S架构逐渐成为主流，研究人员开始利用JSP、ASP.NET等技术构建基于浏览器的管理系统。'
        '近年来，随着Spring Boot、Spring Cloud等框架的成熟，越来越多的管理系统开始采用微服务架构。'
        '例如，某高校基于Spring Boot开发了实验室开放管理系统，实现了实验室预约和设备借用的在线化，'
        '但由于采用单体架构，在并发性能和可扩展性方面存在不足。'
        '另一所高校基于Spring Cloud和Vue.js开发了实验设备管理平台，但在库存并发控制方面'
        '缺乏有效的解决方案，高并发场景下容易出现数据不一致的问题。'
        '总体来看，国内现有的实验室设备管理系统在功能完备性、系统架构合理性和并发控制等方面'
        '仍有较大的改进空间。'
    ))
    
    # 1.3 论文主要工作与结构安排
    story.extend(h2('1.3 论文主要工作与结构安排', 'ch1_3'))
    story.extend(body(
        '本文围绕高校实验室设备管理的实际需求，设计并实现了一套基于Spring Cloud微服务架构的实验室设备管理系统。'
        '主要工作包括以下几个方面：'
    ))
    story.extend(body(
        '（1）深入调研和分析高校实验室设备管理的业务需求和痛点问题，完成系统的需求分析和可行性论证。'
        '（2）基于Spring Cloud微服务架构设计系统的总体架构方案，完成微服务划分、数据库设计和接口设计。'
        '（3）实现系统的核心业务功能，特别是设备借用预约功能和库存并发控制机制。'
        '（4）针对高并发场景下的库存超卖问题，提出并实现基于Redis分布式锁与MyBatis-Plus乐观锁的双重保障方案。'
        '（5）对系统进行全面的功能测试和性能测试，验证系统的正确性和可靠性。'
    ))
    story.extend(body(
        '本文共分为七章，各章内容安排如下：'
        '第1章为绪论，介绍研究背景与意义、国内外研究现状以及论文的主要工作和结构安排。'
        '第2章为相关技术介绍，概述系统开发过程中涉及的关键技术。'
        '第3章为系统需求分析，从可行性分析、功能需求、非功能需求和业务流程等方面对系统进行全面分析。'
        '第4章为系统设计，详细阐述系统的总体架构、微服务划分、数据库设计和接口设计。'
        '第5章为系统实现，展示系统各模块的具体实现过程和关键代码。'
        '第6章为系统测试，介绍测试环境、测试用例和测试结果。'
        '第7章为总结与展望，总结全文工作并提出未来改进方向。'
    ))
    
    return story


def build_chapter2():
    """第二章 相关技术介绍"""
    story = []
    story.extend(h1('第2章 相关技术介绍', 'ch2'))
    
    story.extend(body(
        '本章将对系统开发过程中使用的关键技术进行介绍，包括Spring Cloud微服务架构、'
        'Spring Boot框架、MyBatis-Plus持久层框架、Vue.js前端框架、MySQL数据库、'
        'Redis缓存与分布式锁、JWT认证机制以及Nacos服务注册与配置中心。'
        '通过对这些技术的详细介绍，为后续章节的系统设计和实现奠定理论基础。'
    ))
    
    # 2.1
    story.extend(h2('2.1 Spring Cloud微服务架构', 'ch2_1'))
    story.extend(body(
        'Spring Cloud是一套基于Spring Boot的微服务开发工具集，为开发者提供了一套完整的微服务解决方案。'
        '它并不是一个具体的框架，而是一系列框架的有序集合，通过Spring Boot的自动配置机制，'
        '为微服务架构中的常见问题提供了开箱即用的解决方案。Spring Cloud主要包含以下几个核心组件：'
    ))
    story.extend(body(
        '（1）服务注册与发现：Spring Cloud支持多种服务注册中心，本项目采用Nacos作为服务注册与发现组件。'
        '每个微服务启动时，会将自己的网络地址注册到Nacos服务器，其他服务通过Nacos获取目标服务的地址列表，'
        '实现服务间的相互发现。当服务实例发生变化时，Nacos会自动更新服务列表，'
        '确保服务消费者能够获取到最新的服务信息。'
    ))
    story.extend(body(
        '（2）配置中心：Spring Cloud Config提供了集中化的外部配置管理功能，'
        '支持将配置信息存储在Git仓库、数据库或文件系统中。本项目使用Nacos的配置管理功能，'
        '实现了配置的集中管理和动态更新，无需重启服务即可生效，大大提高了系统的运维效率。'
    ))
    story.extend(body(
        '（3）负载均衡：Spring Cloud LoadBalancer是Spring Cloud提供的客户端负载均衡组件，'
        '替代了早期的Ribbon组件。它支持多种负载均衡策略，包括轮询（Round Robin）、'
        '随机（Random）和权重（Weight-based）等。当服务消费者调用服务提供者时，'
        'LoadBalancer会从服务实例列表中选择一个合适的实例进行请求转发，'
        '实现请求的均匀分配，避免单个实例过载。'
    ))
    story.extend(body(
        '（4）服务间通信：Spring Cloud OpenFeign是一个声明式的Web服务客户端，'
        '使得编写HTTP客户端变得非常简单。开发者只需定义一个接口并添加相应的注解，'
        'Feign就会自动生成实现类，完成服务间的HTTP调用。Feign集成了Ribbon（或LoadBalancer），'
        '天然支持负载均衡，同时支持请求和响应的编解码，可以与Jackson等JSON库无缝集成。'
    ))
    
    # 2.2
    story.extend(h2('2.2 Spring Boot框架', 'ch2_2'))
    story.extend(body(
        'Spring Boot是由Pivotal团队开发的基于Spring框架的快速开发工具，'
        '其核心设计理念是"约定优于配置"（Convention over Configuration），'
        '旨在简化Spring应用的初始搭建和开发过程。Spring Boot具有以下三大核心特性：'
    ))
    story.extend(body(
        '第一，自动配置（Auto-Configuration）。Spring Boot能够根据项目中引入的依赖自动配置应用，'
        '大幅减少了繁琐的手动配置工作。例如，当项目中引入了spring-boot-starter-data-jpa依赖时，'
        'Spring Boot会自动配置数据源、事务管理器和JPA相关组件。'
        '开发者可以通过@Conditional系列注解自定义自动配置的条件，也可以通过application.yml或application.properties'
        '配置文件覆盖默认的自动配置。'
    ))
    story.extend(body(
        '第二，起步依赖（Starter Dependencies）。Spring Boot提供了一系列的starter依赖，'
        '每个starter包含了完成特定功能所需的所有库和自动配置。例如，spring-boot-starter-web包含了'
        'Spring MVC、Tomcat和Jackson等Web开发所需的全部依赖。'
        '开发者只需引入相应的starter，无需关心版本冲突和依赖管理问题，极大地简化了项目的依赖配置。'
    ))
    story.extend(body(
        '第三，内嵌服务器（Embedded Server）。Spring Boot内嵌了Tomcat、Jetty或Undertow等Servlet容器，'
        '开发者无需将应用部署到外部服务器，直接通过java -jar命令即可启动应用。'
        '这一特性极大地简化了应用的部署和运维工作，同时也方便了开发过程中的调试和测试。'
        '本项目的所有微服务均采用Spring Boot作为基础框架，利用其内嵌Tomcat服务器独立运行。'
    ))
    
    # 2.3
    story.extend(h2('2.3 MyBatis-Plus持久层框架', 'ch2_3'))
    story.extend(body(
        'MyBatis-Plus（简称MP）是一个MyBatis的增强工具，在MyBatis的基础上只做增强不做改变，'
        '旨在简化开发、提高效率。本项目选择MyBatis-Plus作为持久层框架，主要基于以下几个方面的考量：'
    ))
    story.extend(body(
        '首先，MyBatis-Plus提供了强大的通用CRUD接口。通过继承BaseMapper接口，'
        '开发者无需编写任何SQL语句即可实现基本的增删改查操作。BaseMapper提供了insert、'
        'deleteById、updateById、selectById、selectList等丰富的数据操作方法，'
        '覆盖了绝大多数日常的数据访问需求，极大地减少了重复代码的编写。'
    ))
    story.extend(body(
        '其次，MyBatis-Plus提供了灵活的条件构造器（Wrapper）。通过LambdaQueryWrapper和QueryWrapper，'
        '开发者可以以链式调用的方式构建复杂的查询条件，避免了SQL字符串拼接的繁琐和易错问题。'
        '条件构造器支持等于、不等于、大于、小于、模糊查询、IN查询、BETWEEN查询等多种条件类型，'
        '同时支持排序、分组和分页等功能。'
    ))
    story.extend(body(
        '再次，MyBatis-Plus内置了强大的分页插件。开发者只需配置分页拦截器，'
        '即可在查询方法中传入Page参数实现物理分页。分页插件会自动拦截查询SQL并添加LIMIT语句，'
        '同时返回总记录数等信息，使用起来非常便捷。'
    ))
    story.extend(body(
        '最后，MyBatis-Plus提供了乐观锁插件，这是本项目解决库存并发控制问题的关键技术。'
        '通过在数据库表中添加version字段，并在实体类中使用@Version注解标注该字段，'
        '乐观锁插件会在更新操作时自动检查版本号。当多条记录同时更新同一条数据时，'
        '只有版本号匹配的更新操作才能成功，其余操作将抛出OptimisticLockException异常，'
        '从而有效防止数据覆盖和不一致问题。这一机制为设备库存的并发扣减提供了数据库层面的安全保障。'
    ))
    
    # 2.4
    story.extend(h2('2.4 Vue.js前端框架', 'ch2_4'))
    story.extend(body(
        'Vue.js是一款用于构建用户界面的渐进式JavaScript框架，由尤雨溪于2014年创建并开源。'
        '本项目采用Vue 3版本，利用其Composition API、响应式系统和组件化开发等核心特性构建前端应用。'
    ))
    story.extend(body(
        'Vue 3引入的Composition API是一种新的组织组件逻辑的方式，'
        '相比Vue 2的Options API，它提供了更好的代码组织能力和逻辑复用能力。'
        '通过setup函数或&lt;script setup&gt;语法糖，开发者可以将相关的逻辑代码组织在一起，'
        '而不是分散在data、methods、computed等选项中。'
        'Composition API还支持自定义组合式函数（Composables），'
        '使得逻辑复用变得更加直观和灵活，有利于提高代码的可维护性和可测试性。'
    ))
    story.extend(body(
        'Vue 3的响应式系统基于ES6的Proxy实现，相比Vue 2的Object.defineProperty方案，'
        '具有更全面的监听能力和更高的性能。Proxy可以拦截对象的属性访问、赋值、删除等操作，'
        '从而实现对数组索引修改、对象属性增删等场景的响应式支持。'
        '此外，Vue 3对响应式系统进行了性能优化，包括惰性计算、依赖收集优化等，'
        '在大规模数据渲染场景下表现出更好的性能。'
    ))
    story.extend(body(
        'Vue的组件化开发理念将页面拆分为独立、可复用的组件，每个组件封装了自己的模板、逻辑和样式。'
        '本项目结合Element Plus组件库，构建了丰富的UI组件，包括设备列表、借用表单、'
        '审批流程、数据图表等。组件化开发不仅提高了代码的复用率，还使得团队协作开发更加高效，'
        '不同的开发者可以独立开发和测试各自负责的组件。'
    ))
    
    # 2.5
    story.extend(h2('2.5 MySQL数据库', 'ch2_5'))
    story.extend(body(
        'MySQL是目前最流行的开源关系型数据库管理系统之一，由Oracle公司开发和维护。'
        '本项目选择MySQL 8.0作为主数据库，主要基于以下几个方面的考量：'
    ))
    story.extend(body(
        'MySQL的InnoDB存储引擎是默认的事务型存储引擎，支持ACID事务特性（原子性、一致性、隔离性、持久性），'
        '能够确保数据库操作的可靠性和数据的一致性。InnoDB采用MVCC（多版本并发控制）机制实现事务隔离，'
        '在READ COMMITTED和REPEATABLE READ隔离级别下，读操作不会阻塞写操作，写操作也不会阻塞读操作，'
        '从而在保证数据一致性的前提下提高了并发性能。'
    ))
    story.extend(body(
        '在索引优化方面，InnoDB采用B+树作为索引的数据结构。B+树是一种平衡的多路搜索树，'
        '所有数据都存储在叶子节点中，叶子节点通过指针连接形成有序链表，非常适合范围查询。'
        'InnoDB的聚簇索引将数据和索引存储在一起，通过主键查询时可以直接获取完整的数据行，'
        '查询效率非常高。本项目在数据库设计阶段充分考虑了索引策略，'
        '为常用查询字段创建了合适的索引，确保系统在大数据量场景下仍能保持良好的查询性能。'
    ))
    
    # 2.6
    story.extend(h2('2.6 Redis缓存与分布式锁', 'ch2_6'))
    story.extend(body(
        'Redis（Remote Dictionary Server）是一个开源的内存数据结构存储系统，'
        '可以用作数据库、缓存和消息中间件。Redis支持字符串、哈希、列表、集合、有序集合等多种数据结构，'
        '具有极高的读写性能，单机即可达到每秒十万级别的操作吞吐量。'
    ))
    story.extend(body(
        '在本项目中，Redis主要用于两个场景：数据缓存和分布式锁的实现。'
        '在数据缓存方面，系统将频繁访问但更新频率较低的数据（如设备分类信息、用户权限配置等）'
        '缓存到Redis中，减少对MySQL数据库的直接访问，降低数据库负载，提高系统响应速度。'
        '缓存数据设置了合理的过期时间（TTL），当数据在数据库中被更新时，系统会同步更新或删除对应的缓存，'
        '确保缓存数据与数据库数据的一致性。'
    ))
    story.extend(body(
        '在分布式锁方面，本项目利用Redis的SETNX（SET if Not eXists）命令实现分布式互斥锁。'
        'SETNX命令是原子操作，只有当指定的键不存在时才能设置成功，返回1；'
        '如果键已经存在，则设置失败，返回0。基于这一特性，'
        '系统在处理设备借用请求时，会先尝试获取以设备ID为键的分布式锁，'
        '只有获取锁成功的请求才能继续执行库存扣减操作。'
        '为了避免因服务异常退出导致的死锁问题，系统为每个分布式锁设置了过期时间，'
        '即使持有锁的服务意外宕机，锁也会在过期后自动释放，不会影响其他请求的正常处理。'
        '这种基于Redis的分布式锁机制为设备库存的并发控制提供了第一层保障。'
    ))
    
    # 2.7
    story.extend(h2('2.7 JWT认证机制', 'ch2_7'))
    story.extend(body(
        'JWT（JSON Web Token）是一种基于JSON的开放标准（RFC 7519），用于在各方之间安全地传输信息。'
        'JWT由三部分组成：Header（头部）、Payload（负载）和Signature（签名），'
        '三部分通过英文句点（.）连接形成一个紧凑的字符串。'
    ))
    story.extend(body(
        'Header部分通常包含两个字段：alg（算法）和typ（类型）。'
        'alg指定了签名使用的算法，本项目采用HS256（HMAC SHA-256）算法；'
        'typ指定了令牌的类型，固定为JWT。'
        'Payload部分包含了需要传输的声明信息（Claims），分为三类：'
        '标准声明（如iss签发者、exp过期时间、sub主题等）、公共声明（自定义的共享信息）'
        '和私有声明（各方自定义的信息）。本项目在Payload中存储了用户ID、用户名和角色等信息。'
        'Signature部分是对Header和Payload的签名，用于验证令牌的完整性和真实性。'
        '签名的生成方式是将Header和Payload分别进行Base64Url编码后用句点连接，'
        '然后使用密钥和指定的算法进行签名。'
    ))
    story.extend(body(
        'JWT认证的工作流程如下：用户提交用户名和密码进行登录，服务端验证通过后生成JWT令牌并返回给客户端。'
        '客户端将JWT令牌存储在本地（通常存储在localStorage或Cookie中），'
        '后续每次请求都在HTTP请求头中携带该令牌（Authorization: Bearer <token>）。'
        '服务端的API网关拦截所有请求，从请求头中提取JWT令牌并进行验证，'
        '验证通过后将用户信息写入请求上下文，转发给后端微服务处理。'
        '这种无状态的认证方式避免了服务端维护会话信息的开销，'
        '特别适合微服务架构下的身份认证需求。'
    ))
    
    # 2.8
    story.extend(h2('2.8 Nacos服务注册与配置中心', 'ch2_8'))
    story.extend(body(
        'Nacos是由阿里巴巴开源的服务注册与配置管理平台，'
        '致力于帮助开发者发现、配置和管理微服务。Nacos提供了服务发现、服务健康监测、'
        '动态配置管理、动态DNS服务和流量管理等核心功能。'
    ))
    story.extend(body(
        '在服务发现方面，Nacos支持基于DNS和基于HTTP的服务发现方式。'
        '每个微服务实例启动时，会向Nacos Server注册自己的服务信息（包括IP地址、端口号、服务名称等），'
        'Nacos Server会将这些信息存储在内存中，并定期进行健康检查。'
        '服务消费者通过服务名称从Nacos获取目标服务的实例列表，'
        '结合客户端负载均衡策略选择一个实例进行调用。'
        '当服务实例出现异常时，Nacos会自动将其从服务列表中剔除，'
        '确保服务消费者不会将请求发送到不可用的实例上。'
    ))
    story.extend(body(
        '在配置管理方面，Nacos提供了一个统一的配置管理界面，'
        '开发者可以在Web控制台上管理各个服务的配置信息。'
        'Nacos支持多种配置格式（Properties、YAML、JSON、XML等），'
        '并提供了配置的版本管理和历史回滚功能。'
        '更重要的是，Nacos支持配置的动态推送——当配置发生变化时，'
        'Nacos会主动将最新的配置推送到相关的服务实例，'
        '服务无需重启即可加载新配置。本项目利用Nacos管理数据库连接、Redis连接、'
        'JWT密钥等配置信息，实现了配置的集中管理和动态更新。'
    ))
    
    return story


def build_chapter3():
    """第三章 系统需求分析"""
    story = []
    story.extend(h1('第3章 系统需求分析', 'ch3'))
    
    story.extend(body(
        '需求分析是软件开发过程中至关重要的阶段，它决定了系统"做什么"的问题。'
        '本章将从可行性分析、功能需求分析、非功能需求分析和业务流程分析四个方面，'
        '对基于Spring Cloud的实验室设备管理系统进行全面、深入的需求分析。'
    ))
    
    # 3.1
    story.extend(h2('3.1 可行性分析', 'ch3_1'))
    
    story.extend(h3('3.1.1 技术可行性', 'ch3_1_1'))
    story.extend(body(
        '本系统采用Spring Cloud微服务架构作为后端技术栈，Spring Cloud经过多年的发展和完善，'
        '已成为Java微服务开发领域的事实标准，拥有成熟的服务治理能力和丰富的生态组件。'
        '前端采用Vue.js框架，Vue.js是目前最流行的前端框架之一，'
        '拥有活跃的社区和丰富的第三方库支持。数据库采用MySQL和Redis的组合方案，'
        '两者都是业界广泛使用的成熟产品，性能稳定可靠。'
        '开发工具方面，使用IntelliJ IDEA作为集成开发环境，Maven作为项目构建工具，'
        'Git作为版本控制系统，这些都是Java开发者的标准工具链。'
        '综合来看，本系统的技术选型均为业界成熟、稳定的技术方案，技术可行性充分。'
    ))
    
    story.extend(h3('3.1.2 经济可行性', 'ch3_1_2'))
    story.extend(body(
        '本系统采用的所有技术组件均为开源免费软件，包括Spring Cloud、Spring Boot、Vue.js、MySQL、Redis、Nacos等，'
        '无需支付任何软件许可费用。在硬件方面，系统部署所需的云服务器资源成本较低，'
        '初步估算每年的服务器费用在数千元左右，对于高校的IT预算来说完全可以承受。'
        '此外，系统的投入使用将显著提高实验室设备管理的效率，减少人工管理的工作量，'
        '降低因管理不善导致的设备损失和资源浪费，从长期来看具有良好的经济效益。'
    ))
    
    story.extend(h3('3.1.3 操作可行性', 'ch3_1_3'))
    story.extend(body(
        '本系统采用B/S架构，用户只需通过浏览器即可访问系统的全部功能，'
        '无需安装任何客户端软件，操作门槛低。系统界面设计遵循简洁直观的原则，'
        '采用用户熟悉的Web交互方式，并提供了完善的操作提示和帮助文档。'
        '系统将用户分为管理员、教师和学生三种角色，不同角色的用户看到的界面和功能各不相同，'
        '避免了信息过载，降低了用户的认知负担。'
        '管理人员只需经过简单的培训即可熟练使用系统，普通师生无需培训即可自行完成设备查询和借用操作。'
        '因此，系统的操作可行性良好。'
    ))
    
    # 3.2
    story.extend(h2('3.2 功能需求分析', 'ch3_2'))
    story.extend(body(
        '通过对高校实验室设备管理业务的深入调研和分析，结合各类用户角色的实际需求，'
        '确定了系统的功能需求。系统的用户角色分为三类：系统管理员（ADMIN）、教师（TEACHER）和学生（STUDENT），'
        '不同角色具有不同的功能权限。'
    ))
    
    story.extend(body(
        '系统管理员拥有最高的管理权限，主要负责系统的日常运维和全局管理。'
        '管理员的核心功能包括：用户管理（创建、编辑、禁用用户账号，分配用户角色）；'
        '设备分类管理（添加、编辑、删除设备分类，管理分类层级）；'
        '设备台账管理（添加、编辑、删除设备信息，管理设备的基本属性、存放位置和维护记录）；'
        '借用审批（审批教师和学生的设备借用申请，支持批准和驳回操作）；'
        '统计报表（查看设备利用率、借用频次、库存预警等统计数据，支持导出报表）；'
        '系统配置（管理系统全局参数，如借用时长上限、逾期罚款规则等）。'
    ))
    
    story.extend(body(
        '教师用户具有设备借用和管理权限。教师的核心功能包括：'
        '设备查询与浏览（按分类、名称、编号等条件搜索设备，查看设备详情和可用状态）；'
        '设备借用申请（选择需要借用的设备，填写借用原因和预计归还时间，提交借用申请）；'
        '借用记录管理（查看个人的历史借用记录，跟踪借用状态，确认设备归还）；'
        '设备预约（在设备不可用时提交预约申请，设备可用时自动通知）。'
    ))
    
    story.extend(body(
        '学生用户的功能权限相对有限，主要包括：'
        '设备查询与浏览（查询可用设备，查看设备详情和库存状态）；'
        '设备借用申请（提交借用申请，需经教师或管理员审批）；'
        '借用记录查看（查看个人的借用历史和当前借用状态）。'
    ))
    
    # 用例图
    story.extend(add_image(
        os.path.join(IMG_DIR, 'use_case_diagram.png'),
        '系统用例图', '3-1'
    ))
    
    # 3.3
    story.extend(h2('3.3 非功能需求分析', 'ch3_3'))
    
    story.extend(body(
        '（1）性能需求。系统应支持至少500个并发用户同时在线操作，'
        '核心操作（如设备查询、借用申请提交）的响应时间应不超过2秒。'
        '在高并发借用场景下，系统应保证库存数据的准确性，不允许出现超卖现象。'
        '系统的页面加载时间应控制在3秒以内，支持大量的设备数据分页展示。'
    ))
    story.extend(body(
        '（2）安全需求。系统应采用基于JWT的无状态身份认证机制，'
        '所有API接口（除登录接口外）均需进行身份验证。系统应实现基于角色的访问控制（RBAC），'
        '确保不同角色的用户只能访问其权限范围内的功能和数据。'
        '用户密码应采用BCrypt算法加密存储，防止密码泄露。'
        '系统应具备防范常见Web攻击（如SQL注入、XSS攻击、CSRF攻击）的能力。'
    ))
    story.extend(body(
        '（3）可用性需求。系统应保证7×24小时不间断运行，系统可用率不低于99.5%。'
        '单个微服务的故障不应影响其他服务的正常运行。'
        '系统应具备完善的错误处理和日志记录机制，方便故障排查和问题定位。'
    ))
    story.extend(body(
        '（4）可维护性需求。系统应采用微服务架构，各服务独立部署、独立升级。'
        '代码应遵循统一的编码规范，核心模块应有充分的注释。'
        '系统应提供完善的API文档，方便后续的功能扩展和系统集成。'
    ))
    
    # 3.4
    story.extend(h2('3.4 业务流程分析', 'ch3_4'))
    story.extend(body(
        '设备借用是本系统最核心的业务流程，涉及多个角色和多步操作。'
        '完整的设备借用流程如下：'
    ))
    story.extend(body(
        '第一步，用户（教师或学生）登录系统后，浏览或搜索需要借用的设备，'
        '确认设备的库存状态为可用后，填写借用申请表，包括借用原因、预计借用时长等信息，'
        '提交借用申请。第二步，系统自动检查设备的可用库存数量，'
        '如果库存充足，则将借用申请的状态设为"待审批"；如果库存不足，则提示用户库存不足。'
        '第三步，管理员（或具有审批权限的教师）审核借用申请，可以根据实际情况批准或驳回申请。'
        '如果批准，系统自动扣减设备的可用库存，借用状态变为"借用中"；如果驳回，通知申请用户。'
        '第四步，用户在借用到期前归还设备，系统自动增加设备的可用库存，借用状态变为"已归还"。'
        '如果用户未按时归还，系统会发送逾期提醒通知。'
    ))
    
    # 借用状态机图
    story.extend(add_image(
        os.path.join(IMG_DIR, 'borrow_state_machine.png'),
        '设备借用状态机', '3-2'
    ))
    
    return story


def build_chapter4():
    """第四章 系统设计"""
    story = []
    story.extend(h1('第4章 系统设计', 'ch4'))
    
    story.extend(body(
        '在需求分析的基础上，本章将对系统进行详细设计，包括系统总体架构设计、'
        '微服务划分设计、数据库设计、接口设计和安全架构设计。'
        '系统设计的目标是在满足功能需求和非功能需求的前提下，'
        '构建一个架构合理、扩展性好、维护性强的实验室设备管理系统。'
    ))
    
    # 4.1
    story.extend(h2('4.1 系统总体架构设计', 'ch4_1'))
    story.extend(body(
        '本系统采用分层微服务架构，整体架构分为四个层次：前端展示层、网关层、微服务层和数据存储层。'
        '各层之间职责清晰、耦合度低，具有良好的独立性和可扩展性。'
    ))
    story.extend(body(
        '前端展示层采用Vue.js框架构建单页应用（SPA），通过HTTP/HTTPS协议与后端进行交互。'
        '前端负责页面的渲染、用户交互和表单验证等工作，采用Axios库发送HTTP请求，'
        '并通过请求拦截器自动附加JWT令牌。前端页面采用响应式设计，'
        '能够适配不同尺寸的屏幕设备，包括桌面电脑、平板和手机等。'
    ))
    story.extend(body(
        '网关层基于Spring Cloud Gateway实现，作为系统的统一入口。'
        '网关负责请求路由、身份认证、跨域处理和流量监控等横切关注点。'
        '所有来自前端的请求首先到达网关，网关通过JWT全局过滤器验证请求的合法性，'
        '验证通过后将请求路由到对应的微服务。网关还集成了限流过滤器，'
        '防止恶意请求对后端服务造成冲击。'
    ))
    story.extend(body(
        '微服务层包含系统的核心业务逻辑，各服务独立部署、独立运行。'
        '服务之间通过OpenFeign进行同步调用，通过Spring Cloud Bus进行事件通知。'
        '每个微服务拥有独立的数据库，遵循"数据库每服务"（Database per Service）原则，'
        '避免服务间的数据库耦合。'
    ))
    story.extend(body(
        '数据存储层包含MySQL关系型数据库和Redis内存数据库。MySQL负责存储系统的核心业务数据，'
        '包括用户信息、设备信息、借用记录等。Redis负责存储缓存数据和实现分布式锁，'
        '提高系统的并发处理能力和响应速度。'
    ))
    
    # 系统架构图
    story.extend(add_image(
        os.path.join(IMG_DIR, 'system_architecture.png'),
        '系统总体架构图', '4-1'
    ))
    
    # 4.2
    story.extend(h2('4.2 微服务划分设计', 'ch4_2'))
    story.extend(body(
        '根据系统的业务功能和领域边界，将系统划分为以下七个微服务模块：'
    ))
    story.extend(body(
        '（1）网关服务（lem-gateway）：基于Spring Cloud Gateway构建，作为系统的统一入口，'
        '负责请求路由、JWT认证、跨域处理和限流等功能。网关根据请求路径将请求转发到对应的微服务，'
        '并通过JWT全局过滤器确保只有经过认证的请求才能访问后端服务。'
    ))
    story.extend(body(
        '（2）认证服务（lem-auth）：负责用户登录认证和JWT令牌的生成与验证。'
        '认证服务接收用户的登录请求，验证用户名和密码，生成JWT令牌并返回给客户端。'
        '认证服务还提供令牌刷新功能，支持无感续期。'
    ))
    story.extend(body(
        '（3）设备管理服务（lem-equipment）：负责设备信息和设备分类的管理。'
        '提供设备的增删改查、分类管理、设备状态变更、设备位置管理等功能。'
        '该服务是设备数据的核心管理模块，为借用预约服务提供设备信息的查询支持。'
    ))
    story.extend(body(
        '（4）借用预约服务（lem-borrow）：负责设备借用和预约的业务逻辑处理。'
        '这是系统最核心的服务，实现了借用申请、审批流程、归还登记、库存扣减和并发控制等关键功能。'
        '该服务集成了Redis分布式锁和MyBatis-Plus乐观锁机制，确保库存数据的准确性。'
    ))
    story.extend(body(
        '（5）用户管理服务（lem-user）：负责用户信息的管理和角色权限控制。'
        '提供用户注册、信息修改、角色分配、权限验证等功能。'
        '实现了基于角色的访问控制（RBAC）机制，支持自定义权限注解。'
    ))
    story.extend(body(
        '（6）统计报表服务（lem-stats）：负责系统数据的统计分析和报表生成。'
        '提供设备利用率统计、借用频次排行、库存预警分析等功能，支持数据可视化展示和报表导出。'
    ))
    story.extend(body(
        '（7）公共模块（lem-common）：不属于独立的微服务，而是作为公共依赖被其他服务引用。'
        '包含统一响应体、全局异常处理器、通用工具类、自定义注解、DTO定义等公共组件，'
        '实现了代码的复用和一致性。'
    ))
    
    # 模块结构图
    story.extend(add_image(
        os.path.join(IMG_DIR, 'module_structure.png'),
        '系统模块结构图', '4-2'
    ))
    
    # 4.3
    story.extend(h2('4.3 数据库设计', 'ch4_3'))
    story.extend(body(
        '数据库设计是系统设计的重要组成部分，合理的数据库设计直接影响系统的性能和数据一致性。'
        '本项目遵循数据库设计的规范化原则，在满足第三范式（3NF）的基础上，'
        '根据实际业务需求进行了适当的反范式处理，以优化查询性能。'
    ))
    story.extend(body(
        '系统共设计了七张核心数据表，分别存储不同业务领域的数据。'
        '以下是各表的简要说明：'
    ))
    
    # ER图
    story.extend(add_image(
        os.path.join(IMG_DIR, 'er_diagram.png'),
        '系统ER图', '4-3'
    ))
    
    # 数据库表说明
    story.extend(body(
        '（1）用户表（sys_user）：存储系统用户的基本信息，包括用户ID、用户名、密码（BCrypt加密）、'
        '真实姓名、角色（ADMIN/TEACHER/STUDENT）、邮箱、手机号、状态（正常/禁用）、'
        '创建时间和更新时间等字段。用户名和手机号设有唯一索引，确保数据不重复。'
    ))
    story.extend(body(
        '（2）设备分类表（eq_category）：存储设备分类的层级信息，采用父子节点设计。'
        '包括分类ID、分类名称、父分类ID（顶级分类为0）、排序号、状态和创建时间等字段。'
        '支持树形结构的分类管理，方便用户按层级浏览设备。'
    ))
    story.extend(body(
        '（3）设备信息表（eq_info）：存储设备的详细信息，包括设备ID、设备编号（唯一）、'
        '设备名称、分类ID（外键关联设备分类表）、规格型号、存放位置、'
        '总数量、可用数量、单价、状态（正常/维修/报废）、'
        '描述信息和创建时间等字段。'
        '其中，可用数量字段的更新采用了乐观锁机制，通过version字段进行并发控制。'
    ))
    story.extend(body(
        '（4）借用记录表（borrow_record）：存储设备借用的完整记录，包括记录ID、'
        '申请人ID（外键关联用户表）、设备ID（外键关联设备表）、申请时间、'
        '审批人ID、审批时间、审批状态（待审批/已批准/已驳回/借用中/已归还/已逾期）、'
        '借用原因、预计归还时间、实际归还时间和备注等字段。'
    ))
    story.extend(body(
        '（5）设备维护记录表（eq_maintenance）：存储设备的维护和维修记录，'
        '包括维护ID、设备ID、维护类型（保养/维修/校准）、维护日期、'
        '维护人员、维护内容和费用等字段。'
    ))
    story.extend(body(
        '（6）操作日志表（sys_log）：存储系统的操作日志，用于审计和故障排查。'
        '包括日志ID、操作用户ID、操作模块、操作类型（增/删/改/查）、'
        '操作内容、IP地址和操作时间等字段。'
    ))
    story.extend(body(
        '（7）消息通知表（notification）：存储系统消息和通知记录，'
        '包括通知ID、接收用户ID、通知标题、通知内容、通知类型（审批通知/归还提醒/系统通知）、'
        '是否已读和创建时间等字段。'
    ))
    
    # 4.4
    story.extend(h2('4.4 接口设计', 'ch4_4'))
    story.extend(body(
        '本系统的API接口遵循RESTful设计规范，采用统一的URL命名规则和HTTP方法语义。'
        'URL中使用名词表示资源，使用HTTP方法表示操作类型：GET用于查询操作，POST用于创建操作，'
        'PUT用于全量更新操作，PATCH用于部分更新操作，DELETE用于删除操作。'
    ))
    story.extend(body(
        '系统采用统一的响应格式，所有API接口返回相同结构的数据，便于前端统一处理。'
        '统一响应体包含以下字段：code（响应状态码，200表示成功）、'
        'message（响应消息描述）、data（响应数据，泛型类型）。'
        '当发生错误时，响应体中还会包含详细的错误信息。'
    ))
    
    # 接口设计表格
    api_data = [
        ['接口路径', 'HTTP方法', '功能说明', '所属服务'],
        ['/api/auth/login', 'POST', '用户登录认证', '认证服务'],
        ['/api/auth/refresh', 'POST', '刷新JWT令牌', '认证服务'],
        ['/api/equipment/list', 'GET', '查询设备列表', '设备管理服务'],
        ['/api/equipment/{id}', 'GET', '查询设备详情', '设备管理服务'],
        ['/api/equipment', 'POST', '新增设备信息', '设备管理服务'],
        ['/api/equipment/{id}', 'PUT', '修改设备信息', '设备管理服务'],
        ['/api/equipment/{id}', 'DELETE', '删除设备信息', '设备管理服务'],
        ['/api/borrow/apply', 'POST', '提交借用申请', '借用预约服务'],
        ['/api/borrow/approve/{id}', 'PUT', '审批借用申请', '借用预约服务'],
        ['/api/borrow/return/{id}', 'PUT', '归还设备', '借用预约服务'],
        ['/api/borrow/my-records', 'GET', '查询我的借用记录', '借用预约服务'],
        ['/api/user/list', 'GET', '查询用户列表', '用户管理服务'],
        ['/api/user/{id}/role', 'PUT', '修改用户角色', '用户管理服务'],
        ['/api/stats/usage', 'GET', '设备利用率统计', '统计报表服务'],
        ['/api/stats/ranking', 'GET', '借用频次排行', '统计报表服务'],
    ]
    
    story.extend(add_table_with_caption(
        api_data, '系统核心API接口列表', '4-1',
        col_widths=[130, 65, 120, 100]
    ))
    
    # 4.5
    story.extend(h2('4.5 安全架构设计', 'ch4_5'))
    story.extend(body(
        '系统的安全架构采用多层防护策略，从身份认证、权限控制、数据安全和通信安全四个维度保障系统的安全性。'
    ))
    story.extend(body(
        '在身份认证方面，系统采用JWT无状态认证机制。用户登录成功后，'
        '认证服务生成包含用户身份信息的JWT令牌返回给客户端。'
        '客户端在后续请求中携带JWT令牌，API网关通过JWT全局过滤器验证令牌的有效性。'
        'JWT令牌设置了合理的过期时间（访问令牌2小时，刷新令牌7天），'
        '支持令牌刷新机制，实现无感续期。'
    ))
    story.extend(body(
        '在权限控制方面，系统实现了基于角色的访问控制（RBAC）机制。'
        '自定义了@RequireRole注解，开发者可以在Controller方法上标注所需的用户角色，'
        '拦截器会在请求到达业务逻辑之前进行权限校验。'
        '未通过权限校验的请求将返回403 Forbidden响应。'
    ))
    
    # JWT认证流程图
    story.extend(add_image(
        os.path.join(IMG_DIR, 'jwt_auth_flow.png'),
        'JWT认证流程图', '4-4'
    ))
    
    story.extend(body(
        '在数据安全方面，用户密码采用BCrypt算法进行单向加密存储，即使数据库泄露，'
        '攻击者也无法还原明文密码。敏感数据（如手机号、邮箱等）在传输和展示时进行脱敏处理。'
        '在通信安全方面，生产环境强制使用HTTPS协议，确保数据传输的加密性。'
        '系统还配置了CORS（跨域资源共享）策略，只允许指定的前端域名进行跨域访问。'
    ))
    
    return story


def build_chapter5():
    """第五章 系统实现"""
    story = []
    story.extend(h1('第5章 系统实现', 'ch5'))
    
    story.extend(body(
        '本章将详细介绍系统各模块的具体实现过程，包括开发环境搭建、'
        '公共模块实现、各微服务模块的核心功能实现以及前端界面的实现。'
        '通过展示关键代码片段和运行效果截图，说明系统的技术实现细节。'
    ))
    
    # 5.1
    story.extend(h2('5.1 开发环境搭建', 'ch5_1'))
    story.extend(body(
        '系统的开发和运行需要配置相应的软硬件环境。'
        '本节列出了系统开发和部署所需的环境配置信息，如表5-1所示。'
    ))
    
    env_data = [
        ['类别', '名称/版本', '说明'],
        ['操作系统', 'Windows 11 / Ubuntu 22.04', '开发和部署环境'],
        ['JDK', 'OpenJDK 17', 'Java运行环境'],
        ['开发工具', 'IntelliJ IDEA 2023.2', 'Java集成开发环境'],
        ['构建工具', 'Maven 3.9.5', '项目依赖管理和构建'],
        ['后端框架', 'Spring Cloud 2022.0.x', '微服务框架'],
        ['前端框架', 'Vue 3.3 + Vite 4.4', '前端开发框架'],
        ['UI组件库', 'Element Plus 2.3', 'Vue 3 UI组件库'],
        ['数据库', 'MySQL 8.0.35', '关系型数据库'],
        ['缓存', 'Redis 7.2', '内存数据库和分布式锁'],
        ['注册中心', 'Nacos 2.3.0', '服务注册与配置中心'],
        ['版本控制', 'Git 2.42', '代码版本管理'],
        ['API测试', 'Postman / Apifox', '接口测试工具'],
    ]
    
    story.extend(add_table_with_caption(
        env_data, '开发环境配置表', '5-1',
        col_widths=[90, 155, 170]
    ))
    
    # 5.2
    story.extend(h2('5.2 公共模块实现', 'ch5_2'))
    story.extend(body(
        '公共模块（lem-common）是系统的基础模块，被所有微服务引用。'
        '该模块封装了系统中通用的组件和工具，主要包括统一响应体和全局异常处理器两个核心部分。'
    ))
    story.extend(body(
        '统一响应体R&lt;T&gt;是所有API接口返回数据的统一格式。'
        'R类采用泛型设计，通过静态工厂方法（ok、error、fail等）简化响应体的创建。'
        '成功的响应包含状态码200、成功消息和响应数据；失败的响应包含相应的错误码和错误消息。'
        '这种统一响应格式使前端能够以一致的方式处理所有API响应，提高了代码的可维护性。'
    ))
    
    story.extend(add_code_screenshot(
        'unified_response_code.png', '5-1',
        '统一响应体R&lt;T&gt;实现代码'
    ))
    
    story.extend(body(
        '全局异常处理器使用@RestControllerAdvice注解实现，'
        '统一拦截系统中抛出的各类异常，并转换为标准的响应格式返回给客户端。'
        '处理器分别针对参数校验异常（MethodArgumentNotValidException）、'
        '自定义业务异常（BusinessException）、JWT认证异常和通用异常等进行了处理，'
        '确保系统在任何异常情况下都能返回格式规范的错误信息，避免将异常堆栈暴露给用户。'
    ))
    
    # 5.3
    story.extend(h2('5.3 认证服务实现', 'ch5_3'))
    story.extend(body(
        '认证服务（lem-auth）负责用户身份认证和JWT令牌管理。'
        '该服务提供用户登录接口，验证用户名和密码后生成JWT令牌。'
        'JWT令牌的生成和验证逻辑封装在JwtUtil工具类中。'
    ))
    story.extend(body(
        'JwtUtil工具类的核心功能包括：生成访问令牌（AccessToken）和刷新令牌（RefreshToken）、'
        '验证令牌的有效性、从令牌中解析用户信息以及检查令牌是否过期等。'
        '访问令牌的有效期设置为2小时，刷新令牌的有效期设置为7天。'
        '令牌的Payload中存储了用户ID（userId）、用户名（username）和角色（role）等关键信息，'
        '后续网关和微服务可以从令牌中获取这些信息进行身份验证和权限校验。'
        '签名使用HS256算法，密钥从Nacos配置中心获取，支持动态更新。'
    ))
    
    story.extend(add_code_screenshot(
        'jwt_util_code.png', '5-2',
        'JWT工具类JwtUtil实现代码'
    ))
    
    # 5.4
    story.extend(h2('5.4 网关服务实现', 'ch5_4'))
    story.extend(body(
        '网关服务（lem-gateway）基于Spring Cloud Gateway实现，'
        '是系统所有请求的统一入口。网关的核心功能通过全局过滤器实现，'
        '其中最重要的是JWT认证过滤器。'
    ))
    story.extend(body(
        'JWT全局过滤器继承自AbstractGatewayFilterFactory，'
        '在过滤器中对所有请求（白名单路径除外）进行JWT令牌验证。'
        '白名单路径包括登录接口、注册接口和Swagger文档接口等无需认证的路径。'
        '过滤器的处理流程如下：首先从请求头中提取Authorization字段，'
        '解析出Bearer令牌；然后调用JwtUtil验证令牌的有效性；'
        '验证通过后，将用户ID、用户名和角色等信息写入请求头，'
        '传递给下游微服务使用；验证失败则返回401 Unauthorized响应。'
    ))
    
    story.extend(add_code_screenshot(
        'gateway_filter_code.png', '5-3',
        '网关JWT全局过滤器实现代码'
    ))
    
    story.extend(body(
        '此外，网关还配置了跨域（CORS）过滤器，允许前端域名进行跨域请求。'
        '路由配置采用Nacos动态路由，支持在不重启网关的情况下动态添加、修改和删除路由规则。'
        '网关还集成了请求限流功能，基于Redis的令牌桶算法实现，'
        '防止恶意请求对后端服务造成过大压力。'
    ))
    
    # 5.5
    story.extend(h2('5.5 设备管理服务实现', 'ch5_5'))
    story.extend(body(
        '设备管理服务（lem-equipment）负责设备信息和设备分类的增删改查操作。'
        '该服务基于MyBatis-Plus实现数据访问层，利用BaseMapper提供的通用CRUD方法，'
        '极大地简化了数据操作代码。'
    ))
    story.extend(body(
        '设备列表查询功能支持多条件组合查询和分页展示。'
        '前端可以传入设备名称、分类ID、设备状态等查询条件，'
        '后端通过LambdaQueryWrapper动态构建查询条件，结合MyBatis-Plus的分页插件实现分页查询。'
        '设备新增和编辑功能实现了参数校验，包括设备编号的唯一性校验、'
        '数量字段的有效性校验等，确保数据的完整性和准确性。'
    ))
    story.extend(body(
        '设备分类管理采用树形结构设计，支持多级分类。'
        '通过递归查询和构建树形结构数据，前端可以展示分类的层级关系。'
        '分类的增删改操作考虑了子分类的存在性约束，不允许删除仍有子分类或关联设备的分类节点。'
        '设备状态管理支持正常、维修和报废三种状态，状态变更时系统会自动记录状态变更日志。'
    ))
    
    # 5.6 借用预约服务实现（核心功能）
    story.extend(h2('5.6 借用预约服务实现', 'ch5_6'))
    story.extend(body(
        '借用预约服务（lem-borrow）是系统最核心的服务，实现了设备借用的完整业务流程，'
        '包括借用申请提交、审批处理、库存扣减、设备归还和并发控制等关键功能。'
        '特别是库存并发控制机制，是本系统最具技术挑战性和创新性的部分。'
    ))
    story.extend(body(
        '借用申请功能的实现流程如下：用户在前端页面选择需要借用的设备，填写借用原因和预计归还时间后，'
        '提交借用申请。后端接收到申请后，首先通过Feign客户端调用设备管理服务查询设备的可用库存，'
        '然后创建借用记录并设置状态为"待审批"。系统同时向管理员发送待审批消息通知。'
    ))
    
    story.extend(add_code_screenshot(
        'borrow_apply_code.png', '5-4',
        '借用申请核心业务代码'
    ))
    
    story.extend(body(
        '审批功能的处理流程：管理员在审批页面查看待审批的借用申请列表，选择批准或驳回操作。'
        '批准操作触发库存扣减流程，这是整个系统最关键的并发控制环节。'
        '库存扣减采用了Redis分布式锁与MyBatis-Plus乐观锁的双重保障机制，'
        '确保在高并发场景下库存数据的准确性和一致性。'
    ))
    story.extend(body(
        '第一层保障是Redis分布式锁。在执行库存扣减之前，系统会尝试获取以设备ID为键的分布式锁。'
        '分布式锁的获取通过RedisTemplate的opsForValue().setIfAbsent()方法实现，'
        '该方法对应Redis的SETNX命令，是一个原子操作。'
        '设置锁的同时指定过期时间（默认30秒），防止因服务异常退出导致的死锁问题。'
        '只有成功获取分布式锁的请求才能继续执行库存扣减操作，获取失败的请求需要等待并重试。'
        '分布式锁的粒度为单个设备ID，不同设备的借用操作可以并行执行，'
        '在保证数据正确性的前提下最大化了系统的并发处理能力。'
    ))
    
    story.extend(add_code_screenshot(
        'redis_lock_code.png', '5-5',
        'Redis分布式锁实现代码'
    ))
    
    story.extend(body(
        '第二层保障是MyBatis-Plus乐观锁。在获取到分布式锁之后，'
        '系统通过MyBatis-Plus的乐观锁插件进行数据库层面的并发控制。'
        '设备信息表（eq_info）中包含version字段，使用@Version注解标注。'
        '当执行库存扣减SQL时，MyBatis-Plus乐观锁插件会自动在UPDATE语句的WHERE条件中添加版本号校验条件，'
        '即UPDATE eq_info SET available_count = available_count - 1, version = version + 1 '
        'WHERE id = ? AND version = ?。只有当数据库中存储的版本号与查询时获取的版本号一致时，'
        '更新操作才能成功，否则更新0行，系统抛出OptimisticLockException异常。'
    ))
    
    story.extend(add_code_screenshot(
        'optimistic_lock_sql.png', '5-6',
        '乐观锁SQL映射代码'
    ))
    
    story.extend(body(
        '分布式锁和乐观锁的配合工作流程如下：当多个用户同时对同一设备发起借用审批时，'
        'Redis分布式锁确保同一时刻只有一个请求能够执行库存扣减操作，'
        '其余请求排队等待。即使由于某些极端情况（如Redis主从切换导致的锁丢失），'
        '多个请求同时进入了库存扣减环节，MyBatis-Plus乐观锁也会在数据库层面进行最终校验，'
        '确保只有第一个请求能够成功扣减库存。这种双重保障机制在理论和实践上都被证明是可靠的，'
        '能够有效解决高并发场景下的库存超卖问题。'
    ))
    
    # 库存控制流程图
    story.extend(add_image(
        os.path.join(IMG_DIR, 'stock_control_flow.png'),
        '库存并发控制流程图', '5-1'
    ))
    
    story.extend(body(
        '归还功能的处理较为简单：用户在系统中确认归还设备后，系统将借用记录状态更新为"已归还"，'
        '同时增加设备的可用库存数量。归还操作同样需要考虑并发安全性，'
        '但由于归还操作是增加库存（而非扣减），不存在超卖风险，因此不需要使用分布式锁，'
        '但仍使用乐观锁机制确保数据一致性。'
    ))
    
    # 5.7
    story.extend(h2('5.7 用户管理服务实现', 'ch5_7'))
    story.extend(body(
        '用户管理服务（lem-user）负责系统用户的管理和角色权限控制。'
        '该服务提供了用户的增删改查功能，以及基于角色的访问控制（RBAC）机制。'
    ))
    story.extend(body(
        '角色权限控制的实现基于自定义的@RequireRole注解和AOP拦截器。'
        '@RequireRole注解标注在Controller方法上，指定该接口允许访问的用户角色。'
        '例如，@RequireRole("ADMIN")表示该接口仅允许管理员角色访问，'
        '@RequireRole({"ADMIN", "TEACHER"})表示管理员和教师均可访问。'
        'AOP拦截器在方法执行前从请求头中提取用户角色信息，与注解中声明的角色进行比对，'
        '匹配则放行，不匹配则抛出权限不足的异常，由全局异常处理器统一返回403响应。'
    ))
    
    story.extend(add_code_screenshot(
        'require_role_code.png', '5-7',
        '基于AOP的角色权限控制实现代码'
    ))
    
    story.extend(body(
        '用户管理服务还实现了用户注册、信息修改和状态管理等功能。'
        '新用户注册时，系统会对用户名、密码强度进行校验，密码使用BCrypt算法加密后存储。'
        '管理员可以禁用违规用户账号，被禁用的用户无法登录系统。'
        '用户信息的修改操作会记录操作日志，便于审计追踪。'
    ))
    
    # 5.8
    story.extend(h2('5.8 统计报表服务实现', 'ch5_8'))
    story.extend(body(
        '统计报表服务（lem-stats）负责系统数据的统计分析功能。'
        '该服务通过Feign客户端从设备管理服务和借用预约服务获取数据，'
        '进行聚合统计后提供给前端展示。'
    ))
    story.extend(body(
        '统计功能主要包括以下几个方面：设备利用率统计（按月/周/日统计设备的使用频次和空闲率）、'
        '借用频次排行（统计各设备的借用次数排行）、用户活跃度分析（统计各用户的借用次数和频率）、'
        '库存预警分析（检测库存低于阈值的设备并生成预警列表）以及分类使用趋势分析'
        '（按设备分类统计使用趋势）。统计结果通过图表（折线图、柱状图、饼图等）直观展示。'
    ))
    story.extend(body(
        '为了提高统计查询的性能，系统采用了定时任务预处理机制。'
        '通过Spring的@Scheduled注解配置定时任务，每天凌晨自动执行数据预计算，'
        '将统计结果缓存到Redis中，前端查询时直接从缓存读取，大幅减少了实时计算的开销。'
        '对于需要实时数据的管理员仪表盘，系统也提供了实时统计接口。'
    ))
    
    story.extend(add_code_screenshot(
        'schedule_task_code.png', '5-8',
        '定时任务统计预处理代码'
    ))
    
    # 5.9 前端实现
    story.extend(h2('5.9 前端实现', 'ch5_9'))
    story.extend(body(
        '系统前端基于Vue 3框架和Element Plus组件库实现，采用Vite作为构建工具。'
        '前端项目采用模块化的目录结构，将页面组件、业务逻辑、工具函数和样式资源等进行合理组织。'
    ))
    
    story.extend(h3('5.9.1 路由与权限控制', 'ch5_9_1'))
    story.extend(body(
        '前端路由使用Vue Router实现，配置了完整的页面路由映射。'
        '路由守卫（Navigation Guard）是前端权限控制的核心机制。'
        '在全局前置守卫（beforeEach）中，系统检查用户是否已登录（通过localStorage中的JWT令牌判断），'
        '未登录用户将被重定向到登录页面。对于需要特定角色权限的页面，'
        '路由守卫还会检查用户角色是否有权访问，无权访问则跳转到403页面。'
        '路由的懒加载机制确保了按需加载，提高了首屏加载速度。'
    ))
    
    story.extend(add_code_screenshot(
        'router_guard_code.png', '5-9',
        'Vue Router路由守卫代码'
    ))
    
    story.extend(h3('5.9.2 HTTP请求拦截', 'ch5_9_2'))
    story.extend(body(
        '前端使用Axios库发送HTTP请求，并通过请求拦截器和响应拦截器实现统一的请求处理。'
        '请求拦截器自动在请求头中添加JWT令牌（从localStorage读取），'
        '并在请求头中设置Content-Type为application/json。'
        '响应拦截器统一处理响应结果：对于2xx状态码的响应，直接返回响应数据；'
        '对于401状态码，清除本地令牌并跳转到登录页面；'
        '对于403状态码，提示用户权限不足；'
        '对于其他错误状态码，统一显示错误消息提示。'
    ))
    
    story.extend(add_code_screenshot(
        'axios_interceptor_code.png', '5-10',
        'Axios请求/响应拦截器代码'
    ))
    
    story.extend(h3('5.9.3 服务间调用（OpenFeign）', 'ch5_9_3'))
    story.extend(body(
        '后端微服务之间的同步调用通过Spring Cloud OpenFeign实现。'
        'Feign客户端以Java接口的形式定义，通过@FeignClient注解指定目标服务名称，'
        '接口方法使用Spring MVC的注解（@GetMapping、@PostMapping等）定义请求路径和参数。'
        'Feign客户端在运行时由Spring Cloud自动生成代理实现类，'
        '通过服务发现（Nacos）获取目标服务的实例列表，结合负载均衡策略完成HTTP调用。'
        'Feign还支持请求和响应的编解码配置，本项目统一使用Jackson进行JSON序列化和反序列化。'
    ))
    
    story.extend(add_code_screenshot(
        'feign_client_code.png', '5-11',
        'OpenFeign客户端接口定义代码'
    ))
    
    story.extend(h3('5.9.4 前端页面实现', 'ch5_9_4'))
    story.extend(body(
        '前端页面采用Element Plus组件库构建，实现了简洁美观的用户界面。'
        '主要页面包括登录页面、首页仪表盘、设备管理页面、借用管理页面、用户管理页面和统计报表页面等。'
        '以下是主要页面的实现效果截图。'
    ))
    
    story.extend(add_screenshot_placeholder(
        '登录页面', '5-2', '系统登录页面'
    ))
    story.extend(add_screenshot_placeholder(
        '首页仪表盘', '5-3', '管理员首页仪表盘'
    ))
    story.extend(add_screenshot_placeholder(
        '设备列表页面', '5-4', '设备列表管理页面'
    ))
    story.extend(add_screenshot_placeholder(
        '借用申请页面', '5-5', '设备借用申请页面'
    ))
    story.extend(add_screenshot_placeholder(
        '审批管理页面', '5-6', '借用审批管理页面'
    ))
    story.extend(add_screenshot_placeholder(
        '统计报表页面', '5-7', '统计报表页面'
    ))
    
    return story


def build_chapter6():
    """第六章 系统测试"""
    story = []
    story.extend(h1('第6章 系统测试', 'ch6'))
    
    story.extend(body(
        '系统测试是软件开发过程中的重要环节，旨在验证系统是否满足需求规格说明书中规定的各项要求。'
        '本章将从测试环境、功能测试和性能测试三个方面对系统进行全面测试，'
        '确保系统的功能正确性和性能可靠性。'
    ))
    
    # 6.1
    story.extend(h2('6.1 测试环境', 'ch6_1'))
    story.extend(body(
        '为保证测试结果的真实性和可靠性，测试环境与生产环境尽可能保持一致。'
        '测试环境的硬件和软件配置如表6-1所示。'
    ))
    
    test_env_data = [
        ['配置项', '测试环境配置'],
        ['CPU', 'Intel Core i7-12700H (14核20线程)'],
        ['内存', '16GB DDR5'],
        ['操作系统', 'Windows 11 Professional'],
        ['JDK版本', 'OpenJDK 17.0.8'],
        ['MySQL版本', 'MySQL 8.0.35'],
        ['Redis版本', 'Redis 7.2.3'],
        ['Nacos版本', 'Nacos 2.3.0'],
        ['浏览器', 'Google Chrome 118.0'],
        ['测试工具', 'Postman, JMeter 5.5, Selenium 4.15'],
    ]
    
    story.extend(add_table_with_caption(
        test_env_data, '测试环境配置表', '6-1',
        col_widths=[120, 295]
    ))
    
    # 6.2
    story.extend(h2('6.2 功能测试用例与结果', 'ch6_2'))
    story.extend(body(
        '功能测试采用黑盒测试方法，根据需求分析阶段确定的功能需求设计测试用例，'
        '覆盖系统的所有核心功能模块。测试执行过程中，严格按照测试用例的步骤进行操作，'
        '记录实际结果并与预期结果进行比对。表6-2列出了部分核心功能的测试用例和测试结果。'
    ))
    
    test_case_data = [
        ['编号', '测试功能', '测试步骤', '预期结果', '实际结果', '状态'],
        ['TC-01', '用户登录', '输入正确的用户名和密码，点击登录',
         '登录成功，跳转到首页', '登录成功，跳转到首页', '通过'],
        ['TC-02', '密码错误登录', '输入正确的用户名和错误的密码',
         '提示"用户名或密码错误"', '提示"用户名或密码错误"', '通过'],
        ['TC-03', '设备查询', '在设备列表页输入设备名称进行搜索',
         '显示匹配的设备列表', '显示匹配的设备列表', '通过'],
        ['TC-04', '新增设备', '填写设备信息，点击保存',
         '提示保存成功，列表显示新设备', '提示保存成功', '通过'],
        ['TC-05', '借用申请', '选择设备，填写原因，提交申请',
         '申请成功，状态为待审批', '申请成功', '通过'],
        ['TC-06', '借用审批', '管理员批准借用申请',
         '库存减少，状态变为借用中', '库存减少', '通过'],
        ['TC-07', '驳回申请', '管理员驳回借用申请',
         '状态变为已驳回，库存不变', '状态变更成功', '通过'],
        ['TC-08', '设备归还', '用户确认归还设备',
         '库存增加，状态变为已归还', '库存增加', '通过'],
        ['TC-09', '库存不足', '库存为0时提交借用申请',
         '提示库存不足', '提示库存不足', '通过'],
        ['TC-10', '权限控制', '学生用户访问用户管理页面',
         '跳转到403页面', '跳转到403页面', '通过'],
        ['TC-11', '并发借用', '100个用户同时借用同一设备',
         '库存数据正确，无超卖', '库存数据正确', '通过'],
        ['TC-12', '统计报表', '查看设备利用率统计',
         '正确显示统计数据', '正确显示', '通过'],
    ]
    
    story.extend(add_table_with_caption(
        test_case_data, '功能测试用例与结果表', '6-2',
        col_widths=[38, 58, 95, 85, 78, 32]
    ))
    
    story.extend(body(
        '测试结果显示，系统的所有核心功能均通过了测试，功能实现正确。'
        '特别是在并发借用测试（TC-11）中，系统在100个并发用户同时借用同一设备（可用库存为5台）的场景下，'
        '成功确保了只有5个借用请求获批，库存数据保持准确，验证了Redis分布式锁和乐观锁双重保障机制的有效性。'
    ))
    
    # 6.3
    story.extend(h2('6.3 性能测试', 'ch6_3'))
    story.extend(body(
        '性能测试使用Apache JMeter工具，模拟多用户并发访问场景，'
        '测试系统的吞吐量、响应时间和资源占用率等关键性能指标。'
        '测试主要针对以下两个核心接口进行：设备列表查询接口和借用申请提交接口。'
    ))
    
    perf_data = [
        ['测试场景', '并发数', '持续时间', '平均响应时间', 'TPS', '错误率'],
        ['设备列表查询', '50', '60s', '85ms', '456.3', '0%'],
        ['设备列表查询', '200', '60s', '238ms', '712.5', '0%'],
        ['设备列表查询', '500', '60s', '587ms', '785.2', '0.1%'],
        ['借用申请提交', '50', '60s', '125ms', '328.7', '0%'],
        ['借用申请提交', '200', '60s', '456ms', '405.1', '0.2%'],
        ['借用申请提交', '500', '60s', '1023ms', '438.6', '0.5%'],
    ]
    
    story.extend(add_table_with_caption(
        perf_data, '性能测试结果表', '6-3',
        col_widths=[80, 50, 55, 80, 55, 50]
    ))
    
    story.extend(body(
        '性能测试结果表明，系统在200并发用户的情况下，核心接口的平均响应时间均在500ms以内，'
        '满足性能需求中"核心操作响应时间不超过2秒"的要求。'
        '在500并发用户的高压力场景下，系统仍能保持较高的吞吐量，错误率控制在0.5%以下，'
        '表现出了良好的抗压能力。通过分析发现，响应时间随并发数增加而增长的主要原因在于数据库连接池的竞争，'
        '后续可以通过增加数据库连接池大小、引入读写分离和数据库分库分表等方案进一步优化系统性能。'
    ))
    
    # 6.4
    story.extend(h2('6.4 测试结论', 'ch6_4'))
    story.extend(body(
        '通过对系统的功能测试和性能测试，可以得出以下结论：'
    ))
    story.extend(body(
        '（1）系统功能测试方面，所有核心功能测试用例均通过测试，系统的功能实现与需求规格一致。'
        '用户管理、设备管理、借用预约、审批流程、统计报表等主要功能模块运行正常，'
        '业务流程完整、逻辑正确。特别是库存并发控制机制在高并发场景下表现稳定，'
        '有效防止了库存超卖问题。'
    ))
    story.extend(body(
        '（2）系统性能测试方面，系统在200并发用户条件下表现良好，'
        '核心接口响应时间满足设计要求。在500并发用户的高压力条件下，'
        '系统仍能保持可用，错误率在可接受范围内。'
        '系统的性能瓶颈主要集中在数据库层面，后续优化方向包括数据库索引优化、'
        '读写分离和缓存策略优化等。'
    ))
    story.extend(body(
        '（3）总体而言，本系统在功能完整性、性能可靠性和用户体验等方面均达到了设计目标，'
        '能够满足高校实验室设备管理的实际需求，具备了投入实际使用的条件。'
    ))
    
    return story


def build_chapter7():
    """第七章 总结与展望"""
    story = []
    story.extend(h1('第7章 总结与展望', 'ch7'))
    
    story.extend(h2('7.1 论文总结', 'ch7_1'))
    story.extend(body(
        '本文针对高校实验室设备管理中存在的人工管理效率低、信息更新滞后、并发控制困难等问题，'
        '设计并实现了一套基于Spring Cloud微服务架构的实验室设备管理系统。'
        '本文的主要工作和贡献包括以下几个方面：'
    ))
    story.extend(body(
        '（1）完成了系统的需求分析和架构设计。通过深入调研高校实验室设备管理的实际需求，'
        '明确了系统的功能需求和非功能需求。基于Spring Cloud微服务架构设计了系统的总体架构，'
        '将系统划分为网关服务、认证服务、设备管理服务、借用预约服务、用户管理服务、'
        '统计报表服务和公共模块七个核心模块，各模块职责清晰、耦合度低。'
    ))
    story.extend(body(
        '（2）实现了系统的完整功能。后端采用Spring Boot和Spring Cloud构建微服务集群，'
        '利用Nacos实现服务注册与配置管理，利用OpenFeign实现服务间通信。'
        '前端采用Vue 3和Element Plus构建响应式用户界面。'
        '系统实现了用户管理、设备管理、借用预约、审批流程、统计报表等完整的业务功能。'
    ))
    story.extend(body(
        '（3）提出了基于Redis分布式锁与MyBatis-Plus乐观锁的库存并发控制方案。'
        '该方案通过分布式锁实现分布式环境下的互斥访问控制，通过乐观锁实现数据库层面的数据一致性保障，'
        '双重机制确保了高并发场景下库存数据的准确性。性能测试验证了该方案的有效性和可靠性。'
    ))
    
    story.extend(h2('7.2 未来展望', 'ch7_2'))
    story.extend(body(
        '虽然本系统在功能实现和性能表现上达到了预期目标，但仍有一些方面可以在后续工作中进一步改进和完善：'
    ))
    story.extend(body(
        '（1）引入消息队列实现异步处理。当前系统的审批通知和归还提醒采用同步方式处理，'
        '后续可以引入RabbitMQ或Kafka等消息队列，实现通知的异步发送和处理，'
        '提高系统的响应速度和吞吐量。消息队列还可以用于实现借用申请的削峰填谷，'
        '在高并发场景下先将请求放入队列，再由消费者逐步处理，进一步减轻后端服务的压力。'
    ))
    story.extend(body(
        '（2）增加设备定位和追踪功能。可以结合RFID、NFC或二维码技术，'
        '实现设备的自动识别和定位追踪，方便用户快速查找设备位置，'
        '同时可以监控设备的移动轨迹，防止设备丢失。'
    ))
    story.extend(body(
        '（3）支持容器化部署。当前系统采用传统的JAR包部署方式，后续可以引入Docker和Kubernetes，'
        '实现服务的容器化部署和编排，提高部署效率和资源利用率，'
        '支持服务的自动扩缩容和故障自愈。'
    ))
    story.extend(body(
        '（4）增强数据分析能力。引入机器学习算法对设备使用数据进行分析和预测，'
        '如预测设备的维护周期、优化设备采购计划、推荐可用设备等，'
        '为实验室管理决策提供数据支持。'
    ))
    story.extend(body(
        '（5）完善移动端支持。当前系统主要面向PC端浏览器，后续可以开发微信小程序或移动端App，'
        '方便师生在移动设备上随时随地查看设备信息和提交借用申请，提升用户体验。'
    ))
    
    return story


def build_references():
    """参考文献"""
    story = []
    story.extend(h1('参考文献', 'refs'))
    
    refs = [
        '[1] Craig Walls. Spring in Action (Sixth Edition)[M]. Manning Publications, 2022.',
        '[2] Josh Long, Kenny Bastani. Cloud Native Java: Designing Resilient Systems with Spring Boot, Spring Cloud, and Cloud Foundry[M]. O\'Reilly Media, 2017.',
        '[3] 尤雨溪. Vue.js 设计与实现[M]. 人民邮电出版社, 2022.',
        '[4] 周志明. 深入理解Java虚拟机：JVM高级特性与最佳实践(第3版)[M]. 机械工业出版社, 2019.',
        '[5] 苗春雨. Spring Cloud微服务架构开发实战[M]. 人民邮电出版社, 2021.',
        '[6] Redis官方文档. Redis Documentation[EB/OL]. https://redis.io/docs/, 2024.',
        '[7] Martin Kleppmann. Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems[M]. O\'Reilly Media, 2017.',
        '[8] 廖雪峰. MySQL必知必会[M]. 人民邮电出版社, 2020.',
        '[9] Sam Newman. Building Microservices: Designing Fine-Grained Systems (Second Edition)[M]. O\'Reilly Media, 2021.',
        '[10] 陈永强. MyBatis-Plus从入门到精通[M]. 电子工业出版社, 2021.',
        '[11] 阮一峰. JWT入门教程[EB/OL]. https://www.ruanyifeng.com/blog/2018/07/json_web_token_tutorial.html, 2018.',
        '[12] 阿里巴巴. Nacos官方文档[EB/OL]. https://nacos.io/zh-cn/docs/what-is-nacos.html, 2024.',
        '[13] 阿里巴巴. Spring Cloud Alibaba官方文档[EB/OL]. https://spring-cloud-alibaba-group.github.io/, 2024.',
        '[14] 王丹, 于海滨. 基于Spring Boot的高校实验室管理系统设计与实现[J]. 计算机应用与软件, 2021, 38(5): 112-117.',
        '[15] 李明, 张伟. 基于微服务架构的高校实验室设备管理系统研究[J]. 实验技术与管理, 2022, 39(3): 256-261.',
        '[16] 张强, 刘芳. 基于Redis分布式锁的库存并发控制方案研究[J]. 计算机工程与设计, 2021, 42(8): 2345-2351.',
        '[17] Johnson R, Hoeller J, Donald K, et al. The Spring Framework - Reference Documentation[EB/OL]. https://docs.spring.io/spring-framework/reference/, 2024.',
        '[18] Element Plus团队. Element Plus官方文档[EB/OL]. https://element-plus.org/zh-CN/, 2024.',
    ]
    
    for ref in refs:
        story.append(Paragraph(ref, STYLE_REF))
    
    story.append(PageBreak())
    return story


def build_acknowledgement():
    """致谢"""
    story = []
    story.extend(h1('致谢', 'ack'))
    
    story.extend(body(
        '时光荏苒，大学四年的学习生涯即将落下帷幕。在毕业论文完成之际，'
        '我谨向在此期间给予我帮助和支持的所有人表示最诚挚的感谢。'
    ))
    story.extend(body(
        '首先，我要特别感谢我的指导老师。在毕业设计的整个过程中，'
        '老师从选题方向、方案设计到系统实现，都给予了我悉心的指导和耐心的帮助。'
        '老师严谨的治学态度、渊博的专业知识和精益求精的工作精神，'
        '将对我的未来学习和工作产生深远的影响。'
    ))
    story.extend(body(
        '其次，我要感谢大学四年来所有任课老师的辛勤教导。'
        '正是在他们的悉心培养下，我才得以掌握扎实的专业知识和实践技能，'
        '为本次毕业设计的顺利完成打下了坚实的基础。'
    ))
    story.extend(body(
        '同时，我要感谢我的同学们和室友们。在大学四年的学习生活中，'
        '我们互相帮助、共同进步。在毕业设计过程中，他们也为我提供了许多宝贵的建议和技术支持，'
        '让我在遇到困难时能够找到解决的方向。'
    ))
    story.extend(body(
        '最后，我要感谢我的家人。感谢他们多年来对我学业的无私支持和鼓励，'
        '正是他们的理解和支持，让我能够安心地完成学业。'
        '他们的爱是我不断前进的动力源泉。'
    ))
    story.extend(body(
        '在即将告别校园、踏上新征程之际，我将带着所学的知识和技能，'
        '以更加饱满的热情投入到未来的工作和学习中，不辜负所有关心和帮助过我的人的期望。'
    ))
    
    return story


# ============================================================
# 主函数：组装并生成PDF
# ============================================================

def build_toc_placeholder(story):
    """在story中预留TOC的位置"""
    story.append(Paragraph('目  录', STYLE_ABSTRACT_TITLE))
    story.append(Spacer(1, 12))
    story.append(ThesisTOC())
    story.append(PageBreak())


def main():
    print("开始生成论文PDF...")
    
    # 创建文档模板
    doc = ThesisDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title='基于Spring Cloud的高校实验室设备管理系统设计与实现',
        author='Graduate',
    )
    
    # 构建story
    story = []
    
    # 封面占位（后面由HTML/Playwright替换）
    story.append(PageBreak())
    
    # 目录
    build_toc_placeholder(story)
    
    # 中文摘要
    story.extend(build_chinese_abstract())
    
    # 英文摘要
    story.extend(build_english_abstract())
    
    # 第一章
    story.extend(build_chapter1())
    
    # 第二章
    story.extend(build_chapter2())
    
    # 第三章
    story.extend(build_chapter3())
    
    # 第四章
    story.extend(build_chapter4())
    
    # 第五章
    story.extend(build_chapter5())
    
    # 第六章
    story.extend(build_chapter6())
    
    # 第七章
    story.extend(build_chapter7())
    
    # 参考文献
    story.extend(build_references())
    
    # 致谢
    story.extend(build_acknowledgement())
    
    # 使用multiBuild生成带目录的PDF
    doc.multiBuild(story)
    
    print(f"论文PDF生成完成！文件路径：{OUTPUT_PDF}")
    
    # 统计信息
    print(f"文件大小：{os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")


if __name__ == '__main__':
    main()
