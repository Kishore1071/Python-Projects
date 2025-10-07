# pip install pypdf

from pypdf import PdfWriter
import glob # for automatically selecting a all files

# pdf_files = ['file1.pdf', 'file2.pdf', 'file3.pdf', 'file4.pdf', 'file5.pdf']
pdf_files = sorted(glob.glob('*.pdf')) # for automatically selecting a all pdf files in current folder (merging order can't be random)

merger = PdfWriter()

for pdf in pdf_files:

    merger.append(pdf)

output_filename = 'converted_file.pdf'
merger.write(output_filename)
merger.close()

print("File Mergerd")