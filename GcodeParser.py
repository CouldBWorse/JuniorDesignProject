class Parser:
    def __init__(self,filename: str,toolChange: tuple):
        self.filename = filename
        self.positions = []
        self.commands = []
        self.toolChangeLoc = toolChange
        self.startPoint = 0
        self.endPoint = 0
        self.shortendCmds = []

    def parse_gcode(self):
        """
        Takes a gcode file name as input. Adds commands and positions to array.
        """
        # Open the G-code file and read its contents
        with open(self.filename, 'r') as f:
            gcode_str = f.read()
        # Split the G-code into individual lines
        gcode_lines = gcode_str.split('\n')
        # Loop through each line of G-code
        for line in gcode_lines:
            # Remove any comments from the line
            line = line.split(';')[0]
            # Split the line into individual commands
            line_commands = line.split()
            # Initialize the X, Y, and Z coordinates for the current line
            x_coord = None
            y_coord = None
            z_coord = None
            # Loop through each command in the line
            for command in line_commands:
                # Check if the command is an X position command
                if command[0] == 'X':
                    # Parse the X coordinate from the command
                    x_coord = float(command[1:])
                # Check if the command is a Y position command
                elif command[0] == 'Y':
                    # Parse the Y coordinate from the command
                    y_coord = float(command[1:])
                # Check if the command is a Z position command
                elif command[0] == 'Z':
                    # Parse the Z coordinate from the command
                    z_coord = float(command[1:])
                # If the command is not a position command, add it to the commands array
                else:
                    self.commands.append(command)
            # If all X, Y, and Z coordinates were found, add them as a tuple to the positions array
            if x_coord is not None and y_coord is not None and z_coord is not None:
                self.positions.append((x_coord, y_coord, z_coord))
    
    def print_gcode(self):
        """
        Prints values for debugging.
        """
        print("Positions:")
        print(self.positions)
        print("Short Commands:")
        print(self.shortendCmds)
    
    def convert_to_mm(self):
        """
        Loop through each position in the positions array and convert it from inches to millimeters.
        """
        for i in range(len(self.positions)):
            x = round(self.positions[i][0] * 25.4,2)
            y = round(self.positions[i][1] * 25.4,2)
            z = self.positions[i][2]
            self.positions[i] = (x, y, z)

    def rel_to_abs(self):
        """
        This method converts the relative coordinates to absolute coordinates.
        """
        for i in range(1, len(self.positions)):
            prev_x = self.positions[i-1][0]
            prev_y = self.positions[i-1][1]
            x = self.positions[i][0]
            y = self.positions[i][1]
            self.positions[i] = (prev_x + x, prev_y + y, self.positions[i][2])

    def defCmds(self):
        """
        This methods interprets the commands in the gcode.
        It also fills in the shortendcmds list to match the length of the positions array.
        """
        for count, cmd in enumerate(self.commands):
            if cmd == 'G20':
                self.convert_to_mm()
            elif cmd == 'G91':
                self.rel_to_abs()
            elif cmd == 'M6' or cmd == 'G28':
                self.positions.insert(count-self.startPoint,self.toolChangeLoc)
            elif cmd == 'G00':
                self.startPoint = count
            elif cmd == 'M2':
                self.endPoint = count

        for i in range(self.startPoint,self.endPoint):
            self.shortendCmds.append(self.commands[i])


#Example of how the class works
if __name__ == "__main__":
    exampleParse = Parser('example2.gcode', (374,0,0))
    exampleParse.parse_gcode()
    exampleParse.defCmds()
    exampleParse.print_gcode()
