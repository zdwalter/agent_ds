---
name: demo
description: Demonstration skill with simple greeting and calculation tools.
allowed-tools:
  - greet
  - add_numbers
  - reverse_string
  - generate_random_number
---

# Demo Skill

This is a sample skill created to demonstrate how to add new skills to the agent system.

## Tools

### greet
Returns a personalized greeting.
- `name`: The name of the person to greet.

### add_numbers
Adds two numbers and returns the sum.
- `a`: First number.
- `b`: Second number.

### reverse_string
Reverse a string.
- `s`: The input string.

### generate_random_number
Generate a random integer between low and high (inclusive).
- `low`: Lower bound (default 0).
- `high`: Upper bound (default 100).
