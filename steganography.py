from PIL import Image
import numpy as np

def encode_image(image_path, secret_message, output_path):
    """
    Encode a secret message into an image using LSB steganography
    """
   
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = np.array(img)
    

    binary_msg = ''.join([format(ord(c), '08b') for c in secret_message])
    binary_msg += '1111111111111110'  
    

    if len(binary_msg) > pixels.size * 3:
        raise ValueError("Message too large for the image")
    
    msg_index = 0
    for row in pixels:
        for pixel in row:
            for i in range(3):  
                if msg_index < len(binary_msg):
                 
                    pixel[i] = (pixel[i] & 0xFE) | int(binary_msg[msg_index])
                    msg_index += 1
    

    encoded_img = Image.fromarray(pixels)
    encoded_img.save(output_path)
    print(f"Message encoded successfully in {output_path}")

def decode_image(image_path):
    """
    Decode a message hidden in an image using LSB steganography
    """
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = np.array(img)
    
    # Extract LSBs from pixels
    binary_msg = ''
    for row in pixels:
        for pixel in row:
            for i in range(3):
                binary_msg += str(pixel[i] & 1)
  
    message = ''
    for i in range(0, len(binary_msg), 8):
        byte = binary_msg[i:i+8]
        if byte == '11111110':  # Our delimiter
            break
        message += chr(int(byte, 2))
    
    return message


if __name__ == "__main__":
 
    original_image = "original.png"
    encoded_image = "encoded.png"
    secret_msg = "This is a top secret message!"
    
    encode_image(original_image, secret_msg, encoded_image)
    
    # Decode the message
    decoded_msg = decode_image(encoded_image)
    print("Decoded message:", decoded_msg)