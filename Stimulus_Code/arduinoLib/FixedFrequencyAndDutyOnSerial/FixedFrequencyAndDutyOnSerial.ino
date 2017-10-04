// Script will flicker an LED on port 13 based on Serial input
// the frequency will only take effect once a high and low time is given
// input in form 'u200' and 'd340'
// must send a pair of commands at present.

int downTicks = 50;
int upTicks = 50;
bool writingUp = false;
bool writingLow = false;
String downString = "";
String upString = "";
bool upDone = false;
bool lowDone = false;

void setup(){
  Serial.begin(9600);
  while(!Serial){}
  pinMode(13, OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(11,OUTPUT);
  downString.reserve(20);
  upString.reserve(20);
}

void loop(){
  digitalWrite(13, HIGH);
  digitalWrite(12,HIGH);
  digitalWrite(11,HIGH);
  delay(upTicks);
  digitalWrite(13, LOW);
  digitalWrite(12,LOW);
  digitalWrite(11,LOW);
  delay(downTicks);  

  if (upDone && lowDone){ // only enters this routine when a new pair is obtained
    upDone = false;
    lowDone = false;
    downTicks = downString.toInt();
    upTicks = upString.toInt();
    upString ="";
    downString="";
  }
}

void serialEvent(){
  while(Serial.available()){
    char inByte = Serial.read();
    Serial.print(inByte);

    if (inByte == 'u'){ // determines wether to set length of up time
      writingUp = true;
    }
    if (inByte == 'd'){ // determines if the down time must be sent
      writingLow = true;
    }

    if (isdigit(inByte)){
      if (writingUp){
         upString +=(char)inByte;
        }
      if (writingLow){
        downString +=(char)inByte;
      }
    }
    
    if (inByte == '\n' && writingUp){ //reset the strings 
      writingUp = false;
      upDone = true;
    }
    if (inByte == '\n' && writingLow){ //reset the strings 
      writingLow = false;
      lowDone = true;
    }   
  }
}





