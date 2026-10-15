import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from lucrare_A_nucleu import desfa

def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"

if __name__ == "__main__":
    test_base64()
    print("Yippieee :D") # realmente nu afisa nimic cand rulam, asa ca am adaugat bucata asta de cod