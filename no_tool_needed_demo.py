from order_status_demo import ask_about_order

result = ask_about_order("What is the capital of France?")

print("First stop_reason:", result["first_stop_reason"])
print("Tool requests:", len(result["requests"]))
print("Answer:", result["answer"])