import sys

import anthropic

from order_tools import TOOLS, get_order_status

MODEL = "claude-sonnet-5-5"


def text_of(response) -> str:
    return "".join(block.text for block in response.content if block.type == "text")


def ask_about_order(question: str, client=None) -> dict:
    client = client or anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]

    first = client.messages.create(
        model=MODEL, max_tokens=1000, tools=TOOLS, messages=messages
    )

    requests = [block for block in first.content if block.type == "tool_use"]
    if not requests:
        return {
            "first_stop_reason": first.stop_reason,
            "requests": [],
            "second_stop_reason": None,
            "answer": text_of(first),
        }

    results = [
        {
            "type": "tool_result",
            "tool_use_id": request.id,
            "content": get_order_status(**request.input),
        }
        for request in requests
    ]

    messages.append({"role": "assistant", "content": first.content})
    messages.append({"role": "user", "content": results})

    second = client.messages.create(
        model=MODEL, max_tokens=1000, tools=TOOLS, messages=messages
    )

    return {
        "first_stop_reason": first.stop_reason,
        "requests": [{"name": r.name, "input": r.input} for r in requests],
        "second_stop_reason": second.stop_reason,
        "answer": text_of(second),
    }


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "Where is order A100?"
    result = ask_about_order(question)

    print("First stop_reason:", result["first_stop_reason"])
    for request in result["requests"]:
        print("Claude asked for:", request["name"], request["input"])
    print("Second stop_reason:", result["second_stop_reason"])
    print("Answer:", result["answer"])