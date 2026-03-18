import pandas as pd


def pct(part, whole):
    return (part / whole) * 100


df = pd.read_csv("pre-training/day-5/titanic.csv")
total_rows = len(df)

print("01) Survived vs didn't (counts and %)")
counts = df["Survived"].value_counts().sort_index()
survived = int(counts.get(1, 0))
not_survived = int(counts.get(0, 0))
print("   Survived:", survived, f"({pct(survived, total_rows):.1f}%)")
print("   Didn't :", not_survived, f"({pct(not_survived, total_rows):.1f}%)")
print()

print("02) Survival rate by passenger class")
by_class = df.groupby("Pclass")["Survived"].mean().sort_index()
for pclass, rate in by_class.items():
    print(f"   Class {pclass}: {rate*100:.1f}%")
print()

print("03) Average age of survivors vs non-survivors")
avg_age = df.groupby("Survived")["Age"].mean()
print(f"   Survived: {avg_age.get(1):.1f}")
print(f"   Didn't : {avg_age.get(0):.1f}")
print()

print("04) Embarkation port with highest survival rate")
by_port = df.dropna(subset=["Embarked"]).groupby("Embarked")["Survived"].mean()
best_port = by_port.idxmax()
print(f"   {best_port}: {by_port[best_port]*100:.1f}%")
print()

print("05) Missing age count and fill missing ages with median age per class")
missing_age = int(df["Age"].isna().sum())
print("   Missing Age values:", missing_age)

median_age_by_class = df.groupby("Pclass")["Age"].median()
df["AgeFilled"] = df["Age"]
for pclass, median_age in median_age_by_class.items():
    mask = (df["Pclass"] == pclass) & (df["AgeFilled"].isna())
    df.loc[mask, "AgeFilled"] = median_age
print("   Filled missing ages into new column: AgeFilled")
print()

print("06) Oldest surviving passenger (name, age, class)")
oldest_survivor = df[df["Survived"] == 1].sort_values("AgeFilled", ascending=False).iloc[0]
print("   Name:", oldest_survivor["Name"])
print("   Age :", float(oldest_survivor["AgeFilled"]))
print("   Class:", int(oldest_survivor["Pclass"]))
print()

print("07) % of women survived vs % of men")
by_sex = df.groupby("Sex")["Survived"].mean()
print(f"   Women: {by_sex.get('female')*100:.1f}%")
print(f"   Men  : {by_sex.get('male')*100:.1f}%")
print()

print("08) Survival rate by AgeGroup (Child/Adult/Senior)")
df["AgeGroup"] = pd.cut(
    df["AgeFilled"],
    bins=[-1, 17, 60, 200],
    labels=["Child", "Adult", "Senior"],
)
by_age_group = df.groupby("AgeGroup")["Survived"].mean()
for group, rate in by_age_group.items():
    print(f"   {group}: {rate*100:.1f}%")
print()

print("09) Among 3rd class, survival rate for men vs women")
third_class = df[df["Pclass"] == 3]
third_by_sex = third_class.groupby("Sex")["Survived"].mean()
print(f"   Women: {third_by_sex.get('female')*100:.1f}%")
print(f"   Men  : {third_by_sex.get('male')*100:.1f}%")
print()

print("10) Drop rows with missing Cabin: remaining rows and % kept")
kept = df.dropna(subset=["Cabin"])
kept_rows = len(kept)
print("   Rows remaining:", kept_rows)
print(f"   % kept: {pct(kept_rows, total_rows):.1f}%")

