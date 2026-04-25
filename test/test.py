import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_full_adder(dut):
    dut._log.info("Starting Gate-Level Hardened Simulation...")

    # 1. Force all inputs to 0 to prevent 'X' propagation from the start
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    
    # 2. Strong Reset: GL netlists often need more time to clear 'X' states
    dut.rst_n.value = 0
    await Timer(50, units="ns") 
    dut.rst_n.value = 1
    await Timer(50, units="ns") 

    # Define Test Cases: (A, B, Cin) -> (Expected Sum, Expected Cout)
    test_cases = [
        (0, 0, 0, 0, 0),
        (1, 0, 0, 1, 0),
        (0, 1, 0, 1, 0),
        (1, 1, 0, 0, 1),
        (1, 1, 1, 1, 1),
    ]

    for a, b, cin, e_sum, e_cout in test_cases:
        # Pack inputs: A=bit0, B=bit1, Cin=bit2
        dut.ui_in.value = (cin << 2) | (b << 1) | a
        
        # 3. Propagation Delay: 
        # GL timing is not instant like RTL. 20ns allows signal settle time.
        await Timer(20, units="ns")

        # 4. Safe Conversion:
        # We catch the ValueError to provide better debugging for students
        try:
            output_val = int(dut.uo_out.value)
            actual_sum = output_val & 1
            actual_cout = (output_val >> 1) & 1
            
            # Verify results
            assert actual_sum == e_sum, f"Failed Sum: A={a} B={b} Cin={cin} | Got {actual_sum}"
            assert actual_cout == e_cout, f"Failed Cout: A={a} B={b} Cin={cin} | Got {actual_cout}"
            
            dut._log.info(f"Input: {a},{b},{cin} -> Sum: {actual_sum}, Cout: {actual_cout} [PASS]")
            
        except ValueError:
            # This triggers if uo_out still contains 'X' or 'Z'
            dut._log.error(f"GL Error at Input {a},{b},{cin}: uo_out is {dut.uo_out.value.binstr}")
            raise
