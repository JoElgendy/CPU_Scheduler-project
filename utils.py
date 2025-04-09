import hashlib

def generate_color(input_number):
    # Convert the input number to a string
    input_str = str(input_number)

    # Hash the string to get a consistent value
    hash_value = hashlib.md5(input_str.encode()).hexdigest()

    # Use the first 6 characters of the hash as a color code
    color = f"#{hash_value[:6]}"  # Taking first 6 characters for RGB Hex code
    
    return color