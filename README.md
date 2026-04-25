# Tiny Tapeout: 1-Bit Full Adder (Educational Example)

[![GDS](../../workflows/gds/badge.svg)](../../workflows/gds/badge.svg) 
[![Docs](../../workflows/docs/badge.svg)](../../workflows/docs/badge.svg) 
[![Test](../../workflows/test/badge.svg)](../../workflows/test/badge.svg)

This repository contains a simple **1-bit Full Adder** designed for Tiny Tapeout. It is intended as an introductory example for students to understand the ASIC design flow, from Verilog RTL to GDSII.

## Project Description

A full adder is a digital circuit that performs addition on three one-bit binary numbers. It consists of three inputs and two outputs:
- **Inputs:** `a`, `b`, and `cin` (carry-in).
- **Outputs:** `sum` and `cout` (carry-out).

In this project, we map these signals to the Tiny Tapeout 8-bit buses to demonstrate how hardware pins interact with internal logic.

## How it Works

The hardware logic is defined in `src/project.v`. It uses a concise behavioral assignment to handle the arithmetic:
```verilog
assign {cout, sum} = a + b + cin;
