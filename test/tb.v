`default_nettype none
`timescale 1ns/1ps

module tb ();

    // Dump signals for GTKWave
    initial begin
        $dumpfile ("tb.vcd");
        $dumpvars (0, tb);
        #1;
    end

    // Standard Signal definitions
    reg  clk;
    reg  rst_n;
    reg  ena;
    reg  [7:0] ui_in;
    reg  [7:0] uio_in;
    wire [7:0] uo_out;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;

    // 1. Declare explicit nets for power to satisfy 'inout' port rules
`ifdef GL_TEST
    wire VPWR = 1'b1;
    wire VGND = 1'b0;
`endif

    // Instantiate the design under test (DUT)
    tt_um_full_adder user_project (
`ifdef GL_TEST
        // 2. Connect the defined nets instead of hardcoded constants
        .VPWR(VPWR),
        .VGND(VGND),
`endif
        .ui_in   (ui_in),
        .uo_out  (uo_out),
        .uio_in  (uio_in),
        .uio_out (uio_out),
        .uio_oe  (uio_oe),
        .ena     (ena),
        .clk     (clk),
        .rst_n   (rst_n)
    );

endmodule
