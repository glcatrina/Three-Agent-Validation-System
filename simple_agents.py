#!/usr/bin/env python3
"""
Three-Agent System - Ready to Run!
Save this as: simple_agents.py
"""

import requests
import json

def ask_ollama(prompt, system_message="", model="llama3.2"):
    """Ask Ollama a question and get response"""
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "system": system_message,
        "stream": False,
        "options": {
            "temperature": 0.5,
            "num_predict": 2000  # Limit response length
        }
    }
    
    try:
        print(f"   Thinking... (using {model})")
        response = requests.post(url, json=data, timeout=120)
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def run_agent_validation(task, max_rounds=3):
    """Run the three-agent validation process"""
    
    print(f"\n🚀 STARTING TASK")
    print(f"📋 Task: {task}")
    print("=" * 80)
    
    current_work = ""
    
    for round_num in range(1, max_rounds + 1):
        print(f"\n🔄 ROUND {round_num}/{max_rounds}")
        print("─" * 50)
        
        # === AGENT 1: WORKER ===
        print("\n🔨 AGENT 1 (WORKER) - Creating the work...")
        
        if round_num == 1:
            # First round - original task
            worker_prompt = f"Complete this task thoroughly and professionally: {task}"
        else:
            # Subsequent rounds - improve based on feedback
            worker_prompt = f"""TASK: {task}

PREVIOUS WORK:
{current_work}

FEEDBACK TO ADDRESS:
{feedback}

Please create an improved version that addresses all the feedback points."""

        worker_system = """You are a skilled professional who creates high-quality work. 
Be thorough, clear, and practical. Include examples when helpful."""
        
        current_work = ask_ollama(worker_prompt, worker_system)
        
        if "Error:" in current_work:
            print(f"❌ Worker failed: {current_work}")
            return None
            
        print(f"✅ Worker completed task")
        print(f"📄 Work length: {len(current_work)} characters")
        print(f"📝 Preview: {current_work[:200]}...")
        
        # === AGENT 2: CRITIC ===
        print(f"\n🔍 AGENT 2 (CRITIC) - Reviewing the work...")
        
        critic_prompt = f"""Please carefully review this work for the task: "{task}"

WORK TO REVIEW:
{current_work}

Provide detailed feedback covering:
1. Overall quality (rate 1-10)
2. Completeness - does it fully address the task?
3. Specific strengths
4. Areas needing improvement
5. Missing elements

Be constructive and specific. If it's good quality (8+), say so clearly."""

        critic_system = """You are an experienced reviewer who provides balanced, helpful feedback. 
Be thorough but fair. Point out both strengths and areas for improvement."""
        
        feedback = ask_ollama(critic_prompt, critic_system)
        
        if "Error:" in feedback:
            print(f"❌ Critic failed: {feedback}")
            return None
            
        print(f"✅ Critic completed review")
        print(f"📄 Feedback length: {len(feedback)} characters")
        print(f"📝 Preview: {feedback[:200]}...")
        
        # === AGENT 3: VALIDATOR ===
        print(f"\n⚖️ AGENT 3 (VALIDATOR) - Making final decision...")
        
        validator_prompt = f"""TASK: {task}

WORKER'S SUBMISSION:
{current_work}

CRITIC'S REVIEW:
{feedback}

As the final validator, decide if this work is acceptable. Consider:
- Does it complete the task requirements?
- Is the quality good enough (7+ out of 10)?
- Are the critic's concerns serious enough to require revision?

Respond with EXACTLY one of these formats:
"APPROVED: [brief reason why it's acceptable]"
"REJECTED: [specific issues that must be fixed]"

Be decisive. Start with either APPROVED or REJECTED."""

        validator_system = """You are the final authority on quality. Make clear decisions. 
If work is solid and addresses the task well, approve it. If there are significant 
issues that impact usefulness, reject it with specific guidance."""
        
        decision = ask_ollama(validator_prompt, validator_system)
        
        if "Error:" in decision:
            print(f"❌ Validator failed: {decision}")
            return None
            
        print(f"✅ Validator made decision")
        print(f"🎯 Decision: {decision[:150]}...")
        

# Check decision - improved parsing
        decision_clean = decision.replace("*", "").replace("#", "").upper().strip()
        
        # Look for approval keywords anywhere in the first part of the response
        approval_keywords = ["APPROVED", "APPROVE", "ACCEPT", "ACCEPTABLE", "GOOD ENOUGH"]
        rejection_keywords = ["REJECTED", "REJECT", "NEEDS IMPROVEMENT", "NOT ACCEPTABLE", "REVISE"]
        
        is_approved = any(keyword in decision_clean[:100] for keyword in approval_keywords)
        is_rejected = any(keyword in decision_clean[:100] for keyword in rejection_keywords)
        
        if is_approved and not is_rejected:
            print(f"\n🎉 SUCCESS! Task approved after {round_num} round(s)")
            print("\n" + "=" * 80)
            print("🏆 FINAL APPROVED WORK:")
            print("=" * 80)
            print(current_work)
            print("\n" + "=" * 80)
            return current_work
        elif is_rejected or not is_approved:
            print(f"📝 Round {round_num} complete - needs improvement")
            if round_num < max_rounds:
                print("🔄 Proceeding to next round...")
        else:
            print("⚠️ Validator response unclear, treating as rejected")

    
    # If we get here, we've used all rounds
    print(f"\n⏰ Maximum rounds ({max_rounds}) reached")
    print("\n" + "=" * 80)
    print("📋 FINAL WORK (NOT APPROVED):")
    print("=" * 80)
    print(current_work)
    print("\n" + "=" * 80)
    return current_work

def main():
    """Main function"""
    print("🤖 THREE-AGENT VALIDATION SYSTEM")
    print("=" * 50)
    print("Agent 1: Worker (creates the work)")
    print("Agent 2: Critic (reviews and provides feedback)") 
    print("Agent 3: Validator (makes final approve/reject decision)")
    print("=" * 50)
    
    # Test connection
    print("\n🔌 Testing Ollama connection...")
    test = ask_ollama("Say 'Connection successful!'", "", "llama3.2")
    
    if "Error:" in test:
        print(f"❌ Connection failed: {test}")
        print("\n💡 Troubleshooting:")
        print("1. Is Ollama running? Try: ollama serve")
        print("2. Is the model available? Try: ollama list")
        return
    else:
        print(f"✅ Connection successful!")
        print(f"🤖 Test response: {test}")
    
    # Sample tasks
    sample_tasks = [
        "Write a Python function to calculate compound interest with documentation and examples",
        "Create a 3-paragraph explanation of why exercise is important for mental health",
        "Design a simple daily routine for someone working from home",
        "Write a professional email declining a job offer politely"
    ]
    
    print(f"\n📋 Choose a task to test:")
    for i, task in enumerate(sample_tasks, 1):
        print(f"{i}. {task}")
    print(f"5. Enter your own task")
    
    # Get user choice
    while True:
        try:
            choice = input(f"\n👉 Enter choice (1-5): ").strip()
            
            if choice in ["1", "2", "3", "4"]:
                selected_task = sample_tasks[int(choice) - 1]
                break
            elif choice == "5":
                selected_task = input("📝 Enter your task: ").strip()
                if selected_task:
                    break
                print("❌ Please enter a task!")
            else:
                print("❌ Please enter 1, 2, 3, 4, or 5")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return
        except:
            print("❌ Invalid input, try again")
    
    # Run the validation process
    print(f"\n🎯 Selected task: {selected_task}")
    input("\n⏯️ Press Enter to start the three-agent process...")
    
    result = run_agent_validation(selected_task, max_rounds=3)
    
    if result:
        print(f"\n✨ Process complete! The three agents worked together to create and validate the work.")
    else:
        print(f"\n❌ Process failed due to technical issues.")

if __name__ == "__main__":
    main()
