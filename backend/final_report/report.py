import io
from html import escape
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
def pdf_bytes(title,sections):
    buf=io.BytesIO();doc=SimpleDocTemplate(buf,pagesize=A4);s=getSampleStyleSheet();story=[Paragraph(title,s['Title']),Spacer(1,12)]
    for h,b in sections:story += [Paragraph(escape(str(h)),s['Heading2']),Paragraph(escape(str(b)).replace('\n','<br/>'),s['BodyText']),Spacer(1,8)]
    doc.build(story);return buf.getvalue()
def html_bytes(title,sections):return ('<html><body><h1>'+escape(title)+'</h1>'+''.join(f'<h2>{escape(str(h))}</h2><pre>{escape(str(b))}</pre>' for h,b in sections)+'</body></html>').encode()
def excel_bytes(sheets):
    b=io.BytesIO()
    with pd.ExcelWriter(b,engine='openpyxl') as w:
        for n,d in sheets.items():d.to_excel(w,sheet_name=n[:31],index=False)
    return b.getvalue()
