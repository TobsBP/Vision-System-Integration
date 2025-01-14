const int buttonPinStart = 7;     // Pino do botão Start
const int buttonPinBoca = 8;      // Pino do botão Boca
const int PinLedBoca = 11;   // Pino do led Boca
const int buzzerPin = 3;          // Pino do buzzer
unsigned long delayTime = 10000;  // Tempo de atraso ajustável (10 segundos)
bool recebido = true;

void setup() {
  pinMode(buttonPinStart, INPUT_PULLUP);  // Configura o botão Start como entrada com resistor pull-up
  pinMode(buttonPinBoca, INPUT_PULLUP);   // Configura o botão Boca como entrada com resistor pull-up
  pinMode(buzzerPin, OUTPUT);             // Configura o buzzer como saída
  pinMode(PinLedBoca, OUTPUT);
  Serial.begin(9600);                     // Inicializa a comunicação serial
  digitalWrite(PinLedBoca, HIGH); 
}

void loop() {
  // Verifica se o botão Start foi pressionado e o comando foi recebido
  if (digitalRead(buttonPinStart) == LOW && recebido) {
    Serial.print("s");  // Envia o comando "s" para o Python
    recebido = false;
    delay(200);  // Pequeno atraso para evitar múltiplas leituras
  }

  // Verifica se há dados disponíveis na serial
  if (Serial.available() > 0) {
    char res = Serial.read();  // Lê o dado recebido

    if (res == 'x') {
      recebido = true;  // Marca que o comando foi recebido
    }

    if (res == 'f') {
      recebido = true;

      tone(buzzerPin, 1000, 1000);  // Toca o buzzer por 1 segundo
      digitalWrite(PinLedBoca, LOW); 
      Serial.println("Jogue na boca de lobo.");

      // Espera até que o botão Boca seja pressionado
      while (digitalRead(buttonPinBoca) == HIGH) {
        delay(100);  // Pequeno atraso para evitar leituras rápidas demais
      }
      Serial.println("Ação concluída.");
      noTone(buzzerPin);  // Para o som do buzzer
      digitalWrite(PinLedBoca, HIGH);
    }
  }

  // Feedback caso nenhum comando tenha sido recebido
  if (!recebido) {
    Serial.println("Nenhuma resposta recebida.");
    delay(500);  // Reduz o envio de mensagens repetidas
  }
}
