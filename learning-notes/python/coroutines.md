# Coroutines in Python

## 1. Coroutine Ki Need Kyu Pari?

Imagine application ko multiple APIs call karni hain.

```text
API A → WAIT
API B → WAIT
API C → WAIT
```

Agar har kaam simply block kare:

```text
A complete
 ↓
B complete
 ↓
C complete
```

I/O-heavy applications ke liye lightweight suspend/resume model useful tha.

Python async programming mein coroutine isi model ka important part hai.

---

# 2. Simple Definition

> Coroutine ek asynchronous computation hai jo `await` point par temporarily suspend ho sakti hai aur baad mein resume ho sakti hai.

Simple:

```text
Coroutine
   ↓
Run
   ↓
await
   ↓
Pause
   ↓
Other async work
   ↓
Resume
```

---

# 3. `async def` Coroutine Function Banata Hai

```python
async def fetch_user():
    return {
        "name": "Ali"
    }
```

Ye ek **coroutine function** hai.

Jab call karte hain:

```python
result = fetch_user()
```

to:

```text
result
 ↓
Coroutine Object
```

milta hai.

---

# 4. Coroutine Object

Example:

```python
async def fetch_user():

    print("Fetching...")

    await asyncio.sleep(2)

    return "Ali"


coro = fetch_user()
```

`coro` final `"Ali"` nahi hai.

Ye coroutine object hai.

Usay execute/drive karna hoga:

```python
result = await coro
```

ya:

```python
asyncio.run(coro)
```

---

# 5. Real Life Analogy

Ek chef imagine karo.

Order A:

```text
Start cooking
 ↓
Oven mein rakha
 ↓
20 min wait
```

Chef oven ke saamne khara nahi rahega.

Woh:

```text
Order A → oven → WAIT

Order B → cooking

Order C → preparing
```

Kisi point par A ready:

```text
Order A
 ↓
Resume
 ↓
Complete
```

Coroutine bhi similar mental model follow karti hai.

---

# 6. Basic Example

```python
import asyncio


async def fetch_data():

    print("Start")

    await asyncio.sleep(2)

    print("End")

    return 42


async def main():

    result = await fetch_data()

    print(result)


asyncio.run(main())
```

Output:

```text
Start
End
42
```

---

# 7. Coroutine ka Flow

```text
async def fetch_data()
          ↓
    Coroutine Function
          ↓
fetch_data()
          ↓
    Coroutine Object
          ↓
       await
          ↓
       Execute
          ↓
    await I/O
          ↓
      Suspend
          ↓
    Resume later
          ↓
       Result
```

---

# 8. Coroutine vs Task

Ye distinction important hai.

Coroutine:

```python
coro = fetch_data()
```

Task:

```python
task = asyncio.create_task(fetch_data())
```

Mental model:

```text
Coroutine
"Async computation"

        ↓

Task
"Scheduled coroutine"
```

Task event loop ke through coroutine ko schedule/track karta hai.

---

# 9. Coroutine vs JavaScript Promise

JavaScript:

```javascript
async function getUser() {
    const response = await fetch("/user");

    return response.json();
}

const promise = getUser();
```

Python:

```python
async def get_user():

    response = await client.get("/user")

    return response.json()


coro = get_user()
```

Conceptually:

```text
JavaScript

async function
      ↓
Promise


Python

async def
      ↓
Coroutine Object
```

Lekin:

> Coroutine aur Promise exact same concept nahi hain.

Better mental mapping:

```text
JS Promise
    ↓
Future result

Python Coroutine
    ↓
Async computation

Python Task
    ↓
Scheduled async computation
```

---

# 10. `asyncio.run()` ka Role

Normal Python code:

```python
async def main():
    ...
```

Calling:

```python
main()
```

coroutine object deta hai.

Execution start karwane ke liye:

```python
asyncio.run(main())
```

Conceptually:

```text
main()
 ↓
Coroutine Object
 ↓
asyncio.run()
 ↓
Event Loop
 ↓
Coroutine runs
 ↓
Result
```

---

# 11. Coroutine Automatically Background Mein Nahi Chalti

Important misconception:

```python
coro = fetch_data()
```

iska matlab ye nahi:

> "fetch_data background mein chal rahi hai."

No.

Coroutine ko await/schedule/run karna hota hai.

---

# 12. Coroutine Kab Use Hoti Hai?

Mostly I/O-bound async applications:

- APIs
- Database
- Redis
- HTTP
- LLM APIs
- Vector DB
- Network requests

AI backend mein example:

```python
async def answer_question(question):

    documents = await vector_search(question)

    answer = await call_llm(
        question,
        documents
    )

    return answer
```

Flow:

```text
Question
   ↓
Coroutine starts
   ↓
Vector DB
   ↓
await
   ↓
Resume
   ↓
LLM
   ↓
await
   ↓
Resume
   ↓
Answer
```

---

# 13. Coroutine aur Thread Same Nahi

Thread:

```text
Process
   ├── Thread A
   └── Thread B
```

Coroutine:

```text
Process
   ↓
Thread
   ↓
Event Loop
   ↓
Coroutine A
Coroutine B
Coroutine C
```

One event-loop thread many coroutines/tasks ko manage kar sakta hai.

---

# 14. Coroutine aur CPU Parallelism

Coroutine:

```text
Task A
 ↓
await
 ↓
Task B
 ↓
await
```

Ye automatically:

```text
CPU Core 1 → Task A
CPU Core 2 → Task B
```

nahi banata.

CPU-heavy workloads ke liye different architecture chahiye.

---

# 15. Common Mistakes

### Mistake 1

```python
result = fetch_data()
```

Thinking:

```text
result = final data
```

Actually:

```text
result = Coroutine Object
```

---

### Mistake 2

Coroutine ko await na karna:

```python
fetch_data()
```

Is se coroutine unawaited reh sakti hai.

---

### Mistake 3

Coroutine = Thread samajhna.

No.

---

### Mistake 4

Coroutine = Parallelism samajhna.

No.

---

# 16. Behind the Scenes

Coroutine ke andar `await` points important hain.

Example:

```python
async def fetch():

    data = await api_call()

    return data
```

Mental model:

```text
fetch starts
   ↓
api_call()
   ↓
await
   ↓
Coroutine suspends
   ↓
Event Loop handles other work
   ↓
API ready
   ↓
Coroutine resumes
   ↓
data
   ↓
return
```

---

# 17. Best Mental Model

Yaad rakho:

> **Coroutine = aisa async kaam jo wait ke point par ruk sakta hai aur baad mein wahi se continue ho sakta hai.**

---

# 18. Quick Revision

```text
async def
   ↓
Coroutine Function

call()
   ↓
Coroutine Object

await / schedule
   ↓
Event Loop
   ↓
Run
   ↓
await
   ↓
Suspend
   ↓
Resume
   ↓
Result
```
