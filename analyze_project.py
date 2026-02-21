import os
import re

def analyze_codebase(root_dir):
    report = []
    report.append("=========================================")
    report.append("      MathPilot Final Project Analysis   ")
    report.append("=========================================")
    
    # Categories to track
    found_ocr = False
    found_asr = False
    found_parser = False
    found_router = False
    found_solver = False
    found_verifier = False
    found_explainer = False
    found_rag = False
    found_hitl = False
    found_memory = False
    found_streamlit = False
    hardcoded_flags = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip virtual envs and git
        dirnames[:] = [d for d in dirnames if d not in ['.venv', 'venv', '.git', '__pycache__', 'node_modules', '.streamlit']]
        
        for file in filenames:
            if file.endswith('.py') or file.endswith('.toml') or file.endswith('.txt'):
                filepath = os.path.join(dirpath, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 1. Multimodal Input
                        if re.search(r'tesseract|easyocr|paddleocr|pytesseract|google\.cloud\.vision|gemini.*flash', content, re.I):
                            found_ocr = True
                        if re.search(r'whisper|SpeechRecognition|speech_recognition|audio_input', content, re.I):
                            found_asr = True
                            
                        # 2 & 4. Agents
                        if re.search(r'class\s+.*Parser', content, re.I) or re.search(r'ParserAgent', content, re.I):
                            found_parser = True
                        if re.search(r'class\s+.*Router', content, re.I) or re.search(r'IntentRouter', content, re.I) or re.search(r'RouterAgent', content, re.I):
                            found_router = True
                        if re.search(r'class\s+.*Solver', content, re.I) or re.search(r'SolverAgent', content, re.I):
                            found_solver = True
                        if re.search(r'class\s+.*Verifier', content, re.I) or re.search(r'VerifierAgent', content, re.I) or re.search(r'CriticAgent', content, re.I):
                            found_verifier = True
                        if re.search(r'class\s+.*Explainer', content, re.I) or re.search(r'ExplainerAgent', content, re.I) or re.search(r'TutorAgent', content, re.I):
                            found_explainer = True
                            
                        # 3. RAG Pipeline
                        if re.search(r'chroma|faiss|pinecone|weaviate|qdrant|vectorstore|embeddings|retriever', content, re.I):
                            found_rag = True
                            
                        # 5. UI
                        if re.search(r'import streamlit|st\.', content):
                            found_streamlit = True
                            
                        # 7. HITL
                        if re.search(r'needs_clarification|hitl|human_in_the_loop|human in the loop|st\.button\(.*Correct.*\)|st\.button\(.*Incorrect.*\)|User Input Required', content, re.I):
                            found_hitl = True
                            
                        # 8. Memory & Self-Learning
                        if re.search(r'sqlite3|sqlalchemy|sessionmaker|context|history', content, re.I):
                            found_memory = True
                            
                        # Check for hardcoding (simplified heuristic: returning large static strings or fixed answers)
                        # Look for strings indicating fake solving:
                        if re.search(r'return\s+["\']The answer is \d+["\']', content) or \
                           re.search(r'return\s+\{.*"answer":\s*"\d+".*\}', content) or \
                           re.search(r'sleep\(.*\)\s*;\s*return\s+["\'].*["\']', content):
                            hardcoded_flags.append(f"Potential hardcoded response found in {filepath}")
                            
                except Exception as e:
                    pass

    # Scoring out of 8 categories (Deployment is 9th but hard to verify statically)
    score = 0
    max_score = 80 # 10 points per section
    
    report.append("\n--- FEATURE CHECKLIST ---")
    
    def check_print(val, name, points):
        nonlocal score
        if val:
            report.append(f"[✓] {name} (+{points} pts)")
            score += points
        else:
            report.append(f"[x] {name} (0 pts)")
            
    # Section 1
    if found_ocr and found_asr:
        check_print(True, "1. Multimodal Input (OCR & ASR)", 10)
    elif found_ocr:
        check_print(True, "1. Multimodal Input (OCR Partial)", 5)
    elif found_asr:
        check_print(True, "1. Multimodal Input (ASR Partial)", 5)
    else:
        check_print(False, "1. Multimodal Input (Missing)", 10)
        
    check_print(found_parser, "2. Parser Agent", 10)
    check_print(found_rag, "3. RAG Pipeline", 10)
    
    agent_count = sum([found_parser, found_router, found_solver, found_verifier, found_explainer])
    if agent_count == 5:
        check_print(True, "4. Multi-Agent System (All 5 agents found)", 10)
    elif agent_count > 0:
        check_print(True, f"4. Multi-Agent System (Partial: {agent_count}/5 agents)", agent_count * 2)
    else:
        check_print(False, "4. Multi-Agent System (No agents found)", 10)
        
    check_print(found_streamlit, "5. Application UI (Streamlit detected)", 10)
    check_print(True, "6. Deployment (Assume True if running on Railway/Streamlit Cloud - manual check required)", 0) # Non-scoring for static
    check_print(found_hitl, "7. Human-in-the-Loop (HITL triggers found)", 10)
    check_print(found_memory, "8. Memory & Self-Learning (DB/Memory found)", 10)
    
    # 9. Hardcoding Check
    report.append("\n--- HARDCODING SCRUTINY ---")
    if len(hardcoded_flags) > 0:
        report.append("[!] WARNING: Potential hardcoded values and mock responses detected:")
        for flag in hardcoded_flags:
            report.append(f"  - {flag}")
        score -= min(30, len(hardcoded_flags) * 10) # Penalty
    else:
        report.append("[✓] No obvious hardcoded mock responses detected. System appears dynamic.")
    
    report.append("\n=========================================")
    report.append(f" FINAL SCORE: {max(0, score)} / {max_score}")
    score_pct = (max(0, score) / max_score) * 100
    report.append(f" EQUIVALENT GRADE: {score_pct:.1f}%")
    report.append("=========================================\n")
    
    return "\n".join(report)

if __name__ == "__main__":
    report_text = analyze_codebase(".")
    with open("grading_report.txt", "w", encoding="utf-8") as rf:
        rf.write(report_text)
    print(report_text)
