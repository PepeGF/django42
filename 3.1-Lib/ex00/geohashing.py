import sys
import antigravity

def check_args():
    if len(sys.argv) != 4:
        print("Usage: python(3) geohashing.py <latitude> <longitude> <date>")
        sys.exit(1)

    
def main():
    try:
        latitude = float(sys.argv[1])
    except ValueError:
        print("Error: Latitude must be valid float number.")
        sys.exit(2)
    try:
        longitude = float(sys.argv[2])
    except ValueError:
        print("Error: Longitude must be valid float number.")
        sys.exit(3)
    try:
        datedow = sys.argv[3].encode('utf-8')
    except Exception as e:
        print(f"Error: Date must be a valid string. {e}")
        sys.exit(4)
    antigravity.geohash(latitude, longitude, datedow)


if __name__ == "__main__":
    check_args()
    main()
