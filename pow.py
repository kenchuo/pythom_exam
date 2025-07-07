def crc16(data: bytes, poly: int, init: int, refin: bool, refout: bool, xorout: int):
    """通用CRC-16計算函數"""
    crc = init
    for byte in data:
        if refin:
            byte = int('{:08b}'.format(byte)[::-1], 2)
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc <<= 1
            crc &= 0xFFFF
    if refout:
        crc = int('{:016b}'.format(crc)[::-1], 2)
    crc ^= xorout
    return crc & 0xFFFF

def crc16_modbus(data: bytes):
    return crc16(data, poly=0x8005, init=0xFFFF, refin=True, refout=True, xorout=0x0000)

def crc16_ccitt(data: bytes):
    return crc16(data, poly=0x1021, init=0xFFFF, refin=False, refout=False, xorout=0x0000)

def crc16_xmodem(data: bytes):
    return crc16(data, poly=0x1021, init=0x0000, refin=False, refout=False, xorout=0x0000)

def crc16_kermit(data: bytes):
    return crc16(data, poly=0x1021, init=0x0000, refin=True, refout=True, xorout=0x0000)

def crc16_yp205_variant1(data: bytes):
    """嘗試匹配YP205讀卡機的變體1"""
    return crc16(data, poly=0x1021, init=0x366C, refin=False, refout=False, xorout=0x0000)

def crc16_yp205_variant2(data: bytes):
    """嘗試匹配YP205讀卡機的變體2"""
    return crc16(data, poly=0x8005, init=0x0000, refin=True, refout=True, xorout=0x0000)

def crc16_yp205_variant3(data: bytes):
    """嘗試匹配YP205讀卡機的變體3 (初始值0xFFFF, 結果不反轉)"""
    return crc16(data, poly=0x8005, init=0xFFFF, refin=False, refout=False, xorout=0x0000)

def input_bytes():
    while True:
        try:
            input_str = input("請輸入14個位元組的十六進制數據（例如: 01 02 03 ... 0E），用空格分隔: ")
            byte_list = [int(b, 16) for b in input_str.split()]
            
            if len(byte_list) != 14:
                print("錯誤：必須輸入正好14個位元組！")
                continue
                
            if any(b < 0 or b > 255 for b in byte_list):
                print("錯誤：每個位元組必須在00到FF之間！")
                continue
                
            return bytes(byte_list)
            
        except ValueError:
            print("錯誤：請輸入有效的十六進制數值（00-FF）！")

def format_crc_result(name: str, crc: int):
    return (
        f"{name:20}: 0x{crc:04X} | "
        f"高位: 0x{(crc >> 8):02X} 低位: 0x{crc & 0xFF:02X} | "
        f"傳輸順序: 0x{crc & 0xFF:02X} 0x{(crc >> 8):02X}"
    )

def main():
    print("YP205讀卡機CRC計算器 (增強版)")
    print("請輸入14個位元組的數據：")
    
    data = input_bytes()
    
    print("\n輸入數據：")
    print(' '.join(f"{b:02X}" for b in data))
    
    print("\n計算結果：")
    print(format_crc_result("CRC-16 Modbus", crc16_modbus(data)))
    print(format_crc_result("CRC-16 CCITT", crc16_ccitt(data)))
    print(format_crc_result("CRC-16 XMODEM", crc16_xmodem(data)))
    print(format_crc_result("CRC-16 Kermit", crc16_kermit(data)))
    print("\nYP205專用變體：")
    print(format_crc_result("YP205 Variant 1", crc16_yp205_variant1(data)))
    print(format_crc_result("YP205 Variant 2", crc16_yp205_variant2(data)))
    print(format_crc_result("YP205 Variant 3", crc16_yp205_variant3(data)))

if __name__ == "__main__":
    main()