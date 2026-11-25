# Capstone — Make the Computer Draw a Box

**Jai Kuntal | Roll No. 2501730416 | K = 16**

| Item | Value |
|---|---|
| K mod 3 | 1 — symbols.txt extra feature not required |
| K mod 4 | 0 — width = 16 pixels (1 word per row) |
| Start row | 16 (rows 16–35), height 20 |
| First screen address | 16384 + 32 × 16 = 16896 |

Files: `CPU.hdl`, `Memory.hdl`, `Computer.hdl`, `assembler.py`, `Box.asm`, `Box.hack`, and `tests/`.

Run `python assembler.py Box.asm` to generate `Box.hack`. Load `Box.hack` in the CPU Emulator and run it while holding a key to test the box drawing behavior.
