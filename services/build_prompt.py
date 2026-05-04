def build_prompt(query: str, scraped_articles: list[dict]) -> str:
    articles_text = ""
    for i, article in enumerate(scraped_articles, 1):
        articles_text += f"\n--- Source {i}: {article['title']} ({article['url']}) ---\n"
        articles_text += article["text"] + "\n"
 
    return f"""You are a research assistant. Based ONLY on the sources below, answer the user's question concisely.
 
User question: {query}
 
Sources:
{articles_text}
 
Instructions:
- Give a clear, direct answer in 2 to 4 sentences.
- Do not mention sources by number; just synthesize the information.
- If sources are insufficient, say so briefly.
"""