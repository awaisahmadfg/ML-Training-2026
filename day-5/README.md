## day-5: titanic dataset analysis

I analyzed the Titanic dataset in `analysis.py` and answered all 10 questions with pandas.

### Most surprising finding

The biggest surprise was the survival gap by gender:
- Women survival rate was about **74%**
- Men survival rate was about **19%**

That is a very large difference, and it clearly shows survival was not random.

### What I would investigate next

If I had more time, I would explore:
- **Class + gender together** (for example: 1st class women vs 3rd class men)
- **Family size effect** (`SibSp + Parch`) to see if traveling alone changed survival odds
- **Fare impact** to check whether higher ticket price linked to better survival chance
- A simple **prediction model** (logistic regression) to measure which features mattered most
