
import streamlit as st
import os
import subprocess
import shutil
from pathlib import Path

# --- CONFIGURATION ---
PROJECT_DIR = "pfe_report"  # The root folder of your report
BUILD_DIR = "build"         # Where the PDF and auxiliary files go
MAIN_FILE = "main.tex"      # The entry point file

# Ensure directories exist
os.makedirs(PROJECT_DIR, exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "chapters"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "frontmatter"), exist_ok=True)
os.makedirs(os.path.join(PROJECT_DIR, "figures"), exist_ok=True)

st.set_page_config(layout="wide", page_title="Local Overleaf PFE")

# --- HELPER FUNCTIONS ---
def get_all_tex_files():
    """Returns a list of all .tex files in the project directory."""
    tex_files = []
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file.endswith(".tex"):
                # Create a relative path for the file browser
                rel_path = os.path.relpath(os.path.join(root, file), PROJECT_DIR)
                tex_files.append(rel_path)
    return tex_files

def compile_latex():
    """Runs pdflatex on the main file."""
    try:
        # Ensure build directory exists
        os.makedirs(BUILD_DIR, exist_ok=True)
        
        # Copy project files individually to avoid rmtree failures on locked PDF files
        for root, dirs, files in os.walk(PROJECT_DIR):
            rel_path = os.path.relpath(root, PROJECT_DIR)
            target_dir = os.path.join(BUILD_DIR, rel_path) if rel_path != "." else BUILD_DIR
            os.makedirs(target_dir, exist_ok=True)
            
            for file in files:
                # Do not copy build outputs from source folder to avoid conflicts
                if file.endswith((".pdf", ".log", ".aux", ".out", ".toc", ".lof", ".lot")):
                    continue
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                try:
                    shutil.copy2(source_file, target_file)
                except Exception:
                    pass # ignore lock errors during copy
        
        # Execute pdflatex twice (to resolve references and Table of Contents)
        result = None
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", MAIN_FILE],
                cwd=BUILD_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        
        if result and result.returncode == 0:
            # Copy the compiled PDF back to the project directory for convenience
            src_pdf = os.path.join(BUILD_DIR, f"{Path(MAIN_FILE).stem}.pdf")
            dest_pdf = os.path.join(PROJECT_DIR, f"{Path(MAIN_FILE).stem}.pdf")
            try:
                if os.path.exists(src_pdf):
                    shutil.copy2(src_pdf, dest_pdf)
            except Exception:
                pass # ignore if locked in target as well
            return True, "Compilation Successful!"
        else:
            err_msg = result.stdout if result else "No execution result"
            return False, err_msg
    except Exception as e:
        return False, str(e)

# --- UI LAYOUT ---
st.title("📝 Local Overleaf for PFE")

# Sidebar: File Explorer
st.sidebar.header("📁 Project Files")
all_files = get_all_tex_files()

# If project is empty, create a basic main.tex
if not all_files:
    with open(os.path.join(PROJECT_DIR, MAIN_FILE), "w") as f:
        f.write(r"\documentclass{report}" + "\n" + r"\begin{document}" + "\n" + "Bonjour! Bienvenue dans votre PFE." + "\n" + r"\end{document}")
    all_files = get_all_tex_files()

selected_file = st.sidebar.selectbox("Select a file to edit", all_files)

# Main Area: Two Columns (Editor | Preview)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"Editing: {selected_file}")
    file_path = os.path.join(PROJECT_DIR, selected_file)
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Text editor
    new_content = st.text_area("LaTeX Source", value=content, height=600)
    
    if st.button("💾 Save File"):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        st.success("File saved!")

with col2:
    st.subheader("📄 PDF Preview")
    if st.button("🚀 Compile PDF"):
        with st.spinner("Compiling... please wait..."):
            success, message = compile_latex()
            if success:
                st.success(message)
            else:
                st.error("Compilation Error")
                st.text(message)

    # Display the PDF
    pdf_path = os.path.join(BUILD_DIR, f"{Path(MAIN_FILE).stem}.pdf")
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            base64_pdf = f.read()
            # Embed PDF in iframe
            import base64
            pdf_base64 = base64.b64encode(base64_pdf).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="100%" height="800" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)
    else:
        st.info("Click 'Compile PDF' to generate the preview.")