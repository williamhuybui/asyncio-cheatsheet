# Personal Notes: Python Async Programming

## Quick Reference

### What is Async?
Async lets your program do other things while waiting for I/O operations (API calls, file reads, database queries, etc.)

### Key Concepts
- **Coroutine**: An async function (defined with `async def`)
- **Event Loop**: Manages and switches between coroutines
- **Concurrency vs Parallelism**:
  - Async = concurrent I/O on single CPU core (tasks take turns while waiting)
  - Parallel = multiple CPU cores simultaneously (use `ProcessPoolExecutor` for CPU-intensive work) (We not doing it here)

### How Async Works
1. Async runs on **one CPU core**, not multiple cores
2. When calling multiple APIs asynchronously, they start sequentially but switch during I/O wait time
3. While waiting for API response (remote side), CPU can run other coroutines
4. This gives appearance of parallel execution without actual parallelism

## Usage Pattern

### 1. Define Async Function
```python
async def my_coroutine():
    # your code here
```

### 2. Call Async Function
```python
# Inside another coroutine
result = await my_coroutine()

# From normal code
asyncio.run(my_coroutine())
```

### 3. Run Multiple Concurrently
```python
await asyncio.gather(
    coroutine_1(),
    coroutine_2(),
    coroutine_3()
)
```

### 4. Error Handling
```python
# Option 1: Return exceptions instead of breaking
await asyncio.gather(c1(), c2(), c3(), return_exceptions=True)

# Option 2: Wrap each in try/except
```

## Throttling Control with Semaphore

### Purpose
Control max number of concurrent API calls to avoid overloading the server

### How It Works
- Semaphore limits how many async tasks run simultaneously
- When a task completes, a new one starts automatically
- Ensures event loop stays at max concurrency with no idle time

### Example Code
```python
sem = asyncio.Semaphore(max_concurrency)

async def run_one(batch):
    async with sem:
        return await embed_batch(batch)

results = await asyncio.gather(*(run_one(b) for b in batches))
```

## Performance Comparison

### Example 1: 4 Summarization Tasks (2s each)
- **Sequential**: 8 seconds total
- **Async with gather**: ~2 seconds total

### Example 2: Embedding 637 Chunks
- **Manual batching** (for loop + gather): Variable performance, may have idle time
- **Semaphore**: Always faster, no idle time in event loop

**Key Insight**: Semaphore performs best because it eliminates idle time by automatically starting new tasks when old ones complete

## Code Examples in Repo
- `api_io_workload.py` - Sequential API calls (Example 1)
- `api_io_workload_async.py` - Concurrent with `asyncio.gather` (Example 1)
- `control_task_throttling.py` - Manual concurrency control (Example 2)
- `control_task_throttling_semaphore.py` - Semaphore-based throttling (Example 2)

## When to Use What
- **Use Async**: I/O-bound operations (APIs, files, databases)
- **Use Parallel (ProcessPoolExecutor)**: CPU-bound operations (ML inference, heavy computation)
- **Use Semaphore**: When you need to limit concurrent operations to avoid overload
