import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Filter and summarize log file.")
    parser.add_argument(
        "--level",
        help="Log level to filter (INFO, WARN, ERROR)",
    )
    parser.add_argument(
        "--service",
        help="Service name to filter (e.g., auth, api, db)",
    )
    parser.add_argument(
        "--out",
        default="filtered_logs.txt",
        help="Output filename (default: filtered_logs.txt)",
    )
    return parser.parse_args()

def is_valid_line(line):
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 4:
        return None
    timestamp, level, service, message = parts
    level_upper = level.upper()
    if level_upper not in ("INFO", "WARN", "ERROR"):
        return None
    # Return normalized components
    return timestamp, level_upper, service, message

def line_matches_filters(parsed_line, level_filter, service_filter):
    timestamp, level_upper, service, message = parsed_line

    if level_filter is not None:
        # level_filter already uppercased by caller
        if level_upper != level_filter:
            return False

    if service_filter is not None:
        if service != service_filter:
            return False

    return True

def main():
    args = parse_args()

    level_filter = args.level.upper() if args.level else None
    service_filter = args.service if args.service else None
    out_filename = args.out

    valid_scanned = 0
    written = 0

    try:
        with open("logs.txt", "r", encoding="utf-8") as infile, \
             open(out_filename, "w", encoding="utf-8") as outfile:

            for line in infile:
                raw = line.rstrip("\n")
                if not raw.strip():
                    # Skip empty lines
                    continue

                parsed = is_valid_line(raw)
                if parsed is None:
                    # Invalid line: ignore completely
                    continue

                valid_scanned += 1

                if line_matches_filters(parsed, level_filter, service_filter):
                    timestamp, level_upper, service, message = parsed
                    out_line = f"{timestamp} | {level_upper} | {service} | {message}\n"
                    outfile.write(out_line)
                    written += 1

    except FileNotFoundError:
        print("Valid lines scanned: 0")
        print("Lines written: 0")
        print(f"Output file: {out_filename}")
        return

    # Summary to terminal
    print(f"Valid lines scanned: {valid_scanned}")
    print(f"Lines written: {written}")
    print(f"Output file: {out_filename}")

if __name__ == "__main__":
    main()
