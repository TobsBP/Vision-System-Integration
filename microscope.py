import cv2
import numpy as np

def main():
    capture_device_index = 0  # Codigo da CAM

    # Abrir o dispositivo de captura
    cap = cv2.VideoCapture(capture_device_index)

    if not cap.isOpened():
        print("Erro ao abrir a captura HDMI.")
        return

    print("Pressione '1' para Tons de Cinza, '2' para Detecção de Bordas, '3' para Desfoque.")
    print("Pressione '4' para Detecção de Vermelho, '5' para Detecção de Preto.")
    print("Pressione 's' para salvar a imagem com o filtro aplicado ou 'q' para sair.")

    current_filter = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame.")
            break

        # Aplicar filtro baseado na escolha do usuário
        if current_filter == "gray":
            filtered_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif current_filter == "edges":
            filtered_frame = cv2.Canny(frame, 100, 200)
        elif current_filter == "blur":
            filtered_frame = cv2.GaussianBlur(frame, (15, 15), 0)
        elif current_filter == "red":
            # Converter para HSV e criar máscara para vermelho
            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])
            mask_red = cv2.inRange(hsv_frame, lower_red1, upper_red1) + cv2.inRange(hsv_frame, lower_red2, upper_red2)
            filtered_frame = cv2.bitwise_and(frame, frame, mask=mask_red)
        elif current_filter == "black":
            # Converter para escala de cinza e criar máscara para preto
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, mask_black = cv2.threshold(gray_frame, 50, 255, cv2.THRESH_BINARY_INV)
            filtered_frame = cv2.bitwise_and(frame, frame, mask=mask_black)
        else:
            filtered_frame = frame

        # Mostrar o feed com o filtro ou detecção aplicada
        cv2.imshow("Feed HDMI com Filtro", filtered_frame)

        # Aguardar entrada do teclado
        key = cv2.waitKey(1) & 0xFF
        if key == ord('0'):
            current_filter = None
            print("Filtro desativado")
        elif key == ord('1'):
            current_filter = "gray"
            print("Filtro: Tons de Cinza")
        elif key == ord('2'):
            current_filter = "edges"
            print("Filtro: Detecção de Bordas")
        elif key == ord('3'):
            current_filter = "blur"
            print("Filtro: Desfoque")
        elif key == ord('4'):
            current_filter = "red"
            print("Detecção de Vermelho")
        elif key == ord('5'):
            current_filter = "black"
            print("Detecção de Preto")
        elif key == ord('s'):
            filename = "filtered_frame.jpg"
            cv2.imwrite(filename, filtered_frame)
            print(f"Imagem salva como {filename}")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()