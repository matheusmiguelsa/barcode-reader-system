import cv2
from pyzbar.pyzbar import decode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Método para ler códigos de barras na imagem e salvar a imagem com marcações
def BarcodeReader(image_path, output_path):
    # Carrega a imagem como um array numpy usando o OpenCV
    img = cv2.imread(image_path)
    
    # Decodifica a imagem em códigos de barras
    detectedBarcodes = decode(img)
    
    # Se nenhum código de barras for detectado, exibe uma mensagem
    if not detectedBarcodes:
        print("Código de barras não detectado ou o código está em branco/corrompido!")
    else:
        # Inicializa um contador para numerar os códigos de barras
        barcode_num = 1
        c = canvas.Canvas(output_path, pagesize=letter)


        # Percorre todos os códigos de barras detectados na imagem
        for barcode in detectedBarcodes:
            print(barcode_num)
            # Obtém as coordenadas do retângulo que envolve o código de barras
            (x, y, w, h) = barcode.rect
            
            # Desenha o retângulo ao redor do código de barras na imagem
            cv2.rectangle(img, (x-10, y-10), (x + w+10, y + h+10), (255, 0, 0), 2)
            if barcode.type == "CODE128":
                text_for_barcode_type = "barcode"
            else:
                text_for_barcode_type = "qrcode"
                
            # Formata o texto com o número do código de barras e seu conteúdo
            text_pdf = f"Código {barcode_num}: {barcode.data.decode('utf-8')} - {len(barcode.data.decode('utf-8'))} - {text_for_barcode_type}"
            text_image = f"{barcode_num}"

            
            # Coloca o texto na imagem
            cv2.putText(img, text_image, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            c.drawString(100, 750 - barcode_num * 20, text_pdf)
            print(text_image)
            
            # Incrementa o contador de código de barras
            barcode_num += 1
            
            # Exibe os dados do código de barras
            print(f"Tipo: {barcode.type}")
            print(f"Dados: {barcode.data}")
            print("---")
    
    # Salva a imagem com as marcações e números identificadores
    temp_image_path = "temp_image.png"
    cv2.imwrite(temp_image_path, img)
    # Adiciona a imagem ao PDF
    c.drawInlineImage(temp_image_path, 100, 370, width=400, height=300)
    
    # Fecha o objeto canvas e salva o PDF
    c.save()
    
    print(f"PDF salvo em: {output_path}")

def listar_arquivos(caminho):
    # Lista todos os arquivos e diretórios no caminho especificado
    lista_arquivos = os.listdir(caminho)
    
    # Filtra apenas os nomes de arquivos (excluindo diretórios)
    nomes_arquivos = [nome for nome in lista_arquivos if os.path.isfile(os.path.join(caminho, nome))]
    
    return nomes_arquivos

diretorio = 'etiqueta_png'  # Substitua pelo caminho da sua pasta
diretorio_output = 'output'  # Substitua pelo caminho da sua pasta
nomes_arquivos = listar_arquivos(diretorio)
nomes_arquivos_output = listar_arquivos(diretorio_output)
lista_definitiva = []
for c in range(len(nomes_arquivos)):
    for c2 in range(len(nomes_arquivos_output)):
        if nomes_arquivos[c].replace(".png", "") == nomes_arquivos_output[c2].replace(".pdf", ""):
            lista_definitiva.append(nomes_arquivos[c].replace(".pdf", "").replace(".png", ""))


if __name__ == "__main__":
    if len(nomes_arquivos) > 0:
        for c in range(len(nomes_arquivos)):
            if nomes_arquivos[c] not in lista_definitiva:
                # Nome do arquivo da imagem onde estão os códigos de barras
                image_path = f"etiqueta_png/{nomes_arquivos[c]}"
                # Caminho para salvar a imagem com as marcações dos códigos de barras
                output_path = f"output/{nomes_arquivos[c]}.pdf".replace(".png", "")

                # Chama a função para ler os códigos de barras na imagem e salvar
                BarcodeReader(image_path, output_path)
                os.system("rm -f temp_image.png")
    else:
        print("Nenhuma imagem nova encontrado!")