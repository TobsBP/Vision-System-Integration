import cv2, serial, signal, sys, os, re
import tensorflow as tf
import numpy as np

np.set_printoptions(suppress=True)

# Load the TensorFlow model and labels
model = tf.saved_model.load("Beta_saved/model.savedmodel")

with open("Beta_saved/labels.txt", "r") as f:
    class_names = [line.strip() for line in f]

# Setting camera and serial port
camera_index = 2
serial_port = '/dev/ttyUSB0'
baud_rate = 9600

def graceful_exit(signum, frame):
    """Clean up resources on exit."""
    print("\nExiting program...")
    if camera.isOpened():
        camera.release()
    cv2.destroyAllWindows()
    sys.exit(0)

def num_fotos_ok():
    caminho_diretorio = 'Imgs/Certas'

    ok = 0

    extensoes_imagens = ['.jpg']

    for arquivo in os.listdir(caminho_diretorio):
        if os.path.splitext(arquivo)[1].lower() in extensoes_imagens:
            match = re.search(r'\d+', arquivo)
            if match:
                numero = int(match.group())  
                if numero > ok: 
                    ok = numero

    return ok

def num_fotos_er():
    caminho_diretorio = 'Imgs/Erradas'

    er = 0

    extensoes_imagens = ['.jpg']

    for arquivo in os.listdir(caminho_diretorio):
        if os.path.splitext(arquivo)[1].lower() in extensoes_imagens:
            match = re.search(r'\d+', arquivo)
            if match:
                numero = int(match.group())
                if numero > er:       
                    er = numero
    
    return er

signal.signal(signal.SIGINT, graceful_exit)

if __name__ == "__main__":

    cont_ok = num_fotos_ok()
    cont_er = num_fotos_er()

    try:
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print("Serial port connected.")

            camera = cv2.VideoCapture(camera_index)
            if not camera.isOpened():
                raise Exception(f"Failed to open camera at index {camera_index}")

            print("Camera initialized. Press ESC to exit.")

            while True:

                ser.reset_input_buffer()  
                ser.reset_output_buffer()

                validation = False

                while not validation:
                    if ser.in_waiting > 0:
                        res = ser.read().decode('utf-8', errors='ignore').strip()

                        if res == 's':
                            print("Received 's' from Arduino. Starting predictions...")

                            for _ in range(5):
                                camera.read()

                            ret, frame = camera.read()
                        
                            if not ret:
                                print("Failed to capture image.")
                                break
                            
                            validation = True
                
                if validation:
                    
                    resized_image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
                    normalized_image = resized_image.astype(np.float32) / 127.5 - 1
                    input_tensor = np.expand_dims(normalized_image, axis=0)
                    
                    for i in range(0,30):

                        predictions = model(input_tensor).numpy()
                        index = np.argmax(predictions)

                        class_name = class_names[index]
                        confidence_score = predictions[0][index]

                        print(f"Class: {class_name} - Confidence Score: {confidence_score:.2%}")

                        if confidence_score > 0.99 and class_name == "0 OK!":  
                            cv2.imwrite(f"Imgs/Certas/image_{cont_ok}.jpg", frame)
                            cont_ok = cont_ok + 1
                            ser.write(b'x')  # Manda pra serial 'x' para informar que foi feito
                            print("Sent 'x' to Arduino.")
                            break
                        elif confidence_score > 0.99 and class_name == "1 Erro!":
                            if i == 29:
                                cv2.imwrite(f"Imgs/Erradas/image_{cont_er}.jpg", frame)
                                print("Sent 'f' to Arduino.")
                                cont_er = cont_er + 1
                                ser.write(b'f')  # Manda pra serial 'f' para informar que nao foi feito
                                break   

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if camera.isOpened():
            camera.release()
        cv2.destroyAllWindows()
