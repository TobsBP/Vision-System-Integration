import cv2

def main():
    capture_device_index = 2  # Índice do dispositivo de captura

    # Abrir o dispositivo de captura
    cap = cv2.VideoCapture(capture_device_index)

    if not cap.isOpened():
        print("Erro ao abrir a captura HDMI.")
        return

    # Definir resolução desejada (opcional, ajustável conforme a necessidade)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Largura
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Altura

    print("Pressione 'q' para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao capturar o frame.")
            break

        # Mostrar o feed em tempo real
        cv2.imshow("Feed HDMI", frame)

        # Tecla para sair
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar o dispositivo de captura e fechar a janela
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
