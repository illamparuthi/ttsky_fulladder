import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_full_adder(dut):
    dut._log.info("Starting Gate-Level Hardened Simulation...")

    # 1. Initialize inputs
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    
    # 2. Reset Sequence: 50ns is recommended for GL netlist stability
    dut.rst_n.value = 0
    await Timer(50, unit="ns") 
    dut.rst_n.value = 1
    await Timer(50, unit="ns") 

    # Define Test Cases: (A, B, Cin) -> (Expected Sum, Expected Cout)
    test_cases = [
        (0, 0, 0, 0, 0),
        (1, 1, 0, 0, 1),
        (1, 1, 1, 1, 1),
        (1, 0, 0, 1, 0),
        (0, 1, 0, 1, 0),
    ]

    for a, b, cin, e_sum, e_cout in test_cases:
        dut.ui_in.value = (cin << 2) | (b << 1) | a
        
        # 3. Propagation Delay: Allow gates time to settle
        await Timer(20, unit="ns")

        # 4. Safe Conversion
        try:
            output_val = int(dut.uo_out.value)
            actual_sum = output_val & 1
            actual_cout = (output_val >> 1) & 1
            
            assert actual_sum == e_sum, f"Sum Error: A={a} B={b} Cin={cin}"
            assert actual_cout == e_cout, f"Cout Error: A={a} B={b} Cin={cin}"
            
            dut._log.info(f"Input: {a},{b},{cin} -> Sum: {actual_sum}, Cout: {actual_cout} [PASS]")
            
        except ValueError:
            # Helps debug 'X' states in the GitHub Action logs
            dut._log.error(f"Logic error: uo_out is {str(dut.uo_out.value)}")
            raise
