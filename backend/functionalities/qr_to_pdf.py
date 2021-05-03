from fpdf import FPDF
import pyqrcode
import os

from company.models import (
    Company,
    QRCode,
)

#Exceptions:
from django.core.exceptions import ObjectDoesNotExist

# no order
BACKGROUND_IMAGE = "img/Modele_QR_1.png"

#order
BACKGROUND_IMAGE = "img/Modele_QR_2.png"

def make_many_qr_pdf(lsTablesNumbers,identifiantEntreprise,lsIdOfTables):

    urlOfTables = []
    subtitles = []

    #Create the subtitles
    for i in range(len(lsTablesNumbers)):
        subtitles.append("N°{}".format(str(lsTablesNumbers[i])))
        urlOfTables.append("www.onTable.fr/orders/{}{}".format(identifiantEntreprise,lsIdOfTables[i]))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    # cellw and cellh are cell width and cell height respectively (set to a quarter of the page)
    (cellw, cellh) = (190/2, 266/2)

    # Size is in millimeters; 300 is arbitrary
    qr_code_size = 75

    for i in range(len(lsTablesNumbers)):

        #Where the QRCodes will be stocked (just the QRCodes)
        pathQRCode = "media/temp/qrcode_img{}{}.png".format(identifiantEntreprise,lsIdOfTables[i])

        url = pyqrcode.create(urlOfTables[i])
        url.png(pathQRCode, scale=1)

        # Adjust these values to be change the position of the QR code relative to the cell
        qr_x_offset = 0    #0
        qr_y_offset = 2.28    #2.7



        if(i > 0 and i % 4 == 0):
            pdf.add_page()
            pdf.set_x(10) #10
            pdf.set_y(10) #10

        pdf.image(BACKGROUND_IMAGE, pdf.get_x(), pdf.get_y(), cellw, cellh)
        image_x = qr_x_offset + pdf.get_x() + cellw/2 - qr_code_size/2
        image_y = pdf.get_y() + cellh/qr_y_offset - qr_code_size/2
        pdf.image(pathQRCode, image_x, image_y, qr_code_size, link=urlOfTables[i])


        pdf.set_font("Arial", size=15)
        pdf.set_text_color(255 , 255, 255)
        text_x = pdf.get_x() + 72.5
        text_y = pdf.get_y() + 128

        pdf.text(text_x, text_y, txt=(identifiantEntreprise+str(lsIdOfTables[i])))

        pdf.set_font("Arial", size=15)
        pdf.set_text_color(255 , 255, 255)
        text_x = pdf.get_x() + 55
        text_y = pdf.get_y() + 128

        pdf.text(text_x, text_y, txt=subtitles[i])

        # Bordure à 0 ou 1
        pdf.cell(w=cellw, h=cellh, border=1, ln=i%2, align='C', fill=False)


    pdf.output("/media/temp/QRCodes_{}.pdf".format(identifiantEntreprise))

    return "/media/temp/QRCodes_{}.pdf".format(identifiantEntreprise)

def get_qrCode(company):
    company_code = company.company_code
    try:
        company_qrcode = QRCode.objects.get(company_id=company.id)
        if company_qrcode :
            return company_qrcode
    except ObjectDoesNotExist:
        urlOfTable = "www.onTable.fr/orders/{}".format(company_code)
        pathQRCode = "media/qrcodes/qrcode_img{}.png".format(company_code)

        url = pyqrcode.create(urlOfTable)
        url.png(pathQRCode, scale=1)

        qrcode = QRCode()
        qrcode.picture.name = pathQRCode
        qrcode.company=company
        qrcode.save()
    return qrcode
def make_1qr_pdf(tableNumber, identifiantEntreprise):

    company = Company.objects.get(company_code=identifiantEntreprise)
    urlOfTable = "www.onTable.fr/orders/{}{}".format(identifiantEntreprise,tableNumber)
    pathQRCode = "/media/temp/qrcode_img{}{}.png".format(identifiantEntreprise,tableNumber)
    subtitles = "N°{}".format(str(tableNumber))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)


    # cellw and cellh are cell width and cell height respectively (set to a quarter of the page)
    (cellw, cellh) = (190/2, 266/2)

    # Size is in millimeters; 300 is arbitrary
    qr_code_size = 75

    url = pyqrcode.create(urlOfTable)
    url.png(pathQRCode, scale=1)

    # Adjust these values to be change the position of the QR code relative to the cell
    qr_x_offset = 0
    qr_y_offset = 2.28

    pdf.image(BACKGROUND_IMAGE, pdf.get_x(), pdf.get_y(), cellw, cellh)
    image_x = qr_x_offset + pdf.get_x() + cellw/2 - qr_code_size/2
    image_y = pdf.get_y() + cellh/qr_y_offset - qr_code_size/2
    pdf.image(pathQRCode, image_x, image_y, qr_code_size, link=urlOfTable)

    text_x = pdf.get_x() + (cellw - pdf.get_string_width(subtitles))/2
    text_y = pdf.get_y() + cellh - 10

    pdf.set_font("Arial", size=15)
    pdf.set_text_color(255 , 255, 255)
    text_x = pdf.get_x() + 72.5
    text_y = pdf.get_y() + 128

    pdf.text(text_x, text_y, txt=(identifiantEntreprise+str(tableNumber)))

    pdf.set_font("Arial", size=15)
    pdf.set_text_color(255 , 255, 255)
    text_x = pdf.get_x() + 55
    text_y = pdf.get_y() + 128

    pdf.text(text_x, text_y, txt=subtitles)

    # Bordure à 0 ou 1
    pdf.cell(w=cellw, h=cellh, border=1, ln=i%2, align='C', fill=False)

    url = None

    try:
        os.remove(pathQRCode)
    except OSError as error:
        raise

    pdf.output("media/temp/qrcode_img{}{}.png".format(identifiantEntreprise,tableNumber))

    return "media/temp/qrcode_img{}{}.png".format(identifiantEntreprise,tableNumber)

def make_many_same_qr_pdf(number, identifiantEntreprise):

    urlOfTable = "www.onTable.fr/orders/{}".format(identifiantEntreprise)
    pathQRCode = "media/temp/qrcode_img{}.png".format(identifiantEntreprise)
    urlOfTable= "www.onTable.fr/orders/{}".format(identifiantEntreprise)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)


    # cellw and cellh are cell width and cell height respectively (set to a quarter of the page)
    (cellw, cellh) = (190/2, 266/2)

    # Size is in millimeters; 300 is arbitrary
    qr_code_size = 75
    url = pyqrcode.create(urlOfTable)
    url.png(pathQRCode, scale=1)

    for i in range(0,number):
        print(i)
        # Adjust these values to be change the position of the QR code relative to the cell
        qr_x_offset = 0
        qr_y_offset = 2.28

        if(i > 0 and i % 4 == 0):
            pdf.add_page()
            pdf.set_x(10) #10
            pdf.set_y(10) #10

        pdf.image(BACKGROUND_IMAGE, pdf.get_x(), pdf.get_y(), cellw, cellh)
        image_x = qr_x_offset + pdf.get_x() + cellw/2 - qr_code_size/2
        image_y = pdf.get_y() + cellh/qr_y_offset - qr_code_size/2
        pdf.image(pathQRCode, image_x, image_y, qr_code_size, link=urlOfTable)

        pdf.set_font("Arial", size=15)
        pdf.set_text_color(255 , 255, 255)
        text_x = pdf.get_x() + 72.5
        text_y = pdf.get_y() + 128

        pdf.text(text_x, text_y, txt=(identifiantEntreprise))


        # Bordure à 0 ou 1
        pdf.cell(w=cellw, h=cellh, border=1, ln=i%2, align='C', fill=False)

        url = None



    pdf.output("media/temp/qrcode_img{}.png".format(identifiantEntreprise))

    try:
        os.remove(pathQRCode)
    except OSError as error:
        raise

    return "media/temp/qrcode_img{}.png".format(identifiantEntreprise)


"""
Exemple de requete
"""
def main():
    #make_many_qr_pdf([1,2,3,4,5],'XAAA',['XA','ZA','ZA','ZA','ZE'])
    #make_many_same_qr_pdf(4,'')
    make_many_qr_pdf([12],'XAAA',['XA'])
    #make_1qr_pdf(5,'XAAA','PA')
    #make_many_same_qr_pdf(4,'UZZZ')
if __name__ == "__main__":
    main()
