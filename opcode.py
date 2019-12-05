# the complete opcode
# can pick used opcodes

def find_parameters(opcode, program, position, parameter_modes, saves=True):
    count = INPUT_PARAMETER_COUNT[opcode]
    length = len(program)
    parameters = []
    end_location = 0
    for i in range(count):
        if i == count - 1 and saves:
            end_location = program[position+i+1]
        else:
            if parameter_modes[i] == 0:
                parameters.append(program[program[position+i+1]])
            else:
                parameters.append(program[position+i+1])
    return parameters, end_location

def opcode1(program, position, parameter_modes=[0, 0, 0]):
    # sum
    params, save_location = find_parameters(1, program, position, parameter_modes)
    value = sum(params)
    return value, save_location

def opcode2(program, position, parameter_modes=[0, 0, 0]):
    # multiplication
    params, save_location = find_parameters(2, program, position, parameter_modes)
    value = 1
    for p in params:
        value *= p
    return value, save_location

def opcode3(program, position, parameter_mode=[0]):
    # input
    _, save_location = find_parameters(3, program, position, parameter_mode)
    value = int(input("Enter value:"))
    return value, save_location

def opcode4(program, position, parameter_mode=[0]):
    # output
    _, print_location = find_parameters(4, program, position, parameter_mode)
    print("Diagnostic result: ", end='')
    print(program[print_location])
    return None

def opcode5(program, position, parameter_modes=[0, 0]):
    # jump if true
    params, _ = find_parameters(5, program, position, parameter_modes, False)
    if params[0] != 0:
        return params[1]

def opcode6(program, position, parameter_modes=[0, 0]):
    # jump if false
    params, _ = find_parameters(6, program, position, parameter_modes, False)
    if params[0] == 0:
        return params[1]

def opcode7(program, position, parameter_modes=[0, 0, 0]):
    # less than
    params, save_location = find_parameters(7, program, position, parameter_modes)
    value = 1 if params[0] < params[1] else 0
    return value, save_location

def opcode8(program, position, parameter_modes=[0, 0, 0]):
    # equals
    params, save_location = find_parameters(8, program, position, parameter_modes)
    value = 1 if params[0] == params[1] else 0
    return value, save_location

def find_parameter_modes(opcode, parameter_modes):
    count = INPUT_PARAMETER_COUNT[opcode]
    if len(parameter_modes) == 0:
        return [0]*count
    elif count == 1:
        return [int(parameter_modes)]
    else:
        param_modes = []
        for mode in reversed(parameter_modes):
            param_modes.append(int(mode))
        if len(param_modes) < count:
            param_modes.extend([0]*(count-len(param_modes)))
        return param_modes

# run(program, available_opcodes, extra_values, halt_print)
# program
#   list of integers
# available_opcodes
#   set of available opcodes, defaults to all
# extra_values
#   (position, value) list for replacement:
#   program[position] = value
# halt_print
#   whether or not to print when the program halts
def run(program, available_opcodes={1, 2, 3, 4, 5, 6, 7, 8}, extra_values=[], halt_print=True):
    jump_codes = {5, 6}
    for val in extra_values:
        program[val[0]] = val[1]

    position = 0
    length = len(program)
    while True:
        code = str(program[position])
        opcode, parameter_modes = int(code[-2:]), code[:-2]
        if opcode == 99:
            if halt_print:
                print("Halted!")
            return program
        if opcode not in available_opcodes:
            print("Error - the encountered opcode is not available!", opcode)
            break
        parameter_modes = find_parameter_modes(opcode, parameter_modes)
        params = OPCODE_FUNCTIONS[opcode](program, position, parameter_modes)
        if opcode in jump_codes:
            position = params if params is not None else (position + INPUT_PARAMETER_COUNT[opcode] + 1)
        else:
            if params is not None:
                program[params[1]] = params[0]
            position += INPUT_PARAMETER_COUNT[opcode] + 1
        position %= length

INPUT_PARAMETER_COUNT = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
}

OPCODE_FUNCTIONS = {
    1: opcode1,
    2: opcode2,
    3: opcode3,
    4: opcode4,
    5: opcode5,
    6: opcode6,
    7: opcode7,
    8: opcode8,
}