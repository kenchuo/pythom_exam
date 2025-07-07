#!/usr/bin/env python3
import re
import sys

# ── 將含任意空白的十六進位字串轉成 bytes ────────────────────
def parse_hex_string(s: str) -> bytes:
    hex_pairs = re.findall(r"[0-9A-Fa-f]{2}", s)
    return bytes(int(h, 16) for h in hex_pairs)

# ── CRC‑16 / Modbus (poly 0xA001, init 0xFFFF, RefIn/Out=True) ──
def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if (crc & 1) else crc >> 1
    return crc                    # no xorout

# ── bytes → "AA BB …" 字串 ───────────────────────────────
def bytes_to_hex(b: bytes) -> str:
    return " ".join(f"{x:02X}" for x in b)

def main() -> None:
    # 1) 讀入完整卡號
    print("輸入 16‑byte 卡號 (例: 66 C3 30 00 10 00 00 00 00 00 00 00 00 59 04 05)")
    card_raw = sys.stdin.readline()
    card = bytearray(parse_hex_string(card_raw))
    if len(card) != 16:
        print(f"錯誤：必須 16 byte，實際 {len(card)} byte"); return

    # 2) 讀入新的尾碼
    print("輸入新的尾碼 (3‑byte，例如: 59 04 06)")
    tail_raw = sys.stdin.readline()
    tail = parse_hex_string(tail_raw)
    if len(tail) != 3:
        print(f"錯誤：尾碼必須 3 byte，實際 {len(tail)} byte"); return

    # 3) 覆蓋索引 13‑15
    card[13:16] = tail

    # 4) 計算索引 2‑15 的 CRC
    crc = crc16_modbus(card[2:16])

    # 5) little‑endian 寫回前兩位
    card[0] = crc & 0xFF
    card[1] = (crc >> 8) & 0xFF

    # 6) 輸出結果
    print("\n新卡號：")
    print(bytes_to_hex(card))
    print(f"計算的 CRC = 0x{crc:04X}")

if __name__ == "__main__":
    main()
