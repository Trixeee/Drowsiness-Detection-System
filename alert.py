import pygame
import threading
import time
import random
from datetime import datetime
import os

# ================= SOUND ALERT =================
def play_sound_alert(sound_path):
    def _play():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception:
            pass
    threading.Thread(target=_play, daemon=True).start()


# ================= ON-SCREEN WARNING =================
def display_warning(frame, text="DROWSINESS DETECTED!"):
    import cv2
    cv2.putText(
        frame,
        text,
        (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 0, 255),
        3
    )


# ================= BFS ALERT PROPAGATION =================
def bfs_alert_propagation(alert_tree, start_node):
    visited = set()
    queue = [start_node]
    order = []

    while queue:
        node = queue.pop(0)
        if node not in visited:
            order.append(node)
            visited.add(node)
            queue.extend(alert_tree.get(node, []))

    return order


# ================= GEN-AI ALERT GENERATOR =================
def generate_gen_ai_alert(alert_type, alert_count):
    """
    Gen-AI style alert generation with:
    - Severity awareness
    - Day / Night context
    - Randomized human-like suggestions
    """

    alert_type = alert_type.lower()

    # ===== DAY / NIGHT DETECTION =====
    hour = datetime.now().hour
    is_night = hour >= 22 or hour <= 5

    # ===== SUGGESTION POOLS =====
    day_low = [
        "Drink some water and stay hydrated.",
        "Blink frequently and adjust your posture.",
        "Open a window slightly for fresh air."
    ]

    day_mid = [
        "Drink some water and slow down slightly.",
        "Stretch your neck and shoulders.",
        "Take a short pause if possible."
    ]

    day_high = [
        "Stop the vehicle safely and take a 10–15 minute break.",
        "Drink water and rest before continuing.",
        "Switch drivers if possible."
    ]

    night_low = [
        "Stay alert and keep the cabin well lit.",
        "Adjust ventilation to avoid monotony.",
        "Focus on road markings to stay attentive."
    ]

    night_mid = [
        "Drink water or a mild caffeinated drink.",
        "Reduce speed and stay extra cautious.",
        "Consider stopping briefly to refresh."
    ]

    night_high = [
        "High risk during night driving. Stop immediately and rest.",
        "Drink water or coffee and take a power nap.",
        "Avoid continuing to drive until fully alert."
    ]

    # ===== MESSAGE LOGIC =====
    if alert_count >= 3:
        base_message = (
            f"High risk detected. Repeated {alert_type} events observed. "
            f"Immediate rest is strongly recommended."
        )
        suggestion = random.choice(night_high if is_night else day_high)

    elif alert_count == 2:
        base_message = (
            f"Moderate fatigue detected due to consecutive {alert_type} signs. "
            f"Driver alertness is decreasing."
        )
        suggestion = random.choice(night_mid if is_night else day_mid)

    else:
        base_message = (
            f"Early signs of {alert_type} detected. "
            f"Driver condition should be monitored."
        )
        suggestion = random.choice(night_low if is_night else day_low)

    return f"{base_message} Suggestion: {suggestion}"


# ================= VOICE ALERT (NON-BLOCKING TTS) =================
def speak_gen_ai_alert(message):
    def _speak():
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 165)
            engine.say(message)
            engine.runAndWait()
        except Exception:
            pass

    threading.Thread(target=_speak, daemon=True).start()


# ================= WHATSAPP ALERT (TWILIO) =================
def send_whatsapp_alert(message):
    """
    Sends WhatsApp alert using Twilio
    Credentials are fetched at runtime (FIXES env loading issue)
    """
    try:
        import os
        from twilio.rest import Client

        ACCOUNT_SID = os.getenv("TWILIO_SID")
        AUTH_TOKEN = os.getenv("TWILIO_TOKEN")

        if not ACCOUNT_SID or not AUTH_TOKEN:
            print("⚠️ Twilio credentials not set (runtime check)")
            return

        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        client.messages.create(
            body=f"🚨 Driver Safety Alert 🚨\n\n{message}",
            from_="whatsapp:+14155238886",   # Twilio sandbox number
            to="whatsapp:+919122316662"     # YOUR WhatsApp number
        )

        print("✅ WhatsApp alert sent successfully")

    except Exception as e:
        print("❌ WhatsApp alert failed:", e)

