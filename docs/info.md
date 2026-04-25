## How it works
This design is a 1-bit full adder. It calculates the binary sum of two bits (`a` and `b`) plus a carry-in bit (`cin`).
- **Sum** = $A \oplus B \oplus Cin$
- **Cout** = $(A \cdot B) + (Cin \cdot (A \oplus B))$

The design is implemented behaviorally in Verilog using bit-concatenation: `{cout, sum} = a + b + cin`.

## How to test
1.  Apply binary values to the first three input pins (`ui_in[0]`, `ui_in[1]`, `ui_in[2]`).
2.  Check the first two output pins (`uo_out[0]` for Sum, `uo_out[1]` for Carry).
3.  Verification can be performed by ensuring the output matches the standard Full Adder truth table.

## External hardware
No external hardware required beyond basic input switches and LEDs.
