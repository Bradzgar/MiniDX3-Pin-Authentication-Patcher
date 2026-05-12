import os


def patch_binary():
    input_filename = "MiniTools.exe"
    output_filename = "MiniTools_Patched.exe"

    # The original 6-byte JLE instruction sequence
    # 0F 8E 90 00 00 00 -> JLE LAB_00406432
    target_signature = b"\x0f\x8e\x90\x00\x00\x00"

    # Inverted JG instruction sequence
    # 0F 8F 90 00 00 00 -> JG LAB_00406432
    patched_sequence = b"\x0f\x8f\x90\x00\x00\x00"

    print("[*] Looking for original MiniTools.exe...")
    if not os.path.exists(input_filename):
        print(f"[!] Error: {input_filename} not found in this folder.")
        print("[-] Please place this script in the same directory as the executable.")
        return

    # Read the original binary data
    with open(input_filename, "rb") as f:
        data = bytearray(f.read())

    # Find the offset of our jump instruction signature
    offset = data.find(target_signature)

    if offset == -1:
        print("[!] Error: Target signature not found!")
        print("[-] The file might already be patched, or it's a different version.")
        return

    print(f"[+] Found target signature at file offset: {hex(offset)}")
    print(
        f"[+] Modifying byte at {hex(offset + 1)}: 0x8E -> 0x8F (Inverting JLE to JG)"
    )

    # Replace the exact sequence
    data[offset : offset + len(target_signature)] = patched_sequence

    # Write the newly patched bytes to the output file
    try:
        with open(output_filename, "wb") as f:
            f.write(data)
        print(f"[++] Success! Patched file saved as: {output_filename}")
        print("[+] You can now run the patched tool and bypass the PIN authentication.")
    except Exception as e:
        print(f"[!] Error writing patched file: {e}")


if __name__ == "__main__":
    patch_binary()
