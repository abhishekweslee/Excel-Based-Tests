import subprocess
import pandas as pd
import time
import threading
import re
import sys
import os
from Core.dev.Common_opts import Paths
from Core.dev.dev_bus_ticket import *

class CLTAuto:
    def __init__(self):
        print("Initializing CLI Tool...")
        self.sheet = pd.read_excel(Paths.excel_path)
        self.process = None
        self.output_thread = None
        self.str = ""

    def start_process(self):
        self.process = subprocess.Popen(
            ["python3", "-m", "Core.dev.dev_bus_ticket"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.enter_data("")

    def enter_data(self, input):
        self.str = ""

        """Send inputs dynamically to the subprocess based on prompts."""
        time.sleep(1)

        def read_output():
            """Continuously read and display output from the subprocess."""
            while True:
                output = self.process.stdout.readline()
                if output == '' and self.process.poll() is not None:
                    break
                if output:
                    self.str = self.str+output
                    sys.stdout.write(output)  # Write directly to stdout
                    sys.stdout.flush()  # Ensure immediate output

        # Start a thread to read and display subprocess output
        self.output_thread = threading.Thread(target=read_output, daemon=True)
        self.output_thread.start()

        # Send inputs sequentially

        self.process.stdin.write(str(input) + '\n')
        self.process.stdin.flush()
        print(input)
        time.sleep(1)

        return self.str

    def close_process(self):
        """Terminate the subprocess."""
        self.process.terminate()
        if self.output_thread:
            self.output_thread.join()
        self.process = None
