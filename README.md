Project Description:
  A Python project that hides secret messages inside image files using Least Significant Bit (LSB) manipulation and XOR encryption. It ensures basic confidentiality and secure message transfer without visibly altering the image.

Features:
  XOR-based encryption and decryption
  LSB embedding of binary message in image pixels
  Verification of embedded message
  Key authentication during decryption
  Image preview using Matplotlib
  Saves the stego image after successful encoding

Technologies Used:
  Python 3.2
  OpenCV
  NumPy
  Matplotlib
  Standard Python libraries: time, os, string

How to Run:
  Prerequisites:
      pip install opencv-python numpy matplotlib
  To Run the Program:
      python stego.py

Steps:

Choose whether to Encrypt or Decrypt
For encryption:
  Enter the message and key
  Provide the cover image path
  Get the stego image as output

For decryption:
  Provide the stego image path
  Enter the decryption key
  View the original message if the key is correct

Folder Structure:
  .
  ├── stego.py                 
  ├── cover_image           
  └── Stego_image/             
