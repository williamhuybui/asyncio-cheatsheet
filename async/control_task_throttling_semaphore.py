import asyncio, os, time
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = "text-embedding-3-large"

def load_txt_file(file_path):
    with open(file_path) as f:
        return f.read()

async def embed_batch(batch):
    """Send one embedding request for a batch of texts."""
    if not batch:
        return []
    resp = await client.embeddings.create(model=MODEL, input=batch)
    return [item.embedding for item in resp.data]

async def main():
    file_paths = [
        'data_source/attention_span.txt',
        'data_source/critical_thinking.txt',
        'data_source/doomscrolling.txt',
        'data_source/dunning_kruger_effect.txt',
    ]

    contents = [load_txt_file(p) for p in file_paths]

    # Split into small chunks
    chunk_size = 500
    all_chunks = []
    for c in contents:
        all_chunks.extend([c[i:i+chunk_size] for i in range(0, len(c), chunk_size)])
    print("Total number of chunks:", len(all_chunks))

    # SETTINGS
    batch_size = 8 
    max_concurrency = 4 
    batches = [all_chunks[i:i+batch_size] for i in range(0, len(all_chunks), batch_size)] # Build all batches
    
    # CONCURRENCY CONTROL (WITH SEMAPHORE)
    sem = asyncio.Semaphore(max_concurrency)
    async def run_one(batch):
        async with sem:
            return await embed_batch(batch)
    results = await asyncio.gather(*(run_one(b) for b in batches))
    embeddings = [e for batch_embs in results for e in batch_embs]

    print("Total embeddings:", len(embeddings))

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Took {(end - start):.3f} seconds")
