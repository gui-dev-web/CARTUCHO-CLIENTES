import streamlit as st
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import tempfile
import win32api
import win32print

st.title("Cadastro clientes")

nome = st.text_input("Nome do cliente:")
telefone = st.text_input("Telefone:")
cartucho = st.text_area("Série e cor do cartucho:")

if st.button("Imprimir"):
    if not nome or not telefone or not cartucho:
        st.warning("Preencha todos os campos antes de imprimir.")
    else:
        # Define tamanho da folha: 80 mm de largura x 200 mm de altura
        largura, altura = 80 * mm, 200 * mm
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmpfile:
            c = canvas.Canvas(tmpfile.name, pagesize=(largura, altura))
            c.setFont("Helvetica", 10)
            c.drawString(10, altura - 20, "--- INFORMAÇÕES ---")
            c.drawString(10, altura - 40, f"Nome: {nome}")
            c.drawString(10, altura - 60, f"Telefone: {telefone}")
            c.drawString(10, altura - 80, "Cartucho:")
            text = c.beginText(10, altura - 100)
            text.textLines(cartucho)
            c.drawText(text)
            c.save()
            arquivo = tmpfile.name

        impressora = win32print.GetDefaultPrinter()
        win32api.ShellExecute(0, "print", arquivo, None, ".", 0)
        st.success(f"Enviado para a impressora: {impressora}")
