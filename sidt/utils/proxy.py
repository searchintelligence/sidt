import subprocess


class Nord():
    """
    A class for NordVPN operations. Requires the NordVPN app to be installed on the system and logged in.
    Use the nordvpn_connect() method to connect to NordVPN.
    Use the nordvpn_disconnect() method to disconnect from NordVPN.
    """

    def disconnect():
        """Disconnect from NordVPN."""

        result = subprocess.run(["nordvpn", "-d"], capture_output=True, text=True)
        return result.stdout, result.stderr

    def connect(country=None):
        """
        Connect to NordVPN. Optionally connect to a specific country.
        Args:
            country (str): The country to connect to.
        Examples:
            nordvpn_connect("United States")
        """

        if country:
            result = subprocess.run(["nordvpn", "-c", "-g", country], capture_output=True, text=True)
        else:
            result = subprocess.run(["nordvpn", "-c"], capture_output=True, text=True)
        
        return result.stdout, result.stderr

