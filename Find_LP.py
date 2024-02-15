#1st identify the strings of ﬁrmwares in the test set.
# 2nd, the FIND-LP algorithm is performed to recognize possible literal pools in the ﬁrmware.

import binascii
import os
import math

def is_printable(char):
    # Check if a character is printable
    # Strings in binary data are often represented as sequences of printable characters.
    # By filtering out non-printable characters, we ensure that we only consider sequences that are likely to be strings.
    return char >= 32 and char <= 126

def extract_strings_from_binary_2(file_path, min_length=4):
    strings = []
    with open(file_path, 'rb') as f:
        byte_string = f.read()
        current_string = ""
        for byte in byte_string:
            if is_printable(byte):
                current_string += chr(byte)
            else:
                if len(current_string) >= min_length:
                    strings.append(current_string)
                current_string = ""
        # Add the last string if it meets the minimum length
        if len(current_string) >= min_length:
            strings.append(current_string)
    return strings
def extract_strings_from_binary(binary_data):
    strings = []
    # with open(file_path, 'rb') as f:
    #     byte_string = f.read()
    current_string = ""
    for byte in binary_data:
        # while byte != b'\x00':  # Null terminator marks end of string
        if is_printable(byte):
            current_string += chr(byte)
        elif byte == 0:  # Null terminator marks end of string
            if current_string:  # Ensure we have accumulated characters
                strings.append(current_string)
                current_string = ""
        # else:
            # if current_string:  # If we were accumulating characters before
            # # Add the accumulated characters to strings before processing the current byte
            #     strings.append(current_string)
            # If the character is not printable and not null, it's not part of a string
            # current_string = ""
    return strings


def FINDLP(string_addresses, start, binary_data, wndsize):
    pos = start
    end = start + len(string_addresses)
    pool_number = 0
    pool_addresses_list = []
    while start <= pos < end:
        addresses = string_addresses[pos:min(pos + wndsize, end)]
        if match_rule1(addresses) and match_rule2(addresses):
            head = pos
            poolSize = wndsize
            pool_addresses= addresses
            pos = MoveWindow(pos, wndsize)
            addresses = string_addresses[pos:min(pos + wndsize, end)]

            while match_rule1(addresses) and match_rule2(addresses) and match_rule3(pool_addresses):
                pool_addresses.extend(addresses)
                poolSize += wndsize
                pos= MoveWindow(pos, wndsize)
                addresses = string_addresses[pos:min(pos + wndsize, end)]

            # it reaches here only if rule 3 doesn't match, so it means the
            # last list of addresses added to the pool_addresses doesn't follow the rule,
            # so we need to skip the values in this window
            del pool_addresses[poolSize - wndsize: poolSize]
            if len(pool_addresses) > 0:
                pool_addresses_list.append(pool_addresses)
                pool_number += 1
                # print("Output:head, poolsize, number of pools", head, len(pool_addresses), pool_number)

        pos+=1
    return pool_addresses_list

def list_string_addresses(start, end):
# Function to list string addresses within the sliding window
    addresses = []
    # Implement logic to identify string addresses within the window
    # Here, we assume some logic to determine string addresses, replace it with actual logic
    for addr in range(start, end):
        if is_string_address(addr):  # Define is_string_address based on your criteria
            addresses.append(addr)
    return addresses
def is_string_address(addr, file_path):
    with open(file_path, 'rb') as f:
        f.seek(addr)  # Move file pointer to the address
        string = ""
        char = f.read(1)
        while char != b'\x00':  # Null terminator marks end of string
            if is_printable(char[0]):  # Check if character is printable
                string += char.decode('utf-8')  # Convert byte to character
            else:
                # If the character is not printable, it's not a valid string
                return False
            char = f.read(1)
        return True  # If null terminator is found, it's a valid string address


def match_rule1(string_addresses):
    # Check if the distance between string addresses is no more than 64 KB
    try:
        # return max(string_addresses) - min(string_addresses) <= 64 * 1024
        for i in range(len(string_addresses) - 1):
            current_address = int(string_addresses[i], 16)  # Convert hexadecimal address to integer
            next_address = int(string_addresses[i + 1], 16)  # Convert hexadecimal address to integer
            if next_address - current_address > 64 * 1024:
                return False
        return True
    except:
        print('empty string')
        return False

def match_rule2(addresses):
    # Check if the string addresses in the same sliding window are unique
    return len(set(addresses)) == len(addresses)

def match_rule3(addresses):
    # Check if the difference value between adjacent string addresses after sorting is less than 100
    sorted_addresses = sorted(addresses)
    for i in range(1, len(sorted_addresses)):
        if int(sorted_addresses[i],16) - int(sorted_addresses[i - 1],16) >= 100:
            return False
    return True

def MoveWindow(pos, wndsize):
    # Function to move the sliding window
    return pos + wndsize

def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

def get_file_size(file_path):
    # Get the size of the file in bytes
    file_size = os.path.getsize(file_path)
    return file_size

def find_string_and_addresses(binary_data):
    string_addresses = []
    current_address = 0x0
    current_offset = 0x0
    strings_values = []
    string_length_vector = []
    offset_vector = []
    # Iterate through the binary data
    while current_address < len(binary_data):
        string_start = current_address
        string_length = 0
        current_string = ""

        # Search for the end of the current string
        while current_address < len(binary_data) and binary_data[current_address] != 0:
            byte = binary_data[current_address]
            if is_printable(byte):
                current_string += chr(byte)
            string_length += 1
            current_address += 1
        # If a string is found, add its address and offset to the respective lists
        if string_length > 0 and current_string != '':
            string_addresses.append(hex(string_start))
            strings_values.append(current_string)
            string_length_vector.append(len(current_string))
            offset_vector.append(hex(current_offset))

        # Move to the next byte after the null terminator
        current_address += 1
        current_offset += 1  # Increment offset

        # # Update the offset after encountering a null terminator
        # current_offset += string_length + 1  # Add 1 for the null terminator
        #
        # # Move to the next byte after the null terminator
        # current_address += 1
        #
        # # Skip any padding bytes until the next string to ensure that the offsets
        # # reflect the cumulative byte positions within the binary data
        # while current_address < len(binary_data) and binary_data[current_address] == 0:
        #     current_address += 1
        #
        # # Update the offset to account for any padding bytes
        # current_offset += current_address - string_start

    return strings_values, string_addresses, string_length_vector, offset_vector

def extract_strings_and_addresses(binary_data):
    strings = []
    addresses = []
    current_address = 0
    current_string = ""

    # Iterate through the binary data
    while current_address < len(binary_data):
        byte = binary_data[current_address]

        if is_printable(byte):
            current_string += chr(byte)
        elif byte == 0:  # Null terminator marks end of string
            if current_string:  # Ensure we have accumulated characters
                strings.append(current_string)
                addresses.append(current_address - len(current_string))
                current_string = ""
        # else:
        #     # If the character is not printable and not null, it's not part of a string
        #     current_string = ""

        current_address += 1

    return strings, addresses

def word_aligned(length):
    """
    Aligns the length of a string to the closest multiple of 4.

    Parameters:
        length (int): The original length of the string.

    Returns:
        int: The aligned length.
    """
    # Check if the length is already a multiple of 4
    if length % 4 == 0:
        return length
    else:
        # Calculate the next multiple of 4 greater than the original length
        aligned_length = ((length // 4) + 1) * 4
        return aligned_length

def euclidean_distance(vector1, vector2):
    """
    Calculates the Euclidean distance between two vectors.

    Parameters:
        vector1 (list): The first vector.
        vector2 (list): The second vector.

    Returns:
        float: The Euclidean distance between the two vectors.
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same length")

    squared_diffs = [(x - y) ** 2 for x, y in zip(vector1, vector2)]
    sum_squared_diffs = sum(squared_diffs)
    distance = math.sqrt(sum_squared_diffs)
    return distance

def determine_image_base(pool_addresses_list, length_vector, offset_vector, string_addresses):
    m= len(length_vector)
    n = 0
    potential_bases = []
    # find the word-aligned string length vector
    aligned_length = []
    for k_i in length_vector:
        aligned_length.append(word_aligned(k_i))

    for LP in pool_addresses_list:
        # Sort the pool
        LP.sort()

        n= len(LP)
        aligned_list = []
        for sa_i in LP:
            if int(sa_i,16) % 4 != 0:
                aligned_list.append(False)
                aligned = False
                break
            else:
                aligned_list.append(True)
                aligned = True

        V_LP = []
        # Iterate over the string addresses to calculate string lengths
        for i in range(len(LP) - 1):  # Stop at the second-to-last address
            length = int(LP[i + 1],16) - int(LP[i],16)  # Calculate length between consecutive addresses
            V_LP.append(length)
# create SV_i
        SV = []
        for i in range(0 , m-n+2):
            if aligned == False:
                SV.append(length_vector[i:n+i-1])
            else:
                SV.append(aligned_length[i:n + i - 1])
            distance = euclidean_distance(V_LP, SV[i])
            if distance == 0:
                base = hex(int(string_addresses[i],16) - int(offset_vector[i], 16))
                print("it matches successfully ", i, V_LP, SV[i], string_addresses[i], offset_vector[i], base)
                potential_bases.append(string_addresses[i])

    return potential_bases

def main():
    # binary_file_path = '/home/narges/Downloads/SamsungGearFit/1.50.0415/wingtip_ex.bin'
    binary_file_path = '/home/narges/Downloads/Pebble-2.9/tintin_fw.bin'
    # binary_file_path = '/home/narges/Downloads/Modx_outputs/am335x-pm-firmware.elf'
# Read the binary file.
    binary_data = read_binary_file(binary_file_path)

    print("File size:",len(binary_data),"bytes")
    # print("File size:", get_file_size(binary_file_path), "bytes")
# 1st identify the strings of firmwares and their addresses in the binary file.

    # strings = extract_strings_from_binary(binary_data)
    # Here, the strings value, their addreses and their lengths are extracted
    strings, string_addresses, string_length_vector, offset_vector = find_string_and_addresses(binary_data)

    # for string in strings:
    #     print(string)
    print("Number of strings:", len(strings))
    # print("Number of String Addresses:", len(string_addresses))

 # 2nd, Find LP
    start = 0x1000  # Start position
    wndsize = 3  # Size of the sliding window
    pool_addresses_list = FINDLP(string_addresses, start, binary_data, wndsize)
    print("Number of literal pools: ",len(pool_addresses_list))

# 3rd, find lenght_vector and offset_vector of all strings

# 4th, determine the image base
    image_bases = determine_image_base(pool_addresses_list, string_length_vector, offset_vector, string_addresses)
    print(len(image_bases))
    print("image_bases:", len(set(image_bases)))
