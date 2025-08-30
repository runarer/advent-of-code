import math as m, re

board = list(open('data.txt'))

# Lager en dict av posisjonen til alle symboler og en tom liste for hver,
# Listen er til tall rundt.
chars = {(r, c): [] for r in range(140) for c in range(140)
                    if board[r][c] not in '01234566789.'}

# Leter igjennom linje for linje
for r, row in enumerate(board):

    # Finner alle nummer i en linje 
    for n in re.finditer(r'\d+', row):
        # og lager et set med posisjonene rundt tallet (og tallet, men det er for enkelthetskyld.)
        edge = {(r, c) for r in (r-1, r, r+1)
                       for c in range(n.start()-1, n.end()+1)}

        # Dette er ny bruk av & for meg. Leste som dict og ikke set.
        # Nummer som har et symbol rundt blir lagt til i listen til symbolet.
        for o in edge & chars.keys():
            # Symboler som har tall rundt seg får disse lagt til i en liste.
            chars[o].append(int(n.group()))

print(sum(sum(p)    for p in chars.values()),
      sum(m.prod(p) for p in chars.values() if len(p)==2))

# Løsningen antar (som er riktig) at ingen andre symboler en '*' kan ha mer en ett tall
# rundt seg. Og ingen tall har mer enn ett symbol rundt seg.