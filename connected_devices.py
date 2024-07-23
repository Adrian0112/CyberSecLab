import subprocess


def get_connected_devices():
    try:
        # Run the arp-scan command to scan the local network
        result = subprocess.run(['sudo', 'arp-scan', '-l'], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        return f"arp-scan command failed with error: {e}"
    except FileNotFoundError:
        return "arp-scan is not installed. Install it using 'sudo apt install arp-scan'."

    # Split the output into lines and filter out empty lines and headers
    lines = output.split('\n')
    devices = [line for line in lines if len(line.strip()) > 0 and line.strip() != 'Interface']

    return devices


if __name__ == "__main__":
    devices = get_connected_devices()
    if isinstance(devices, str):
        # Print error message if the result is a string (i.e., an error message)
        print(devices)
    else:
        # Print each device on a new line
        for device in devices:
            print(device)
