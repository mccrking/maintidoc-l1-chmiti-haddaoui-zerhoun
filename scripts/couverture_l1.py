from pathlib import Path
import io
import pymupdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor,white
from reportlab.lib.utils import ImageReader

def ajouter_couverture(file,logo):
    file=Path(file);logo=Path(logo)
    assert logo.is_file()
    w,h=A4;buffer=io.BytesIO();c=canvas.Canvas(buffer,pagesize=A4)
    green=HexColor('#000000');navy=HexColor('#000000');gray=HexColor('#000000')
    c.setFillColor(white);c.rect(0,0,w,h,fill=1,stroke=0)
    c.setFillColor(green);c.rect(0,h-12,w,12,fill=1,stroke=0)
    iw,ih=ImageReader(str(logo)).getSize();dw=390;dh=dw*ih/iw
    c.drawImage(str(logo),(w-dw)/2,h-56-dh,width=dw,height=dh,mask='auto')
    c.setFillColor(navy);c.setFont('AB',36);c.drawCentredString(w/2,535,'MaintiDoc')
    c.setFont('A',15);c.drawCentredString(w/2,505,'Assistant documentaire multimodal')
    c.drawCentredString(w/2,483,'et agentique pour la maintenance')
    c.setFillColor(white);c.setStrokeColor(green);c.roundRect(66,411,w-132,42,5,fill=1,stroke=1)
    c.setFillColor(navy);c.setFont('AB',13);c.drawCentredString(w/2,427,'LIVRABLE 1 - CADRAGE, CORPUS ET ARCHITECTURE')
    c.setFillColor(gray);c.setFont('AB',10);c.drawCentredString(w/2,369,'GROUPE')
    c.setFillColor(navy);c.setFont('AB',17);c.drawCentredString(w/2,343,'CHMITI-HADDAOUI-ZERHOUN')
    c.setFont('A',13)
    for y,name in [(313,'Mehdi Chmiti'),(292,'Ismail Haddaoui'),(271,'Ayman Zerhoun')]:c.drawCentredString(w/2,y,name)
    c.setFillColor(gray);c.setFont('AB',10);c.drawCentredString(w/2,217,'ENCADRÉ PAR')
    c.setFillColor(navy);c.setFont('AB',15);c.drawCentredString(w/2,192,'Pr. Mariam CHERRABI')
    c.setFillColor(gray);c.setFont('A',11);c.drawCentredString(w/2,130,'Module : IA générative multimodale - EMSI 2026')
    c.drawCentredString(w/2,107,'1 novembre 2026')
    c.setStrokeColor(green);c.setLineWidth(1);c.line(66,69,w-66,69)
    c.showPage();c.save()
    cover=pymupdf.open(stream=buffer.getvalue(),filetype='pdf');source=pymupdf.open(file)
    assert len(source)==14,'La page de garde doit précéder les 14 pages du rapport.'
    result=pymupdf.open();result.insert_pdf(cover);result.insert_pdf(source)
    result.set_metadata(source.metadata)
    toc=source.get_toc()
    if toc:result.set_toc([[1,'Page de garde',1]]+[[level,title,p+1] for level,title,p in toc])
    data=result.tobytes(garbage=4,deflate=True)
    source.close();cover.close();result.close();file.write_bytes(data)
    with pymupdf.open(file) as check:
        assert len(check)==15
        assert 'Pr. Mariam CHERRABI' in check[0].get_text()
