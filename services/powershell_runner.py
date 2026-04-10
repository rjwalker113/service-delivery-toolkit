# services/powershell_runner.py

import subprocess
import threading
from kivy.clock import Clock


def run_powershell_streaming(script_path, on_output, on_complete):
    '''
    Runs a PowerShell script and streams output line-by-line.
    - script_path: full path to the .ps1 file
    - on_output: callback(text)
    - on_complete: callback(return_code)
    '''

    def _run():
        # Start PowerShell process
        process = subprocess.Popen(
            [
                "powershell.exe",
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", script_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Stream stdout
        for line in process.stdout:
            Clock.schedule_once(lambda dt, t=line: on_output(t.rstrip()))

        # Stream stderr
        for line in process.stderr:
            Clock.schedule_once(lambda dt, t=line: on_output("[ERROR] " + t.rstrip()))

        # Wait for process to finish
        process.wait()

        # Notify completion
        Clock.schedule_once(lambda dt: on_complete(process.returncode))

    # Run in background thread
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
