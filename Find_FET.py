from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
import pickle  # Using pickle for serialization

def FIND_FET(start, wnd, gap_max, binary_data):
    pos = start
    end = start + len(binary_data)
    function_entry_table = []

    while start + pos < end:
        # Determine if the current position corresponds to a Thumb instruction
        is_thumb = check_if_thumb_instruction(binary_data, pos)

        function_entries = find_function_entries_in_window(binary_data, pos, wnd, is_thumb)
        for gap in range(gap_max + 1):
            if match_rule1(function_entries, pos) and match_rule2(function_entries) and match_rule3(pos):
                head = pos
                table_size = wnd
                pos = MoveWindow(pos, table_size, is_thumb)

                while match_rule1(function_entries, pos) and match_rule2(function_entries) and match_rule3(pos):
                    table_size += 1
                    pos = MoveWindow(pos, table_size, is_thumb)

                pos += table_size
                print_output(head, gap, table_size, function_entries)
                function_entry_table.extend(function_entries)
                break

        pos += 1
    return function_entry_table

def find_function_entries_in_window(binary_data, start, window_size, is_thumb):
    disasm = Cs(CS_ARCH_ARM, CS_MODE_THUMB if is_thumb else CS_MODE_ARM)
    function_entries = []

    end_position = start + window_size

    for insn in disasm.disasm(binary_data, start):
        address = insn.address

        # Check if the address is within the specified window size
        if start <= address < end_position:
            function_entries.append(address)

    return function_entries

# def find_function_entries_in_window(binary_data, start, window_size):
#     disasm_arm = Cs(CS_ARCH_ARM, CS_MODE_ARM)
#     disasm_thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
#
#     function_entries = []
#     end_position = start + window_size
#
#     for insn in disasm_arm.disasm(binary_data, start):
#         if match_rule3(insn.address):
#             # Check if the address is within the specified window size
#             if start <= insn.address < end_position:
#                 function_entries.append(insn.address)
#             # function_entries.append(insn.address)
#
#
#     for insn in disasm_thumb.disasm(binary_data, start):
#         if match_rule3(insn.address):
#             # function_entries.append(insn.address)
#             # Check if the address is within the specified window size
#             if start <= insn.address < end_position:
#                 function_entries.append(insn.addre# fileSize = 1000  # Size of the filess)
#
#     return function_entries

def match_rule1(function_entries, pos):
    # Rule 1: Check distance between each two function entry addresses in the window not more than 64KB
    window_size = 64 * 1024
    for i in range(len(function_entries)):
        for j in range(i + 1, len(function_entries)):
            if abs(function_entries[i] - function_entries[j]) > window_size:
                return False
    return True

def match_rule2(function_entries):
    # Rule 2: Check that function entry addresses within the sliding window are not the same
    return len(set(function_entries)) == len(function_entries)

def match_rule3(address):
    # Rule 3: Check ARM/Thumb entry address rules
    return (address % 4 == 0) or (address % 2 == 1)

def check_if_thumb_instruction(binary_data, pos):
    # Implement logic to check if the instruction at the given position is a Thumb instruction
    # Thumb-2 instructions have a specific format in the most significant half-word
    thumb2_signature = b'\xe0\x00'

    # Check if the instruction at the given position matches the Thumb-2 signature
    if binary_data[pos:pos + 2] == thumb2_signature:
        return True
    else:
        return False

def MoveWindow(pos, table_size, is_thumb):
    # Move the window by updating the position with a fixed offset
    # You might need to customize this based on your firmware's structure
    # return pos + table_size  # Replace 1 with the appropriate offset or logic
    # Move the window by updating the position based on ARM or Thumb instruction size
    instruction_size = 2 if is_thumb else 4
    # return pos + instruction_size  #if we use instruction_size, then FET-FIND stucks in While loop.
    # return pos + (table_size * instruction_size)
    return pos + table_size

def print_output(head, gap, table_size, functions):
    # Implement the logic for outputting the result
    print(f"Head: {head}, Gap: {gap}, Table Size: {table_size}, function_entries: {functions}")

# def find_function_entry_point(binary_data):
#     disasm = Cs(CS_ARCH_X86, CS_MODE_32)
#     potential_entry_points = []
#
#     for address, _, _, _ in disasm.disasm(binary_data, 0x1000):
#         potential_entry_points.append(address)
#
#     return potential_entry_points

def find_first_function_entry(binary_data):
    disasm = Cs(CS_ARCH_X86, CS_MODE_32)
    potential_entry_points = []

    # for address, _, _, _ in disasm.disasm(binary_data, 0x1000):
    for insn in disasm.disasm(binary_data, 0x1000):
        potential_entry_points.append(insn.address)

    if potential_entry_points:
        return min(potential_entry_points)
    else:
        return None
def read_binary_file(file_path):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data


def FIND_BASE(binary_file, function_entry_table, T):
    bin_file_size = len(binary_file)
    entry = sorted(set(function_entry_table))  # Deduplicate and sort function entry addresses

    for x in range(entry[-1] - bin_file_size, entry[0] + 1):
        ThumbCount = 0
        ArmCount = 0

        for j in range(len(entry)-1):
            if entry[j] % 2 == 1:
                if binary_file[entry[j] - x] == 0xB5:
                    ThumbCount += 1
            else:
                if (
                    binary_file[entry[j] - x + 2] == 0x2D
                    and binary_file[entry[j] - x + 3] == 0xE9
                ):
                    ArmCount += 1
        print(x, ThumbCount, ArmCount)
        if ((ThumbCount + ArmCount) / len(entry)) > T:
            print(x)
            return x  # Output: x

    return None  # No suitable base address found

def save_function_entry_table(function_entry_table, filename):
    with open(filename, 'wb') as file:
        pickle.dump(function_entry_table, file)

def load_function_entry_table(filename):
    with open(filename, 'rb') as file:
        function_entry_table = pickle.load(file)
    return function_entry_table

def main():
    binary_file_path = '/home/narges/Desktop/AlmostSuccessfuleFW/ARMarchitecture/EX6150v2_EX6100v2-V1.0.1.108.zip'
    # binary_file_path = '/home/narges/Downloads/iAUDIO_E2_1.13.zip'
    # binary_file_path = '/home/narges/Downloads/shortList/1719-DIR822A1_FW103WWb03.bin'
    binary_data = read_binary_file(binary_file_path)

    # Specify the starting point (initial function entry address)
    # start_address = 0x1000  # Replace with your actual starting address
    # potential_entry_points = find_function_entry_point(binary_data)

    # if potential_entry_points:
    #     print(f"Potential function entry points:")
    #     for entry_point in potential_entry_points:
    #         print(hex(entry_point))
    # else:
    #     print("No potential function entry points found.")

    first_function_entry = find_first_function_entry(binary_data)

    if first_function_entry is not None:
        print("Actual starting address of the first function entry point:")
        print("0x%X" % first_function_entry)
    else:
        print("No function entry points found.")

    window_size = 5
    max_gap = 3

    function_entry_table= FIND_FET(first_function_entry, window_size, max_gap, binary_data)
    # save_function_entry_table(function_entry_table, 'function_entry_table.pkl')
    print(len(function_entry_table))

    # function_entry_table = load_function_entry_table('function_entry_table.pkl')
    # Use the output of FIND_FET in FIND_BASE
    T_value = 0.4  # In this experiment, the parameter T is set to 40% (according to the paper)
    base_address = FIND_BASE(binary_data, function_entry_table, T_value)

if __name__ == "__main__":
    main()