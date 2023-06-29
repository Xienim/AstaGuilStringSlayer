def string_to_hex(string):
    hex_string = ""
    for char in string:
        hex_value = hex(ord(char))[2:]
        hex_string += hex_value.zfill(2)
    return hex_string


def decrypter(var1, var2):
    result = ""
    result1 = ""
    result2 = ""
    stream = ""
    skiper5 = True
    var2_index = 0
    prev_hex_var1 = None

    for i in range(0, len(var1), 2):
        if skiper5:
            skiper5 = False
            prev_hex_var1 = var1[i:i+2]
        else:
            hex_var1 = var1[i:i+2]
            hex_var2 = hex(ord(var2[var2_index % len(var2)]))
            var2_index += 1
            xor_result = hex(int(hex_var1, 16) ^ int(hex_var2, 16))

            if int(xor_result, 16) <= int(prev_hex_var1, 16):
                if int(xor_result, 16) > int(prev_hex_var1, 16):
                    pass
                else:
                    xor_result = hex(int(xor_result, 16) + 0xFF)[2:]
                    xor_result = hex(int(xor_result, 16) - int(prev_hex_var1, 16))[2:]
                    result += xor_result
            else:
                sub_result = hex(int(xor_result, 16) - int(prev_hex_var1, 16))
                result += sub_result[2:]

            prev_hex_var1 = hex_var1
    result = result[::-1]
    result = ''.join([result[i:i+2][::-1] for i in range(0, len(result), 2)])
    
    for x in range(0, len(result), 2):
        hex_result1 = result[x:x+2]
        result1 += hex((int(hex_result1,16) - 0x0A) ^ 0xFF )[2:]
    
    prev_hex_var2 = None
    skiper3 = True
    for c in range(0, len(result1), 2):
        if skiper3:
            skiper3 = False
            prev_hex_var2 = hex(int(result1[c:c+2], 16) - 0x41)[2:]
            skiper = 0      
        else:
            if skiper == 0:
                hex_var3 = result1[c:c+2] 
                local1 = hex(int(hex_var3, 16) - 0x41)
                local2 = hex(int(local1, 16) * 0x4 )
                local3 = hex(int(local2, 16) + int(local1, 16) )
                local4 = hex(int(local3, 16) * 0x4 )
                local13 = hex(int(local4, 16) + int(local3, 16) )
                skiper = 1
            else:
                local5 = result1[c:c+2]
                local6 = hex(int(local5, 16) - 0x41)
                local7 = hex(int(local6, 16) + int(local13, 16))
                local8 = hex(int(local7, 16) - int(prev_hex_var2, 16))
                stream += hex(int(local8,16) - 0x64)
                skiper = 0
                
    return stream


def Get_Values_From_File(filename, key):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        value_enc = line.strip()
        result = decrypter(value_enc, key)
        result = result.replace("0x", "")
        result = result.replace("x", "")
        result_chars = ''.join([chr(int(result[i:i+2], 16)) for i in range(0, len(result), 2)])
        print("{} ---> {}".format(result_chars,value_enc))
        
        
    
# Modify Here
filename = "filename.txt"
key = "KEY_HERE"
Get_Values_From_File(filename, key)
