# Three-Agent Validation System with Ollama

A powerful multi-agent AI system that uses three specialized agents to collaboratively create, review, and validate high-quality work through iterative feedback loops.

![Three-Agent System](https://img.shields.io/badge/Agents-3-blue) ![Python](https://img.shields.io/badge/Python-3.8+-green) ![Ollama](https://img.shields.io/badge/Ollama-Compatible-orange) ![Languages](https://img.shields.io/badge/Languages-Multi--language-purple)

## 🤖 How It Works

The system employs three specialized AI agents that work together:

1. **🔨 Agent 1 (Worker)**: Creates the initial work and implements improvements based on feedback
2. **🔍 Agent 2 (Critic)**: Provides detailed feedback, identifies issues, and suggests improvements
3. **⚖️ Agent 3 (Validator)**: Makes final approval decisions and guides the improvement process

The agents continue working in rounds until the quality meets your standards or the maximum iterations are reached.

## ✨ Features

- 🌐 **Beautiful Web Interface**: Real-time progress tracking with responsive design
- 🖥️ **Command Line Interface**: Quick CLI for simple tasks
- 🔄 **Iterative Improvement**: Automatic feedback loops until quality standards are met
- 🌍 **Multi-language Support**: Works with English, Romanian, Spanish, French, German, and more
- 🎯 **Customizable Quality**: Adjustable validation criteria and agent personalities
- 📊 **Progress Monitoring**: Watch agents work in real-time
- 🚀 **Background Processing**: Run tasks while you do other work
- 📱 **Mobile Friendly**: Access from any device

## 🚀 Quick Start

### Prerequisites

- [Ollama](https://ollama.ai) installed and running
- Python 3.8+ with pip
- At least one language model (recommended: \`ollama pull llama3.2\`)

### Installation

1. **Clone the repository:**
\`\`\`bash
git clone https://github.com/glcatrina/Three-Agent-Validation-System.git
cd Three-Agent-Validation-System
\`\`\`

2. **Set up virtual environment:**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\\Scripts\\activate     # Windows
\`\`\`

3. **Install dependencies:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Verify Ollama is running:**
\`\`\`bash
curl http://localhost:11434/api/tags
\`\`\`

### Usage

#### 🌐 Web Interface (Recommended)
\`\`\`bash
python3 web_agents.py
\`\`\`
Then open: **http://localhost:5000**

#### 🖥️ Command Line Interface
\`\`\`bash
python3 simple_agents.py
\`\`\`

## 🎯 Example Tasks

### English Examples
- "Write a Python function to calculate compound interest with documentation and examples"
- "Create a marketing strategy for a sustainable clothing brand targeting millennials"
- "Design a daily routine for someone working from home effectively"
- "Write a professional email declining a job offer politely"

### Romanian Examples
- "Scrie un ghid complet pentru lucrul de acasă eficient"
- "Creează o strategie de marketing pentru o cafenea locală din București"
- "Explică în română cum să instalezi Python pe Windows cu pași detaliați"
- "Dezvoltă o funcție Python pentru calcularea impozitului pe venit în România"

## ⚙️ Configuration

### Model Selection
Edit the model parameter in your files to use different Ollama models:
\`\`\`python
# For better quality (if you have it)
model="llama3.1:70b"

# For speed
model="llama3.2"

# For coding tasks
model="deepseek-coder:6.7b"
\`\`\`

## 🌐 Multi-language Support

The system works excellently with multiple languages:
- 🇺🇸 **English** (best performance)
- 🇷🇴 **Romanian** (very good performance)
- 🇪🇸 **Spanish**, 🇫🇷 **French**, 🇩🇪 **German** (very good)
- 🇷🇺 **Russian**, 🇨🇳 **Chinese**, 🇯🇵 **Japanese** (good)

For best Romanian results, use larger models like \`llama3.1:70b\`.

## 🔧 Running in Background

### Using Screen (Recommended)
\`\`\`bash
screen -S web-agents
python3 web_agents.py
# Press Ctrl+A, then D to detach
# Reconnect later with: screen -r web-agents
\`\`\`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: \`git checkout -b feature-name\`
3. Commit changes: \`git commit -am 'Add feature'\`
4. Push to branch: \`git push origin feature-name\`
5. Submit a Pull Request

## 📝 License

MIT License - feel free to use, modify, and distribute!

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for excellent local LLM hosting
- [Flask](https://flask.palletsprojects.com/) for the web framework
- The open-source AI community for inspiration and feedback

---

**Built with ❤️ for the AI community**

⭐ **Star this repo if you find it useful!**
