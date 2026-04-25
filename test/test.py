import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_full_adder(dut):
    dut._log.info("Starting Full Adder Simulation...")

    # Initialize Control Signals
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await Timer(10, units="ns")
    dut.rst_n.value = 1  # Release reset

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
        
        await Timer(1, units="ns")

        # Extract outputs from the 8-bit uo_out bus
        actual_sum = int(dut.uo_out.value) & 1
        actual_cout = (int(dut.uo_out.value) >> 1) & 1

        # Verify results
        assert actual_sum == e_sum, f"Failed Sum: A={a} B={b} Cin={cin}"
        assert actual_cout == e_cout, f"Failed Cout: A={a} B={b} Cin={cin}"
        
        dut._log.info(f"Input: {a},{b},{cin} -> Sum: {actual_sum}, Cout: {actual_cout} [PASS]")
