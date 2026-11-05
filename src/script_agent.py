import json
import random
from typing import Dict, List, Any, Optional, Union
import requests
import config

# Built-in High-Retention Sleep Wellness Scripts with Explicit Dynamic Graphic Card Definitions
CURATED_SLEEP_SCRIPTS = [
    {
        "title": "Why You Wake Up at 3 AM Every Night",
        "topic": "3am_wake_up",
        "scenes": [
            {
                "narration": "If you keep waking up between 3:00 and 4:00 AM every single night, listen carefully.",
                "visual_keyword": "luxury dark bedroom cozy bed",
                "graphic_card": {
                    "tag": "BIOLOGY ALERT",
                    "title": "THE 3 AM WAKEUP GLITCH",
                    "subtitle": "Persistent nighttime awakenings are not an accident",
                    "color": "red",
                    "icon": "⚠️"
                }
            },
            {
                "narration": "This is not a coincidence. It is usually caused by a sudden nighttime spike in your stress hormone, cortisol.",
                "visual_keyword": "brain neural network glowing cortisol",
                "graphic_card": {
                    "tag": "HORMONAL SPIKE",
                    "title": "CORTISOL SURGE DETECTED",
                    "subtitle": "Emergency survival hormones flooding bloodstream",
                    "color": "red",
                    "icon": "⚡"
                }
            },
            {
                "narration": "When your liver runs low on glycogen during the night, your brain releases adrenaline and cortisol to maintain your blood sugar levels.",
                "visual_keyword": "circadian rhythm body clock monitor",
                "graphic_card": {
                    "tag": "METABOLIC SCAN",
                    "title": "LIVER GLYCOGEN DEPLETED",
                    "subtitle": "Blood glucose drop triggers adrenaline alarm",
                    "color": "cyan",
                    "icon": "🧬"
                }
            },
            {
                "narration": "This triggers a survival fight-or-flight response that jolts you wide awake with a racing mind.",
                "visual_keyword": "alarm clock 3 am digital red"
            },
            {
                "narration": "The quick fix? Eat a small spoonful of raw honey or almond butter thirty minutes before bed to stabilize your glucose overnight.",
                "visual_keyword": "raw honey remedy spoon kitchen",
                "graphic_card": {
                    "tag": "PROVEN PROTOCOL",
                    "title": "THE RAW HONEY HACK",
                    "subtitle": "1 Tbsp before bed restores liver glycogen overnight",
                    "color": "green",
                    "icon": "🍯"
                }
            },
            {
                "narration": "Save this video for tonight and follow for science-backed sleep hacks.",
                "visual_keyword": "peaceful deep sleep cozy blanket sunrise"
            }
        ]
    },
    {
        "title": "The Navy SEAL 2-Minute Sleep Method",
        "topic": "military_sleep_method",
        "scenes": [
            {
                "narration": "How military pilots fall asleep in under two minutes, even in loud combat zones.",
                "visual_keyword": "military airplane soldier breathing",
                "graphic_card": {
                    "tag": "MILITARY PROTOCOL",
                    "title": "THE 2-MINUTE SLEEP METHOD",
                    "subtitle": "Developed for combat pilots to sleep under intense stress",
                    "color": "amber",
                    "icon": "⚡"
                }
            },
            {
                "narration": "Step one. Relax every single muscle in your face, including your jaw, tongue, and the muscles around your eyes.",
                "visual_keyword": "close up peaceful human face eyes closed",
                "graphic_card": {
                    "tag": "STEP 1 OF 4",
                    "title": "FACIAL MUSCLE RELEASE",
                    "subtitle": "Drop tension from jaw, tongue, and eyelids completely",
                    "color": "cyan",
                    "icon": "🧠"
                }
            },
            {
                "narration": "Step two. Drop your shoulders as low as they will go, followed by your upper and lower arms on both sides.",
                "visual_keyword": "meditation breathing relaxing shoulders"
            },
            {
                "narration": "Step three. Exhale deeply, releasing tension from your chest, thighs, calves, and feet.",
                "visual_keyword": "calm ocean waves slow motion dark blue",
                "graphic_card": {
                    "tag": "STEP 3 OF 4",
                    "title": "FULL SOMATIC EXHALE",
                    "subtitle": "De-escalate nervous system from fight-or-flight",
                    "color": "cyan",
                    "icon": "🌊"
                }
            },
            {
                "narration": "Step four. Clear your mind completely for ten seconds by repeating the words 'don't think' over and over.",
                "visual_keyword": "deep galaxy stars peaceful night sky",
                "graphic_card": {
                    "tag": "MENTAL RESET",
                    "title": "10-SECOND MIND CLEAR",
                    "subtitle": "Repeat 'don't think' to shut down mental chatter",
                    "color": "purple",
                    "icon": "✨"
                }
            },
            {
                "narration": "With six weeks of practice, this method has a ninety-six percent success rate. Save this to try tonight.",
                "visual_keyword": "deep peaceful sleep cozy bed night",
                "graphic_card": {
                    "tag": "PROVEN RESULTS",
                    "title": "96% SUCCESS RATE",
                    "subtitle": "Save this protocol and try it tonight",
                    "color": "green",
                    "icon": "📌"
                }
            }
        ]
    },
    {
        "title": "The 10-3-2-1-0 Sleep Rule",
        "topic": "sleep_formula",
        "scenes": [
            {
                "narration": "This is the world-famous 10 3 2 1 0 sleep formula used by elite performers.",
                "visual_keyword": "successful person waking up energetic morning",
                "graphic_card": {
                    "tag": "ELITE FORMULA",
                    "title": "THE 10-3-2-1-0 SLEEP RULE",
                    "subtitle": "The exact countdown framework for flawless sleep",
                    "color": "amber",
                    "icon": "⚡"
                }
            },
            {
                "narration": "10 hours before bed: no more caffeine. It takes ten full hours for caffeine to clear your bloodstream.",
                "visual_keyword": "black coffee cup clock time",
                "graphic_card": {
                    "tag": "T-MINUS 10 HOURS",
                    "title": "NO MORE CAFFEINE",
                    "subtitle": "Caffeine half-life takes 10 full hours to clear",
                    "color": "amber",
                    "icon": "☕"
                }
            },
            {
                "narration": "3 hours before bed: no more heavy food or alcohol. Digestion ruins your deep restorative sleep.",
                "visual_keyword": "healthy dinner light food evening"
            },
            {
                "narration": "2 hours before bed: stop working. Give your nervous system time to shift into recovery mode.",
                "visual_keyword": "closing laptop relaxing living room evening",
                "graphic_card": {
                    "tag": "T-MINUS 2 HOURS",
                    "title": "SHUT DOWN WORK",
                    "subtitle": "Allow nervous system to transition to parasympathetic",
                    "color": "cyan",
                    "icon": "💻"
                }
            },
            {
                "narration": "1 hour before bed: shut down all screens. Blue light destroys your natural melatonin production.",
                "visual_keyword": "phone turned off reading book bedside lamp",
                "graphic_card": {
                    "tag": "T-MINUS 1 HOUR",
                    "title": "ZERO SCREENS",
                    "subtitle": "Blue light suppression cuts melatonin by 50%",
                    "color": "red",
                    "icon": "📵"
                }
            },
            {
                "narration": "And zero is the number of times you hit snooze tomorrow morning. Follow for daily sleep science.",
                "visual_keyword": "peaceful luxury bedroom dark cozy atmosphere",
                "graphic_card": {
                    "tag": "WAKE UP ZERO",
                    "title": "ZERO SNOOZE HITS",
                    "subtitle": "Wake up with instant energy and focus",
                    "color": "green",
                    "icon": "☀️"
                }
            }
        ]
    },
    {
        "title": "Why You Must Stop Taking Melatonin",
        "topic": "magnesium_sleep",
        "scenes": [
            {
                "narration": "Stop taking melatonin pills. If you struggle to stay in deep sleep, take this one mineral instead.",
                "visual_keyword": "tired person rubbing eyes insomnia bed",
                "graphic_card": {
                    "tag": "WARNING",
                    "title": "STOP TAKING MELATONIN",
                    "subtitle": "Supplements can downregulate natural receptors",
                    "color": "red",
                    "icon": "⚠️"
                }
            },
            {
                "narration": "Over sixty percent of adults lack adequate magnesium, the mineral that activates your parasympathetic nervous system.",
                "visual_keyword": "calm relaxing spa water drops nature"
            },
            {
                "narration": "Specifically, Magnesium Glycinate binds directly to GABA receptors, calming neural activity and quieting bedtime thoughts.",
                "visual_keyword": "neuroscience brain neural network glowing",
                "graphic_card": {
                    "tag": "SCIENCE DISCOVERY",
                    "title": "MAGNESIUM GLYCINATE",
                    "subtitle": "Activates inhibitory GABA receptors in the brain",
                    "color": "cyan",
                    "icon": "🧬"
                }
            },
            {
                "narration": "Take two hundred to four hundred milligrams thirty minutes before sleep, and watch your deep sleep score transform.",
                "visual_keyword": "glass of water with supplement capsule bedroom",
                "graphic_card": {
                    "tag": "RECOMMENDED DOSE",
                    "title": "200 TO 400 MG",
                    "subtitle": "Consume 30-45 minutes before sleep with water",
                    "color": "green",
                    "icon": "💊"
                }
            },
            {
                "narration": "Save this tip and share it with someone who needs better rest.",
                "visual_keyword": "peaceful deep sleep cozy blanket"
            }
        ]
    }
]

class ScriptAgent:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key or config.GEMINI_API_KEY

    def generate_script(self, research_or_topic: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Recreates the viral video in our own BioSlumber style.
        Accepts either:
        - A full research dict from ViralTrendScout.deep_research_viral_video (Recommended)
        - A topic string prompt
        """
        if self.api_key:
            try:
                print(f"[ScriptAgent] Generating custom remake script with Gemini 2.5 Flash...")
                return self._generate_with_gemini(research_or_topic)
            except Exception as e:
                print(f"[ScriptAgent] Gemini generation note ({e}). Utilizing curated sleep science library.")

        return self._generate_from_library(research_or_topic)

    def _generate_with_gemini(self, context_input: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}

        # Build comprehensive prompt using the deep research deconstruction
        if isinstance(context_input, dict):
            research_info = (
                f"Original Video Title: {context_input.get('title', '')}\n"
                f"What The Full Original Video Is About: {context_input.get('original_full_concept', '')}\n"
                f"Viral Hook Angle: {context_input.get('viral_hook', '')}\n"
                f"Core Problem/Pain Point: {context_input.get('core_problem', '')}\n"
                f"Scientific Biological Mechanism: {context_input.get('scientific_mechanism', '')}\n"
                f"The Actionable Solution/Hack: {context_input.get('actionable_hack', '')}\n"
                f"Remake Strategy: {context_input.get('remake_strategy', '')}"
            )
            target_title = context_input.get("suggested_title") or context_input.get("title")
        else:
            research_info = f"Topic to recreate: {context_input}"
            target_title = str(context_input)[:40]

        system_prompt = (
            "You are an elite short-form video creator and scriptwriter for 'BioSlumber' (a premium scientific sleep & wellness channel). "
            "We are REMAKING a proven viral video in our own unique style. "
            "Deliver the EXACT SAME valuable lesson, problem, biological mechanism, and actionable hack as the original video, "
            "but rewritten in our authoritative, science-backed (Andrew Huberman / Matthew Walker) voice.\n\n"
            "Requirements:\n"
            "1. Script must be 100-130 words (35 to 45 seconds spoken calmly).\n"
            "2. Total 5 to 6 scenes. Each scene narration must be 1-2 punchy spoken sentences in English.\n"
            "3. For EACH scene, provide:\n"
            "   - 'narration': The spoken voiceover text.\n"
            "   - 'visual_keyword': 2 to 4 concise, high-relevance search words for stock video/photo search (e.g. 'alarm clock night', 'military soldier', 'raw honey spoon', 'black coffee cup').\n"
            "   - 'graphic_card' (on 2 to 3 key scenes): Specification for a trendy floating HUD callout card. Include:\n"
            "       * 'tag': e.g. 'BIOLOGY SCAN', 'PROVEN PROTOCOL', 'WARNING', 'STEP 1', 'FACT CHECK'\n"
            "       * 'title': Big bold 3-5 word headline\n"
            "       * 'subtitle': 1-line punchy explanation\n"
            "       * 'color': 'red' (danger/problem), 'cyan' (science/biology), 'green' (solution/hack), or 'amber' (warning/formula)\n"
            "       * 'icon': '⚠️', '⚡', '🧬', '🍯', '🌙', '☕', or '🧠'\n\n"
            "Format strictly as JSON:\n"
            "{\n"
            '  "title": "High CTR Video Title",\n'
            '  "topic": "core_topic_key",\n'
            '  "scenes": [\n'
            '    {\n'
            '      "narration": "Hook opening sentence (0-3s).",\n'
            '      "visual_keyword": "cozy dark bedroom night",\n'
            '      "graphic_card": {"tag": "BIOLOGY ALERT", "title": "HEADLINE", "subtitle": "Detail line", "color": "red", "icon": "⚠️"}\n'
            '    },\n'
            '    ...\n'
            '  ]\n'
            "}"
        )

        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"{system_prompt}\n\nRESEARCH REPORT OF VIRAL HIT TO RECREATE:\n{research_info}"}]}
            ],
            "generationConfig": {
                "temperature": 0.65,
                "responseMimeType": "application/json"
            }
        }

        models_to_try = ["gemini-2.5-flash", "gemini-flash-latest"]
        for model_name in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=22)
                if response.status_code == 200:
                    raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
                    parsed = json.loads(raw_text)
                    print(f"[ScriptAgent] Script successfully created via {model_name}!")
                    return parsed
            except Exception:
                pass

        raise RuntimeError("Gemini models failed to respond.")

    def _generate_from_library(self, context_input: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Returns matching or random viral script from the built-in library."""
        topic_str = ""
        if isinstance(context_input, dict):
            topic_str = f"{context_input.get('title', '')} {context_input.get('core_problem', '')}".lower()
        else:
            topic_str = str(context_input).lower()

        if topic_str:
            for script in CURATED_SLEEP_SCRIPTS:
                if any(word in script["title"].lower() or word in script["topic"].lower() for word in topic_str.split() if len(word) > 3):
                    return script

        return random.choice(CURATED_SLEEP_SCRIPTS)

    def get_full_script_text(self, script_data: Dict[str, Any]) -> str:
        """Combines all scene narrations into a continuous voiceover text."""
        return " ".join([scene["narration"] for scene in script_data.get("scenes", [])])


if __name__ == "__main__":
    agent = ScriptAgent()
    sample_research = {
        "title": "Why You Keep Waking Up at 3:00 AM",
        "original_full_concept": "Waking at 3 AM is caused by nocturnal liver glycogen depletion triggering cortisol.",
        "viral_hook": "Why you wake up at 3 AM every night",
        "core_problem": "Waking at 3 AM with active mind",
        "scientific_mechanism": "Adrenal cortisol surge",
        "actionable_hack": "1 tsp raw honey before bed"
    }
    script = agent.generate_script(sample_research)
    print("Generated Script Title:", script.get("title"))
    for i, s in enumerate(script.get("scenes", [])):
        print(f"Scene {i+1}: [{s.get('visual_keyword')}] {s.get('narration')[:50]}...")
