import cv2 # for accessing image
import numpy as np  # image to array conversion
import string 
import os 
import matplotlib.pyplot as plt
import time

# Encryption
def xor_encrypt(message,key):
    # For generating corresponding ascii values of all the characters in the message and key with the duplicates
    # Here ord() is a built-in function which maps the character to its corresponding ascii value
    message_ascii = [ ord(char) for char in message ] # Stores the ascii values of each and every characters in message in the list
    key_ascii = [ ord(char) for char in key ] # stores the ascii values of each and every characters in key in the list 
    encrypted_ascii = []
    # for loop runs till the last character and encrypts the character one by one 
    for i in range(len(message_ascii)):
        encrypted_char = message_ascii[i] ^ key_ascii[i % len(key_ascii)] # Ex: message_ascii[0]^key_asccii[0 % len(key_ascii)] = 65 ^ key_ascii[0 % 3] = 65 ^ 49 = 112
        encrypted_ascii.append(encrypted_char)
    # Convert encrypted ASCII values back to characters
    encrypted_message = ''.join(chr(val) for val in encrypted_ascii)
    return encrypted_message


# Convert Encrypted message into binary ( 0s and 1s)
def binary_string(encrypted_message):
    binary_format = ""  # Initialize empty string to hold binary data
    # Loop through each character in the encrypted message
    for char in encrypted_message:
        ascii_value = ord(char)  # Convert char to ASCII (integer)
        binary_char = format(ascii_value, '08b') # Convert ASCII to 8-bit binary string
        binary_format += binary_char # Add binary to the full message  
    return binary_format


# Embedding the binary format into the image's LSB
def embed_message_in_image(image, binary_format):
    flat_image = image.flatten() # Flattening the image from 3d to 1d because working with 1d is easier than 3d
    if len( binary_format ) > len ( flat_image ):
        print("Length of the message is large, Please Choose Another Image")
        exit(1)
    # Loop through every bit of the binary message and change the LSB of each pixel in the image
    for i in range(len(binary_format)): # Loops through each bit of the binary message
        original_pixel = flat_image[i]  # Extract the ith pixel of the image
        original_binary = format(original_pixel,'08b')  # Convert the extracted image's pixel value to binary format
        new_binary = original_binary[:-1] + binary_format[i] # Delete the last bit of the image pixel's last bit and concatenate the ith bit of the binary message
        new_pixel = int(new_binary,2) # Convert binary format back into integer value, here 2 indicates that it is binary value ( 10: Decimal, 16: Hexadecimal)
        flat_image[i] = new_pixel # Change the new pixel value with old pixel value
    stego_image = flat_image.reshape(image.shape) # Reshape the whole image once all the iterations are done
    
    return stego_image

# Verifying whether the Binary format of the message is embedded into the image
def verify(stego_image,binary_format):
    flat_stego_image = stego_image.flatten()
    extracted_bit = ""
    for i in range(len(binary_format)):
        formating = format(flat_stego_image[i],'08b') # formatting the extracted pixel
        lsb = formating[-1] # accessing last bit from every formatted pixel
        extracted_bit += lsb # append it to the extracted_bit string
    
    if extracted_bit == binary_format:
        print("Message Embedding Successful")
        image_rgb = cv2.cvtColor(stego_image, cv2.COLOR_BGR2RGB) # Converting BGR color channel to RGB color channel
        plt.imshow(image_rgb)
        plt.title("Stego Image")
        plt.axis('off')  # Hide axis ticks
        plt.show()
        return True
    else:
        print("Message Embedding Unsuccessful")
        return False

# Extract the message which is in decimal value format from each pixel 
def extract_message():
    stego_image_path = input("Enter the path of the Stego Image: ")
    stego_image = cv2.imread(stego_image_path)
    if stego_image is None:
        print("Invalid path or stego Image not Found")
        exit(1)
    else:
        h,w,c = stego_image.shape
        print(f"Image Found - Height: {h}, Width: {w}, Channel:{c}")

    flat_image = stego_image.flatten()
    extracted_bits = ""
    for i in range(len(flat_image)):
        formatting = format(flat_image[i],'08b')
        lsb = formatting[-1] # access only the last bit from the binary fomat 
        extracted_bits += lsb
    return extracted_bits # So here I get the Binary format of the Cipher Text

# Convert the Binary format to Cipher text
def binary_Cipher(extracted_bits):
    cipher_text = ""
    for i in range (0,len(extracted_bits),8): # range(start,end,step) , here for next iteration i value is incremented by the value of step instead of incrementing by 1
        byte = extracted_bits[i:i+8]
        if len(byte) < 8:
            continue
        int_value = int(byte,2) # integer value of 8 bit binary value
        text = chr(int_value)
        cipher_text += text
    return cipher_text # So here we get Cipher Text

# Now decrypt the message using key and cipher text
def xor_decrypt(key,cipher_text):
    decrypted = ""
    for i in range (len(cipher_text)):
        ascii_ct = ord(cipher_text[i])
        ascii_key = ord(key[i % len(key)])
        original_message = chr(ascii_ct ^ ascii_key)
        if original_message == "~":
            break
        decrypted += original_message
    return decrypted


def main():
    choice = input("If You want to Encrypt enter 'E' or If you want to Decrypt enter 'D':   ").strip().upper()
    if choice == "E":
        original_message = input("Enter the Message: ") 
        message = "Prefix:" + original_message + "~"
        key = input("Enter the Key : ")
        encrypted_message = xor_encrypt(message,key)
        binary_format = binary_string(encrypted_message)
         # Load the cover image
        image_path = input("Enter the Cover Image Path: ")
        image = cv2.imread(image_path)
        if image is None:
            print("Image Not Found")
            exit(1)
        else:
            h,w,c = image.shape
            print(f"Image Found - Height: {h}, Width: {w}, Channel:{c}")
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Converting BGR color channel to RGB color channel
            plt.imshow(image_rgb)
            plt.title("Cover Image")
            plt.axis('off')  # Hide axis ticks
            plt.show()
        stego_image = embed_message_in_image(image,binary_format)
        verification = verify(stego_image,binary_format)
        

        # Save the image
        
        file_name = input("Enter the Output File Name: ")
        output_path = fr"C:\Users\aksha\Desktop\Steganography\Stego_image\{file_name}.png"
        if verification:
            success = cv2.imwrite(output_path,stego_image)
            if success:
                print("Stego Image saved to", output_path)
            else:
                print("Image Not Saved")
        else:
            print("Image not saved (Error occured during verification)")

    elif choice == "D":
        extracted_bits = extract_message()
        decryption_key = input("Enter the key for Decryption: ")
        time.sleep(2)
        cipher_text = binary_Cipher(extracted_bits)
        decrypted = xor_decrypt(decryption_key,cipher_text)
        if decrypted.startswith("Prefix:"):
            print("Key Verified")
            print("Decryption in Progress....")
            time.sleep(5)
            prefix_end = decrypted.find(":") + 1
            actual_message = decrypted[prefix_end:].rstrip("~")
            print("Secret Message: ", actual_message)
        else:
            print("Incorrect Key. Decryption Failed.")
    
    else:
        print("Invalid Choice ! Please enter 'E' or 'D'.")

if __name__ == "__main__":
    main()
