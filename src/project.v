`default_nettype none

module tt_um_full_adder (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (1=out, 0=in)
    input  wire       ena,      // always 1 when powered
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    // 1. Internal Wires for Adder Logic
    wire a   = ui_in[0];
    wire b   = ui_in[1];
    wire cin = ui_in[2];
    wire sum;
    wire cout;

    // 2. Full Adder Implementation 
    assign {cout, sum} = a + b + cin;

    // 3. Output Mapping
    assign uo_out[0] = sum;
    assign uo_out[1] = cout;

    // 4. Tie off unused pins to prevent floating signals
    assign uo_out[7:2] = 6'b000000;
    assign uio_out     = 8'b00000000;
    assign uio_oe      = 8'b00000000;

endmodule
