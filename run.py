from src.detector import run_detection
from config.settings import DATA_PATH

def main():
    print("Starting money laundering detection...")
    flags = detect_patterns(DATA_PATH)
    if flags:
        print("Detected issues:")
        for flag in flags:
            print(f"- {flag}")
    else:
        print("No issues detected.")

if __name__ == "__main__":
    main()