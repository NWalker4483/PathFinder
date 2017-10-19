#include <signal.h>


#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#define DELAY 70000
#define LEVELS 7
#define INCREMENT  0.15
FILE *fp;
class ESC{
    public:
    int pin;
    int max_value;
    int min_value;
    int speed;
    bool calibrated;
    
    ESC(int in, int ax_value = 2000,int in_value = 700,int peed=0,bool alibrated=false){
    pin=in;
    max_value=ax_value;
    min_value=in_value;
    calibrated=alibrated;
    if(min_value<=speed<=max_value){
        speed = peed;
    }
    else{
        std::cout<<"Either no speed was given or given speed is either above or below the allowed range and has been set to minimum";
        speed = in_value;
    };/*
    if (alibrated == false){
        */
}};
int main(){
return 0;
}

    
void  INThandler(int sig)
{
    int pin;
        signal(sig, SIG_IGN);
    //turn all pins off
        for (pin = 0; pin < 8; pin++){
        fprintf(fp, "%i=%f\n", pin,0.0);
        fflush(fp);
    }
    fclose(fp);
        exit(0);
}
 
int main(void)
{
    signal(SIGINT, INThandler);
 
    // arrays used to control brightness of a row of LEDs. left then right animation.
    float left[] = {0,0,0,0,0,0,0,0,1,0.75,0.375,0.18,0.09,0.04,0.005,0,0,0,0,0,0,0,0};
    float right[] = {0,0,0,0,0,0,0,0,0.005,0.04,0.09,0.18,0.375,0.75,1,0,0,0,0,0,0,0,0};
 
    int pin = 0;
    float pwm = 0.0;
 
    // open the pi-blaster device file. If it fails, confirm that pi-blaster has been started
    fp = fopen("/dev/pi-blaster", "w");
    if (fp == NULL) {
        printf("Error opening file\n");
        exit(0);
     }
 
    // create the PWM values which are used for the animation going in one direction
    float pwdPower[LEVELS*4];
    float i;
    int j;
    int count = 7;
 
    for (j = 0; j < LEVELS ;  j++){
        pwdPower[j] = 0.0;
    }
 
    for (i = 0.0; i < 1 ; i +=INCREMENT){        if (i>1.0)i=1.0;
        pwdPower[count] = i;
            count++;
    }
 
    for (i = 1; i >0.00001 ; i -=INCREMENT){
        if (i<0.0)i=0.0;
        pwdPower[count] = i;
            count++;
    }
 
        for (j = 0; j < (LEVELS) ;  j++){
                pwdPower[count] = 0.0;
        count++;
        }
 
///////////////////////////////////////////////////////////////////
 
    //This section illustrates different brightness levels
    // using PWM with a 2 second puase between levels.
 
    // Enable all pins using the value 0.002 for PWM
    for (pin = 0; pin < 8; pin++){
                fprintf(fp, "%i=%f\n", pin,0.002);
                       fflush(fp);
    }
    sleep(2);
 
    // Enable all pins using the value 0.03 for PWM
    for (pin = 0; pin < 8; pin++){
                    fprintf(fp, "%i=%f\n", pin,0.03);
                        fflush(fp);
    }
    sleep(2);
 
    // Enable all pins using the value 0.05 for PWM
    for (pin = 0; pin < 8; pin++){
                    fprintf(fp, "%i=%f\n", pin,0.5);
                        fflush(fp);
    }
    sleep(2);
///////////////////////////////////////////////////////////////////
 
    // This section will cycle through the power levels 5 times.
    for (j = 0; j < 5 ; j++){
        for (i = 0.0; i < 1 ; i +=INCREMENT){
            for (pin = 0; pin < 8; pin++){                       fprintf(fp, "%i=%f\n", pin,i );                             fflush(fp);             }       usleep(DELAY);      }               for (i = 1; i >0.00001 ; i -=INCREMENT){
            for (pin = 0; pin < 8; pin++){
                        fprintf(fp, "%i=%f\n", pin,i );
                            fflush(fp);
            }
        usleep(DELAY);
 
        }
    }
///////////////////////////////////////////////////////////////////
 
    // The below section performs the animations
    int c = 0;
    int g;
    for(g = 0; g < 2; g++){      for(c = 16; c>= 0; c--){
            for (pin = 0; pin < 8  ; pin++){
                            fprintf(fp, "%i=%f\n", pin, right[pin+c]);
                            fflush(fp);
            }
        usleep(DELAY);
        }
        for(c = 0; c < 16; c++){
            for (pin = 0; pin < 8; pin++){
                        fprintf(fp, "%i=%f\n", pin, left[pin+c]);
                            fflush(fp);
            }
        usleep(DELAY);
        }
    }
 
    for(g = 0; g < 4; g++){
        for(c = 0; c < (LEVELS*3); c++){
            for (pin = 0; pin < 8; pin++){
                            fprintf(fp, "%i=%f\n", pin, pwdPower[pin+c]);
                        fflush(fp);
            }
            usleep(DELAY);
        }
    }
 
    //turn all pins off
        for (pin = 0; pin < 8; pin++){
        fprintf(fp, "%i=%f\n", pin,0.0);
        fflush(fp);
    }
    fclose(fp);
    return 0;
}
