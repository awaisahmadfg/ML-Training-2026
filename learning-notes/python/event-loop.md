# Event Loop

## 1. Problem

Suppose application ke paas 3 requests hain:

```text
Request A → API → WAIT 3 sec

Request B → Database → WAIT 2 sec

Request C → Redis → WAIT 1 sec
```

Agar program simply har request ke wait mein khara rahe:

```text
A → WAIT → complete
B → WAIT → complete
C → WAIT → complete
```

to waiting time efficiently use nahi hota.

Event Loop isi problem ko solve karne mein important role play karta hai.

---

# 2. Event Loop Kya Hai?

Simple words:

> Event Loop ek coordinator hai jo async tasks ko dekhta hai, runnable work chalata hai aur jab koi I/O operation ready hota hai to related coroutine ko resume karwata hai.

Mental model:

```text
Event Loop
    ↓
Konsa kaam run ho sakta hai?
    ↓
Run
    ↓
Agar wait hai
    ↓
Doosra async kaam
    ↓
Pehla kaam ready
    ↓
Resume
```

---

# 3. Real Life Analogy

Restaurant manager imagine karo.

Orders:

```text
Order A → Oven
Order B → Kitchen
Order C → Drinks
```

Manager oven ke saamne 20 minutes khara nahi rahega.

Instead:

```text
Check A
 ↓
A oven mein hai

Check B
 ↓
B par kaam karo

Check C
 ↓
C par kaam karo

A ready
 ↓
A continue
```

Event Loop bhi isi tarah waiting async work ko manage karta hai.

---

# 4. Basic Python Example

```python
import asyncio


async def download():

    print("Download started")

    await asyncio.sleep(3)

    print("Download finished")


async def main():

    await download()


asyncio.run(main())
```

Flow:

```text
asyncio.run(main())
        ↓
Event Loop
        ↓
main()
        ↓
download()
        ↓
await sleep(3)
        ↓
waiting
        ↓
3 sec later
        ↓
download resumes
        ↓
finished
```

---

# 5. Multiple Tasks

Suppose:

```python
async def task_a():

    await asyncio.sleep(3)

    print("A done")


async def task_b():

    await asyncio.sleep(1)

    print("B done")
```

Agar dono properly schedule hon:

```text
0 sec
 │
 ├── A starts
 │      ↓
 │    waiting
 │
 └── B starts
        ↓
      waiting
        ↓
1 sec
 ↓
B done

3 sec
 ↓
A done
```

Output:

```text
B done
A done
```

---

# 6. Event Loop aur Thread

Simplified Python architecture:

```text
Python Process
      ↓
Main Thread
      ↓
Event Loop
      ↓
Tasks / Coroutines
      ├── API call
      ├── DB call
      ├── Redis
      └── LLM API
```

Important:

**Event Loop aur Thread same cheez nahi hain.**

Thread ek execution unit hai.

Event Loop async work ka coordinator hai.

---

# 7. One Thread + Many Coroutines

Ye concept important hai:

```text
1 Process

    ↓

1 Event Loop Thread

    ↓

100 Coroutines
```

Conceptually:

```text
Main Thread
│
└── Event Loop
      ├── Coroutine A
      ├── Coroutine B
      ├── Coroutine C
      ├── Coroutine D
      └── ...
```

Ye zaroori nahi ke 100 coroutines ek waqt mein CPU par literally simultaneously execute kar rahi hon.

Event Loop unko cooperative manner mein progress karwata hai.

---

# 8. `await` ka Role

Suppose:

```python
await call_llm()
```

LLM API response ka wait ho raha hai.

Coroutine effectively:

```text
Coroutine A
    ↓
LLM request
    ↓
WAIT
```

Event Loop:

```text
A waiting hai
 ↓
B runnable hai?
 ↓
B run karo
 ↓
C runnable hai?
 ↓
C run karo
```

Jab LLM response ready:

```text
A
 ↓
Resume
```

---

# 9. Event Loop CPU Parallelism Nahi Hai

Ye:

```text
1 Event Loop
+
100 Coroutines
```

iska matlab:

```text
100 CPU cores
```

nahi hai.

Instead:

```text
Task A → run → await

Task B → run → await

Task C → run → await
```

Isay cooperative concurrency samajhna better hai.

---

# 10. Blocking Code ka Problem

Async function ke andar:

```python
async def endpoint():

    time.sleep(10)

    return "done"
```

Problem:

```text
Event Loop
    ↓
time.sleep(10)
    ↓
BLOCKED
    ↓
Other async tasks wait
```

Isliye async code mein blocking operations ko identify karna important hai.

---

# 11. Correct Async Waiting

Instead:

```python
await asyncio.sleep(10)
```

Concept:

```text
Coroutine
   ↓
await
   ↓
Suspend
   ↓
Event Loop free
   ↓
Other tasks
```

---

# 12. AI Backend Example

RAG chatbot:

```text
User
 ↓
FastAPI
 ↓
Question
 ↓
Vector DB search
 ↓
await
 ↓
Documents
 ↓
LLM API
 ↓
await
 ↓
Answer
```

Agar multiple independent operations hon:

```text
                Request
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
   Vector DB    Redis       User DB
       │           │           │
       └───────────┼───────────┘
                   ↓
                  LLM
```

Event Loop in async operations ko efficiently coordinate kar sakta hai.

---

# 13. Common Misconceptions

### Event Loop = Thread?

No.

```text
Thread
   ↓
Event Loop
```

A thread can run an event loop.

---

### Async = Parallel?

No.

Async primarily gives concurrency.

---

### Event Loop = CPU worker?

No.

Event Loop ka main benefit I/O-bound asynchronous work mein hota hai.

---

### Event Loop automatically every task ko parallel chala deta hai?

No.

Tasks/coroutines scheduling aur await points important hain.

---

# 14. Behind the Scenes

Simplified flow:

```text
Coroutine/Task
      ↓
Event Loop
      ↓
Runnable?
   /       \
 YES       WAITING
 ↓           ↓
Run       Other work
 ↓
await I/O
 ↓
Suspend
 ↓
I/O ready
 ↓
Resume
```

---

# 15. Quick Revision

```text
Event Loop
    ↓
Async tasks ko coordinate karta hai
    ↓
Task runs
    ↓
Task reaches await
    ↓
Task waits
    ↓
Other task can run
    ↓
I/O ready
    ↓
Original task resumes
```

### Remember

> **Event Loop = async work ka coordinator.**
