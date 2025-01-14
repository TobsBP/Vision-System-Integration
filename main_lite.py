import cv2, serial, signal, sys, os, re
import tensorflow as tf
import numpy as np

np.set_printoptions(suppress=True)

# Path to your TFLite model
tflite_model_path = "converted_tflite/model_unquant.tflite" 

# Inicialize o intérprete TFLite
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Obtenha detalhes de entrada e saída
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Tamanho esperado do modelo
input_shape = input_details[0]['shape'] 
input_height = input_shape[1]
input_width = input_shape[2]

with open("converted_tflite/labels.txt", "r") as f:
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

    extensoes_imagens = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

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

    extensoes_imagens = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

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

                validation = False

                while not validation:
                    if ser.in_waiting > 0:
                        res = ser.read().decode('utf-8', errors='ignore').strip()
                        if res == 's':
                            print("Received 's' from Arduino. Starting predictions...")
                            ret, frame = camera.read()
                
                            if not ret:
                                print("Failed to capture image.")
                                break
                            
                            validation = True
                
                if validation: 
                    
                    resized_image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
                    normalized_image = resized_image.astype(np.float32) / 127.5 - 1
                    input_data = np.expand_dims(normalized_image, axis=0).astype(np.float32)

                    for i in range(30):
                        interpreter.set_tensor(input_details[0]['index'], input_data)

                        interpreter.invoke()

                        output_data = interpreter.get_tensor(output_details[0]['index'])
                        class_index = np.argmax(output_data) 

                        class_name = class_names[class_index]
                        confidence_score = output_data[0][class_index]

                        print(f"Class: {class_name} - Confidence Score: {confidence_score:.2%}")

                        if confidence_score > 0.99 and class_name == "0 OK!":  
                            cv2.imwrite(f"Imgs/image_{cont_ok}.jpg", frame)
                            cont_ok = cont_ok + 1
                            ser.write(b'x')  # Manda pra serial 'x' para informar que foi feito
                            print("Sent 'x' to Arduino.")
                        elif confidence_score > 0.99 and class_name == "1 Erro!":
                            if i == 29:
                                cont_er = cont_er + 1
                                ser.write(b'f')  # Manda pra serial 'f' para informar que nao foi feito
                                cv2.imwrite(f"Imgs/image_{cont_er}.jpg", frame)
                                print("Sent 'f' to Arduino.")
                                break

    except KeyboardInterrupt:
        print("Program interrupted by user.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if camera.isOpened():
            camera.release()
        cv2.destroyAllWindows()
