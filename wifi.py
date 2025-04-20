import subprocess

def get_saved_wifi_passwords():
    # Get the list of saved Wi-Fi profiles
    profiles_data = subprocess.check_output(["netsh", "wlan", "show", "profiles"], text=True)
    profiles = []
    
    for line in profiles_data.splitlines():
        if "All User Profile" in line:
            profile_name = line.split(":")[1].strip()
            profiles.append(profile_name)
    
    wifi_details = []

    for profile in profiles:
        try:
            # Get the profile details including the key (password)
            profile_info = subprocess.check_output(
                ["netsh", "wlan", "show", "profile", profile, "key=clear"],
                text=True
            )

            password = None
            for line in profile_info.splitlines():
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    break

            wifi_details.append({"SSID": profile, "Password": password if password else "N/A"})
        
        except subprocess.CalledProcessError:
            wifi_details.append({"SSID": profile, "Password": "Error retrieving password"})

    return wifi_details

# Example usage
if __name__ == "__main__":
    passwords = get_saved_wifi_passwords()
    for wifi in passwords:
        print(f"SSID: {wifi['SSID']}, Password: {wifi['Password']}")
