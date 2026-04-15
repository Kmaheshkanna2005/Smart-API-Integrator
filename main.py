import json
from scraper import fetch_api_docs
from parser import analyze_api_data
from generator import generate_wrapper

def run_tool(url, goal):
    print(f"\n🚀 Starting Smart DevTool for: {url}")
    
    # 1. Scrape
    raw_data = fetch_api_docs(url)
    
    # 2. Parse
    print("🧠 Analyzing documentation with AI...")
    metadata = analyze_api_data(raw_data, goal, url)
    
    if "error" in metadata:
        print(f"❌ Error: {metadata['error']}")
        return

    # 3. New: Ask for language
    lang_choice = input("💻 Which language do you need? (python / javascript): ").lower()
    if lang_choice not in ["python", "javascript"]:
        lang_choice = "python" # default

    # 4. Generate
    print(f"🛠️ Generating your {lang_choice} wrapper class...")
    filename = generate_wrapper(metadata, language=lang_choice)
    
    print(f"\n✅ SUCCESS!")
    print(f"Your code is waiting in: {filename}")
    
    # Inside your run_tool function in main.py, after the generator finishes:

    print(f"\n--- 📋 INTEGRATION SUMMARY ---")
    print(f"🔹 Endpoint Found: {metadata.get('method')} {metadata.get('endpoint')}")
    print(f"🔹 Auth Detected: {metadata.get('auth_type')}")
    print(f"🔹 Language: {lang_choice.upper()}")
    print(f"🔹 File Saved: {filename}")
    print(f"------------------------------")

if __name__ == "__main__":
    print("--- 🤖 Smart DevTool: API Integrator ---")
    
    target_url = input("🔗 Enter the API Documentation URL: ")
    
    # This loop keeps the tool running until the user types 'exit'
    while True:
        print("\n" + "-"*30)
        user_goal = input("🎯 What do you want to do? (or type 'exit' to quit): ")
        
        if user_goal.lower() == 'exit':
            print("Goodbye! 👋")
            break
            
        run_tool(target_url, user_goal)
        print("\n✅ Task Complete! Check 'generated_api_client.py'")