import cv2, serial, sys, os, re, datetime, time, subprocess
import tensorflow as tf
import numpy as np

np.set_printoptions(suppress=True)

# Load the TensorFlow model and labels
model = tf.saved_model.load("Beta_saved/model.savedmodel")

with open("Beta_saved/labels.txt", "r") as f:
    class_names = [line.strip() for line in f]

# Setting camera and serial port
camera_index = 0
serial_port = '/dev/ttyUSB0'
baud_rate = 9600

# Path to main image folder
main_folder = 'Imgs'

# Debug mode 
debug = False

# Create the folder of the day
hoje = datetime.datetime.now().strftime("Dia_%d_%m_%y")
diretorio_hoje = os.path.join(main_folder, hoje)

def create_folder(diretorio_hoje):
    if not os.path.exists(diretorio_hoje):
        os.makedirs(diretorio_hoje)
        os.makedirs(os.path.join(diretorio_hoje, 'Certas'))
        os.makedirs(os.path.join(diretorio_hoje, 'Erradas'))

def num_fotos_ok():
    caminho_diretorio = f'Imgs/{hoje}/Certas'

    ok = 0

    extensoes_imagens = ['.jpg', '.png',]

    for arquivo in os.listdir(caminho_diretorio):
        if os.path.splitext(arquivo)[1].lower() in extensoes_imagens:
            match = re.search(r'\d+', arquivo)
            if match:
                numero = int(match.group())  
                if numero > ok: 
                    ok = numero

    return ok

def num_fotos_er():
    caminho_diretorio = f'Imgs/{hoje}/Erradas'

    er = 0

    extensoes_imagens = ['.jpg', '.png',]

    for arquivo in os.listdir(caminho_diretorio):
        if os.path.splitext(arquivo)[1].lower() in extensoes_imagens:
            match = re.search(r'\d+', arquivo)
            if match:
                numero = int(match.group())
                if numero > er:       
                    er = numero
    
    return er

def save_image_ok(frame, cont_ok):
    cv2.imwrite(f"Imgs/{hoje}/Certas/image_{cont_ok}.jpg", frame)
    cont_ok = cont_ok + 1
    return cont_ok

def save_image_er(frame, cont_er):
    cv2.imwrite(f"Imgs/{hoje}/Erradas/image_{cont_er}.jpg", frame)
    cont_er = cont_er + 1
    return cont_er

def export_folder():
    # Define source and destination paths
    src_path = f"Imgs/{hoje}"
    dest_path_base = "Path/to/server/"
    server_username = "username"  
    server_ip = "server_ip_address"
 
    # Check if the source folder exists
    if not os.path.exists(src_path):
        print(f"Source folder '{src_path}' does not exist.")
        return

    # Define the initial destination path
    dest_path = f"{server_username}@{server_ip}:{dest_path}/{hoje}"

    # Increment the counter if the folder already exists in the destination
    counter = 1
    while os.path.exists(dest_path):
        dest_path = os.path.join(dest_path_base, f"{hoje}_{counter}")
        counter += 1

    try:
        subprocess.run(["scp", "-r", src_path, dest_path], check=True)
        print(f"Folder successfully transferred to: {dest_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error transferring folder: {e}")

def main():
    # Wait for the Arduino to connect
    while True:
        try:
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            print("Arduino conectado!")
            break
        except serial.SerialException:
            print("Esperando Arduino...")
            time.sleep(1)

    # Wait for the camera to connect
    while True:
        camera = cv2.VideoCapture(camera_index)
        if camera.isOpened():
            print("Câmera conectada!")
            break
        else:
            print("Esperando Câmera...")
            time.sleep(1)
        
    create_folder(diretorio_hoje)

    cont_ok = num_fotos_ok()
    cont_er = num_fotos_er()

    try:
        # Connect to the serial port
        with serial.Serial(serial_port, baud_rate, timeout=1) as ser:
            print("Serial port connected.")

            if not camera.isOpened():
                raise Exception(f"Failed to open camera at index {camera_index}")

            print("Camera initialized...")

            while True:

                # Reset the input and output buffers
                ser.reset_input_buffer()  
                ser.reset_output_buffer()

                validation = False

                # Wait for a signal from the Arduino
                while not validation:
                    if ser.in_waiting > 0:
                        res = ser.read().decode('utf-8', errors='ignore').strip()

                        if res == 's':
                            print("Received 's' from Arduino. Starting predictions...")

                            # Clear the input buffer
                            for _ in range(5):
                                camera.read()
                            
                            validation = True
                            
                        elif res == 'e':
                            print("Received 'e' from Arduino. Exporting folder...")
                            export_folder()
                            print("Ending the program...")
                            sys.exit()
                
                if validation:
                    
                    for i in range(0,10):

                        ret, frame = camera.read()
                    
                        if not ret:
                            print("Failed to capture image.")
                            break

                        # Resize and normalize the frame
                        resized_image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
                        normalized_image = resized_image.astype(np.float32) / 127.5 - 1
                        input_tensor = np.expand_dims(normalized_image, axis=0)

                        # Make predictions
                        predictions = model(input_tensor).numpy()
                        index = np.argmax(predictions)

                        # Get the results
                        class_name = class_names[index]
                        confidence_score = predictions[0][index]

                        # Print the results
                        print(f"Class: {class_name} - Confidence Score: {confidence_score:.2%}")

                        # Based on the results, save the image
                        if confidence_score > 0.99 and class_name == "0 OK!":  
                            cont_ok = save_image_ok(frame, cont_ok)
                            if debug: print("Sent 'x' to Arduino.")
                            ser.write(b'x')
                            break
                        elif confidence_score > 0.99 and class_name == "1 Erro!":
                            cont_er = save_image_er(frame, cont_er)
                            if debug: print("Sent 'f' to Arduino.")
                            ser.write(b'f')  
                            break  
                        else:
                            if i == 9:
                                cont_er = save_image_er(frame, cont_er)
                                if debug: print("Sent 'f' to Arduino.")
                                ser.write(b'f')   
                                break

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if camera.isOpened():
            camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()