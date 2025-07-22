#!/usr/bin/env python3
"""
Flask Web Interface for Three-Agent Validation System
Run this to access your agents through a web browser
"""

from flask import Flask, render_template, request, jsonify, session
import requests
import json
import uuid
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change this to something secure

# Store active sessions and their progress
active_sessions = {}

def ask_ollama(prompt, system_message="", model="llama3.2"):
    """Ask Ollama a question and get response"""
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "system": system_message,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 800
        }
    }
    
    try:
        response = requests.post(url, json=data, timeout=120)
        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            return f"Error: HTTP {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def run_agent_validation_async(session_id, task, max_rounds=3):
    """Run the three-agent validation process asynchronously"""
    
    # Initialize session data
    active_sessions[session_id] = {
        "status": "running",
        "task": task,
        "current_round": 0,
        "max_rounds": max_rounds,
        "rounds": [],
        "final_result": None,
        "start_time": datetime.now().isoformat()
    }
    
    current_work = ""
    
    for round_num in range(1, max_rounds + 1):
        # Update session status
        active_sessions[session_id]["current_round"] = round_num
        active_sessions[session_id]["status"] = f"Round {round_num} - Agent 1 Working"
        
        # === AGENT 1: WORKER ===
        if round_num == 1:
            worker_prompt = f"Complete this task thoroughly and professionally: {task}"
        else:
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
            active_sessions[session_id]["status"] = "error"
            active_sessions[session_id]["error"] = current_work
            return
        
        # Update status
        active_sessions[session_id]["status"] = f"Round {round_num} - Agent 2 Reviewing"
        
        # === AGENT 2: CRITIC ===
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
            active_sessions[session_id]["status"] = "error"
            active_sessions[session_id]["error"] = feedback
            return
        
        # Update status
        active_sessions[session_id]["status"] = f"Round {round_num} - Agent 3 Deciding"
        
        # === AGENT 3: VALIDATOR ===
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
            active_sessions[session_id]["status"] = "error"
            active_sessions[session_id]["error"] = decision
            return
        
        # Store round data
        round_data = {
            "round": round_num,
            "worker_output": current_work,
            "critic_feedback": feedback,
            "validator_decision": decision,
            "timestamp": datetime.now().isoformat()
        }
        active_sessions[session_id]["rounds"].append(round_data)
        
        # Check decision - improved parsing
        decision_clean = decision.replace("*", "").replace("#", "").upper().strip()
        approval_keywords = ["APPROVED", "APPROVE", "ACCEPT", "ACCEPTABLE", "GOOD ENOUGH"]
        rejection_keywords = ["REJECTED", "REJECT", "NEEDS IMPROVEMENT", "NOT ACCEPTABLE", "REVISE"]
        
        is_approved = any(keyword in decision_clean[:100] for keyword in approval_keywords)
        is_rejected = any(keyword in decision_clean[:100] for keyword in rejection_keywords)
        
        if is_approved and not is_rejected:
            # Task approved!
            active_sessions[session_id]["status"] = "completed"
            active_sessions[session_id]["final_result"] = {
                "approved": True,
                "rounds_used": round_num,
                "final_work": current_work,
                "completion_time": datetime.now().isoformat()
            }
            return
    
    # If we get here, we've used all rounds without approval
    active_sessions[session_id]["status"] = "completed"
    active_sessions[session_id]["final_result"] = {
        "approved": False,
        "rounds_used": max_rounds,
        "final_work": current_work,
        "completion_time": datetime.now().isoformat()
    }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/start_task', methods=['POST'])
def start_task():
    """Start a new validation task"""
    data = request.json
    task = data.get('task', '').strip()
    
    if not task:
        return jsonify({"error": "Task cannot be empty"}), 400
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    # Start the validation process in a background thread
    thread = threading.Thread(target=run_agent_validation_async, args=(session_id, task))
    thread.daemon = True
    thread.start()
    
    return jsonify({"session_id": session_id})

@app.route('/get_status/<session_id>')
def get_status(session_id):
    """Get the current status of a validation session"""
    if session_id not in active_sessions:
        return jsonify({"error": "Session not found"}), 404
    
    return jsonify(active_sessions[session_id])

@app.route('/list_models')
def list_models():
    """Get available Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [model['name'] for model in response.json()['models']]
            return jsonify({"models": models})
        else:
            return jsonify({"error": "Cannot connect to Ollama"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test_connection')
def test_connection():
    """Test Ollama connection"""
    test_response = ask_ollama("Say 'Connection OK'", "", "llama3.2")
    if "Error:" in test_response:
        return jsonify({"connected": False, "error": test_response})
    else:
        return jsonify({"connected": True, "response": test_response})

if __name__ == '__main__':
    print("🌐 Starting Three-Agent Validation Web Interface...")
    print("📁 Make sure you have the templates/index.html file")
    print("🚀 Once started, open: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
