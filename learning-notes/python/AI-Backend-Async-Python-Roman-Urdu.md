# Python Async — AI Backend Complete Guide (Roman Urdu)

> **Scope:** FastAPI / RAG / LLM backends ke liye asyncio concepts — scratch se medium-advanced.  
> **Style:** To the point, concept clear, chhote real-world examples.

---

## 0. Shuruat — AI backend mein asli problem kya hai?

Tumhara server zyada tar **wait** karta hai, **calculate** kam:

```text
User: "Meri policy cover karti hai dental?"
    ↓
Redis (session)     → 20ms WAIT
Postgres (user)     → 40ms WAIT
Vector DB (docs)    → 120ms WAIT
OpenAI API (LLM)    → 2000ms WAIT
Postgres (save)     → 30ms WAIT
```

In wait ke dauran CPU mostly **khaali** reh sakta hai. Agar ek hi thread har user ko **line mein** wait karaye, to 100 users = bohot slow.

**Async ka goal:** jab Request A LLM ka jawab wait kar rahi ho, tab Request B vector search kar sake — **same process, same thread (event loop), alag coroutines**.

**Async ka goal NAHI:** GPU par model train karna ya 8 CPU cores par Python loop chalana.

---

## 1. Process vs Thread vs Coroutine

### 1.1 Process

**Matlab:** Ek chalta hua program ka apna environment (memory alag).

**Real example:**

```text
Uvicorn tumhari FastAPI app chala raha hai  → 1 Python Process
Alag Celery worker embeddings banata hai     → doosra Process
```

Agar embedding worker crash ho, FastAPI process alag hai — isolation.

### 1.2 Thread

**Matlab:** Process ke **andar** execution ka ek rasta; threads **same process ki memory** share karte hain.

**Real example:** FastAPI process ke andar:

```text
Main Thread  → Event Loop + tumhare async endpoints
(optional) Worker threads → sync library jo async nahi hai
```

### 1.3 Coroutine

**Matlab:** Lightweight async kaam jo `await` par **rukta** hai, thread **nahi** banata.

**Real example:** 500 simultaneous chat users:

```text
500 threads   → heavy (memory + OS scheduling)
500 coroutines on 1 event loop → common pattern (I/O APIs ke liye)
```

### 1.4 Comparison table

| | Process | Thread | Coroutine |
|---|---------|--------|-----------|
| **Weight** | Bhari | Medium | Halki |
| **Memory** | Alag space | Shared | Bahut kam |
| **AI use** | Worker / CPU job | Sync SDK offload | HTTP, DB, LLM wait |
| **10k network waits** | Usually overkill | Costly | Suitable |

### 1.5 Decision (yaad rakho)

```text
Network / DB / LLM wait + async client available  →  coroutine + await
Sirf sync library (purana SDK)                      →  thread / asyncio.to_thread
Heavy CPU (Python loop, big image)                  →  alag process / worker queue
```

### 1.6 GIL — sirf itna

CPython **GIL** ki wajah se **CPU-bound pure Python** par threads se zyada cores nahi milte.  
**I/O wait** (network) par ye kam matter karta hai — isliye LLM backends async use karte hain.

**Galat:** "Async laga di → 8 core use ho gaye."  
**Sahi:** "Async laga di → wait overlap ho gayi → latency kam."

### 1.7 Restaurant analogy (ek dafa)

| OS concept | Analogy |
|------------|---------|
| Process | Alag restaurant building |
| Thread | Us restaurant ke chefs |
| Coroutine | Orders — oven par wait, chef doosra order dekhta hai |
| Event loop | Manager jo orders rotate karta hai |

---

## 2. Event Loop

### 2.1 Kya hai?

**Event loop** = async system ka **manager**:

```text
Kaun sa task ab run ho sakta hai?
    → chalao
    → await / I/O wait → suspend
    → doosra task
    → pehla I/O ready → resume
```

### 2.2 Python mein start

```python
import asyncio

async def main():
    print("start")

asyncio.run(main())  # loop create → main chalao → loop band
```

Production **FastAPI + Uvicorn** apna loop chalate hain — tum `async def` endpoint likhte ho.

### 2.3 Architecture (real deployment)

```text
Internet
   ↓
Uvicorn (Python Process)
   ↓
Main Thread
   ↓
Event Loop
   ↓
Har HTTP request ≈ coroutine tree
   ├── get_user()
   ├── vector_search()
   └── call_openai()
```

### 2.4 Blocking — sab se common production bug

**Scenario:** Endpoint `async def` hai lekin andar sync block:

```python
import time

async def broken_health():
    time.sleep(10)  # ❌ POORA event loop 10 sec freeze
    return {"ok": True}
```

Is 10 sec mein **koi aur user** ki request process nahi hogi (same worker par).

**Fix (simulate I/O):**

```python
async def ok_health():
    await asyncio.sleep(0.01)  # ✅ suspend, loop free
    return {"ok": True}
```

**Real fix (sync HTTP):** `requests.get()` mat use karo endpoint mein — `httpx.AsyncClient` ya sync call ko `asyncio.to_thread()` mein daalo.

### 2.5 1 thread, bahut coroutines

```text
1 Event Loop Thread
   ├── Coroutine: User A → LLM wait
   ├── Coroutine: User B → Redis wait
   └── Coroutine: User C → running
```

Ye **parallel CPU cores nahi** — ye **concurrent I/O** hai (cooperative).

### 2.6 Event loop revision (3 lines)

1. Loop tasks ko **rotate** karta hai.  
2. `await` = "main wait par hoon, doosron ko chance do."  
3. `time.sleep` / sync block = "main sab ko rok diya."

---

## 3. Coroutines

### 3.1 Definition

**Coroutine** = aisi async computation jo **`await` par pause** ho sakti hai aur baad mein **continue**.

### 3.2 `async def` — function nahi, coroutine factory

```python
async def get_user_name(user_id: str) -> str:
    # pretend DB call
    await asyncio.sleep(0.05)
    return "Ali"
```

Call:

```python
x = get_user_name("u1")
# x = coroutine object — abhi "Ali" NAHI
name = await x  # ab run hua
```

**Rule:** `async def` ko bina `await` / `asyncio.run` / `create_task` ke chhodoge to warning: "coroutine was never awaited".

### 3.3 Flow diagram

```text
async def foo()     →  coroutine function
foo()               →  coroutine object (scheduled nahi)
await foo()         →  execute + result
```

### 3.4 Coroutine vs Task

| | Coroutine object | Task |
|---|------------------|------|
| **State** | Ban gaya, loop par nahi bhi ho sakta | Loop par **scheduled** |
| **Create** | `coro = fetch()` | `task = asyncio.create_task(fetch())` |
| **Use** | Turant `await coro` | Background + baad mein `await task` |

**Real:** Pehle user fetch background mein start, beech mein cache check, end par user ka result lo — `create_task`.

---

## 4. Async / Await

### 4.1 Synchronous (line mein)

```python
async def sync_style_bad_for_independent_io():
    user = await db_get_user()      # 50ms
    history = await db_get_history()  # 80ms
    # total ~ 130ms — history ko user ki zaroorat nahi thi parallel ke liye
```

Agar **dono independent** hon:

```python
user, history = await asyncio.gather(
    db_get_user(),
    db_get_history(),
)
# total ~ max(50, 80) ≈ 80ms
```

### 4.2 `await` ka matlab

> Is step ka result aane tak **is coroutine** ko pause karo; **event loop** doosra kaam chalaye.

**Important:** Ek hi coroutine ke andar:

```python
await a()
await b()
```

= **pehle a khatam, phir b** (overlap nahi).

### 4.3 JavaScript se familiar ho to

```text
async/await          → same idea
Promise.all([...])   → asyncio.gather(...)
fetch()              → httpx async get
```

### 4.4 FastAPI real skeleton

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/ask")
async def ask(question: str, user_id: str):
    # Step 1: parallel fetch (independent)
    profile, chunks = await asyncio.gather(
        load_user_profile(user_id),
        search_vectors(question),
    )
    # Step 2: LLM ko teeno chahiye — serial
    answer = await call_llm(question, profile, chunks)
    await save_turn(user_id, question, answer)
    return {"answer": answer}
```

Yahan **concept:** parallel jahan **dependency nahi**; LLM **baad mein** kyunki usay chunks chahiye.

---

## 5. `asyncio.create_task()`

### 5.1 Problem

```python
await fetch_embeddings()   # 2 sec
await fetch_metadata()     # 1 sec
# ≈ 3 sec — doosra pehle wale ke baad start
```

### 5.2 Solution

```python
t1 = asyncio.create_task(fetch_embeddings())
t2 = asyncio.create_task(fetch_metadata())
emb = await t1
meta = await t2
# ≈ 2 sec overlap
```

### 5.3 Ek line definition

> Coroutine ko **Task** bana kar **abhi** event loop par schedule karo; caller aage badh sakta hai.

### 5.4 Kya NAHI karta

```text
New thread     ❌
New process    ❌
Extra CPU core ❌
Celery job     ❌  (process restart ke baad bhi chale — ye alag system hai)
```

### 5.5 Real: pehle LLM start, beech mein logging

```python
async def handle(q: str):
    llm_task = asyncio.create_task(call_llm(q))
    await log_request(q)           # chhota kaam
    answer = await llm_task        # LLM shayad pehle se chal raha ho
    return answer
```

Faida tab jab **beech ka kaam** aur **LLM wait** overlap ho sake.

### 5.6 Timeout + cancel (production)

```python
task = asyncio.create_task(call_llm(prompt))
try:
    async with asyncio.timeout(45):
        return await task
except TimeoutError:
    task.cancel()
    raise HTTPException(504, "LLM slow")
```

User tab band kare / gateway timeout — cancel se paisa/latency bach sakti hai (provider par depend).

---

## 6. `asyncio.gather()`

### 6.1 Definition

> **Kai** independent coroutines ko **saath progress** karwao; **ek `await`** par **sab ke results** (order = argument order).

```python
a, b, c = await asyncio.gather(op_a(), op_b(), op_c())
```

### 6.2 Real RAG latency

Independent:

```text
User profile DB     200ms
Chat history DB     300ms
Vector search       500ms
─────────────────────────
Serial: 1000ms
Gather: ~500ms (max)
```

```python
profile, history, docs = await asyncio.gather(
    get_profile(user_id),
    get_history(user_id),
    vector_search(question),
)
reply = await call_llm(question, profile, history, docs)
```

LLM **gather ke baad** — kyunki prompt mein docs chahiye.

### 6.3 Result order vs finish order

```python
async def slow():
    await asyncio.sleep(2)
    return "slow"

async def fast():
    await asyncio.sleep(0.1)
    return "fast"

slow_r, fast_r = await asyncio.gather(slow(), fast())
# slow_r == "slow", fast_r == "fast"  (input order fix)
# fast pehle complete hota hai, lekin tuple order change nahi
```

### 6.4 Kab use NAHI karo

**Dependent chain:**

```python
user = await get_user(email)
tenant_id = user["tenant_id"]
docs = await search_docs(tenant_id, q)  # tenant_id ke bina search galat
```

`get_user` aur `search_docs` ko **gather mat karo** — pehle user, phir search.

### 6.5 `gather` vs `create_task` — quick

| Tool | Kab |
|------|-----|
| `create_task` | Ek ko background, beech mein aur kaam |
| `gather` | Kai independent, sab ka result ek saath chahiye |

Simple case: seedha `gather(a(), b())` — andar tasks ban jati hain.

### 6.6 Errors — partial failure

```python
results = await asyncio.gather(
    openai_call(),
    backup_model_call(),
    return_exceptions=True,
)
```

Ek fail ho to doosra result phir bhi mil sakta hai — design carefully (primary fail → fallback logic).

### 6.7 Bahut saari calls — real rate limit

**Galat:**

```python
await asyncio.gather(*[embed(chunk) for chunk in 50_000_chunks])
```

OpenAI / DB **429 / connection exhausted**.

**Theek — Semaphore:**

```python
sem = asyncio.Semaphore(20)

async def embed_limited(chunk: str):
    async with sem:
        return await embed_api(chunk)

vectors = await asyncio.gather(*[embed_limited(c) for c in chunks])
```

Matlab: **max 20** embed ek waqt active — baqi queue mein.

---

## 7. Medium Advanced — AI backend patterns

### 7.1 Blocking library offload

**Scenario:** Internal library sirf sync:

```python
def sync_rerank(query: str, docs: list) -> list:
    return reranker_model.score(query, docs)  # 200ms CPU+lib
```

```python
async def endpoint(q: str, docs: list):
    ranked = await asyncio.to_thread(sync_rerank, q, docs)
    return await call_llm(q, ranked[:5])
```

Event loop thread **block nahi** hoti.

### 7.2 HTTP client (real)

```python
import httpx

client = httpx.AsyncClient(timeout=30.0)  # app startup par banao, reuse

async def call_llm(prompt: str) -> str:
    r = await client.post(
        "https://api.openai.com/v1/chat/completions",
        json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]},
        headers={"Authorization": f"Bearer {API_KEY}"},
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
```

Har request par **naya client mat banao** — connection pool ke liye reuse.

### 7.3 End-to-end mental model (ek request)

```text
HTTP POST /chat
    │
    ├─ gather: session(Redis) + history(PG) + vectors(Pinecone)
    │
    ├─ await: LLM (serial — upar ka data chahiye)
    │
    └─ await: save message (serial; ya create_task agar fire-and-forget safe ho)
    │
    JSON response
```

### 7.4 Checklist — code review par dekho

- [ ] Endpoint `async def` + andar `requests` / `time.sleep`?  
- [ ] Independent DB calls serial `await`?  
- [ ] LLM se pehle wahi data `gather` mein jo bina LLM ke mil sakta hai?  
- [ ] Har external call par **timeout**?  
- [ ] Bulk embed/search par **semaphore** ya batch?  
- [ ] `create_task` bina `await` — exception kho gayi?

---

## 8. Cheat sheet (print kar sakte ho)

### Keywords

```text
Process    → alag program instance
Thread     → process ke andar path
Coroutine  → async fn ka runnable object
Task       → loop par scheduled coroutine
Event Loop → coroutines coordinate
await      → pause until step done (loop free)
create_task→ schedule now, await later
gather     → many independent, one wait, all results
```

### Time math (independent I/O)

```text
Serial:  t1 + t2 + t3
Gather:  max(t1, t2, t3)
```

### Misconceptions — NO

```text
Async = multi-core CPU        ❌
Coroutine = Thread            ❌
create_task = new thread      ❌
gather = threads              ❌
Har cheez gather se fast      ❌  (dependencies serial rehni chahiye)
```

---

## 9. Chhota practice project (khud likho)

**Goal:** Fake RAG — 3 `asyncio.sleep` calls (0.2, 0.3, 0.5), phir fake LLM sleep 1.0.

1. Sab serial `await` — time note karo.  
2. Pehle teen `gather`, phir LLM — time note karo.  
3. Endpoint mein `time.sleep(1)` daal kar dekho — do parallel requests slow kyun hoti hain.

Expected samajh: (2) ka pehla hissa ~0.5s + LLM 1s ≈ 1.5s total; (1) ≈ 0.2+0.3+0.5+1 = 2.0s.

---

## 10. Related files (detail ke liye)

Is repo folder mein topic-wise lambi notes:

- `process-vs-thread.md`
- `event-loop.md`
- `coroutines.md`
- `async-await.md`
- `asyncio-create-task.md`
- `asyncio.gather().md`

**Pehle ye guide padho → phir individual file deep dive.**

---

*Last updated: learning path AI Backend async (Python asyncio + FastAPI mindset).*
