"""Advent of Code: 2023.20.1"""
import sys
from typing import Self

type Signal = tuple[Self,Self,bool]

class Module():
    def __init__(self,label:str) -> None:
        self.destination_modules : list[Self] = []        
        self.status : bool = False
        self.label : str = None
        self.label = label

    def recive_pulse(self,pulse : bool,sender:Self) -> list[Signal]:
        pass

    def subscribe_to(self,subcribe: Self) -> None:
        self.destination_modules.append(subcribe)
        subcribe.connect(self)

    def connect(self, input_module : Self ) -> None:
        pass

class Output(Module):
    def __init__(self, label: str) -> None:
        self.label = label
    def recive_pulse(self,pulse : bool,sender:Self) -> list[Signal]:
        return []

class Button(Module):
    def __init__(self, label: str) -> None:
        self.label = label

class Broadcaster(Module):
    def recive_pulse(self, pulse: bool, sender: Self) -> list[Signal]:
        self.status = pulse

        signals : list[Signal] = []
        for mod in self.destination_modules:
            signals.append( (self,mod,self.status) )
        return signals

class FlipFlop(Module):
    def __init__(self, label: str) -> None:
        super().__init__(label)
        self.fliped : bool = False

    def recive_pulse(self, pulse: bool, sender: Module) -> list[Signal]:
        signals : list[Signal] = []
        
        if not pulse: # Low pulse
            self.status = not self.status # Flip signal.
        
            for mod in self.destination_modules:
                signals.append( (self,mod,self.status) )
        
        return signals

class Conjunction(Module):
    def __init__(self, label: str) -> None:
        super().__init__(label)
        self.last_signal : dict[Module,bool] = {}

    def recive_pulse(self, pulse: bool,sender : Module) -> list[Signal]:
        self.last_signal[ sender ] = pulse
        self.status = not all(self.last_signal.values())

        signals : list[Signal] = []
        for mod in self.destination_modules:
            signals.append( (self,mod,self.status) )
        return signals

    def connect(self, input_module: Self) -> None:
        self.last_signal[input_module] = False

def ModulesFactory(lines:list[str]) -> Broadcaster:
    modules : dict[str,Module] = { "output" : Output("output")}
    signal_to : dict[str,list[str]] = {"output" : []}
    broadcaster = None

    # Parse input
    for line in lines:
        label, sends_to = line.strip().split(" -> ")

        mod_type = label[0]

        if mod_type == 'b':
            broadcaster = Broadcaster(label)
            modules[label] = broadcaster
        elif mod_type == '%':
            label = label[1:]
            modules[label] = FlipFlop(label)
        else:
            label = label[1:]
            modules[label] = Conjunction(label)

        signal_to[label] = sends_to.split(', ')

    mods = list(modules.keys())

    for label in mods:
        for subs in signal_to[label]:
            if subs not in modules:
                modules[subs] = Output(subs)
            modules[label].subscribe_to(modules[subs])

    return modules

    #return broadcaster

def push_button(broadcaster:Module) -> int:
    #print(broadcaster.label,find.label)
    button_presses = 0

    done = False

    max_presses = 10000

    while not done:
        button_presses += 1

        signals_to_send : list[tuple[Module,Module,bool]] = [(Button("button"),broadcaster,False)]                

        while signals_to_send:
            new_signals_to_send : list[tuple[Module,bool]] = []

            for sender,reciver, pulse in signals_to_send:
                new_signals_to_send += reciver.recive_pulse(pulse,sender)

            for s,r,p in new_signals_to_send:
                # if r.label == "rx":
                if s.label == "ll":
                    if all(s.last_signal.values()):
                        print(button_presses)
                    # print(f"rx found {s} {r} {p}")
                    # if not p:
                    #     done = True

            signals_to_send = new_signals_to_send
        
        if button_presses == max_presses:
            break

    return button_presses


def main():
    """Start"""
    #get argument
    if len(sys.argv) < 2:
        sys.exit("Usage: python " + sys.argv[0] + " filename")
    filename = sys.argv[1]
    try:
        with open(filename, 'rt', encoding="utf-8") as file:
            lines = file.readlines()
    except IOError as err:
        print(f"{err}\nError opening {filename}. Terminating program.", file=sys.stderr)
        sys.exit(1)

    # Do stuff with lines    
    #broadcaster = ModulesFactory(lines)
    #push_button(broadcaster)
    #print(all_modules["gf"].last_signal.keys())
    #print(push_button(broadcaster))

    all_modules : dict[str,Module] = ModulesFactory(lines)
    push_button(all_modules["broadcaster"])
    # for i in range(3923):
    #     push_button(all_modules["broadcaster"])
        # if all(all_modules["ll"].last_signal.values()):
        #     print(i+1)
        #     break

    print("-------------------------------------------------")
    print(all_modules["qf"].last_signal.values())
    print(all_modules["gv"].last_signal.values())
    print(all_modules["rc"].last_signal.values())
    print(all_modules["ll"].last_signal.values())
    print(all_modules["kl"].last_signal.values())

    print(3923*4007*3767*3931) # 232774988886497



if __name__ == "__main__":
    main()
