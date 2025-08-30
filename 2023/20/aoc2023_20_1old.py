"""Advent of Code: 2023.20.1"""
import sys
from typing import Self

class Module():
    #destination_modules : list[Self] = []
    #status : bool = False
    #label : str = None

    def __init__(self,label:str) -> None:
        self.destination_modules : list[Self] = []        
        self.status : bool = False
        self.label : str = None
        self.label = label

    def recive_pulse(self,pulse : bool,sender:Self) -> None:
        pass

    def subscribe_to(self,subcribe: Self) -> None:
        self.destination_modules.append(subcribe)
        subcribe.connect(self)

    def send_pulse(self) -> None:
        for mods in self.destination_modules:
            print(f"{self.label} -{"High" if self.status else "Low"} -> {mods.label}")
            mods.recive_pulse(self.status,self)
        for mods in self.destination_modules:
            mods.send_pulse()

    def connect(self, input_module : Self ) -> None:
        pass

class Broadcaster(Module):
    def recive_pulse(self, pulse: bool, sender: Self) -> None:
        self.status = pulse
        self.send_pulse()

class FlipFlop(Module):
    def __init__(self, label: str) -> None:
        super().__init__(label)
        self.fliped : bool = False

    def recive_pulse(self, pulse: bool, sender: Module) -> None:
        if not pulse: # Low pulse
            self.status = not self.status # Flip signal.
            self.fliped = True
        else:
            self.fliped = False

    def send_pulse(self) -> None:
        if self.fliped:
            super().send_pulse() # Send signal

            #for mods in self.destination_modules:
            #    mods.recive_pulse(status,self)

class Conjunction(Module):
    

    def __init__(self, label: str) -> None:
        super().__init__(label)
        self.last_signal : dict[Module,bool] = {}

    # def subscribe_to(self, subcribe: Self) -> None:
    #     super().subscribe_to(subcribe)
        #self.last_signal.append(False)
        
        # print(self.destination_modules)
        # print(self.last_signal)

    def recive_pulse(self, pulse: bool,sender : Module) -> None:
        self.last_signal[ sender ] = pulse

        self.status = all(self.last_signal)

        #self.send_pulse()

        #for mods in self.destination_modules:
        #    mods.recive_pulse(status,self)
    def connect(self, input_module: Self) -> None:
        self.last_signal[input_module] = False


def ModulesFactory(lines:list[str]) -> Broadcaster:
    modules : dict[str,Module] = {}
    signal_to : dict[str,list[str]] = {}
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

    # print(signal_to)

    for label, mod in modules.items():
        for subs in signal_to[label]:
            mod.subscribe_to(modules[subs])

    return broadcaster

def controller(broadcaster:Module):
    signals_to_send : list[tuple[Module,Module,bool]] = [(None,broadcaster,False)]

    while signals_to_send:
        new_signals_to_send : list[tuple[Module,bool]] = []

        for sender,reciver, pulse in signals_to_send:
            new_signals_to_send += reciver.recive_pulse(pulse,sender)

        signals_to_send = new_signals_to_send


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
    broadcaster = ModulesFactory(lines)

    broadcaster.recive_pulse(False,None)

    #print(broadcaster)





if __name__ == "__main__":
    main()
