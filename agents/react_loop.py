"""
ReAct Loop Agent for Competitive Intelligence
Implements Thought-Action-Observation cycle using Anthropic API with tool_use.
"""

import json
import os
import re
import warnings
from dotenv import load_dotenv
from anthropic import Anthropic
import httpx

warnings.filterwarnings("ignore", category=RuntimeWarning)

load_dotenv(override=True)

# Tool definition for Claude API
WEB_SEARCH_TOOL = {
    "name": "web_search",
    "description": (
        "Search the web for current information about companies, markets, "
        "financials, and competitive intelligence. Returns top results with "
        "titles, URLs, and snippets."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find relevant information",
            }
        },
        "required": ["query"],
    },
}

SYSTEM_PROMPT = """You are a Competitive Intelligence analyst specializing in European banking.
You follow the ReAct methodology: Think > Act > Observe > Repeat.

RULES:
- Always search for REAL, verifiable data before answering.
- Cite every claim with a source URL.
- If data conflicts, note the discrepancy and assign confidence: HIGH/MEDIUM/LOW/UNCERTAIN.
- Never fabricate numbers or sources.
- Stop when you have sufficient evidence (at least 2 sources) or after 5 search cycles.
- Format your final answer with clear sections and source citations.

When you have enough information, provide your FINAL ANSWER directly (without calling tools).
Structure it as:
## Answer
[Your synthesized answer]

## Sources
- [title](url) - what it provided
"""


def execute_web_search(query: str, max_results: int = 5) -> list[dict]:
    """Execute a web search using DuckDuckGo HTML endpoint."""
    try:
        # Try the duckduckgo_search library first
        from duckduckgo_search import DDGS
        ddgs = DDGS()
        results = list(ddgs.text(f"{query} site:.com OR site:.org", max_results=max_results))
        if results:
            return [
                {
                    "title": r.get("title", ""),
                    "url": r.get("href", r.get("link", "")),
                    "snippet": r.get("body", r.get("snippet", "")),
                }
                for r in results
            ]
    except Exception:
        pass

    # Fallback: use DuckDuckGo HTML with httpx
    try:
        from urllib.parse import unquote
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = httpx.get(
            "https://html.duckduckgo.com/html/",
            params={"q": query, "kl": "us-en"},
            headers=headers,
            timeout=15,
            follow_redirects=True,
        )
        results = []
        html = resp.text
        # Find all result links and snippets
        links = re.finditer(r'class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</(?:a|span|td)', html, re.DOTALL)
        for i, link in enumerate(links):
            raw_url = link.group(1)
            raw_title = re.sub(r"<[^>]+>", "", link.group(2)).strip()
            raw_snippet = re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else ""
            uddg = re.search(r"uddg=([^&]+)", raw_url)
            final_url = unquote(uddg.group(1)) if uddg else raw_url
            results.append({"title": raw_title, "url": final_url, "snippet": raw_snippet})
            if len(results) >= max_results:
                break
        return results if results else [{"title": "No results", "url": "", "snippet": f"No results for: {query}"}]
    except Exception as e:
        return [{"title": "Search Error", "url": "", "snippet": str(e)}]


def react_loop(question: str, max_cycles: int = 5, verbose: bool = True) -> dict:
    """
    Run a ReAct loop to answer a CI question.

    Args:
        question: The competitive intelligence question to answer.
        max_cycles: Maximum Think-Act-Observe cycles (default 5).
        verbose: Print intermediate steps.

    Returns:
        dict with 'answer', 'sources', and 'cycles' used.
    """
    client = Anthropic()
    messages = [{"role": "user", "content": question}]
    sources_collected = []

    for cycle in range(1, max_cycles + 1):
        if verbose:
            print(f"\n{'='*50}")
            print(f"  CYCLE {cycle}/{max_cycles}")
            print(f"{'='*50}")

        # Call Claude with web_search tool
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=[WEB_SEARCH_TOOL],
            messages=messages,
        )

        # Process response blocks
        assistant_content = response.content
        tool_use_block = None
        text_parts = []

        for block in assistant_content:
            if block.type == "text":
                text_parts.append(block.text)
                if verbose:
                    print(f"\n[THINK] {block.text[:300]}...")
            elif block.type == "tool_use":
                tool_use_block = block

        # If no tool call, Claude has given final answer
        if response.stop_reason == "end_turn" or tool_use_block is None:
            final_answer = "\n".join(text_parts)
            if verbose:
                print(f"\n[FINAL ANSWER] Reached after {cycle} cycle(s)")
            return {
                "answer": final_answer,
                "sources": sources_collected,
                "cycles": cycle,
            }

        # Execute the tool call
        query = tool_use_block.input.get("query", "")
        if verbose:
            print(f"\n[ACT] Searching: '{query}'")

        search_results = execute_web_search(query)
        sources_collected.extend(
            {"url": r["url"], "title": r["title"]} for r in search_results if r["url"]
        )

        if verbose:
            print(f"[OBSERVE] Got {len(search_results)} results")
            for r in search_results[:3]:
                title = r['title'][:60]
                # Safe print for Windows console
                try:
                    print(f"  - {title}")
                except UnicodeEncodeError:
                    print(f"  - {title.encode('ascii', 'replace').decode()}")

        # Feed results back to Claude
        messages.append({"role": "assistant", "content": assistant_content})
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": json.dumps(search_results, ensure_ascii=False),
                    }
                ],
            }
        )

    # Max cycles reached - ask Claude for final answer without tools
    messages.append(
        {
            "role": "user",
            "content": "Maximum search cycles reached. Please provide your final answer now with the information gathered so far.",
        }
    )
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    final_answer = "\n".join(b.text for b in response.content if b.type == "text")
    return {
        "answer": final_answer,
        "sources": sources_collected,
        "cycles": max_cycles,
    }


# --------------- CLI Entry Point ---------------
if __name__ == "__main__":
    test_questions = [
        "What is Revolut revenue 2024?",
        "How many BBVA branches are in Spain?",
        "What fintech licences has Revolut obtained?",
    ]

    for i, q in enumerate(test_questions, 1):
        print(f"\n{'#'*60}")
        print(f"  QUESTION {i}: {q}")
        print(f"{'#'*60}")

        result = react_loop(q)

        print(f"\n{'-'*60}")
        print(f"ANSWER:\n{result['answer']}")
        print(f"\nCycles used: {result['cycles']}")
        print(f"Sources found: {len(result['sources'])}")
        print(f"{'-'*60}")
