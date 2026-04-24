import argparse
import csv
import os
import random


def generate_row(rng: random.Random) -> dict:
    gender = rng.choice(["female", "male", "nonbinary"])
    age = rng.randint(13, 80)

    base = 5.0 + max(0, 30 - age) * 0.10
    gender_effect = {"female": 0.2, "male": 0.0, "nonbinary": 0.1}[gender]
    noise = rng.gauss(0, 2.0)

    hours_per_week = max(0.0, base + gender_effect + noise)
    return {"age": age, "gender": gender, "netflix_hours_per_week": round(hours_per_week, 2)}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a random dataset of Netflix watch time by gender and age."
    )
    parser.add_argument("-n", "--num-rows", type=int, default=500, help="Number of rows to generate.")
    parser.add_argument("--seed", type=int, default=30, help="Random seed for reproducibility.")
    parser.add_argument(
        "-o",
        "--out",
        default=os.path.join("data", "netflix_watchtime.csv"),
        help="Output CSV path (default: data/netflix_watchtime.csv).",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)

    rng = random.Random(args.seed)
    fieldnames = ["age", "gender", "netflix_hours_per_week"]

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for _ in range(args.num_rows):
            writer.writerow(generate_row(rng))

    print(f"Wrote {args.num_rows} rows to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

