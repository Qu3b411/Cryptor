#!/bin/bash

printf '\x02' | dd conv=notrunc of=./foo bs=1 seek=5
