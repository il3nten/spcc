# Exp 1: Data Warehouse, Data Mart
import pandas as pd
# ---------- SOURCE TABLES ----------
customer = pd.DataFrame({
    "CustomerID": ["C1", "C2", "C3"],
    "Name": ["Rahul", "Amit", "Priya"],
    "City": ["Mumbai", "Pune", "Mumbai"]
})

product = pd.DataFrame({
    "ProductID": ["P1", "P2", "P3"],
    "Product": ["Laptop", "Mouse", "Keyboard"],
    "Category": ["Electronics", "Accessories", "Accessories"]
})

sales = pd.DataFrame({
    "SaleID": [1, 2, 3, 4],
    "CustomerID": ["C1", "C2", "C3", "C1"],
    "ProductID": ["P1", "P2", "P3", "P2"],
    "Date": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
    "Quantity": [1, 2, 1, 1],
    "Amount": [50000, 2000, 3000, 1000]
})

# ---------- DIMENSION TABLES ----------
dim_customer = customer
dim_product = product

dim_date = pd.DataFrame({
    "Date": ["2026-01-01", "2026-01-02",
             "2026-01-03", "2026-01-04"],
    "Month": ["Jan"] * 4,
    "Year": [2026] * 4
})	# ---------- FACT TABLE ----------
fact_sales = sales.merge(dim_customer, on="CustomerID") \
                  .merge(dim_product, on="ProductID")

print("\n--- SALES FACT TABLE ---")
print(fact_sales)

# ---------- SNOWFLAKE ----------
dim_category = pd.DataFrame({
    "CategoryID": ["CAT1", "CAT2"],
    "Category": ["Electronics", "Accessories"]
})

dim_product_snowflake = product.merge(
    dim_category, on="Category"
)

print("\n--- SNOWFLAKE PRODUCT ---")
print(dim_product_snowflake)

# ---------- FACT CONSTELLATION ----------
returns = pd.DataFrame({
    "ReturnID": [1, 2],
    "CustomerID": ["C1", "C2"],
    "ProductID": ["P2", "P3"],
    "ReturnAmount": [1000, 3000]
})

print("\n--- RETURN FACT TABLE ---")
print(returns)

# Now understand exactly what the code is doing
# Don't try to memorize the code blindly. Understand these 5 blocks.
# ________________________________________
# 1. Source Tables
# customer = pd.DataFrame(...)product = pd.DataFrame(...)sales = pd.DataFrame(...)
# These represent the operational/source data from which our warehouse is built.
# We have:
# Customer
# Product
# Sales
# For example:
# Customer
# C1 → Rahul → Mumbai

# Product
# P1 → Laptop → Electronics

# Sales
# C1 bought P1 for ₹50,000
# The data is deliberately tiny because we don't need a real dataset during the practical.
# ________________________________________
# 2. Dimension Tables
# We create:
# dim_customer = customerdim_product = product
# These are our dimensions.
# A dimension describes who, what, where, or when.
# Customer dimension
# CustomerID
# Name
# City
# Answers:
# Who purchased?
# Product dimension
# ProductID
# Product
# Category
# Answers:
# What was purchased?
# Date dimension
# Date
# Month
# Year
# Answers:
# When was it purchased?
# So conceptually:
#              DIMENSIONS

#         Customer
#            ↓
#         Product
#            ↓
#           Date
# ________________________________________
# 3. Fact Table
# This is the most important part.
# fact_sales = sales.merge(dim_customer, on="CustomerID") \                  .merge(dim_product, on="ProductID")
# We are combining the sales information with the dimensions.
# The fact table contains measurable business events.
# Our important measures are:
# Quantity
# Amount
# For example:
# SaleID = 1
# Customer = C1
# Product = P1
# Quantity = 1
# Amount = 50000
# So:
# Sales is our fact because it records a business event and contains numerical measures such as Quantity and Amount.
# ________________________________________
# 4. Star Schema
# Our main warehouse can be represented as:
#               DIM_CUSTOMER
#                     |
#                     |
# DIM_PRODUCT ---- FACT_SALES
#                     |
#                     |
#                  DIM_DATE
# More conceptually:
#                  Customer
#                     |
#                     |
# Product -------- Sales -------- Date
# The fact table is at the center and dimensions surround it.
# That's why it's called a:
# Star Schema
# Viva answer
# Q: What is a Star Schema?
# A Star Schema consists of one central fact table connected directly to multiple dimension tables.
# ________________________________________
# 5. Snowflake Schema
# Now look at:
# dim_category = pd.DataFrame({    "CategoryID": ["CAT1", "CAT2"],    "Category": ["Electronics", "Accessories"]})
# Previously:
# Product
# ----------------
# ProductID
# Product
# Category
# We split the category information into another table.
# So now:
# DIM_PRODUCT
#      |
#      ↓
# DIM_CATEGORY
# Conceptually:
#                     DIM_CATEGORY
#                          |
#                          |
#                     DIM_PRODUCT
#                          |
#                          |
# DIM_CUSTOMER ------ FACT_SALES ------ DIM_DATE
# This is Snowflake Schema.
# Why?
# Because the dimension has been normalized into additional related tables.
# Viva answer
# Q: Difference between Star and Snowflake?
# In Star Schema, dimensions are generally denormalized and directly connected to the fact table. In Snowflake Schema, dimensions are normalized into additional related tables.
# ________________________________________
# 6. Fact Constellation
# Now we create another fact table:
# returns = pd.DataFrame({    "ReturnID": [1, 2],    "CustomerID": ["C1", "C2"],    "ProductID": ["P2", "P3"],    "ReturnAmount": [1000, 3000]})
# We now have:
# FACT_SALES
#     |
#     |
#     ├──── Customer
#     |
#     └──── Product


# FACT_RETURNS
#     |
#     |
#     ├──── Customer
#     |
#     └──── Product
# Both fact tables can use the same dimensions.
# Therefore:
#              DIM_CUSTOMER
#               /         \
#              /           \
#       FACT_SALES       FACT_RETURNS
#              \           /
#               \         /
#               DIM_PRODUCT
# This is a:
# Fact Constellation / Galaxy Schema
# Viva answer
# Q: What is Fact Constellation?
# It contains multiple fact tables that share common dimension tables.

# Exp 2: Perform OLAP operations
import pandas as pd

# Sales data
df = pd.DataFrame({
    "Year": [2025,2025,2025,2025,2026,2026,2026,2026],
    "City": ["Mumbai","Mumbai","Pune","Pune",
             "Mumbai","Mumbai","Pune","Pune"],
    "Product": ["Laptop","Mouse","Laptop","Mouse",
                "Laptop","Mouse","Laptop","Mouse"],
    "Sales": [50000,2000,45000,3000,60000,2500,55000,3500]
})

# 1. SLICE - select one year
slice_data = df[df["Year"] == 2026]
print("\n--- SLICE ---")
print(slice_data)

# 2. DICE - select multiple conditions
dice_data = df[(df["Year"] == 2026) &
               (df["City"].isin(["Mumbai","Pune"])) &
               (df["Product"] == "Laptop")]
print("\n--- DICE ---")
print(dice_data)
	
# 3. ROLL-UP - summarize sales by Year
rollup = df.groupby("Year")["Sales"].sum()
print("\n--- ROLL-UP ---")
print(rollup)

# 4. DRILL-DOWN - Year → City → Product
drilldown = df.groupby(
    ["Year", "City", "Product"]
)["Sales"].sum()
print("\n--- DRILL-DOWN ---")
print(drilldown)

# 5. PIVOT - Year vs City
pivot = pd.pivot_table(
    df,
    values="Sales",
    index="Year",
    columns="City",
    aggfunc="sum"
)
print("\n--- PIVOT ---")
print(pivot)


# This is more important than memorizing the code.
# ________________________________________
# ① SLICE
# Meaning
# Slice selects one particular value from one dimension.
# Our code:
# slice_data = df[df["Year"] == 2026]
# We're saying:
# Give me only sales for the year 2026.
# Original:
# 2025 Mumbai Laptop
# 2025 Mumbai Mouse
# 2025 Pune   Laptop
# 2025 Pune   Mouse
# 2026 Mumbai Laptop
# 2026 Mumbai Mouse
# 2026 Pune   Laptop
# 2026 Pune   Mouse
# After slicing:
# 2026 Mumbai Laptop
# 2026 Mumbai Mouse
# 2026 Pune   Laptop
# 2026 Pune   Mouse
# Easy way to remember
# SLICE = ONE dimension value
# Example:
# All sales in 2026.
# ________________________________________
# ② DICE
# Dice applies multiple conditions.
# Our code:
# dice_data = df[    (df["Year"] == 2026) &    (df["City"].isin(["Mumbai","Pune"])) &    (df["Product"] == "Laptop")]
# We're asking:
# Give me Laptop sales in 2026 for Mumbai and Pune.
# Result:
# 2026 Mumbai Laptop 60000
# 2026 Pune   Laptop 55000
# Easy memory trick
# SLICE → one cut
# DICE  → multiple cuts
# Viva question
# Q: Difference between Slice and Dice?
# Answer:
# Slice selects a single value from one dimension, whereas Dice selects a subset using multiple dimensions or conditions.
# ________________________________________
# ③ ROLL-UP
# Roll-up means aggregation.
# We're going from detailed data:
# City + Product
# to a higher-level summary:
# Year
# Code:
# rollup = df.groupby("Year")["Sales"].sum()
# Let's calculate it.
# 2025
# 50000 + 2000 + 45000 + 3000
# = 100000
# 2026
# 60000 + 2500 + 55000 + 3500
# = 121000
# Output:
# 2025    100000
# 2026    121000
# So:
# Detailed
#    ↓
# Summarized
# Memory trick
# Roll-up = Zoom OUT
# You're moving upward in the hierarchy.
# ________________________________________
# ④ DRILL-DOWN
# Drill-down is the opposite.
# You start with:
# Year
# and move towards:
# Year → City → Product
# Our code:
# drilldown = df.groupby(    ["Year", "City", "Product"])["Sales"].sum()
# Output conceptually:
# 2025
#  ├── Mumbai
#  │    ├── Laptop → 50000
#  │    └── Mouse  → 2000
#  │
#  └── Pune
#       ├── Laptop → 45000
#       └── Mouse  → 3000

# 2026
#  ├── Mumbai
#  │    ├── Laptop → 60000
#  │    └── Mouse  → 2500
#  │
#  └── Pune
#       ├── Laptop → 55000
#       └── Mouse  → 3500
# Memory trick
# Drill-down = Zoom IN
# You're getting increasingly detailed information.
# ________________________________________
# ⑤ PIVOT
# Pivot changes the orientation/view of the data.
# Our code:
# pivot = pd.pivot_table(    df,    values="Sales",    index="Year",    columns="City",    aggfunc="sum")
# Output:
# City    Mumbai   Pune
# Year
# 2025    52000    48000
# 2026    62500    58500
# Notice what happened.
# Original:
# Year | City | Product | Sales
# Now we have:
#              City
#           Mumbai   Pune
# Year
# 2025       52000  48000
# 2026       62500  58500
# We're simply viewing the same information from another orientation.
# Memory trick
# Pivot = Rotate the view
# It doesn't fundamentally change the data.


# Exp 4: Linear Regression
import numpy as np
from sklearn.linear_model import LinearRegression

# Dataset
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([35, 40, 50, 55, 65])

# Create and train model
model = LinearRegression()
model.fit(X, y)

# Model parameters
print("Slope:", model.coef_[0])
print("Intercept:", model.intercept_)

# Prediction
hours = np.array([[6]])
prediction = model.predict(hours)

print("Predicted marks for 6 hours:", prediction[0])

# Step 1 — Import NumPy
# import numpy as np
# We use NumPy to create the input arrays.
# ________________________________________
# Step 2 — Import Linear Regression
# from sklearn.linear_model import LinearRegression
# This provides the Linear Regression algorithm.
# ________________________________________
# 5. Create the Dataset
# X = np.array([[1], [2], [3], [4], [5]])y = np.array([35, 40, 50, 55, 65])
# Here:
# X = Hours Studied
# y = Marks
# Notice that X is written as:
# [[1], [2], [3], [4], [5]]
# rather than:
# [1, 2, 3, 4, 5]
# because scikit-learn expects the input features in the form:
# [number of samples × number of features]
# Here we have:
# 5 samples
# 1 feature
# So:
# \[ X = 5 \times 1 \]
# ________________________________________
# 6. Create the Model
# model = LinearRegression()
# This creates the Linear Regression model.
# At this point, the model hasn't learned anything yet.
# ________________________________________
# 7. Train the Model
# model.fit(X, y)
# This is the most important line.
# The model looks at:
# Hours → Marks
# and finds the best-fit line:
# \[ y = mx+c \]
# It calculates the appropriate:
# m → slope
# c → intercept
# ________________________________________
# 8. Display Slope
# model.coef_[0]
# This gives \(m\).
# The slope tells us approximately:
# How much the predicted marks change when study hours increase by one hour.
# For example, if:
# Slope ≈ 7
# then increasing study time by one hour increases predicted marks by approximately 7 marks according to the learned model.
# ________________________________________
# 9. Display Intercept
# model.intercept_
# This gives \(c\).
# So our learned equation will be approximately:
# \[ Marks = m(Hours) + c \]
# ________________________________________
# 10. Prediction
# This is the actual purpose of the model.
# hours = np.array([[6]])prediction = model.predict(hours)
# We're asking:
# If a student studies for 6 hours, what marks does the model predict?
# Then:
# print(prediction[0])
# prints the predicted value.
# ________________________________________
# 11. Expected Output
# You'll get something approximately like:
# Slope: 7.5
# Intercept: 26.5
# Predicted marks for 6 hours: 71.5
# The exact values depend on the dataset.
# The important thing is:
# Training Data
#      ↓
# Linear Regression
#      ↓
# Best-fit line
#      ↓
# New input = 6 hours
#      ↓
# Predicted marks
# ________________________________________
# 12. What is Actually Happening Mathematically?
# The model tries to minimize the prediction error.
# For every point:
# \[ Error = Actual - Predicted \]
# The standard Linear Regression approach minimizes the sum of squared errors:
# \[ SSE = \sum (y_i-\hat{y_i})^2 \]
# where:
# •	\(y_i\) = actual value
# •	\(\hat y_i\) = predicted value
# The resulting line is the best-fit line.
# You probably don't need to manually calculate this for this practical unless your faculty specifically asks for mathematical calculation.
# ________________________________________
# 13. Optional Graph
# If your examiner asks for visualization, we can add this:
# import matplotlib.pyplot as pltplt.scatter(X, y)plt.plot(X, model.predict(X))plt.xlabel("Hours Studied")plt.ylabel("Marks")plt.title("Linear Regression")plt.show()
# This produces:
# Marks
#   |
# 70|                         ●
# 60|                    ●
# 50|              ●
# 40|        ●
# 30|   ●
#   |
#   +------------------------------
#       1    2    3    4    5
#            Hours
# But I would not put the graph in the base code unless required. The first version is faster to write.

# Exp 6: Design Clustering Hierarchical method 

import numpy as np
from sklearn.cluster import AgglomerativeClustering

# Dataset
X = np.array([
    [1, 1],
    [2, 1],
    [5, 5],
    [6, 5],
    [10, 10]
])

# Create model
model = AgglomerativeClustering(n_clusters=2)

# Perform clustering
labels = model.fit_predict(X)

# Display results
points = ["A", "B", "C", "D", "E"]

for point, label in zip(points, labels):
    print(point, "-> Cluster", label)

# Step 1 — Import NumPy
# import numpy as np
# We use NumPy to store our coordinate data.
# ________________________________________
# Step 2 — Import the algorithm
# from sklearn.cluster import AgglomerativeClustering
# This gives us the hierarchical clustering algorithm.
# ________________________________________
# 5. Dataset
# X = np.array([    [1, 1],    [2, 1],    [5, 5],    [6, 5],    [10, 10]])
# Each row represents one point:
# A = (1,1)
# B = (2,1)
# C = (5,5)
# D = (6,5)
# E = (10,10)
# ________________________________________
# 6. Create the Model
# model = AgglomerativeClustering(n_clusters=2)
# We're telling the algorithm:
# Divide the data into 2 clusters.
# ________________________________________
# 7. Perform Clustering
# labels = model.fit_predict(X)
# This does two things:
# fit
# The algorithm analyzes the relationships between points.
# predict
# It assigns each point to a cluster.
# So labels might be:
# [0, 0, 1, 1, 1]
# Meaning:
# A → Cluster 0
# B → Cluster 0

# C → Cluster 1
# D → Cluster 1
# E → Cluster 1
# Remember:
# Cluster numbers have no inherent meaning.
# It could instead produce:
# [1, 1, 0, 0, 0]
# and that's equally correct.
# ________________________________________
# 8. Display Results
# for point, label in zip(points, labels):    print(point, "-> Cluster", label)
# This simply combines:
# A + its cluster
# B + its cluster
# ...
# to make the output easy to understand.
# ________________________________________
# 9. Expected Output
# You may get:
# A -> Cluster 0
# B -> Cluster 0
# C -> Cluster 1
# D -> Cluster 1
# E -> Cluster 1
# The exact cluster numbers may be reversed:
# A -> Cluster 1
# B -> Cluster 1
# C -> Cluster 0
# D -> Cluster 0
# E -> Cluster 0
# That is not an error.
# ________________________________________




# Exp 7: Design Apriori Algorithm

# // using external libraries
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Mock transaction dataset
df = pd.DataFrame({
    "Milk":   [1, 1, 0, 1, 1],
    "Bread":  [1, 1, 1, 1, 1],
    "Butter": [0, 1, 1, 1, 0],
    "Eggs":   [0, 0, 1, 0, 1]
})

# Convert 0/1 values to Boolean
df = df.astype(bool)

# Generate frequent itemsets
frequent_itemsets = apriori(
    df,
    min_support=0.40,
    use_colnames=True
)

print("Frequent Itemsets:")
print(frequent_itemsets)

# Generate association rules
rules = association_rules(
    frequent_itemsets,
    metric="confidence",
    min_threshold=0.60
)

print("\nAssociation Rules:")
print(rules[
    ["antecedents", "consequents",
     "support", "confidence", "lift"]
])

#  1. Understand the Dataset
# We have 5 transactions:
# T	Milk	Bread	Butter	Eggs
# T1	1	1	0	0
# T2	1	1	1	0
# T3	0	1	1	1
# T4	1	1	1	0
# T5	1	1	0	1
# 1 means the customer purchased the item.
# 0 means they didn't.
# For example:
# T2 = Milk + Bread + Butter
# ________________________________________
# 2. Why are we using 0 and 1?
# Apriori needs to know whether an item is present or absent in each transaction.
# So:
# 1 → item present
# 0 → item absent
# Then:
# df = df.astype(bool)
# converts:
# 1 → True
# 0 → False
# which is the format expected by mlxtend.
# ________________________________________
# 3. The Important Part — Apriori
# frequent_itemsets = apriori(    df,    min_support=0.40,    use_colnames=True)
# There are three important things here.
# df
# Our transaction dataset.
# min_support=0.40
# We're saying:
# An itemset must appear in at least 40% of transactions to be considered frequent.
# We have 5 transactions.
# Therefore:
# \[ 5 \times 0.40 = 2 \]
# So an itemset must occur in at least 2 transactions.
# use_colnames=True
# Without this, the output may represent items using column indexes.
# With it, we get meaningful results such as:
# {Milk, Bread}
# instead of:
# {0, 1}
# ________________________________________
# 4. What Frequent Itemsets Will We Get?
# Let's manually understand a few.
# Milk
# Milk occurs in:
# T1
# T2
# T4
# T5
# So:
# \[ Support(Milk)=\frac{4}{5}=0.8 \]
# Therefore it is frequent.
# ________________________________________
# Bread
# Bread occurs in all 5:
# \[ Support(Bread)=\frac{5}{5}=1.0 \]
# Frequent.
# ________________________________________
# Butter
# Butter occurs in:
# T2
# T3
# T4
# Therefore:
# \[ Support(Butter)=\frac35=0.6 \]
# Frequent.
# ________________________________________
# Eggs
# Eggs occurs in:
# T3
# T5
# Therefore:
# \[ Support(Eggs)=\frac25=0.4 \]
# Also frequent because our threshold is 0.40.
# ________________________________________
# Milk + Bread
# They occur together in:
# T1
# T2
# T4
# T5
# Therefore:
# \[ Support(Milk,Bread)=\frac45=0.8 \]
# Frequent.
# ________________________________________
# 5. Association Rules
# Now this:
# rules = association_rules(    frequent_itemsets,    metric="confidence",    min_threshold=0.60)
# takes the frequent itemsets and generates rules.
# For example:
# Milk → Bread
# or:
# Butter → Bread
# ________________________________________
# 6. What does metric="confidence" mean?
# We're telling association_rules():
# Generate rules based on confidence.
# And:
# min_threshold=0.60
# means:
# Only show rules whose confidence is at least 60%.
# ________________________________________
# 7. Understanding the Output Columns
# We print:
# rules[    ["antecedents", "consequents",     "support", "confidence", "lift"]]
# antecedents
# The IF part.
# Example:
# {Milk}
# in:
# Milk → Bread
# ________________________________________
# consequents
# The THEN part.
# {Bread}
# ________________________________________
# support
# How frequently the entire combination occurs.
# For:
# Milk → Bread
# this means:
# \[ Support(Milk,Bread) \]
# ________________________________________
# confidence
# How often Bread occurs when Milk occurs.
# \[ Confidence(Milk\rightarrow Bread) = \frac{Support(Milk,Bread)} {Support(Milk)} \]
# For our data:
# \[ =\frac{0.8}{0.8}=1 \]
# So:
# Confidence = 1.0 = 100%
# ________________________________________
# lift
# Measures the strength of the association.
# \[ Lift(A\rightarrow B) = \frac{Confidence(A\rightarrow B)} {Support(B)} \]
# General interpretation:
# Lift > 1  → positive association
# Lift = 1  → no significant association
# Lift < 1  → negative association
# ________________________________________
# 8. Expected Output
# The exact ordering can vary, but you'll see something like:
# Frequent Itemsets:

#     support              itemsets
# 0     0.8                  (Milk)
# 1     1.0                  (Bread)
# 2     0.6                  (Butter)
# 3     0.4                  (Eggs)
# 4     0.8                  (Milk, Bread)
# 5     0.4                  (Milk, Butter)
# 6     0.6                  (Bread, Butter)
# 7     0.4                  (Bread, Eggs)
# ...

# Association Rules:

#   antecedents consequents support confidence lift
#   {Milk}      {Bread}      0.8     1.00       1.0
#   {Butter}    {Bread}      0.6     1.00       1.0
#   ...
# Don't memorize the exact output. The values depend on the dataset.
# ________________________________________
# 9. Why I Prefer This Dataset Over glass.csv
# Your original code:
# df = pd.read_csv("glass.csv")
# followed by:
# df = df.apply(lambda x: x > x.mean()).astype(bool)
# is technically possible, but it's not ideal for your practical.
# The problem is that the examiner could ask:
# "Why are you comparing each value with the column mean?"
# And you'd have to explain that you're converting continuous numerical features into Boolean transaction-like data.
# Our version is much cleaner:
# Customer purchases
#         ↓
# 0 / 1 transaction matrix
#         ↓
# Apriori
#         ↓
# Frequent itemsets
#         ↓
# Association rules
# It is a proper market-basket scenario and requires almost no explanation.
# ________________________________________
# 10. If the Examiner Asks "Why 0.40?"
# Say:
# "I selected a minimum support of 40% for this small dataset. Since there are five transactions, an itemset must occur in at least two transactions to be considered frequent."
# That's a very good answer.
# ________________________________________
# 11. If They Ask "Why mlxtend?"
# Say:
# "mlxtend provides an implementation of the Apriori algorithm and association-rule generation, allowing us to efficiently obtain frequent itemsets and rules."
# ________________________________________
# 12. If They Ask "What is the Apriori Principle?"
# This is the most important theory question:
# If an itemset is infrequent, all of its supersets will also be infrequent.
# Example:
# {Milk, Butter} = infrequent

# Therefore:

# {Milk, Butter, Bread}
# cannot be frequent.
# This allows Apriori to reduce the search space.
# ________________________________________

