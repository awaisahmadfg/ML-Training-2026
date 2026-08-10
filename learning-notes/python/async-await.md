# Async / Await — Python vs JavaScript

## 1. Why Async Programming Exists

Software mein bohat saare kaam aise hote hain jahan program ko actually calculate nahi karna hota, balkay kisi external cheez ka **wait** karna hota hai.

Examples:

- API response
- Database query
- LLM response
- Vector database search
- Redis
- File/network operation

Example:

```text
Python App
    ↓
API ko request bheji
    ↓
WAIT 3 seconds
    ↓
Response aya
```

Problem ye hai ke in 3 seconds mein CPU ko us particular task ke liye kuch nahi karna.

Agar application ke paas aur kaam available hai to hum chahte hain:

```text
Task A → API request → WAIT
                         ↓
                     Task B run
                         ↓
                     Task C run
                         ↓
              A ka response ready
                         ↓
                     A continue
```

Isi type ke I/O-heavy workloads ke liye asynchronous programming useful hai.

---

# 2. Synchronous Programming

Normal synchronous code:

```python
result = call_api()

print(result)

print("Next task")
```

Mental model:

```text
call_api()
    ↓
WAIT
    ↓
response
    ↓
print()
    ↓
next task
```

Program ek operation ko complete karta hai aur phir next operation par jata hai.

---

# 3. Asynchronous Programming

Async mein idea ye hai:

> Jab program kisi I/O operation ke result ka wait kar raha ho, to event loop doosra useful async work handle kar sakta hai.

Example:

```python
async def get_user():
    user = await call_api()
    return user
```

Yahan:

```text
call_api()
    ↓
await
    ↓
waiting
    ↓
Event Loop doosra async work kar sakta hai
```

Important:

`await` API ko faster nahi banata.

Ye **waiting time ko efficiently use** karne mein help karta hai.

---

# 4. `async def`

Python mein:

```python
async def fetch_user():
    ...
```

`async def` ek **coroutine function** define karta hai.

Example:

```python
async def fetch_user():
    return {"name": "Ali"}
```

Agar hum isay call karein:

```python
user = fetch_user()
```

to normal function ki tarah direct result nahi milega.

Humein coroutine object milega.

```text
fetch_user()
     ↓
Coroutine Object
```

---

# 5. `await`

`await` ka simple matlab:

> "Is async operation ka result chahiye. Jab tak ye ready hota hai, event loop doosra async kaam handle kar sakta hai."

Example:

```python
async def main():
    user = await fetch_user()
    print(user)
```

Flow:

```text
main()
 ↓
fetch_user()
 ↓
await
 ↓
wait
 ↓
result ready
 ↓
resume
 ↓
print result
```

---

# 6. Complete Example

```python
import asyncio

async def fetch_user():
    print("Fetching user...")

    await asyncio.sleep(2)

    print("User received")

    return {
        "name": "Ali"
    }


async def main():

    user = await fetch_user()

    print(user)


asyncio.run(main())
```

Output:

```text
Fetching user...
User received
{'name': 'Ali'}
```

---

# 7. `asyncio.run()`

Python ke normal synchronous entry point se async code start karne ke liye:

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
Coroutine executes
 ↓
Result
```

Important:

```python
main()
```

sirf coroutine object create karta hai.

While:

```python
asyncio.run(main())
```

async execution ko actually run karwata hai.

---

# 8. JavaScript vs Python

JavaScript:

```javascript
async function fetchUser() {
    const response = await fetch("/user");

    return response.json();
}
```

Python:

```python
async def fetch_user():
    response = await client.get("/user")

    return response.json()
```

Dono mein basic idea similar hai:

```text
async
 ↓
await
 ↓
I/O operation
 ↓
wait
 ↓
continue
```

Lekin implementation/runtime same nahi hai.

---

# 9. JavaScript Promise vs Python Coroutine

JavaScript:

```javascript
const promise = fetch("/users");
```

Promise future result ko represent karta hai.

Python:

```python
coro = fetch_users()
```

Coroutine object asynchronous computation ko represent karta hai jo baad mein await/schedule ho sakti hai.

Simple mental mapping:

```text
JavaScript Promise
    ↓
Future result

Python Coroutine
    ↓
Async computation

Python Task
    ↓
Scheduled coroutine
```

Promise aur coroutine ko exact same cheez nahi samajhna chahiye.

---

# 10. Async Kab Use Karna Hai?

Async especially useful hai jab application:

- HTTP APIs call kare
- Database se data le
- Redis use kare
- Vector database use kare
- LLM APIs call kare
- Network requests kare
- External services ka wait kare

AI backend mein ye bohat common hai.

Example:

```text
FastAPI
   ↓
User Request
   ↓
LLM API
   ↓
WAIT
```

Async approach application ko is waiting time mein doosra async work handle karne deti hai.

---

# 11. AI Backend Example

Suppose user chatbot ko question bhejta hai:

```text
"What is our refund policy?"
```

Backend ko:

```text
1. Vector DB se relevant documents lene hain
2. LLM ko prompt bhejna hai
3. Response return karna hai
```

Flow:

```text
User
 ↓
FastAPI
 ↓
Vector DB
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
 ↓
User
```

Ye typical async AI backend flow hai.

---

# 12. Async Kab Use Nahi Karna?

Async har jagah use karna zaroori nahi.

CPU-heavy tasks:

- Large mathematical calculations
- ML training
- Video encoding
- Heavy image processing
- Huge CPU computations

Example:

```python
async def calculate():
    # huge CPU calculation
```

Sirf `async` likhne se ye calculation magically faster nahi hogi.

---

# 13. Async != Parallelism

Ye important distinction hai.

Async ka primary goal:

```text
Concurrency
```

Parallelism:

```text
Multiple CPU cores
```

Simple:

```text
Async

Task A
  ↓
WAIT
  ↓
Task B
  ↓
WAIT
  ↓
Task A resume
```

Parallelism:

```text
CPU Core 1 → Task A
CPU Core 2 → Task B
CPU Core 3 → Task C
```

Dono different concepts hain.

---

# 14. Common Mistake

Ye:

```python
result = fetch_user()
```

final result nahi hai.

Ye:

```text
Coroutine Object
```

hai.

Async function ko execute/drive karne ke liye:

```python
result = await fetch_user()
```

ya top-level se:

```python
asyncio.run(fetch_user())
```

use kar sakte hain.

---

# 15. Another Common Mistake

Async code mein:

```python
time.sleep(5)
```

dangerous ho sakta hai.

Kyun?

`time.sleep()` current thread ko block karta hai.

Async waiting ke liye:

```python
await asyncio.sleep(5)
```

use hota hai.

Difference:

```text
time.sleep()

Thread BLOCK
    ↓
Event Loop stuck
```

while:

```text
await asyncio.sleep()

Coroutine WAIT
    ↓
Event Loop other work
```

---

# 16. Best Mental Model

Async ko is sentence se yaad rakho:

> "Main kisi external cheez ka wait kar raha hoon, is waiting time ko waste nahi karna."

---

# 17. Quick Revision

```text
async def
    ↓
Coroutine Function

call()
    ↓
Coroutine Object

await
    ↓
Async operation

wait
    ↓
Event Loop can handle other async work

result ready
    ↓
Coroutine resumes
```

### Remember

```text
async = async function define karo

await = async operation ka wait karo

asyncio.run() = top-level se async code run karo

async ≠ parallelism
```
