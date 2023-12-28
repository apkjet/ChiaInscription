import subprocess
import argparse
import re
import time
import sys

# Define command-line arguments
parser = argparse.ArgumentParser(description="Run Chia wallet send command multiple times.")
parser.add_argument("--tick", type=str, help="Value to replace 'tick' in the command.",default='mojo')
parser.add_argument("--iter", type=int, help="Number of times to run the command.", default=1000000)
parser.add_argument("--finger", required=True, type=int, help="wallet fingerprint to run the command.")
parser.add_argument("--fee", type=float,help="Fee value to use in the command.", default=0.00005)

# Parse the command-line arguments
args = parser.parse_args()

# Chia wallet send command template
chia_send_command_template = [
    "chia",
    "wallet",
    "send",
    "-f",
    "{}".format(args.finger), #replace wallet fingerprint
    "-t",
    "xch1jdwmg5aa0qf3yr5jekhxdpmjp5p8lf7nhdl3lvfu4xr27ayx2m2q0sm3l9", # replace wallet
    "-a",
    "0.000000000001",
    "-e",
    "{{'p':'xchs','op':'mint','tick':'{}','amt':'1000'}}".format(args.tick),
    "--override",
    "--fee",
    str(args.fee),
]

# Function to run Chia send command and get block height and tx ID
def run_chia_send_command():
    try:
        print("Running Chia send command...")
        send_output = subprocess.check_output(chia_send_command_template, text=True)
        print(f"Command Output: {send_output}")
        match = re.search(r"-f (\d+) -tx (0x[a-fA-F0-9]+)", send_output)
        if match:
            block_height = match.group(1)
            tx_id = match.group(2)
            print(f"Block Height: {block_height}")
            print(f"Transaction ID: {tx_id}")
            return block_height, tx_id
        else:
            print("Block Height and Transaction ID not found in output.")
            return None, None
    except subprocess.CalledProcessError as e:
        print(f"Error running Chia send command: {e}")
        return None, None

for i in range(args.iter):
    block_height, tx_id = run_chia_send_command()
