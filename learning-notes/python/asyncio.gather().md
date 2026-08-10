# asyncio.gather()

## What is asyncio.gather()?

`asyncio.gather()` Python asyncio ka function hai jo multiple async operations ko **concurrently run/progress** karwata hai aur phir un sab ke results ka wait karta hai.

Simple words:

> Multiple independent async kaam hain → unko ek saath start/progress karo → sab complete hone par results lo.

---

## Why do we need it?

Suppose 2 API calls hain:

```python
users = await get_users()       # 2 sec
products = await get_products() # 3 sec
```

Ye sequentially chalenge:

```text
get_users
   ↓
  2 sec
   ↓
get_products
   ↓
  3 sec
```

Total:

```text
2 + 3 = 5 sec
```

Lekin dono independent hain, isliye hum unko concurrently chala sakte hain:

```python
users, products = await asyncio.gather(
    get_users(),
    get_products()
)
```

Ab roughly:

```text
get_users   ────────── 2 sec
get_products ───────────────── 3 sec

Total ≈ 3 sec
```

---

# Basic Example

```python
import asyncio


async def get_users():
    await asyncio.sleep(2)
    return ["Ali", "Ahmed"]


async def get_products():
    await asyncio.sleep(3)
    return ["Laptop", "Phone"]


async def main():

    users, products = await asyncio.gather(
        get_users(),
        get_products()
    )

    print(users)
    print(products)


asyncio.run(main())
```

Output:

```text
['Ali', 'Ahmed']
['Laptop', 'Phone']
```

Total time approximately **3 seconds** instead of 5 seconds.

---

# How it works

```text
                 asyncio.gather()
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Task A        Task B       Task C
          │            │            │
          ↓            ↓            ↓
        async         async         async
          │            │            │
          └────────────┼────────────┘
                       ↓
                 All completed
                       ↓
                    Results
```

---

# Important: Result Order

Suppose:

```python
async def A():
    await asyncio.sleep(3)
    return "A"


async def B():
    await asyncio.sleep(1)
    return "B"
```

```python
a, b = await asyncio.gather(
    A(),
    B()
)
```

`B` pehle complete hoga:

```text
B → 1 sec
A → 3 sec
```

Lekin results input order mein milenge:

```python
a == "A"
b == "B"
```

So:

> Completion order aur result order different ho sakta hai.

---

# Sequential await vs gather()

## Sequential

```python
a = await A()
b = await B()
c = await C()
```

Flow:

```text
A ──────
        B ─────────
                  C ───
```

Total time:

```text
A + B + C
```

---

## gather()

```python
a, b, c = await asyncio.gather(
    A(),
    B(),
    C()
)
```

Flow:

```text
A ─────────
B ─────────────
C ─────

Total ≈ longest operation
```

Approximately:

```text
max(A, B, C)
```

---

# gather() vs create_task()

## create_task()

```python
task = asyncio.create_task(
    get_users()
)
```

Simple meaning:

> Coroutine ko Task bana kar schedule karo.

---

## gather()

```python
users, products = await asyncio.gather(
    get_users(),
    get_products()
)
```

Simple meaning:

> Multiple async operations ko collectively run/progress karo aur results collect karo.

Mental model:

```text
create_task()
     ↓
"Is kaam ko schedule karo"


gather()
     ↓
"Multiple kaamon ko
collectively wait/collect karo"
```

---

# gather() + create_task()

Dono saath bhi use ho sakte hain:

```python
task1 = asyncio.create_task(get_users())
task2 = asyncio.create_task(get_products())

users, products = await asyncio.gather(
    task1,
    task2
)
```

Lekin simple case mein direct `gather()` cleaner hai:

```python
users, products = await asyncio.gather(
    get_users(),
    get_products()
)
```

---

# Real AI Backend Example

RAG chatbot mein user question ke liye multiple independent operations ho sakti hain:

```text
                User Question
                      │
                      ↓
              asyncio.gather()
             /       |        \
            ↓        ↓         ↓
         User     History   Vector Search
          Data      Data       Results
             \       |        /
              \      |       /
               └─────┼──────┘
                     ↓
                    LLM
                     ↓
                   Answer
```

Code:

```python
async def answer_question(user_id, question):

    user, history, documents = await asyncio.gather(

        get_user(user_id),

        get_chat_history(user_id),

        vector_search(question)
    )

    answer = await call_llm(
        user=user,
        history=history,
        documents=documents,
        question=question
    )

    return answer
```

Yahan:

```text
get_user()
get_chat_history()
vector_search()
```

independent hain, isliye `gather()` useful hai.

---

# When to use gather()

Use `gather()` when:

- Multiple async operations independent hon.
- Sab ke results chahiye hon.
- APIs ko concurrently call karna ho.
- Multiple database/Redis calls karni hon.
- RAG mein multiple sources se data fetch karna ho.
- Dashboard ke multiple APIs ko fetch karna ho.

Example:

```python
results = await asyncio.gather(
    get_users(),
    get_orders(),
    get_revenue()
)
```

---

# When NOT to use gather()

Agar ek operation ka result doosre operation ke liye required ho:

```text
Get User
   ↓
Get User ID
   ↓
Get Orders
```

To sequentially:

```python
user = await get_user()

orders = await get_orders(
    user["id"]
)
```

Yahan `get_orders()` ko user ka result chahiye.

---

# Error Handling

Normally agar ek operation exception raise kare:

```python
results = await asyncio.gather(
    A(),
    B(),
    C()
)
```

to exception propagate ho sakti hai.

Agar exceptions ko results ke andar receive karna ho:

```python
results = await asyncio.gather(
    A(),
    B(),
    C(),
    return_exceptions=True
)
```

Possible result:

```python
[
    "A result",
    ValueError("Something went wrong"),
    "C result"
]
```

Iska use carefully karna chahiye, especially critical operations ke liye.

---

# Large Number of Tasks

Ye avoid karo:

```python
await asyncio.gather(
    *[call_api(item) for item in huge_list]
)
```

Agar thousands/millions operations hon to:

- Memory issue
- API rate limit
- Database overload
- Connection exhaustion
- External service throttling

ho sakta hai.

Production mein concurrency limit ke liye `asyncio.Semaphore`, queues ya connection pools use kiye ja sakte hain.

Example:

```python
semaphore = asyncio.Semaphore(10)


async def limited_call(item):

    async with semaphore:
        return await call_api(item)
```

Ab maximum roughly 10 operations ek waqt mein active rakhne ka control hai.

---

# JavaScript Comparison

Python:

```python
users, products = await asyncio.gather(
    get_users(),
    get_products()
)
```

JavaScript:

```javascript
const [users, products] = await Promise.all([
    getUsers(),
    getProducts()
]);
```

Conceptually:

```text
Python                 JavaScript

asyncio.gather()   ≈   Promise.all()
```

Dono ka common purpose:

```text
Multiple independent async operations
              ↓
       Concurrent progress
              ↓
          Wait for all
              ↓
           Results
```

---

# Important Concepts

```text
Coroutine
    ↓
create_task()
    ↓
Task
    ↓
Event Loop
```

Aur multiple async operations:

```text
Coroutine A ──┐
Coroutine B ──┼──→ asyncio.gather()
Coroutine C ──┘
                    ↓
              All results
```

---

# Key Difference

### `await`

```python
result = await operation()
```

> Ek operation ka result wait karo.

### `create_task()`

```python
task = asyncio.create_task(operation())
```

> Coroutine ko Task bana kar schedule karo.

### `gather()`

```python
results = await asyncio.gather(
    operation_a(),
    operation_b(),
    operation_c()
)
```

> Multiple async operations ko collectively run/wait karke results collect karo.

---

# Important Note

`asyncio.gather()`:

- Thread create nahi karta.
- Process create nahi karta.
- CPU-heavy code automatically faster nahi karta.
- Mainly I/O-bound async operations ke liye useful hai.

Examples of I/O:

```text
API request
Database query
Redis
File/network I/O
Vector database
LLM API
```

---

# Quick Mental Model

```text
Multiple independent async jobs
              ↓
       asyncio.gather()
              ↓
      Run/progress together
              ↓
        Wait for all
              ↓
       Results together
```

## One-line summary

> **`asyncio.gather()` multiple independent async operations ko concurrently progress karwata hai aur unke results collectively return karta hai.**
