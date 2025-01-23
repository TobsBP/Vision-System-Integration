# Vision-System-Integration

## Main Scripts

There are two main scripts provided in this project: `main.py` and `main_lite.py`.

### main.py
This script uses the full TensorFlow model for image classification. It is suitable for environments where computational resources are not a constraint. The script performs the following tasks:
- Connects to the Arduino and camera.
- Captures images from the camera.
- Uses the TensorFlow model to classify the images.
- Sends results back to the Arduino and saves the images in appropriate folders.

### main_lite.py
This script uses a TensorFlow Lite model for image classification. It is optimized for environments with limited computational resources. The script performs similar tasks as `main.py` but with a lighter model:
- Connects to the Arduino and camera.
- Captures images from the camera.
- Uses the TensorFlow Lite model to classify the images.
- Sends results back to the Arduino and saves the images in appropriate folders.

Both scripts ensure that the system remains locked until the "boca de lobo" button is pressed, and they provide functionality to export the captured images to a specified server path.

## Other Scripts

### load_screen.py
This script just opens a screen to show the video from the video capture board. I use it to see the Raspberry Pi screen.
- Connects to the USB port. 

### microscope.py
This script just opens a screen to show the video from the video capture board, but here I can apply some filters. I was testing some filters to use in the AI.
- Connects to the USB port.
---

# Microscope - Setup and Operation  

## Requirements  
- **Lighting:** Proper lighting for color visualization.  
- **Capture Card:** For image viewing and manipulation.  
- **Verification:** Always verify the microscope code in the `main.py` file.  
- **Computer:** For data processing.  
- **Arduino:** For button communication.  

## Height Specifications  
- **Recommended Height:** 30 cm (without focal lens). This height provides optimal performance.  

## Important Notes  
- The camera index (used by Python to identify the device) may change if new USB devices are connected.  
- **Common Indices:** `0, 1, 2, 3...`.  
- If the device cannot be found, use the `lsusb` command to list all connected USB devices.  

---

# Installation Guide

This guide provides step-by-step instructions to install TensorFlow (CPU version), PySerial, and OpenCV in a Python environment.

## Prerequisites

1. **Python Installed**: Ensure Python 3.9.21 is installed.
   - Download from [python.org](https://www.python.org/downloads/).

2. **Pip Updated**: Update pip to the latest version:
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Virtual Environment (Optional but Recommended)**: Create a virtual environment to isolate your packages:
   ```bash
   python3.9 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

## Installation Steps

### 1. Install Required Packages
Use the `requirements.txt` file to install all necessary packages.

Run the following command:
```bash
pip install -r requirements.txt
```

Verify the installations:
```bash
python -c "import tensorflow as tf; print(tf.__version__)"
python -c "import serial; print(serial.__version__)"
python -c "import cv2; print(cv2.__version__)"
```
You should see the version numbers for TensorFlow, PySerial, and OpenCV printed.

## Troubleshooting

### Common Issues
- **Pip Installation Error:** Ensure pip is updated: `pip install --upgrade pip`.
- **Conflicting Dependencies:** Use a virtual environment to avoid conflicts.

### Checking Installed Packages
List installed packages and their versions:
```bash
pip list
```

### Uninstall a Package
To uninstall a package, use:
```bash
pip uninstall <package_name>
```
For example:
```bash
pip uninstall tensorflow-cpu
```

## Additional Resources
- [TensorFlow Documentation](https://www.tensorflow.org/install/pip)
- [PySerial Documentation](https://pyserial.readthedocs.io/en/latest/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

## How It Works  

### Initialization  
1. The Arduino sends an `'s'` character to initialize the system.  
2. The `main.py` script detects this character and starts the process.  

### Python Processing  
- Activates the camera (or microscope).  
- Initializes the Artificial Intelligence (AI).  

### Artificial Intelligence  
- Trained to recognize specific patterns of colors and positions.  

### Process  
1. The AI analyzes the captured image **10 times**.  
2. If the wires are out of alignment or the confidence score is below 99%:  
   - The system sends an `'f'` character to the Arduino.  
   - A LED is turned on to indicate an error.  
3. If the wires are correctly aligned and the confidence score is above 99%:  
   - The system sends an `'x'` character to the Arduino.  
   - The image is saved in the "Certas" folder.
4. The system remains locked until the "boca de lobo" button is pressed.  

---

# Microscópio - Configuração e Funcionamento  

## Requisitos  
- **Iluminação:** Boa iluminação para visualização das cores.  
- **Placa de captura:** Visualizar e manipular as imagens.  
- **Verificação:** Confira sempre o código do microscópio no arquivo `main.py`.  
- **Computador:** Para processamento de dados.  
- **Arduino:** Comunicação com os botões.  

## Especificações de Altura  
- **Altura recomendada:** 30 cm (sem lente focal). Nessa altura, o desempenho é otimizado.  

## Observações Importantes  
- O índice da câmera (usado pelo Python para identificar o dispositivo) pode variar se novos dispositivos USB forem conectados.  
- **Índices comuns:** `0, 1, 2, 3...`.  
- Caso o dispositivo não seja encontrado, use o comando `lsusb` para listar todos os dispositivos USB conectados.  

---

# Guia de Instalação

Este guia fornece instruções passo a passo para instalar TensorFlow (versão para CPU), PySerial e OpenCV em um ambiente Python.

## Pré-requisitos

1. **Python Instalado**: Certifique-se de que o Python 3.9.21 esteja instalado.
   - Baixe em [python.org](https://www.python.org/downloads/).

2. **Pip Atualizado**: Atualize o pip para a versão mais recente:
   ```bash
   python -m pip install --upgrade pip
   ```

3. **Ambiente Virtual (Opcional, mas Recomendado)**: Crie um ambiente virtual para isolar seus pacotes:
   ```bash
   python3.9 -m venv meuambiente
   source meuambiente/bin/activate  # No Windows: meuambiente\Scripts\activate
   ```

## Passos de Instalação

### 1. Instalar Pacotes Requeridos
Use o arquivo `requirements.txt` para instalar todos os pacotes necessários.

Execute o seguinte comando:
```bash
pip install -r requirements.txt
```

Verifique as instalações:
```bash
python -c "import tensorflow as tf; print(tf.__version__)"
python -c "import serial; print(serial.__version__)"
python -c "import cv2; print(cv2.__version__)"
```
Você deverá ver os números das versões do TensorFlow, PySerial e OpenCV impressos.

## Solução de Problemas

### Problemas Comuns
- **Erro na Instalação com Pip:** Certifique-se de que o pip está atualizado: `pip install --upgrade pip`.
- **Conflitos de Dependências:** Use um ambiente virtual para evitar conflitos.

### Verificar Pacotes Instalados
Liste os pacotes instalados e suas versões:
```bash
pip list
```

### Desinstalar um Pacote
Para desinstalar um pacote, use:
```bash
pip uninstall <nome_do_pacote>
```
Por exemplo:
```bash
pip uninstall tensorflow-cpu
```

## Recursos Adicionais
- [Documentação do TensorFlow](https://www.tensorflow.org/install/pip)
- [Documentação do PySerial](https://pyserial.readthedocs.io/en/latest/)
- [Documentação do OpenCV](https://docs.opencv.org/)

---
## Scripts Principais

Existem dois scripts principais fornecidos neste projeto: `main.py` e `main_lite.py`.

### main.py
Este script usa o modelo completo do TensorFlow para classificação de imagens. É adequado para ambientes onde os recursos computacionais não são uma restrição. O script realiza as seguintes tarefas:
- Conecta-se ao Arduino e à câmera.
- Captura imagens da câmera.
- Usa o modelo TensorFlow para classificar as imagens.
- Envia os resultados de volta para o Arduino e salva as imagens em pastas apropriadas.

### main_lite.py
Este script usa um modelo TensorFlow Lite para classificação de imagens. É otimizado para ambientes com recursos computacionais limitados. O script realiza tarefas semelhantes ao `main.py`, mas com um modelo mais leve:
- Conecta-se ao Arduino e à câmera.
- Captura imagens da câmera.
- Usa o modelo TensorFlow Lite para classificar as imagens.
- Envia os resultados de volta para o Arduino e salva as imagens em pastas apropriadas.

Ambos os scripts garantem que o sistema permaneça bloqueado até que o botão "boca de lobo" seja pressionado, e fornecem funcionalidade para exportar as imagens capturadas para um caminho de servidor especificado.

## Outros Scripts

### load_screen.py
Este script apenas abre uma tela para mostrar o vídeo da placa de captura de vídeo. Eu uso para ver a tela do Raspberry Pi.
- Conecta-se à porta USB.

### microscope.py
Este script apenas abre uma tela para mostrar o vídeo da placa de captura de vídeo, mas aqui eu posso aplicar alguns filtros. Eu estava testando alguns filtros para usar na IA.
- Conecta-se à porta USB.

---

## Funcionamento  

### Inicialização  
1. O Arduino envia um caractere `'s'` para inicializar o sistema.  
2. O script `main.py` detecta o caractere e inicia o processo.  

### Processamento com Python  
- Ativa a câmera (ou microscópio).  
- Inicializa a Inteligência Artificial (IA).  

### Inteligência Artificial  
- Treinada para reconhecer padrões específicos de cores e posições.  

### Processo  
1. A IA analisa a foto capturada **10 vezes**.  
2. Se os fios estiverem fora do padrão ou a confiança for inferior a 99%:  
   - O sistema envia o caractere `'f'` para o Arduino.  
   - Um LED é aceso, indicando erro.  
3. Se os fios estiverem corretamente alinhados e a confiança for superior a 99%:  
   - O sistema envia o caractere `'x'` para o Arduino.  
   - A imagem é salva na pasta "Certas".
4. Enquanto o botão da "boca de lobo" não for pressionado, o sistema permanecerá travado.  

---