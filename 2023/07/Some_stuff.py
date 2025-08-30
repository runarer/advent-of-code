def card_value_2(card):
    value = 0

    if card == 'T':
        value = 58
    elif card == 'J':
        value = 49
    elif card == 'Q':
        value = 60
    elif card == 'K':
        value = 61
    elif card == 'A':
        value = 62
    else:
        value = ord(card)
    return value

def card_value_1(card):
    value = 0
    if card in "23456789":
        value = ord(card)
    elif card == 'T':
        value = 58
    elif card == 'J':
        value = 59
    elif card == 'Q':
        value = 60
    elif card == 'K':
        value = 61
    elif card == 'A':
        value = 62
    return value