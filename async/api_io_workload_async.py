import asyncio, os, time
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=api_key)

def load_txt_file(file_path):
    with open(file_path) as f:
        content = f.read()
    return content

async def summarize(text):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the following text briefly."},
                {"role": "user", "content": text},
            ],
        )
        summary = response.choices[0].message.content
    except Exception as e:
        return e
    return summary

async def main():
    file_paths = [
        'data_source/attention_span.txt',
        'data_source/critical_thinking.txt',
        'data_source/doomscrolling.txt',
        'data_source/dunning_kruger_effect.txt',
    ]

    contents = [load_txt_file(file_path) for file_path in file_paths]
    tasks = [summarize(content) for content in contents] #Note that without await here, tasks is a list of coroutine objects
    results = await asyncio.gather(*tasks)
    for i, summary in enumerate(results):
        print(f"\nSummary of file {i+1}: {summary[:80]}")

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()
    print(f"Took {end - start:.3f} seconds")