def read_config(file_path):
    config = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            # Ignore comments and empty lines
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Split key and value by '='
            try:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                config[key] = value
            except ValueError:
                # If there's an invalid line, you can choose to skip it or raise an error
                continue
    
    return config

# Usage example
config_file = "Config.txt"
config = read_config(config_file)

cam = config['cam_port']
cam_port = int(cam)
print("Camera Port is:", cam)