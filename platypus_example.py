from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, \
    ImageAndFlowables
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import black, yellow, purple


PAGE_WIDTH, PAGE_HEIGHT = A4
doc_title = 'Hello world'
pageinfo = 'platypus example'


def stylesheet():
    styles = dict()
    # get some common styles
    basic_styles = getSampleStyleSheet()
    styles.update(basic_styles.byName)
    # define a custom style
    styles['Alert'] = ParagraphStyle(
        name='Alert',
        parent=styles['Italic'],
        leading=14,
        alignment=TA_CENTER,
        backColor=yellow,
        borderColor=black,
        borderWidth=1,
        borderPadding=5,
        borderRadius=2,
        spaceBefore=10,
        spaceAfter=10,
        textColor=purple,
    )
    return styles


# noinspection PyUnusedLocal
def first_page(canvas, doc):
    """Define the annotations on the first page of a document.

    Annotations will be appended to the SimpleDocTemplate.PageTemplates, a list
    of PageTemplate objects. Here we can draw logos, page numbers, footers, etc

    Parameters
    ----------
    canvas : Canvas
    doc : SimpleDocTemplate
    """
    canvas.saveState()
    canvas.setFont(psfontname='Times-Bold', size=16, leading=0)

    # draw an image in the center of the page
    logo = 'Python_logo_1.png'
    img_width = 25*mm
    img_height = 25*mm
    canvas.drawInlineImage(
        logo, x=PAGE_WIDTH/2 - img_width/2, y=PAGE_HEIGHT/2 + img_height/2,
        width=img_width, height=img_height)

    canvas.drawCentredString(
        x=PAGE_WIDTH/2.0, y=PAGE_HEIGHT-20*mm, text=doc_title)
    canvas.setFont(psfontname='Times-Bold', size=9, leading=0)
    mytext = 'First Page / {}'.format(pageinfo)
    canvas.drawString(x=30*mm, y=20*mm, text=mytext)
    canvas.restoreState()


def add_call_to_action(flowables):
    flowables.append(Spacer(width=1 * mm, height=20 * mm))
    styles = stylesheet()
    style = styles['Alert']
    par = Paragraph(text='Call to Action!', style=style)
    flowables.append(par)
    style = styles['Italic']
    par = Paragraph(text='This is the text of the call to action', style=style)
    flowables.append(par)
    return flowables


def draw_watermark(canvas, doc):
    canvas.saveState()
    styles = stylesheet()
    style = styles['Alert']
    # we can draw directly on the canvas
    canvas.setFont(psfontname='Times-Bold', size=48)
    canvas.translate(PAGE_WIDTH / 2, PAGE_HEIGHT / 2)
    canvas.rotate(45)
    canvas.drawCentredString(x=0, y=0, text=doc.watermark)

    # or we can define a paragraph and call drawOn to draw it on the canvas
    par = Paragraph(text=doc.watermark, style=style)
    # if we want to draw the paragraph on the canvas we NEED the following line
    w, h = par.wrap(availWidth=doc.width, availHeight=doc.bottomMargin)
    par.drawOn(canvas=canvas, x=0 * mm, y=0 * mm)

    canvas.restoreState()


def later_pages(canvas, doc):
    """Define the annotations on all pages except the first one.

    Parameters
    ----------
    canvas : Canvas
    doc : SimpleDocTemplate
    """
    canvas.saveState()
    canvas.setFont(psfontname='Times-Bold', size=9)
    mytext = 'Page {} {}'.format(doc.page, pageinfo)
    canvas.drawString(x=100*mm, y=10*mm, text=mytext)

    draw_watermark(canvas, doc)

    style = stylesheet()['Italic']
    canvas.setFont(psfontname='Times-Bold', size=9)
    par = Paragraph(
        text='This is a multi-line footer.  It goes on every page.  ' * 5,
        style=style)
    w, h = par.wrap(availWidth=doc.width, availHeight=doc.bottomMargin)
    par.drawOn(canvas=canvas, x=doc.leftMargin, y=h)

    canvas.restoreState()


def main():
    # define the document template (the outermost container for the document)
    doc = SimpleDocTemplate(
        filename='phello.pdf', pagesize=A4, leftMargin=1*cm, bottomMargin=6*cm)

    styles = stylesheet()
    flowables = list()
    # add a vertical gap (we have to assign width too)
    flowables.append(Spacer(width=1*mm, height=50*mm))

    for i in range(100):
        if i < 25:
            style = styles['Normal']
        elif i == 25:
            style = styles['Alert']
            logo = 'Python_logo_1.png'
            im = Image(logo, width=30*mm, height=30*mm)
            flowables.append(im)
        elif 25 < i <= 75:
            style = styles['Code']
        elif 75 < i <= 90:
            style = styles['Definition']
        else:
            style = styles['Italic']

        bogustext = ('Paragraph number {}. '.format(i))
        p = Paragraph(text=bogustext, style=style)
        flowables.append(p)
        flowables.append(Spacer(width=1*mm, height=2*mm))

    flowables = add_call_to_action(flowables)

    doc.watermark = 'DRAFT'
    # build the document using flowables
    doc.build(flowables, onFirstPage=first_page, onLaterPages=later_pages)


if __name__ == '__main__':
    main()
