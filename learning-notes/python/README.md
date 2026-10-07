# Python Async — AI Backend Learning Notes

Roman Urdu notes: async programming jo **LLM APIs, RAG, FastAPI** backends ke liye zaroori hai.

## Kahan se shuru karein?

| Order | File | Topic |
|------:|------|--------|
| — | **[AI-Backend-Async-Python-Roman-Urdu.md](./AI-Backend-Async-Python-Roman-Urdu.md)** | **Poora guide ek jagah (recommended revision)** |
| 1 | [process-vs-thread.md](./process-vs-thread.md) | Process, Thread, Coroutine |
| 2 | [event-loop.md](./event-loop.md) | Event Loop |
| 3 | [coroutines.md](./coroutines.md) | Coroutines |
| 4 | [async-await.md](./async-await.md) | Async / Await |
| 5 | [asyncio-create-task.md](./asyncio-create-task.md) | `asyncio.create_task()` |
| 6 | [asyncio.gather().md](./asyncio.gather().md) | `asyncio.gather()` |

## Ek line summary

```text
I/O wait overlap karo (async) — CPU cores magically nahi milte.
Independent calls → gather; blocking sync code → thread/executor; heavy CPU → process/worker.
```
