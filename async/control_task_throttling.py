import asyncio, os, time
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)
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
    num_batch = len(all_chunks) // batch_size + (1 if len(all_chunks) % batch_size != 0 else 0)
    batches = [all_chunks[i:i+batch_size] for i in range(0, len(all_chunks), batch_size)] # Build all batches
    
    # CONCURRENCY CONTROL (MANUAL)
    result = []
    for i in range(0, num_batch, max_concurrency):
        current_batches = batches[i : i + max_concurrency]
        tasks = [embed_batch(b) for b in current_batches]
        sub_results = await asyncio.gather(*tasks)
        for r in sub_results:
            result.extend(r)

    print("Total embeddings:", len(result))

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Took {(end - start):.3f} seconds")
