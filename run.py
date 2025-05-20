import uvicorn
import socket

# Import our application
from app.main import app

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception:
        # Fallback method
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception:
            return "Could not determine IP address"

if __name__ == "__main__":
    print("Starting Sensor Monitoring System...")
    
    # Get and display IP address
    ip_address = get_ip_address()
    port = 8000
    
    print("\n" + "="*50)
    print(f"Local access:  http://localhost:{port}")
    print(f"Network access: http://{ip_address}:{port}")
    print("="*50)
    print("\nShare the network access URL to allow others on your network to connect")
    print("Press Ctrl+C to stop the server")
    
    # Start the server
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)