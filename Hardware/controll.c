#include <stdio.h>
#include <unistd.h>
#include <linux/joystick.h>
#include <fcntl.h>
#include <pigpio.h>
#include <pigpiod_if2.h>

#define LEFT_PWM 18
#define LEFT_PIN0 17
#define LEFT_PIN1 27

#define RIGHT_PWM 19
#define RIGHT_PIN0 13
#define RIGHT_PIN1 6

#define FREQ 500
#define MAX_DUTY 50

#define BUTTON_DATA_MAX 12
#define STICK_DATA_MAX 6
#define MAX_STICK 32767
#define BUTTON_X 0
#define BUTTON_A 1
#define BUTTON_B 2
#define BUTTON_Y 3
#define BUTTON_LB 4
#define BUTTON_RB 5
#define BUTTON_LT 6
#define BUTTON_RT 7
#define BUTTON_BACK 8
#define BUTTON_START 9
#define BUTTON_STICKLEFT 10
#define BUTTON_STICKRIGHT 11
#define LEFT_STICK_X 0
#define LEFT_STICK_Y 1
#define RIGHT_STICK_X 2
#define RIGHT_STICK_Y 3
#define CROSS_STICK_X 4
#define CROSS_STICK_Y 5

void cmdview(char btn[],int stk[])
{
        printf("X = %d\t",btn[BUTTON_X]);
        printf("A = %d\t",btn[BUTTON_A]);
        printf("B = %d\t",btn[BUTTON_B]);
        printf("Y = %d\t",btn[BUTTON_Y]);
        printf("LB = %d\t",btn[BUTTON_LB]);
        printf("RB = %d\t",btn[BUTTON_RB]);
        printf("LT = %d\t",btn[BUTTON_LT]);
        printf("RT = %d\t",btn[BUTTON_RT]);
        printf("Back = %d\t",btn[BUTTON_BACK]);
        printf("Start = %d\n",btn[BUTTON_START]);
        printf("ButtonLeft = %d\t",btn[BUTTON_STICKLEFT]);
        printf("ButtonRight = %d\t",btn[BUTTON_STICKRIGHT]);
        printf("Left_X = %d\t",stk[LEFT_STICK_X]);
        printf("Left_Y = %d\t",stk[LEFT_STICK_Y]);
        printf("Right_X = %d\t",stk[RIGHT_STICK_X]);
        printf("Right_Y = %d\t",stk[RIGHT_STICK_Y]);
        printf("Cross_X = %d\t",stk[CROSS_STICK_X]);
        printf("Cross_Y = %d\n",stk[CROSS_STICK_Y]);
}

void controll(char btn[],int stk[],int pi)
{
    int stick_x,stick_y;
    int leftfreq,rightfreq;
    int leftduty,rightduty;
    double leftrate,rightrate;

    stick_x = stk[LEFT_STICK_X];
    stick_y = stk[LEFT_STICK_Y] * -1;

    if(stick_x == 0 && stick_y > 0){
        forword(stick_y,pi);
    }else if(stick_x > 0 && stick_y > 0){
        r_forword(stick_x,stick_y);
    }else if(stick_x > 0 && stick_y == 0){
        right(stick_x);
    }else if(stick_x > 0 && stick_y < 0){
        r_back(stick_x,stick_y);
    }else if(stick_x == 0 && stick_y < 0){
        back(stick_y);
    }else if(stick_x < 0 && stick_y < 0){
        l_back(stick_x,stick_y);
    }else if(stick_x < 0 && stick_y == 0){
        left(stick_x);
    }else if(stick_x < 0 && stick_y > 0){
        l_forword(stick_x,stick_y);
    }else{
        no_move(pi);
    }

    //    printf("X:%d,Y:%d\n",stick_x,stick_y);
}

void forword(int stick,int pi){
    double rate;
    int percent;
    rate = (double)stick / MAX_STICK;
    percent = rate * MAX_DUTY;

    gpio_write(pi,LEFT_PIN0,0);
    gpio_write(pi,LEFT_PIN1,1);
    gpio_write(pi,RIGHT_PIN0,0);
    gpio_write(pi,RIGHT_PIN1,1);

    hardware_PWM(pi,LEFT_PWM,FREQ,percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,percent);

    printf("forword:l=%d%,r=%d%\n",percent,percent);
}

void r_forword(int stick_x,int stick_y,int pi){
    double l_rate,r_rate,distance;
    int l_percent,r_percent;
    if(stick_x > stick_y){
        distance = stick_x;
    }else{
        distance = stick_y;
    }
    l_rate = distance / MAX_STICK;
    r_rate = (double)stick_y / MAX_STICK;
    l_percent = l_rate * MAX_DUTY;
    r_percent = r_rate * MAX_DUTY;

	gpio_write(pi,LEFT_PIN0,0);
    gpio_write(pi,LEFT_PIN1,1);
    gpio_write(pi,RIGHT_PIN0,0);
    gpio_write(pi,RIGHT_PIN1,1);

    hardware_PWM(pi,LEFT_PWM,FREQ,l_percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,r_percent);
    
    printf("r_forword:l=%d%,r=%d%\n",l_percent,r_percent);
}

void right(int stick,int pi){
    double rate;
    int percent;
    rate = (double)stick / MAX_STICK;
    percent = rate * MAX_DUTY;
    
    gpio_write(pi,LEFT_PIN0,0);
    gpio_write(pi,LEFT_PIN1,1);
    gpio_write(pi,RIGHT_PIN0,0);
    gpio_write(pi,RIGHT_PIN1,1);

    hardware_PWM(pi,LEFT_PWM,FREQ,percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,percent);
    
    printf("right:l=%d%,r=0%\n",percent);
}
void r_back(int stick_x,int stick_y,int pi){
    double l_rate,r_rate,distance;
    int l_percent,r_percent;
    stick_y = stick_y * -1;
    if(stick_x > stick_y){
        distance = stick_x;
    }else{
        distance = stick_y;
    }
    l_rate = distance / MAX_STICK;
    r_rate = (double)stick_y / MAX_STICK;
    l_percent = l_rate * MAX_DUTY;
    r_percent = r_rate * MAX_DUTY;
    
    gpio_write(pi,LEFT_PIN0,1);
    gpio_write(pi,LEFT_PIN1,0);
    gpio_write(pi,RIGHT_PIN0,1);
    gpio_write(pi,RIGHT_PIN1,0);

    hardware_PWM(pi,LEFT_PWM,FREQ,l_percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,r_percent);
    
    printf("r_back:l=%d%,r=%d%\n",l_percent,r_percent);
}
void back(int stick,int pi){
    double rate;
    int percent;
    stick = stick * -1;
    rate = (double)stick / MAX_STICK;
    percent = rate * MAX_DUTY;

    gpio_write(pi,LEFT_PIN0,1);
    gpio_write(pi,LEFT_PIN1,0);
    gpio_write(pi,RIGHT_PIN0,1);
    gpio_write(pi,RIGHT_PIN1,0);

    hardware_PWM(pi,LEFT_PWM,FREQ,percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,percent);
    
    printf("back:l=%d%,r=%d%\n",percent,percent);
}
void l_back(int stick_x,int stick_y,int pi){
    double l_rate,r_rate,distance;
    int l_percent,r_percent;
    stick_y = stick_y * -1;
    stick_x = stick_x * -1;
    if(stick_x > stick_y){
        distance = stick_x;
    }else{
        distance = stick_y;
    }
    r_rate = distance / MAX_STICK;
    l_rate = (double)stick_y / MAX_STICK;
    l_percent = l_rate * MAX_DUTY;
    r_percent = r_rate * MAX_DUTY;
    
    gpio_write(pi,LEFT_PIN0,1);
    gpio_write(pi,LEFT_PIN1,0);
    gpio_write(pi,RIGHT_PIN0,1);
    gpio_write(pi,RIGHT_PIN1,0);

    hardware_PWM(pi,LEFT_PWM,FREQ,l_percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,r_percent);
    
    printf("l_back:l=%d%,r=%d%\n",l_percent,r_percent);
}
void left(int stick,int pi){
    double rate;
    int percent;
    stick = stick * -1;
    rate = (double)stick / MAX_STICK;
    percent = rate * MAX_DUTY;
    
    gpio_write(pi,LEFT_PIN0,0);
    gpio_write(pi,LEFT_PIN1,1);
    gpio_write(pi,RIGHT_PIN0,0);
    gpio_write(pi,RIGHT_PIN1,1);

    hardware_PWM(pi,LEFT_PWM,FREQ,percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,percent);
    
    printf("left:l=0%,r=%d%\n",percent);
}
void l_forword(int stick_x,int stick_y,int pi){
    double l_rate,r_rate,distance;
    int l_percent,r_percent;
    stick_x = stick_x * -1;
    if(stick_x > stick_y){
        distance = stick_x;
    }else{
        distance = stick_y;
    }
    r_rate = distance / MAX_STICK;
    l_rate = (double)stick_y / MAX_STICK;
    l_percent = l_rate * MAX_DUTY;
    r_percent = r_rate * MAX_DUTY;
    
    gpio_write(pi,LEFT_PIN0,0);
    gpio_write(pi,LEFT_PIN1,1);
    gpio_write(pi,RIGHT_PIN0,0);
    gpio_write(pi,RIGHT_PIN1,1);

    hardware_PWM(pi,LEFT_PWM,FREQ,l_percent);
    hardware_PWM(pi,RIGHT_PWM,FREQ,r_percent);
    
    printf("l_forword:l=%d%,r=%d%\n",l_percent,r_percent);
}
void no_move(int pi){

    gpio_write(pi,LEFT_PIN0,0);
    gpio_write(pi,LEFT_PIN1,1);
    gpio_write(pi,RIGHT_PIN0,0);
    gpio_write(pi,RIGHT_PIN1,1);

    hardware_PWM(pi,LEFT_PWM,FREQ,0);
    hardware_PWM(pi,RIGHT_PWM,FREQ,0);
    
    printf("no_move\n");
}

int main(void)
{   
    int pi;
    int cnt;
    cnt = 0;

    pi = pigpio_start(0,0);

    set_mode(pi,LEFT_PWM,PI_OUTPUT);
    set_mode(pi,LEFT_PIN0,PI_OUTPUT);
    set_mode(pi,LEFT_PIN1,PI_OUTPUT);

    set_mode(pi,RIGHT_PWM,PI_OUTPUT);
    set_mode(pi,RIGHT_PIN0,PI_OUTPUT);
    set_mode(pi,RIGHT_PIN1,PI_OUTPUT);

    int fd;

    fd = open( "/dev/input/js0", O_RDONLY );
    if(fd < 0){
        printf ("Can't find USB receiver.\n");
        return 1;
    }

    char ButtonData[BUTTON_DATA_MAX];
    int StickData[STICK_DATA_MAX];

    struct js_event  event;

    while (1){
        read(fd,&event,sizeof(event));
        switch( event.type & ~JS_EVENT_INIT){
            case JS_EVENT_BUTTON:
                if( event.number < BUTTON_DATA_MAX ){
                    ButtonData[event.number] = event.value;
                }
                break;
            case JS_EVENT_AXIS:
                if( event.number < STICK_DATA_MAX ){
                    StickData[event.number] = event.value;
                }
                break;
        }
        cnt++;
        if(cnt > 13){
            //cmdview(ButtonData,StickData);
            controll(ButtonData,StickData,pi);
        }
    }
    close( fd );

    return 0;
}

