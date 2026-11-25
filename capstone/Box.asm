// Box.asm   Roll No 2501730416   K = 16
// Box: starts at row K = 16, 20 rows tall, 16 pixels wide (1 word),
//      attached to the left edge of the screen.
//   width  = 16 * ((16 mod 4) + 1) = 16 * 1 = 16 pixels = 1 word
//   first word address = SCREEN + 32*16 = 16384 + 512 = 16896
// Box is black while any key is pressed, white (erased) when released.

(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE           // key pressed -> use black
    @colour
    M=0             // no key -> white (erase)
    @PAINT
    0;JMP
(PRESSED)
    @colour
    M=-1            // all 16 bits = 1 -> black

(PAINT)
    @16896
    D=A
    @addr
    M=D             // addr = first word of row 16
    @20
    D=A
    @rows
    M=D             // 20 rows to paint

(ROW)
    @colour
    D=M
    @addr
    A=M
    M=D             // word 0 (pixels 0-15)

    @32
    D=A
    @addr
    M=D+M           // addr += 32 -> start of next row

    @rows
    M=M-1
    D=M
    @ROW
    D;JGT           // more rows left?

    @LOOP
    0;JMP           // check keyboard again
