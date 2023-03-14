%
G21 G17 G90
G00 X100 Y100 Z1             ; point B
G01 X100 Y250 Z0            ; point C
G01 X250 Y250 Z0            ; point D
G01 X250 Y100 Z0           ; point E
G01 X100 Y100 Z0            ; point F
M6
G01 X100 Y100 Z0            ; point F
G01 X100 Y250 Z0            ; point C
G01 X250 Y250 Z0            ; point D
G01 X250 Y100 Z0           ; point E
G01 X100 Y100 Z0            ; point F
G28
M2
%