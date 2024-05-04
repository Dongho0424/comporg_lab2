// hazard.v

// This module determines if pipeline stalls or flushing are required

// TODO: declare propoer input and output ports and implement the
// hazard detection unit

module hazard #(
  parameter DATA_WIDTH = 32
)(
    input taken,

    output reg ifid_flush,
    output reg idex_flush,
    output reg exmem_flush
);

always @(*) begin
    ifid_flush = taken;
    idex_flush = taken;
    exmem_flush = taken;
end


endmodule
