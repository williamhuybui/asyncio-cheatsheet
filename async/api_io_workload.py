import asyncio, os, time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def load_txt_file(file_path):
    with open(file_path) as f:
        content = f.read()
    return content

def summarize(text):
    try:
        response = client.chat.completions.create(
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

def main():
    file_paths = [
        'data_source/attention_span.txt',
        'data_source/critical_thinking.txt',
        'data_source/doomscrolling.txt',
        'data_source/dunning_kruger_effect.txt',
    ]

    contents = [load_txt_file(file_path) for file_path in file_paths]
    for i, content in enumerate(contents):
        summary = summarize(content)
        print(f"\nSummary of file {i+1}: {summary[:80]}")

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f"Took {end - start:.3f} seconds")
