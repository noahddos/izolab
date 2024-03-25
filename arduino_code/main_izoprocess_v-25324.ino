int volume = 0;
int list = 0;
int needtemp = 0;
char mode_ = 'N';
#define PIN_ENA 9 // Вывод управления скоростью вращения мотора №1
#define PIN_IN3 7 // Вывод управления направлением вращения мотора №1
#define PIN_IN4 6 // Вывод управления направлением вращения мотора №1
#define PIN_IN1 10
#define PIN_IN2 11
float needpressure = 0;
const int buttonp = 2;
const int buttonp2 = 3;
const int buttontemp1 = 4;
const int buttontemp2 = 5;

const int power = 80;

#include <Wire.h>
#include <MS5611.h>
MS5611 ms5611;
#include <Wire.h> 
#include <LiquidCrystal_I2C.h> 

LiquidCrystal_I2C lcd(0x27,16,2); 


void setup() {
  pinMode(buttonp, INPUT);
  pinMode(buttontemp1,INPUT);
  pinMode(buttontemp2,INPUT);
  pinMode(PIN_IN3, OUTPUT);
  pinMode(PIN_IN4, OUTPUT);
  pinMode(PIN_IN1, OUTPUT);
  pinMode(PIN_IN2, OUTPUT);
  pinMode(PIN_ENA, OUTPUT);
  digitalWrite(PIN_IN3, LOW); 
  digitalWrite(PIN_IN4, LOW);
  Serial.begin(9600); // begin 
  while(!ms5611.begin(MS5611_ULTRA_HIGH_RES))
  {
    delay(10);
  }
  lcd.init();
  lcd.backlight();
  delay(1000);  
}

void display(int l){
  Serial.println(String(ms5611.readTemperature())+' '+String(ms5611.readPressure())+' '+' '+String(volume*1.6));
  if (l == 0){ 
      lcd.setCursor(0,0);
      lcd.print("P=");
      lcd.setCursor(2,0);
      lcd.print(ms5611.readPressure());
      lcd.setCursor(8,0);
      lcd.print("Pa");
      lcd.setCursor(15,0);
      lcd.print(mode_);
      // temperature for lcd
      lcd.setCursor(0,1);
      lcd.print("T=");
      lcd.setCursor(2,1);
      lcd.print(ms5611.readTemperature());
      lcd.setCursor(7,1);
      lcd.print( "C");
      lcd.setCursor(9,1);
      lcd.print("V=");
      lcd.setCursor(11,1);
      lcd.print(volume*1.6);
  }
  if (l == 1){
    lcd.setCursor(0,0);
    lcd.print("realtemp");
    lcd.setCursor(8,0);
    lcd.print(ms5611.readTemperature());
    lcd.setCursor(0,1);
    lcd.print("needtemp");
    lcd.setCursor(8,1);
    lcd.print(needtemp);
  }

  if (digitalRead(buttontemp1) == HIGH && digitalRead(buttontemp2) == HIGH){// Choose list on screen
    if (list == 1){
      list -=1;
    }
    else{
      list +=1;
    }
    lcd.clear();
    delay(200);
  }
}

void loop(){
  analogWrite(PIN_ENA,power);
  display(list);
  if (digitalRead(buttontemp1) == HIGH && list == 1){
    needtemp +=1;
  }
  if (digitalRead(buttontemp2) == HIGH && list == 1){
    needtemp -=1;
  }
  if (needtemp > ms5611.readTemperature()){
    digitalWrite(PIN_IN1,HIGH);
  }else{
    digitalWrite(PIN_IN1,LOW);
  }
  if (list == 0 && digitalRead(buttontemp1)){
    lcd.clear();
    delay(500);
    char cur = mode_;
    while (true){
      lcd.setCursor(4,0);
      lcd.print("MODE");
      lcd.setCursor(0,1);
      lcd.print("1-N");
      lcd.setCursor(4,1);
      lcd.print("2-P");
      if (digitalRead(buttontemp1)== HIGH){
        mode_ = 'P';
        needpressure = ms5611.readPressure();
        lcd.clear();
        lcd.setCursor(4,0);
        lcd.print("DONE");
        delay(1000);
        lcd.clear();
        break;
      }
      if (digitalRead(buttontemp2) == HIGH){
        mode_ = 'N';
        needpressure = ms5611.readPressure();
        lcd.clear();
        lcd.setCursor(4,0);
        lcd.print("DONE");
        delay(1000);
        lcd.clear(); 
        break;
      }
    }
  }
  if (mode_ == 'P'){
    if (ms5611.readPressure() - needpressure > 800){
      while(( analogRead(A0) > 200 )){
        int v = analogRead(A0);
        digitalWrite(PIN_IN3,LOW);
        digitalWrite(PIN_IN4,HIGH);
        delay(10);
        if (analogRead(A0) - v > 800){
          volume += 1;
        }
        display(list);
      }
    }
    if ( needpressure - ms5611.readPressure() > 800){
      while(( analogRead(A0) > 200 )){
        int v = analogRead(A0);
        digitalWrite(PIN_IN3,HIGH);
        digitalWrite(PIN_IN4,LOW);
        delay(10);
        if (analogRead(A0) - v > 800){
          volume -= 1;
        }
        display(list);
      }
    }
  }
  if (digitalRead(buttonp) == HIGH){
    int cur = volume;
    while(( analogRead(A0) > 200) || (digitalRead(buttonp) == HIGH)){
      int v =analogRead(A0);
      digitalWrite(PIN_IN3,LOW);
      digitalWrite(PIN_IN4,HIGH);
      delay(10);
      if (analogRead(A0) - v > 800){
        volume += 1;
        display(list);
      }  
   }
   if (cur == volume){
    volume += 1;
   }
    digitalWrite(PIN_IN4,LOW);
    digitalWrite(PIN_IN3,LOW);
  }

  if (digitalRead(buttonp2)== HIGH){ // Move right 
    int cur = volume;
    while(( analogRead(A0) > 200) || (digitalRead(buttonp2) == HIGH)){
      int v =analogRead(A0);
      digitalWrite(PIN_IN3,HIGH);
      digitalWrite(PIN_IN4,LOW);
      delay(10);
      if (analogRead(A0) - v  > 800){
        volume -= 1;
        display(list);
      }
   }
   if (cur == volume){
    volume -=1;
   }
    digitalWrite(PIN_IN4,LOW);
    digitalWrite(PIN_IN3,LOW);
  }
}
