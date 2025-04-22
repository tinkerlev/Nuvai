# 🤝 Contributing to Nuvai

Thank you for your interest in contributing to **Nuvai**!

Whether you're a developer, a cybersecurity enthusiast, or just someone who wants to help make the internet safer — you're welcome here. Your support helps us make secure development accessible to everyone.

You can contribute by fixing bugs, adding features, improving the UI, writing documentation, testing vulnerability rules, or just sharing ideas and feedback.

---

## 🛠️ How to Contribute

### 1. Fork the Repository  
Click the **"Fork"** button in the top right corner of this page to create your own copy.

### 2. Clone Your Fork
```bash
git clone https://github.com/tinkerlev/Nuvai.git
cd Nuvai
```

### 3. Create a Branch
```bash
git checkout -b feature/my-feature
```
Creating a separate branch helps us keep changes organized.

### 4. Make Your Changes  
You're free to work on anything — code, docs, UI, reports, rules, etc. Please write clean, clear, and secure code if working on logic.

### 5. Commit Your Work
```bash
git commit -m "Add feature: short explanation here"
```

### 6. Push to Your Fork
```bash
git push origin feature/my-feature
```

### 7. Open a Pull Request
Go to your fork on GitHub and click **"New Pull Request"**.

Explain:
- What you changed
- Why you changed it
- Anything to be aware of when reviewing

A pull request is just a friendly suggestion to improve the project — we’ll review it together 💬

---

## 📦 Project Setup

### Backend (Flask API)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend (React App)
```bash
cd ../frontend
npm install
npm run dev
```

---

## ✅ Before Submitting

Please make sure:
- [ ] Your code runs without errors or crashes
- [ ] You didn't leave any debug prints or secrets
- [ ] You explained what you changed
- [ ] Your feature or fix is easy to understand
- [ ] You tested your contribution on Linux (Ubuntu / WSL / Kali)

💡 Not sure? Open a draft PR and ask — we're happy to help!

---

## 🧠 Adding or Editing Vulnerability Rules

If you're contributing to one of the language scanners (e.g. `python_scanner.py`, `html_scanner.py`):

- Use safe and efficient regex or AST-based methods  
- Avoid unnecessary false positives  
- Register your check in `scanner_controller.py`  
- Add comments to explain what the rule does  
- Test your rule on real or demo code in the `/examples/` folder  

---

## 🤋 Not a Coder? You Can Still Help!

- Report bugs, typos, or strange behavior  
- Suggest new vulnerability types  
- Help write documentation or translate  
- Share feedback or test upcoming versions  

Every voice matters 💙

---

## 📬 Need Help?

Have a question, idea, or need help with GitHub?  
Feel free to open a [discussion or issue](https://github.com/tinkerlev/Nuvai) — or email us directly:

**Contact: Eliran Loai Deeb**  
📧 elirandeeb@gmail.com  
🌐 [https://github.com/tinkerlev/Nuvai](https://github.com/tinkerlev/Nuvai)

---

Thank you for helping us secure the future of development 🛡️  
Your contribution makes a real difference.