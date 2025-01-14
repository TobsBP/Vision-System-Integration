# Vision-System-Integration

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
1. A IA analisa a foto capturada **30 vezes**.  
2. Se os fios estiverem fora do padrão:  
   - O sistema envia o caractere `'f'` para o Arduino.  
   - Um LED é aceso, indicando erro.  
3. Enquanto o botão da "boca de lobo" não for pressionado, o sistema permanecerá travado.  

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
1. The AI analyzes the captured image **30 times**.  
2. If the wires are out of alignment:  
   - The system sends an `'f'` character to the Arduino.  
   - A LED is turned on to indicate an error.  
3. The system remains locked until the "boca de lobo" button is pressed.  

