import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_full_adder(dut):
    dut._log.info("Starting Gate-Level Hardened Simulation...")

    # 1. Initialize all inputs to avoid 'X' propagation
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    
    # 2. Longer Reset: Give the netlist more time to stabilize
    dut.rst_n.value = 0
    await Timer(20, units="ns") 
    dut.rst_n.value = 1
    await Timer(20, units="ns") 

    # Define Test Cases: (A, B, Cin) -> (Expected Sum, Expected Cout)
    test_cases = [
        (0, 0, 0, 0, 0),
        (1, 0, 0, 1, 0),
        (0, 1, 0, 1, 0),
        (1, 1, 0, 0, 1),
        (1, 1, 1, 1, 1),
    ]

    for a, b, cin, e_sum, e_cout in test_cases:
        # Pack inputs into the 8-bit ui_in bus
        dut.ui_in.value = (cin << 2) | (b << 1) | a
        
        # 3. Increased Propagation Delay: 
        # 1ns is often too short for gate-level timing. 10ns is safer.
        await Timer(10, units="ns")

        # 4. Robust Conversion:
        # We use .integer to try and get the value, but catch the error if it's 'X'
        try:
            # We use bitwise masking on the full value to be safe
            output_val = int(dut.uo_out.value)
            actual_sum = output_val & 1
            actual_cout = (output_val >> 1) & 1
            
            # Verify results
            assert actual_sum == e_sum, f"Failed Sum: A={a} B={b} Cin={cin} | Got {actual_sum}"
            assert actual_cout == e_cout, f"Failed Cout: A={a} B={b} Cin={cin} | Got {actual_cout}"
            
            dut._log.info(f"Input: {a},{b},{cin} -> Sum: {actual_sum}, Cout: {actual_cout} [PASS]")
            
        except ValueError:
            # If signals are still 'X', this will print the binary string for debugging
            dut._log.error(f"Logic error at Input {a},{b},{cin}: uo_out contains 'X' or 'Z' -> {dut.uo_out.value.binstr}")
            raise
