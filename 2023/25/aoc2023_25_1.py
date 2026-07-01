"""Advent of Code: 2023.25.1

Stoer-Wagner (Steg-for-steg)

Hver runde i algoritmen kalles en fase, og hver fase gjør følgende:
    
    Start med en tilfeldig node: 
        Du oppretter en mengde med noder som starter med denne ene noden.
   
    Legg til den "nærmeste" noden: 
        Finn den noden utenfor mengden som har sterkest tilknytning 
        (høyest samlet kantvekt) til nodene som allerede er i mengden. Legg 
        den til. 
    
    Gjenta til alle noder er valgt: 
        Fortsett med dette til alle nodene i grafen er lagt til i mengden.
    
    Finn de to siste nodene: 
        De to siste nodene som ble lagt til i mengden kalles ofte s og t.
    
    Registrer kuttet: 
        Det minste kuttet mellom akkurat disse to nodene (s-t kuttet) er rett 
        og sways lik summen av kantene som går inn til den aller siste noden (t). 
        Lagre denne verdien.
    
    Slå sammen nodene: 
        Slå nodene s og t sammen til én enkelt node (kontraksjon). Alle kanter som 
        gikk til s eller t går nå til den nye super-noden.  
    
Dette gjentas i en ny fase på den nye, mindre grafen. Når du har kjørt nok faser til 
at det bare er én node igjen, ser du på alle de lagrede verdiene fra steg 5. Den 
laveste verdien er grafens minimumskutt. 

Siden vi vet at kuttet skal være 3 kan vi stoppe algoritmen når vi finner et kutt med 3 kanter.

"""
import sys

def StoerWagner(graph):
    while len(graph)> 1:
    # lag en hashtable med kant veridene
        edgeWeight = {}
        for node in graph:
            edgeWeight[node] = 0

        # Start med en "tilfeldig node", tar første
        nodeToAdd = next(iter(graph))
                
        while len(edgeWeight) > 2:
            # newGraph.append(nodeToAdd)
            del edgeWeight[nodeToAdd]

            for edge in graph[nodeToAdd]:
                # hvis edge ikke finnes så er den behandlet
                if edge in edgeWeight:
                    edgeWeight[edge] += 1

            # Finn neste 
            maxEdges = 0
            for edge in edgeWeight:
                if edgeWeight[edge] > maxEdges:
                    maxEdges = edgeWeight[edge]
                    nodeToAdd = edge

            # Har vi en løsning? Hvis summen av kantene er 3, så har vi funnet et kutt
            # Dette forenkler algoritmen.
            sumEdges = sum(edgeWeight.values()) 
            if sumEdges == 3:  
                return len(edgeWeight)

    return 0


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
    wires = {}

    for line in lines:
        endpoint,connectedList = line.strip().split(':')
        connected = connectedList.strip().split()

        if endpoint not in wires.keys():
            wires[endpoint] = connected
        else:
            wires[endpoint].extend(connected)

        for c in connected:
            if c not in wires.keys():
                wires[c] = [endpoint]
            else:
                wires[c].append(endpoint)
    
    # Finn partisjonene
    originalSize = len(wires)
    partisionOneSize = StoerWagner(wires)
    partisionTwoSize = originalSize - partisionOneSize

    print("Answer is:", partisionOneSize*partisionTwoSize)


if __name__ == "__main__":
    main()
