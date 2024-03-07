import binascii
from PIL import Image 
import math
def Stego():
    #processing the message
    x = input("Enter the text to hidden: ")
    x = x+"$70p"#Stop character to stop retriving the message
    message = ''.join(format(ord(char), '08b') for char in x)

    #processing the cover image and obtaining the pixel array
    pixels_to_be_used = math.ceil(len(message)/6)
    cover_image_name = input("Enter the name of the cover image: ")
    cover_image = Image.open(cover_image_name)
    cover_image = cover_image.convert("RGB")
    width, height = cover_image.size
    pixel_array = list(cover_image.getdata())
    steg_array = pixel_array[:pixels_to_be_used]

    #Stegnogrphy process
    bin_steg_array = []
    for i in steg_array:
        x = bin(i[0])[2:]
        if len(x) < 8:
            x = ("0"*(8-len(x))) + x
        y = bin(i[1])[2:]
        if len(y) < 8:
            y = ("0"*(8-len(y))) + y
        z = bin(i[2])[2:]
        if len(z) < 8:
            z = ("0"*(8-len(z))) + z
        bin_steg_array.append((x,y,z))

    #converting binary back to intergers
    k = 0
    bin_steg_done_array = []
    for i in bin_steg_array:
        tup = []
        for j in i:
            j = j[:-3] + message[k:k+2] 
            tup.append(j)
            k+=2
        tup = tuple(tup)
        bin_steg_done_array.append(tup)
    for i in bin_steg_done_array:
        tup = []
        for j in i:
            j = int(j, 2)
            tup.append(j)
        bin_steg_done_array[bin_steg_done_array.index(i)] = tuple(tup)

    #updating the stegnography done part to original pixel array
    pixel_array[:pixels_to_be_used] = bin_steg_done_array

    #Creating the stego work
    steg_image = Image.new("RGB", (width, height))
    steg_image.putdata(pixel_array)
    steg_image_name = "stego_"+cover_image_name
    steg_image.save(steg_image_name)
    print("Stego image has been created under the name ", steg_image_name)
#--------------------------------------------------------------------Stego done
def retreival():
    #opening the image
    name = input("Enter the name of the file: ")
    steg_image = Image.open(name)
    steg_image = steg_image.convert("RGB")
    width, height = steg_image.size
    pixel_array = list(steg_image.getdata())
    #retreiving the image
    stop_char = "$70p"
    message = ""
    bin_message = ""
    k=0
    for i in pixel_array:
        message = ""
        x = bin(i[0])[2:][-2:]
        if len(x) == 1:
            x = "0" + x
        y = bin(i[1])[2:][-2:]
        if len(y) == 1:
            y = "0" + y
        z = bin(i[2])[2:][-2:]
        if len(z) == 1:
            z = "0" + z
        bin_message += (x+y+z)
        if len(bin_message)%8 == 0:
            for i in range(0, len(bin_message), 8):
                byte = bin_message[i:i+8]
                message += chr(int(byte, 2)) 
        if stop_char in message:
            break
    print(message.replace("$70p", ""))

print("Welcome to Stegnography")
print("Enter you choice : ")
choice = input("Stego or detect : ").lower()
if choice == "stego":
    Stego()
elif choice == "detect":
    retreival()
else:
    print("please enter a valid choice")












