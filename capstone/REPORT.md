# Capstone Project Report — Make the Computer Draw a Box

**Name:** Jai Kuntal  
**Roll Number:** 2501730416  
**Personal Number (K):** 16  
**Course:** Nand to Tetris – I (ETCCNT301)  
**School:** School of Engineering & Technology, K.R. Mangalam University

## 1. Personal parameters

K is the last two digits of roll number 2501730416, so **K = 16**.

| Parameter | Value |
|---|---|
| K | 16 |
| K mod 3 | 1 — optional symbols.txt extension is not required |
| K mod 4 | 0 — width = 16 × (0 + 1) = **16 pixels (1 word)** |
| Starting row / height | Row 16; 20 rows (rows 16–35) |
| Position | Left edge of the screen |
| First word address | 16384 + 32 × 16 = **16896** |

## 2. Hack computer implementation

The project contains `CPU.hdl`, `Memory.hdl`, and `Computer.hdl`. The CPU decodes A- and C-instructions, uses the ALU and destination bits to update registers or memory, and combines ALU flags with jump bits to control the program counter. Memory selects RAM16K, Screen, or Keyboard using address bits. Computer connects the CPU, memory, and ROM32K. The supplied implementation uses built-in ALU, ARegister, DRegister, PC, RAM16K, Screen, Keyboard, ROM32K and basic gate/multiplexer chips.

## 3. Python two-pass assembler

`assembler.py` translates Hack assembly (`.asm`) into machine code (`.hack`) in two passes. Pass 1 removes comments and whitespace, ignores blank lines and records labels with the ROM address of the next instruction. Pass 2 translates A-instructions into a leading `0` plus a 15-bit address, and C-instructions into the Hack `111` + comp + dest + jump format. Predefined symbols and labels are resolved from the symbol table; new variables receive RAM addresses beginning at 16.

The assembler accepts destination letters and commutative operands in either order. Add, Max, Rect and Pong sources were assembled, producing 6, 16, 25 and 27,483 instructions respectively. These counts describe assembly generation and do not alone establish comparison with official test outputs.

## 4. Box drawing program

The Hack screen begins at address 16384 and each row contains 32 words, with each word controlling 16 pixels. Row 16 begins at `16384 + 32 × 16 = 16896`. Since K mod 4 = 0, the box width is 16 pixels (one word per row). The program paints 20 rows, from row 16 through row 35, at the left edge of the screen.

The program checks `KBD`. If a key is pressed, `colour` is set to -1 (black); otherwise it is set to 0 (white). It initializes `addr` to 16896 and `rows` to 20. For each row it writes `colour` to the current screen word, adds 32 to `addr`, decrements `rows`, and repeats until all 20 rows are processed. It then checks the keyboard again.

## 5. Build and verification notes

The updated `Box.asm` assembled into `Box.hack` with 34 machine instructions, 4 labels and 3 variables. The K=16 configuration does not require the K mod 3 = 0 `symbols.txt` extension. The report appendix distinguishes the supplied CPU test screenshot from the Memory editor syntax-status screenshot. A fresh CPU Emulator run of this K=16 `Box.hack`, plus current Memory and Computer test results, should be captured before claiming those specific tests passed.
