import os
from automata.fa.dfa import DFA

dir_path = os.path.dirname(os.path.realpath(__file__))

states = {
    'start', 'm', 'u', 'l', 'open',
    'num1_0', 'num1_1', 'num1_2', 'num1_3',
    ',',
    'num2_0', 'num2_1', 'num2_2', 'num2_3',
    'close',
}

transitions = {
    'start': {'m': 'm'},
    'm': {'u': 'u'},
    'u': {'l': 'l'},
    'l': {'(': 'open'},
    # Start of num1
    'open': {**{str(i): 'num1_1' for i in range(1, 10)},'0': 'num1_0'},
    'num1_0': {',': ','},  # if num1 was '0'
    # After First digit of num1
    'num1_1': {**{str(i): 'num1_2' for i in range(10)}, ',': ','},
    # After Second digit of num1
    'num1_2': {**{str(i): 'num1_3' for i in range(10)}, ',': ','},
    'num1_3': {',': ','},  # After Third digit of num1
    # Start of num2
    ',': {**{str(i): 'num2_1' for i in range(1, 10)}, '0': 'num2_0'},
    'num2_0': {')': 'close'},  # if num2 was '0'
    'num2_1': {**{str(i): 'num2_2' for i in range(10)}, ')': 'close'},  # After First digit of num2
    'num2_2': {**{str(i): 'num2_3' for i in range(10)}, ')': 'close'},  # After Second digit of num2
    'num2_3': {')': 'close'},  # After Third digit of num2
    'close': {},
}

dfa = DFA(
    states=states,
    input_symbols=set('0123456789(),mul'),
    transitions=transitions,
    initial_state='start',
    final_states={'close'},
    allow_partial=True
)

do_dfa = DFA(
    states=set('don\'t').union({'start', 'do', 'dont', 'do(', 'dont('}),
    input_symbols=set('don\'t()'),
    transitions={
        'start': {'d': 'd'},
        'd': {'o': 'o'},
        'o': {'n': 'n', '(': 'do('},
        'n': {'\'': '\''},
        '\'': {'t': 't'},
        't': {'(': 'dont('},
        'do(': {')': 'do'},
        'dont(': {')': 'dont'},
        'do': {}, 'dont': {}
    },
    initial_state='start',
    final_states={'do', 'dont'},
    allow_partial=True
)


def read_char(dfa, current_state, char):
    if char not in dfa.input_symbols:
        return None

    if char in dfa.transitions.get(current_state, {}):
        return dfa.transitions[current_state][char]

    return None


class ReadMUL:
    def __init__(self):
        self.current_state = dfa.initial_state
        self.args = ['']
        self.argsi = 0
        self.total = 0

    def read(self, ch, last_do):
        self.current_state = read_char(dfa, self.current_state, ch)

        # invalid state
        if self.current_state is None:
            self.reset()
            return False

        if ch in '0123456789':
            self.args[self.argsi] += ch

        if ch == ',':
            self.args.append('')
            self.argsi += 1

        if self.current_state in dfa.final_states:
            self.calc_args(last_do)
            self.reset()

        return True

    def calc_args(self, last_do):
        if last_do is False:
            return

        self.total += int(self.args[0]) * int(self.args[1])

    def reset(self):
        self.current_state = dfa.initial_state
        self.args = ['']
        self.argsi = 0


class ReadDO:
    def __init__(self):
        self.current_state = do_dfa.initial_state
        self.last_do = None

    def read(self, ch):
        self.current_state = read_char(do_dfa, self.current_state, ch)

        # invalid state
        if self.current_state is None:
            self.reset()
            return False

        if self.current_state in do_dfa.final_states:
            self.last_do = self.current_state == 'do'
            self.reset()

        return True

    def reset(self):
        self.current_state = do_dfa.initial_state


def part_one():
    mul = ReadMUL()
    do = ReadDO()

    reading_mul = True

    with open(os.path.join(dir_path, 'input.txt'), 'r') as f:
        for line in f:
            for ch in line:
                if reading_mul:
                    reading_mul = mul.read(ch, do.last_do)

                    if not reading_mul:
                        reading_mul = not do.read(ch)
                else:
                    reading_mul = not do.read(ch)

                    if reading_mul:
                        reading_mul = mul.read(ch, do.last_do)

    print(mul.total)


part_one()
