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

    # def send_pulse(self) -> None:
    #     for mods in self.destination_modules:
    #         print(f"{self.label} -{"High" if self.status else "Low"} -> {mods.label}")
    #         mods.recive_pulse(self.status,self)
    #     for mods in self.destination_modules:
    #         mods.send_pulse()

    def connect(self, input_module : Self ) -> None:
        pass

class Output(Module):
    def __init__(self, label: str) -> None:
        self.label = label
    def recive_pulse(self,pulse : bool,sender:Self) -> list[Signal]:
        #print(f"Output got: {"High" if pulse else "Low"}")
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

    return broadcaster

def push_button(broadcaster:Module,times=1) -> int:
    low_pulses = 0
    high_pulses = 0

    for _ in range(times):
        signals_to_send : list[tuple[Module,Module,bool]] = [(Button("button"),broadcaster,False)]        
        low_pulses += 1

        while signals_to_send:
            new_signals_to_send : list[tuple[Module,bool]] = []

            for sender,reciver, pulse in signals_to_send:
                # print(f"{sender.label} -{"High" if pulse else "Low"} -> {reciver.label}")
                new_signals_to_send += reciver.recive_pulse(pulse,sender)

            high_pulses_this_turn = sum(1 if x else 0 for _,_,x in new_signals_to_send)
            high_pulses += high_pulses_this_turn
            low_pulses += len(new_signals_to_send) - high_pulses_this_turn

            signals_to_send = new_signals_to_send

    return low_pulses*high_pulses


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
    print(push_button(broadcaster,1000))





if __name__ == "__main__":
    main()
