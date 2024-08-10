from markdown_pdf import MarkdownPdf, Section

# def create_pdf(markdown_content: str):
#     pdf = MarkdownPdf()
#     pdf.meta["title"] = 'Generated Content'
#     pdf.add_section(Section(markdown_content, toc=False))
#     pdf.save('output.pdf')

def create_pdf(markdown_content: str):
    try:
        pdf = MarkdownPdf()
        pdf.meta["title"] = 'Generated Content'
        pdf.add_section(Section(markdown_content, toc=False))
        pdf.save('output.pdf')
        print("PDF generated successfully.")
    except Exception as e:
        print(f"An error occurred while creating the PDF: {e}")