score = 72

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print("Score:", score, "Grade:", grade)


# Yaha per score ek list hai jo k pending hai abhi seekhna
scores = [95, 82, 67, 74]

# s ek temporary variable hai jo list ke har element ko represent karega
for s in scores:
    if s >= 90:
        grade = "A"
    elif s >= 80:
        grade = "B"
    elif s >= 70:
        grade = "C"
    else:
        grade = "F"
    print("Score:", s, "Grade:", grade)



# Imagine apky pass ek classifier ki list hai about predicted probablities aur apko unko classify karna hai :
    # Find out: How many are high(>= 0.9), medium(between 0.7 and 0.9), low(<0.7)

pred_probs = [0.95, 0.3, 0.8, 1.2, -0.1, 0.72, 0.99]

high = 0
medium = 0
low = 0
invalid = 0

for p in pred_probs:
    if p < 0 or p > 1:
        invalid += 1
        # Baaki loop iterations ko skip kar do 
        continue  

    if p >= 0.9:
        high += 1
    elif p >= 0.7:
        medium += 1
    else:
        low += 1

print("High confidence:", high)
print("Medium confidence:", medium)
print("Low confidence:", low)
print("Invalid values:", invalid)


# EARLY STOPPING ek technique hai jo hum ML mie use kerty: 
    # Ismie automatically app model ko train kerna band ker detay ho 
    # Yeh technique OVERFITTING ko prevent karne ke liye use hoti hai.