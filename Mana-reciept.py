import re

import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import Image
from reportlab.lib import colors
from random import randrange
from datetime import date
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph



# Read the main CSV file into a pandas DataFrame
csv_file_path = '/home/rostam/Desktop/Customers.csv'
df_customers = pd.read_csv(csv_file_path, delimiter='\t')

# Read the services CSV file into a pandas DataFrame
services_file_path = '/home/rostam/Desktop/Services.csv'
df_services = pd.read_csv(services_file_path, delimiter='\t')


# Function to create the PDF receipt
def create_receipt(customer_name, customer_address, customer_id, df_service):
    pdf_file_path = f"{customer_name}_receipt.pdf"
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Create a SimpleDocTemplate with letter size and set the font
    doc = SimpleDocTemplate(pdf_file_path, pagesize=letter)
    story = []

    # Header with provider's logo
    header_frame = Frame(5, 740, 500, 100, showBoundary=0)
    logo_path = '/home/rostam/Desktop/GTR.jpeg'  # Replace with the path to your provider's logo
    # c.drawImage(logo_path, 172, 740, width=100, height=50)
    logo = Image(logo_path, width=100, height=50)
    c.setFillColor(colors.gray)

    # Move "Auftragsbestätigung" text to right above the horizontal line
    c.drawString(72, 735, "Auftragsbestätigung")
    c.drawRightString(523, 755, "Provider Logo")
    # c.drawRightString(523, 735, "Provider Name")
    # c.drawRightString(523, 715, "Provider Address")
    c.drawImage(logo_path, 430, 720, width=100, height=50)

    # Draw a horizontal line below the header
    c.line(50, 710, 550, 710)

    # Footer with provider's address
    # footer_frame = Frame(0, 0, 550, 50, showBoundary=0)
    # footer_text = Paragraph(f"Provider's Address: {provider_address}", getSampleStyleSheet()["Normal"])
    # footer_frame.addFromList([footer_text], c)

    # Customer address on the top left
    c.drawString(72, 680, customer_name)
    c.drawString(72, 660, customer_address)

    # Provider address on the top right
    a_nr = randrange(1000, 100000)
    c.drawString(400, 680, f"Antragnummer: {a_nr}")
    c.drawString(400, 660, f"Datum: {date.today()}")
    c.drawString(400, 640, f"Kundennr.: {customer_id}")
    c.drawString(400, 620, f"Ansprechpartner.: Mana Moli")

    # Set greeting text
    # c.setFont("Helvetica-Bold", 14)
    # c.drawString(72, 620, "Dear " + customer_name + ",")
    # c.setFont("Helvetica", 12)
    # c.drawString(72, 600, "Thank you for choosing our services. We are pleased to provide the following services:")

    c.setFont("Helvetica-Bold", 14)
    story.append(Paragraph("Dear Valued Customer,", c))
    c.setFont("Helvetica", 12)
    story.append(Paragraph("Thank you for choosing our services. We are pleased to provide the following services:", c))

    # Add a vertical space (margin) after the header
    c.drawString(72, 570, "")  # You can adjust the vertical position as needed

    # Calculate the height of greeting text and add a margin below it
    greeting_text_height = 640
    vertical_margin = 10
    vertical_position = greeting_text_height - vertical_margin

    # Add a vertical space (margin) after the header
    story.append(Paragraph("", c))
    # List of provided services and prices in a table
    data = [['Pos.', 'Service', 'Count', 'Einzelprice', 'Gesamtpreis']]  # Add 'Count' column as the third column
    for idx, row in df_service.iterrows():
        data.append([str(idx + 1), row['service'], str(row['Menge']), row['Einzelpreis'],
                     row['Einzelpreis'] * row['Menge']])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), 'white'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), 'white'),
        ('GRID', (0, 0), (-1, -1), 1, 'black')
    ]))

    # Calculate the required height of the table
    # width, height = table.wrap(400, 200)
    # table.drawOn(c, 72, vertical_position - height)
    #
    # # Save the canvas
    # c.save()

    # Add the table to the story
    story.append(table)

    # Build the story and create the PDF
    doc.build(story)
    return a_nr


# Ask for customer's ID as input
customer_id = 125#int(input("Enter customer's ID: "))

# Check if customer ID exists in the main DataFrame
if customer_id not in df_customers['id'].values:
    print("Customer ID not found.")
else:
    # Extract customer information from the main DataFrame using customer ID
    row_customer = df_customers[df_customers['id'] == customer_id].iloc[0]
    customer_name = row_customer['name']
    customer_address = row_customer['address']
    provider_name = 'GTR'#row_customer['Service Provider Name']
    provider_address = 'Nelsensrt 1'#row_customer['Service Provider Address']

    # Extract services for the customer from the services DataFrame using customer ID
    df_services_for_customer = df_services[df_services['id'] == customer_id]
    df_services_for_customer['price_sum'] = \
        df_services_for_customer['Menge'] * df_services_for_customer['Einzelpreis']
    services = df_services_for_customer['service'].tolist()
    count = df_services_for_customer['Menge'].tolist()
    prices = df_services_for_customer['Einzelpreis'].tolist()
    prices_all = df_services_for_customer['price_sum'].tolist()

    # Create the PDF receipt
    auf_nr = create_receipt(customer_name, customer_address, customer_id, df_services_for_customer)
    df_customers.loc[df_customers["id"] == customer_id, "a_nr"] = auf_nr
    df_customers.to_csv(re.sub(".csv", "_updated.csv", csv_file_path), sep='\t')
    print("Receipt generated successfully.")
