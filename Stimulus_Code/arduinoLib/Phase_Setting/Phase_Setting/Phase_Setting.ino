// the purpose of the encoding of discrete phase differences
// this discrete method is IN LIGHT of the lack of true parrallel on arduino.
// this script assumes a fixed phase of 50% as this was found effective in the conducted tests

int Left[4] = {0, 0, 1,1};

int RightVals[4][4]={{0, 0,1,1},{0, 1, 1,0},{1,1,0,0},{1,0, 0, 1}};

String recvStr = "";
bool doneRecv = false;
char index = 'a'; //used to determine which phase to use
int selectedRow = 1;

int QuaterLength = 250;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial){}
  pinMode(13,OUTPUT);
  pinMode(12,OUTPUT);
  pinMode(11,OUTPUT);
  recvStr.reserve(20);
  digitalWrite(12,0);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int i=0; i<=3; i++){
    digitalWrite(13, Left[i]);
    digitalWrite(11, RightVals[selectedRow][i]);
    delay(QuaterLength);
    //Serial.print(selectedRow);
  }
  if (doneRecv == true){
    doneRecv = false;
    QuaterLength = recvStr.toInt();
    recvStr ="";
    if (index=='a')
    selectedRow = 0;
    else if (index=='b')
    selectedRow =1;
    else if (index=='c')
    selectedRow=2;
    else
    selectedRow =3;
  }

}

void serialEvent(){
  while(Serial.available()){
    char inByte = Serial.read();
     if (inByte =='\n')
      doneRecv = true;
     else if (inByte=='a'){
     index = 'a';}
     else if (inByte=='b'){
     index = 'b';}
     else if (inByte=='c'){
     index = 'c';}
     else if (inByte=='d'){
     index ='d';}

     if (isdigit(inByte)){
       recvStr += (char)inByte;
     }
  }
}

