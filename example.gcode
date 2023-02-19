%
G21 G17 G90
G00 X50 Y50 Z0              ; point B
G01 X50 Y50 Z-1             ; point B
G01 X50 Y80 Z-1            ; point C
G01 X90 Y100 Z-1            ; point D
G01 X150 Y40 Z-1           ; point E
G01 X100 Y10 Z-1            ; point F
G01 X50 Y130 Z-1            ; point G
M6
G01 X80 Y80 Z-1            ; point H
G01 X190 Y10 Z-1           ; point I
G01 X130 Y100 Z-1           ; point J
G01 X110 Y80 Z-1            ; point K
G01 X110 Y50 Z-1            ; point L
G01 X50 Y50 Z-1             ; point B
G01 X50 Y50 Z0
G28
M2
%