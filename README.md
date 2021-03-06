# LSB-investigation [![python](https://img.shields.io/badge/Python-2.7-green.svg?style=style=flat-square)](https://www.python.org/downloads/) [![version](https://img.shields.io/badge/Version-Beta-blue.svg?style=style=flat-square)](https://twitter.com/133_cesium) [![license](https://img.shields.io/badge/License-GPL_3-orange.svg?style=style=flat-square)](https://github.com/C3s1um133/LSB-investigation/blob/master/LICENSE)

Version 2.7 of an old script I made for building steganography challenges.

### Main libraries :
#### hackercodecs -> https://github.com/jdukes/hackercodecs

Careful : It does not uses the 'pip install hackercodecs' yet.
Try to run the script for the first time, eventually it will handle the download process itself.
Either way : You need to download the full package (linked above) in order to fully take advantage of the creation process.

#### Installing project and dependencies : PIL

```
pip install Pillow
wget -q https://raw.githubusercontent.com/C3s1um133/LSB-investigation/master/hackercodecs.py
wget -q https://raw.githubusercontent.com/C3s1um133/LSB-investigation/master/Diagnostic_LSB.py
chmod +x Diagnostic_LSB.py
```

### Usage:

The script handles several of technics for hiding and retrieving hidden messages in a picture.
- The list will be describe in the Creation module below -
Help:

```
./Diagnostc_LSB.py -h
```

#### Investigation / grabing the LSBs

For printing all the referenced modes of LSB technics found in the parsed picture.

```
./Diagnostic_LSB.py --extract img.png 
```

#### Creation of "steganographied" picture

Technics of insertion of messages in the RGBs of pixels :
##### One bit diagonal :

```
[-idr|--insert-diag-red] Diagonal, only for RED 

[-idg|--insert-diag-green] Diagonal, only for GREEN 

[-idb|--insert-diag-blue] Diagonal, only for BLUE

[-ida|--insert-diag-rgb] Diagonal, for all RGB 
```

##### One bit inlines from top-left-hand corner :

```
[-ir|--insert-red] First 3 lines, only for RED 

[-ig|--insert-green] First 3 lines, only for GREEN 

[-ib|--insert-blue] First 3 lines, only for BLUE 

[-ia|--insert-rgb] First 3 lines, for all RGB 
```

##### Two bits inlines from top-left-hand corner :

```
[-ir2|--insert-2-bits-red] First 3 lines, 2 LSB, only for RED

[-ig2|--insert-2-bits-green] First 3 lines, 2 LSB, only for GREEN

[-ib2|--insert-2-bits-blue] First 3 lines, 2 LSB, only for BLUE
```

##### Three bits inlines from top-left-hand corner :

```
[-ir3|--insert-3-bits-red] First 3 lines, 3 LSB, only for RED 

[-ig3|--insert-3-bits-green] First 3 lines, 3 LSB, only for GREEN 

[-ib3|--insert-3-bits-blue] First 3 lines, 3 LSB, only for BLUE

[-ia3|--insert-3-bits-rgb] First 3 lines, 3 LSB, for all RGB 
```

##### One bit out of Two pixels inlines from top-left-hand corner :

```
[-i2r|--insert-pair-red] 1 out of 2 pixels [even ones], only for RED

[-i2g|--insert-pair-green] 1 out of 2 pixels, only for GREEN 

[-i2b|--insert-pair-blue] 1 out of 2 pixels, only for BLUE

[-i2a|--insert-pair-rgb] 1 out of 2 pixels, for all RGB
```

#### Creation with Encoding utils

The script allows you to encode the message to hide into those formats:

```
ascii85, base16, base32, base64, bin, entity, entityhex, morse, rot1, rot10, rot11, rot12, rot13, rot14, rot15, rot16, rot17, rot18, rot19, rot2, rot20, rot21, rot22, rot23, rot24, rot25, rot3, rot4, rot5, rot6, rot7, rot8, rot9, url, yenc
```

### Try it
Exemple with the 3 leasts significant bits of RED color insertion mode of a message encoded in base64 :

```
./Diagnostic_LSB.py -ir3 PNG_transparency_demonstration_1.png -enc "base64" "My_credit_card_PIN_:_1290468493102384659182"
43
TXlfY3JlZGl0X2NhcmRfUElOXzpfMTI5MDQ2ODQ5MzEwMjM4NDY1OTE4Mg==

[+] MSG successfully hidden in IMG_5bXBXshBPAP386fRxg.png
```

Then we gather information from the newly created picture:

```
./Diagnostic_LSB.py -e IMG_5bXBXshBPAP386fRxg.png
```

### UGLY AND DOESN'T WORK FROM ONE PICTURE TO ANOTHER, GONNA REMAKE IT SOON
