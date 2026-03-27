"""
Day 5 - Pandas + Data (Titanic)

Run:
    python3 analysis.py
"""

import pandas as pd


def pct(value: float) -> str:
    """Format a numeric value as a percentage with 2 decimals."""
    return f"{value:.2f}%"


def main() -> None:
    # Load Titanic dataset from local CSV.
    df = pd.read_csv("titanic.csv")

    print("=== Titanic Data Analysis (Day 5) ===")
    print(f"Total rows loaded: {len(df)}")
    print("-" * 60)

    # 01) Survival counts and percentages.
    total = len(df)
    survival_counts = df["Survived"].value_counts().sort_index()
    not_survived_count = int(survival_counts.get(0, 0))
    survived_count = int(survival_counts.get(1, 0))
    print("01) Survived vs Didn't Survive (counts + percentages)")
    print(f"Did not survive: {not_survived_count} ({pct(not_survived_count / total * 100)})")
    print(f"Survived:        {survived_count} ({pct(survived_count / total * 100)})")
    print("-" * 60)

    # 02) Survival rate by passenger class.
    class_survival = df.groupby("Pclass")["Survived"].mean().sort_index() * 100
    print("02) Survival rate by passenger class")
    for pclass, rate in class_survival.items():
        print(f"Class {int(pclass)}: {pct(rate)}")
    print("-" * 60)

    # 03) Average age of survivors vs non-survivors.
    avg_age_by_survival = df.groupby("Survived")["Age"].mean()
    print("############ Average age (survived vs non-survived)", avg_age_by_survival)
    print("03) Average age (survived vs non-survived)")
    print(f"Did not survive: {avg_age_by_survival.get(0):.2f}")
    print(f"Survived:        {avg_age_by_survival.get(1):.2f}")
    print("-" * 60)

    # 04) Embarkation port with highest survival rate.
    embark_survival = df.dropna(subset=["Embarked"]).groupby("Embarked")["Survived"].mean() * 100
    top_port = embark_survival.idxmax()
    top_port_rate = embark_survival.max()
    print("04) Embarkation port with highest survival rate")
    for port, rate in embark_survival.sort_values(ascending=False).items():
        print(f"Port {port}: {pct(rate)}")
    print(f"Highest: Port {top_port} ({pct(top_port_rate)})")
    print("-" * 60)

    # 05) Missing Age count and fill by median age per class.
    missing_age_before = int(df["Age"].isna().sum())
    # Fill missing age using median age within each passenger class.
    df["Age"] = df.groupby("Pclass")["Age"].transform(lambda s: s.fillna(s.median()))
    missing_age_after = int(df["Age"].isna().sum())
    print("05) Missing Age values + class median fill")
    print(f"Missing Age before fill: {missing_age_before}")
    print(f"Missing Age after fill:  {missing_age_after}")
    print("-" * 60)

    # 06) Oldest surviving passenger.
    survived_df = df[df["Survived"] == 1]
    oldest_survivor_row = survived_df.loc[survived_df["Age"].idxmax()]
    print("06) Oldest surviving passenger")
    print(f"Name:  {oldest_survivor_row['Name']}")
    print(f"Age:   {oldest_survivor_row['Age']:.1f}")
    print(f"Class: {int(oldest_survivor_row['Pclass'])}")
    print("-" * 60)

    # 07) Survival % of women vs men.
    sex_survival = df.groupby("Sex")["Survived"].mean() * 100
    print("07) Survival % by sex")
    for sex, rate in sex_survival.items():
        print(f"{sex.title()}: {pct(rate)}")
    print("-" * 60)

    # 08) Create AgeGroup and show survival rate per group.
    # bins: (-inf,18), [18,60), [60, inf)
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[-1, 17, 60, float("inf")],
        labels=["Child", "Adult", "Senior"],
    )
    agegroup_survival = df.groupby("AgeGroup", observed=False)["Survived"].mean() * 100
    print("08) Survival rate by AgeGroup")
    for group, rate in agegroup_survival.items():
        print(f"{group}: {pct(rate)}")
    print("-" * 60)

    # 09) In 3rd class, survival rate for men vs women.
    third_class = df[df["Pclass"] == 3]
    third_class_by_sex = third_class.groupby("Sex")["Survived"].mean() * 100
    print("09) 3rd class survival rate (men vs women)")
    for sex, rate in third_class_by_sex.items():
        print(f"{sex.title()}: {pct(rate)}")
    print("-" * 60)

    # 10) Drop rows with missing Cabin and measure rows kept.
    original_rows = len(df)
    cabin_clean_df = df.dropna(subset=["Cabin"])
    remaining_rows = len(cabin_clean_df)
    kept_percent = remaining_rows / original_rows * 100
    print("10) After dropping rows with missing Cabin")
    print(f"Rows remaining: {remaining_rows}")
    print(f"Kept from original: {pct(kept_percent)}")
    print("-" * 60)


if __name__ == "__main__":
    main()
