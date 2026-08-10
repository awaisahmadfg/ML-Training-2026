# asyncio.create_task()

## 1. Previous Concept Mein Problem

Hum already jaante hain:

```python
async def task_a():
    await asyncio.sleep(3)


async def task_b():
    await asyncio.sleep(2)
```

Agar:

```python
await task_a()
await task_b()
```

likhen:

```text
A
 ↓
WAIT 3 sec
 ↓
A complete
 ↓
B
 ↓
WAIT 2 sec
 ↓
B complete
```

Total approximately:

```text
3 + 2 = 5 seconds
```

Lekin agar A aur B independent hain, to hum chahte hain:

```text
A → WAIT
B → WAIT

Dono waiting periods overlap karein.
```

Yahan `asyncio.create_task()` useful hota hai.

---

# 2. `create_task()` Kya Problem Solve Karta Hai?

Simple definition:

> `asyncio.create_task()` ek coroutine ko asyncio Task mein schedule karta hai taa-ke Event Loop usay doosre async work ke saath concurrently progress kar sake.

Simple words:

> "Is async kaam ko schedule kar do, main meanwhile doosra kaam kar raha hoon."

---

# 3. Basic Example

```python
import asyncio


async def task_a():

    print("A started")

    await asyncio.sleep(3)

    print("A finished")


async def task_b():

    print("B started")

    await asyncio.sleep(2)

    print("B finished")


async def main():

    a = asyncio.create_task(task_a())

    b = asyncio.create_task(task_b())

    await a
    await b


asyncio.run(main())
```

Possible output:

```text
A started
B started
B finished
A finished
```

Total approximately:

```text
3 seconds
```

instead of:

```text
5 seconds
```

---

# 4. Ye Kaise Hua?

Timeline:

```text
Time →

A: ███████████████
   start       finish
   0 sec       3 sec

B: ██████████
   start   finish
   0 sec   2 sec
```

Dono tasks ka waiting time overlap kar raha hai.

---

# 5. Coroutine vs Task

Ye distinction bohat important hai.

### Coroutine

```python
coro = task_a()
```

Mental model:

```text
Coroutine Object
```

### Task

```python
task = asyncio.create_task(
    task_a()
)
```

Mental model:

```text
Coroutine
    ↓
create_task()
    ↓
Task
    ↓
Event Loop
```

Task coroutine ko schedule aur track karta hai.

---

# 6. Direct `await` vs `create_task()`

### Direct await

```python
await task_a()
```

Mental model:

> "Mujhe is operation ko await karna hai."

Agar immediately doosra:

```python
await task_b()
```

hai, to flow sequential ho sakta hai.

---

### `create_task()`

```python
a = asyncio.create_task(task_a())

b = asyncio.create_task(task_b())

await a
await b
```

Mental model:

```text
A ko schedule karo
 ↓
B ko schedule karo
 ↓
Dono Event Loop par progress kar sakte hain
 ↓
Results ka wait karo
```

---

# 7. Real AI Backend Example

Suppose RAG chatbot ko ye 3 cheezein chahiye:

```text
1. User permissions
2. Chat history
3. Vector search
```

Agar ye independent hain:

```python
permission_task = asyncio.create_task(
    check_permission(user_id)
)

history_task = asyncio.create_task(
    get_chat_history(user_id)
)

search_task = asyncio.create_task(
    vector_search(question)
)
```

Phir results:

```python
permission = await permission_task
history = await history_task
documents = await search_task
```

Flow:

```text
                   User Request
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
     Permission      History      Vector Search
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                       LLM
                        ↓
                     Answer
```

Agar ye operations independent hain, concurrency latency improve kar sakti hai.

---

# 8. `create_task()` + `gather()`

Multiple results collect karne ke liye `asyncio.gather()` useful hai.

Example:

```python
results = await asyncio.gather(
    check_permission(user_id),
    get_chat_history(user_id),
    vector_search(question)
)
```

Concept:

```text
gather()
   ↓
Multiple async operations
   ↓
Concurrent progress
   ↓
Wait
   ↓
Results together
```

Agar task handles specifically chahiye:

```python
permission_task = asyncio.create_task(
    check_permission(user_id)
)

history_task = asyncio.create_task(
    get_chat_history(user_id)
)

search_task = asyncio.create_task(
    vector_search(question)
)

permission, history, documents = await asyncio.gather(
    permission_task,
    history_task,
    search_task
)
```

---

# 9. Important: `create_task()` Background Job Nahi Hai

Ye misconception avoid karo.

```python
task = asyncio.create_task(send_email())
```

iska matlab durable background job nahi.

Architecture:

```text
Process
  ↓
Event Loop
  ↓
Task
```

Agar process crash ho:

```text
Process dies
     ↓
Task also dies
```

Durable background jobs ke liye job queue / worker architecture use hota hai.

Examples:

```text
Celery
RQ
Cloud job systems
Worker processes
```

---

# 10. Kab `create_task()` Use Karna Hai?

Use when:

### 1. Operations independent hon

```text
API A
API B
API C
```

---

### 2. Sab async hon

```python
async def operation():
    ...
```

---

### 3. Tum unko concurrently start karna chahte ho

```python
task_a = asyncio.create_task(a())
task_b = asyncio.create_task(b())
```

---

### 4. Task object manage karna ho

For example:

- cancellation
- result
- exception
- status/lifecycle

---

# 11. Kab Use Nahi Karna?

Agar dependency ho:

```text
Get User
   ↓
User ID
   ↓
Get Orders
```

To:

```python
user = await get_user()

orders = await get_orders(
    user["id"]
)
```

better hai.

Yahan concurrency possible nahi kyun ke orders ke liye pehle user chahiye.

---

# 12. `create_task()` CPU Parallelism Nahi Hai

Ye:

```python
asyncio.create_task(
    heavy_cpu_work()
)
```

automatically:

```text
CPU Core 1
CPU Core 2
```

nahi banata.

Agar coroutine CPU-heavy kaam kare:

```text
Event Loop
    ↓
CPU Heavy Work
████████████████
    ↓
Other async tasks delayed
```

Isliye CPU-heavy workloads ke liye suitable process/worker/offloading architecture consider karo.

---

# 13. Common Mistake — Artificial Concurrency

Har async function ko task banana zaroori nahi.

Bad:

```python
task = asyncio.create_task(
    simple_operation()
)

result = await task
```

Agar tumhein immediately result hi chahiye aur parallelism ka koi benefit nahi:

```python
result = await simple_operation()
```

zyada simple hai.

---

# 14. Common Mistake — Fire and Forget

Example:

```python
asyncio.create_task(send_email())
```

Aur phir task ko completely ignore kar diya.

Potential problems:

```text
Exception
Cancellation
Application shutdown
Resource cleanup
```

Production code mein task lifecycle ko samajhna important hai.

---

# 15. Cancellation

Task cancel kiya ja sakta hai:

```python
task = asyncio.create_task(
    long_operation()
)

task.cancel()
```

Conceptually:

```text
Task
 ↓
cancel()
 ↓
Cancellation requested
 ↓
Coroutine cleanup/termination
```

Useful cases:

- Client disconnect
- Timeout
- Request no longer relevant
- Shutdown

---

# 16. Timeout

External API ko forever wait nahi karna chahiye.

Example:

```python
async with asyncio.timeout(10):

    result = await call_external_api()
```

Flow:

```text
API Call
   ↓
WAIT
   ↓
10 seconds
   ↓
Timeout
```

AI production systems mein timeout important hai kyun ke:

```text
LLM slow
Vector DB slow
External API slow
```

ho sakte hain.

---

# 17. Behind the Scenes

Simplified flow:

```text
Coroutine
    ↓
create_task()
    ↓
Task object
    ↓
Event Loop
    ↓
Run coroutine
    ↓
await network I/O
    ↓
Coroutine temporarily suspends
    ↓
Event Loop handles other work
    ↓
I/O ready
    ↓
Coroutine resumes
    ↓
Task completes
```

Important:

`create_task()` new thread nahi banata.

`create_task()` new process nahi banata.

---

# 18. JavaScript Comparison

JavaScript:

```javascript
const usersPromise = fetch("/users");

const productsPromise = fetch("/products");

const results = await Promise.all([
    usersPromise,
    productsPromise
]);
```

Python:

```python
results = await asyncio.gather(
    get_users(),
    get_products()
)
```

Conceptual similarity:

```text
JavaScript
Promise.all()

Python
asyncio.gather()
```

Lekin implementation internally different hai.

---

# 19. Real RAG Latency Example

Suppose:

```text
Permission check = 200ms
Chat history    = 300ms
Vector search   = 500ms
```

Sequential:

```text
200 + 300 + 500
= 1000ms
```

If independent and concurrent:

```text
max(200, 300, 500)
≈ 500ms
```

Actual production latency network conditions, connection pools, scheduling, database load etc. ki wajah se different hogi.

Lekin mental model:

```text
Sequential:

A ──────
        B ───────
                 C ─────────

Concurrent:

A ──────
B ─────────
C ─────────────────
```

---

# 20. Best Practices

- Independent operations ko hi concurrently run karo.
- Dependencies ko artificially parallel mat karo.
- `create_task()` ko thread samajhne ki mistake mat karo.
- CPU-heavy work ke liye async par depend mat karo.
- External calls par timeout rakho.
- Exceptions properly handle karo.
- Cancellation ko ignore mat karo.
- Unlimited tasks create mat karo.
- Production mein concurrency limits aur connection pools consider karo.
- Simple case mein direct `await` ko prefer karo; unnecessary abstraction mat banao.

---

# 21. Final Mental Model

```text
Coroutine
    ↓
create_task()
    ↓
Task
    ↓
Event Loop
    ↓
Run
    ↓
await I/O
    ↓
Suspend
    ↓
Other task runs
    ↓
I/O ready
    ↓
Resume
    ↓
Complete
```

### Remember

> `asyncio.create_task()` ka simple matlab hai:

> **"Is coroutine ko Event Loop par schedule kar do taa-ke ye doosre async work ke saath concurrently progress kar sake."**

It does **not** mean:

```text
New Thread ❌
New Process ❌
CPU Parallelism ❌
Durable Background Job ❌
```
