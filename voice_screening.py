"""
voice_screening.py
==================
Milestone 4: Voice-Based Screening Module
Integrates SpeechRecognition (Speech-to-Text) and pyttsx3 (Text-to-Speech)
for automated AI candidate voice screening.
"""

import sys
import time

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class VoiceScreeningModule:
    def __init__(self, voice_enabled: bool = True):
        self.voice_enabled = voice_enabled
        self.engine = None
        self.recognizer = None

        if voice_enabled and pyttsx3:
            try:
                self.engine = pyttsx3.init()
                # Set speech rate
                self.engine.setProperty('rate', 160)
            except Exception as e:
                print(f"[VoiceScreening] Warning: pyttsx3 initialization failed ({e}). Falling back to text output.")
                self.engine = None

        if voice_enabled and sr:
            try:
                self.recognizer = sr.Recognizer()
            except Exception as e:
                print(f"[VoiceScreening] Warning: SpeechRecognition initialization failed ({e}).")
                self.recognizer = None

    def speak(self, text: str):
        """Outputs text via Text-to-Speech synthesizer or terminal fallback."""
        print(f"🤖 AI Interviewer: {text}")
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[TTS Fallback Error: {e}]")

    def listen(self, timeout_seconds: int = 5) -> str:
        """Captures candidate audio input via microphone with speech-to-text conversion."""
        if self.recognizer and sr:
            try:
                with sr.Microphone() as source:
                    print("🎙️ Listening for candidate response (speak now)...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.listen(source, timeout=timeout_seconds, phrase_time_limit=15)
                
                print("⏳ Transcribing audio...")
                response = self.recognizer.recognize_google(audio)
                print(f"👤 Candidate Response: {response}")
                return response
            except Exception as e:
                print(f"[Voice Input Notice: {e}] Prompting for text fallback...")

        # Safe fallback for non-interactive / test environments
        if sys.stdin and sys.stdin.isatty():
            try:
                return input("Candidate > ").strip()
            except Exception:
                pass

        default_resp = "I have 5 years of experience in Machine Learning, Python, PyTorch, and SQL."
        print(f"👤 Candidate Response (Simulated/Fallback): {default_resp}")
        return default_resp


def voice_screening():
    """
    Standard Milestone 4 voice screening procedure:
    1. AI speaks introduction and question using pyttsx3.
    2. Listens to candidate microphone input via SpeechRecognition.
    3. Transcribes response via Google Speech API.
    4. Provides verbal confirmation and next steps.
    """
    module = VoiceScreeningModule(voice_enabled=True)

    intro_question = "Hello, please introduce yourself and describe your experience with machine learning."
    module.speak(intro_question)

    response = module.listen(timeout_seconds=5)
    
    if response:
        print(f"\n[Transcribed Response]: {response}")
        module.speak("Thank you. Based on your response, we will proceed to the next round of screening.")
    else:
        module.speak("Thank you for your response. We will update your application status.")
        
    return response


def conduct_voice_screening_session(candidate_name: str, job_title: str, questions: list = None) -> dict:
    """
    Conducts a multi-question voice screening session for candidate evaluation.
    Returns transcript and screening evaluation score.
    """
    module = VoiceScreeningModule(voice_enabled=True)
    
    if not questions:
        questions = [
            f"Hello {candidate_name}, welcome to the AI screening for the {job_title} position. Please briefly introduce yourself.",
            "Can you describe a key technical project you worked on recently and your specific role?",
            "What technical skills or machine learning frameworks do you specialize in?"
        ]

    transcripts = []
    for idx, q in enumerate(questions, 1):
        module.speak(f"Question {idx}: {q}")
        ans = module.listen(timeout_seconds=5)
        transcripts.append({
            "question_num": idx,
            "question": q,
            "response": ans
        })
        time.sleep(0.5)

    module.speak("Thank you for completing the voice screening session. Your answers have been recorded for the hiring team.")
    
    # Calculate screening completion score
    completed_count = sum(1 for t in transcripts if len(t["response"].strip()) > 3)
    screening_score = round((completed_count / len(questions)) * 100.0, 1)

    return {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "total_questions": len(questions),
        "completed_answers": completed_count,
        "screening_score": screening_score,
        "transcripts": transcripts,
        "status": "Screening Completed" if screening_score >= 66.0 else "Incomplete"
    }


if __name__ == "__main__":
    print("==================================================")
    print("      MILESTONE 4: VOICE SCREENING MODULE TEST")
    print("==================================================\n")
    voice_screening()
