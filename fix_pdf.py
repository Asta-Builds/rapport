import os
import shutil
from pathlib import Path
from local_overleaf import compile_latex

# Setup paths to match local_overleaf.py
PROJECT_DIR = "pfe_report"
BUILD_DIR = "build"

print("Cleaning build directory...")
if os.path.exists(BUILD_DIR):
    shutil.rmtree(BUILD_DIR)

print("Compiling through local_overleaf logic...")
# We need to make sure pdflatex is in the path for the subprocess call inside compile_latex
os.environ["PATH"] += os.pathsep + r"C:\Users\078526\AppData\Local\Programs\MiKTeX\miktex\bin\x64"

success, message = compile_latex()

if success:
    print("Compilation Successful!")
    pdf_path = os.path.join(BUILD_DIR, "main.pdf")
    if os.path.exists(pdf_path):
        print(f"PDF generated at: {pdf_path}")
        print(f"Size: {os.path.getsize(pdf_path)} bytes")
    else:
        print("PDF file not found in build directory!")
else:
    print("Compilation Failed!")
    print(f"Error: {message}")
