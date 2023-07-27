import re
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph, SimpleDocTemplate
from reportlab.platypus.flowables import Image
from reportlab.lib import colors
from random import randint
from datetime import date
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import locale
import math

# locale.setlocale(locale.LC_ALL, 'de')


# Read the main CSV file into a pandas DataFrame
csv_file_path = 'Customers.csv'
df_customers = pd.read_csv(csv_file_path, delimiter='\t')

# Read the services CSV file into a pandas DataFrame
services_file_path = 'Services2.csv'
df_services = pd.read_csv(services_file_path, delimiter='\t')

# Read the document type CSV file into a pandas DataFrame
doc_file_path = 'doc_info.csv'
df_doc = pd.read_csv(doc_file_path, delimiter='\t')


# Function to create the PDF receipt
def create_receipt(doc_ttl, greeting_txt, main_txt, doc_nr_type, doc_nr, customer_name, customer_address, #customer_address2,
                   customer_tel, customer_id, df_service):
    pdf_file_path = f"{customer_name}_{doc_nr_type}.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Create a SimpleDocTemplate with letter size and set the font
    # doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    # story = []

    # Header with provider's logo
    header_frame = Frame(5, 740, 500, 100, showBoundary=0)
    logo_path = 'GTR.jpeg'  # Replace with the path to your provider's logo
    # c.drawImage(logo_path, 172, 740, width=100, height=50)
    logo = Image(logo_path, width=100, height=50)
    c.setFillColor(colors.gray)

    # Move "Auftragsbestätigung" text to right above the horizontal line
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, 730, doc_ttl)
    c.drawRightString(523, 755, "Provider Logo")
    # c.drawRightString(523, 735, "Provider Name")
    # c.drawRightString(523, 715, "Provider Address")
    c.drawImage(logo_path, 430, 720, width=100, height=50)

    # Draw a horizontal line below the header
    c.line(50, 710, 550, 710)

    # footer line
    c.line(50, 50, 550, 50)
    # Footer with provider's address
    # footer_frame = Frame(0, 0, 740, 50, showBoundary=0)
    # footer_text = Paragraph(f"Provider's Address: {provider_address}", getSampleStyleSheet()["Normal"])
    # footer_frame.addFromList([footer_text], c)
    c.setFont("Helvetica", 8)
    c.drawString(50, 40, "GTR")
    c.drawString(50, 30, "Nelsenstr 1")
    c.drawString(50, 20, "41748 Viersen")

    c.drawString(170, 40, "+49 176 5579 1865")
    c.drawString(170, 30, "gtr.renovierung@outlook.com")
    c.drawString(170, 20, "Geschäftsführer: H. Ghaderi")

    c.drawString(290, 40, "Bank N26")
    c.drawString(290, 30, "DE07100110012033287789")
    c.drawString(290, 20, "BIC: NTSBDEB1XXX")

    c.drawString(410, 40, "Ust. ID: DE361613180")
    c.drawString(410, 30, "")
    c.drawString(410, 20, "Amtsgericht Viersen")

    # Customer address on the top left
    c.setFont("Helvetica-Bold", 8)
    c.drawString(72, 680, customer_name)
    c.drawString(72, 665, customer_address)
    # c.drawString(72, 650, customer_address2)
    c.drawString(72, 650, "Tel. " + customer_tel)

    # Provider address on the top right
    c.setFont("Helvetica-Bold", 8)
    c.drawString(400, 680, f"{doc_nr_type}: {doc_nr}")
    c.drawString(400, 665, f"Datum: {date.today()}")
    c.drawString(400, 650, f"Kundennr.: {customer_id}")
    c.drawString(400, 635, f"Ansprechpartner.: Mana Moli")

    # Set greeting text
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.black)
    c.drawString(72, 600, "Sehr geehrte(r) " + customer_name + ",")
    c.setFont("Helvetica", 10)
    c.drawString(72, 580, greeting_txt)
    # "vielen Dank für Ihren Auftrag. Gemäß unseres Angebotes erbringen wir folgende Leistungen:")

    # story
    # c.setFont("Helvetica-Bold", 14)
    # story.append(Paragraph("Dear Valued Customer,", c))
    # c.setFont("Helvetica", 12)
    # story.append(Paragraph("Thank you for choosing our services. We are pleased to provide the following services:", c))

    # Add a vertical space (margin) after the header
    c.drawString(72, 570, "")  # You can adjust the vertical position as needed

    # Calculate the height of greeting text and add a margin below it
    greeting_text_height = 600
    vertical_margin = 10
    vertical_position = greeting_text_height - vertical_margin

    # Add a vertical space (margin) after the header
    # story.append(Paragraph("", c))
    # List of provided services and prices in a table
    data = [['Pos.', 'Leistung', 'Einheit', 'Menge', 'Einzelprice',
             'Gesamtpreis']]  # Add 'Count' column as the third column
    df_service['total_sum'] = df_service['Menge'] * df_service['Einzelpreis']
    for idx, row in df_service.iterrows():
        data.append([str(idx + 1), row['service'], row['Einheit'], str(row['Menge']),
                     # locale.format('%.4f', row['Einzelpreis'], 1),
                     f"€{row['Einzelpreis']:,.2f}",
                     f"€{row['total_sum']:,.2f}"])
    # add the last row for the total sum of all prices
    data.append(["", "", "", "", "Gesamtsumme", f"€{df_service['total_sum'].sum():,.2f}"])
    table = Table(data)
    table.setStyle(TableStyle([
        # Set borders for the entire table
        # ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Draw border around the entire table
        # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),  # Draw inner grid lines

        # Set custom borders for specific cells
        # ('BOX', (0, 0), (-1, 0), 1, colors.black),  # Draw border for the header row
        # ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),  # Draw line below the header row
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),  # Draw line above the last row

        # Skip drawing some borders
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Add bottom padding to the header row to remove the border

        # Set background color for the header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),

        # Set alignment and font for the header row
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        # Decrease font size for all cells in the table
        ('FONTSIZE', (0, 0), (-1, -1), 9),

        # Set bold style for the 'Count' column (index 2)
        ('FONT', (1, 1), (1, -1), 'Helvetica-Bold'),

        # Set alignment for the 'Count' column (index 2)
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),

    ]))

    # Calculate the required height of the table
    width, height = table.wrap(400, 200)
    table.drawOn(c, 72, vertical_position - height - 25)

    style = ParagraphStyle(
        'Normal',
        fontSize=10,
        fontName='Helvetica',
    )

    c.setFont("Helvetica", 10)
    # c.drawString(72, vertical_position - height - 50 - 100,
    text = main_txt
    # """Als Kleinunternehmer im Sinne von § 19 Abs. 1 UStG wird Umsatzsteuer nicht berechnet.\n
    # Die Preise sind ohne Materialkosten. Die Kosten für die benötigten und gekauften Materialien müssen gleichzeitig
    # mit der Lieferung der Quittung beglichen werden.\n
    # Zahlungsbedingungen: Zahlbar in bar bei Übergabe oder binnen 7 Tage nach Leistungsdatum per Überweisung.
    # Wir bedanken uns für den Auftrag und freuen uns auf die angenehme Zusammenarbeit.\n
    # Bei Rückfragen stehen wir selbstverständlich jederzeit gerne zur Verfügung.\n
    # Hiermit bestätige ich die obigen Auftrag.\n Unterschrift:___________________"""

    # text = text.replace('\n','<br />\n')
    style = getSampleStyleSheet()
    custom_style = ParagraphStyle(name='CustomStyle', parent=style['Normal'], leading=20)  # Increase line spacing to 20
    paragraph = Paragraph(text, custom_style)
    paragraph.strike = 0  # Remove the strike style (if present)
    # paragraph.addStyle(style['Bold'], 0)
    width, height = paragraph.wrap(400, 200)

    # paragraph_position =

    paragraph.drawOn(c, 72, vertical_position - height - 320)

    # Save the canvas
    c.save()

    # Add the table to the story
    # story.append(table)

    # Build the story and create the PDF
    # doc.build(story)


# Ask for customer's ID as input
c_id = 125  # int(input("Enter customer's ID: "))
doc_type = input("Enter the document type: ")

if doc_type not in df_doc['doc_type'].values:
    print("Document type not found.")
else:
    # Check if customer ID exists in the main DataFrame
    if c_id not in df_customers['id'].values:
        print("Customer ID not found.")
    else:
        # Extract customer information from the main DataFrame using customer ID
        row_customer = df_customers[df_customers['id'] == c_id].iloc[0]
        c_name = row_customer['name']
        c_addr = row_customer['address']
        # c_addr2 = row_customer['address2']
        c_tel = row_customer['tel']
        provider_name = 'GTR'  # row_customer['Service Provider Name']
        provider_address = 'Nelsensrt 1'  # row_customer['Service Provider Address']

        # Extract services for the customer from the services DataFrame using customer ID
        df_services_for_customer = df_services[df_services['id'] == c_id]
        df_services_for_customer['price_sum'] = \
            df_services_for_customer['Menge'] * df_services_for_customer['Einzelpreis']
        services = df_services_for_customer['service'].tolist()
        count = df_services_for_customer['Menge'].tolist()
        prices = df_services_for_customer['Einzelpreis'].tolist()
        prices_all = df_services_for_customer['price_sum'].tolist()

        # Get the texts for the corresponding document type
        greet_txt = df_doc[df_doc['doc_type'] == doc_type]['greet_text'].values[0]
        body_txt = df_doc[df_doc['doc_type'] == doc_type]['main_text'].values[0]

        nr_type = df_doc[df_doc['doc_type'] == doc_type]['nr_type'].values[0]
        doc_title = df_doc[df_doc['doc_type'] == doc_type]['doc_title'].values[0]
        d_nr = df_customers[df_customers['id'] == c_id]['doc_nr'].values[0]
        if math.isnan(d_nr):
            d_nr = randint(1000, 100000)
            df_customers.loc[df_customers["id"] == c_id, "doc_nr"] = d_nr
            df_customers.to_csv(re.sub(".csv", "_updated.csv", csv_file_path), sep='\t')

        # Create the PDF receipt
        create_receipt(doc_title, greet_txt, body_txt, nr_type, d_nr, c_name, c_addr, #c_addr2,
                                 str(c_tel), c_id, df_services_for_customer)

        print("Receipt generated successfully.")
