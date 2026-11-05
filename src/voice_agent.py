import asyncio
import base64
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
import edge_tts
import config

class VoiceAgent:
    def __init__(self, voice: str = "", elevenlabs_key: str = "", elevenlabs_voice_id: str = ""):
        self.edge_voice = voice or config.VOICE_NAME
        self.rate = config.VOICE_RATE
        self.pitch = config.VOICE_PITCH
        self.elevenlabs_key = elevenlabs_key or config.ELEVENLABS_API_KEY
        self.elevenlabs_voice_id = elevenlabs_voice_id or config.ELEVENLABS_VOICE_ID

    def generate_speech(self, text: str, output_path: Path) -> List[Dict[str, Any]]:
        """
        Main entry point for voice generation:
        1. Tries ElevenLabs (if ELEVENLABS_API_KEY is configured).
        2. Automatic fallback to Microsoft Edge Neural TTS (100% free, unlimited).
        """
        if self.elevenlabs_key:
            try:
                print(f"[VoiceAgent] Synthesizing hyper-realistic voice via ElevenLabs (Voice: {self.elevenlabs_voice_id})...")
                cues = self._generate_with_elevenlabs(text, output_path)
                if cues and output_path.exists() and output_path.stat().st_size > 1000:
                    print(f"[VoiceAgent] ElevenLabs voiceover saved: {output_path.name}")
                    return cues
            except Exception as e:
                print(f"[VoiceAgent] ElevenLabs failed ({e}). Falling back to Microsoft Edge Neural Voice.")

        # Fallback to Edge-TTS
        return asyncio.run(self._generate_with_edge_tts(text, output_path))

    def _generate_with_elevenlabs(self, text: str, output_path: Path) -> List[Dict[str, Any]]:
        """
        Calls ElevenLabs API with character/word alignment timestamps.
        """
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.elevenlabs_voice_id}/with-timestamps"
        headers = {
            "xi-api-key": self.elevenlabs_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.80,
                "style": 0.05
            }
        }

        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"ElevenLabs status {resp.status_code}: {resp.text[:200]}")

        data = resp.json()
        audio_b64 = data.get("audio_base64")
        if not audio_b64:
            raise RuntimeError("ElevenLabs response did not contain audio_base64.")

        # Save MP3 audio
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(audio_b64))

        alignment = data.get("alignment", {})
        characters = alignment.get("characters", [])
        start_times = alignment.get("character_start_times_seconds", [])
        end_times = alignment.get("character_end_times_seconds", [])

        # Reconstruct sentence cues from character alignment
        cues = self._parse_elevenlabs_alignment(characters, start_times, end_times, text)
        return cues

    def _parse_elevenlabs_alignment(
        self,
        characters: List[str],
        start_times: List[float],
        end_times: List[float],
        full_text: str
    ) -> List[Dict[str, Any]]:
        """Groups character alignments into sentence cues for subtitle engine."""
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', full_text) if s.strip()]
        if not characters or not start_times:
            # Fallback to proportional duration splitting
            return self._proportional_cues(sentences, end_times[-1] if end_times else 40.0)

        cues: List[Dict[str, Any]] = []
        char_idx = 0
        total_chars = len(characters)

        for sent in sentences:
            # Find start time of sentence
            while char_idx < total_chars and characters[char_idx].isspace():
                char_idx += 1
            if char_idx >= total_chars:
                break

            s_start = start_times[char_idx] if char_idx < len(start_times) else 0.0
            # Advance through characters of this sentence
            sent_len = len(sent)
            end_target = min(total_chars - 1, char_idx + sent_len - 1)
            s_end = end_times[end_target] if end_target < len(end_times) else s_start + 4.0
            char_idx = end_target + 1

            cues.append({
                "type": "SentenceBoundary",
                "text": sent,
                "start": s_start,
                "end": max(s_start + 0.5, s_end)
            })

        return cues

    def _proportional_cues(self, sentences: List[str], total_duration: float) -> List[Dict[str, Any]]:
        total_words = sum(len(s.split()) for s in sentences) or 1
        current_time = 0.0
        cues = []
        for s in sentences:
            w_count = len(s.split())
            dur = (w_count / total_words) * total_duration
            cues.append({
                "type": "SentenceBoundary",
                "text": s,
                "start": current_time,
                "end": current_time + dur
            })
            current_time += dur
        return cues

    async def _generate_with_edge_tts(self, text: str, output_path: Path) -> List[Dict[str, Any]]:
        print(f"[VoiceAgent] Synthesizing voiceover with Microsoft Edge Neural Voice: '{self.edge_voice}'...")
        comm = edge_tts.Communicate(
            text=text,
            voice=self.edge_voice,
            rate=self.rate,
            pitch=self.pitch
        )

        cues: List[Dict[str, Any]] = []

        with open(output_path, "wb") as f:
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    f.write(chunk["data"])
                elif chunk["type"] in ("SentenceBoundary", "WordBoundary"):
                    start_sec = chunk["offset"] / 10_000_000.0
                    duration_sec = chunk["duration"] / 10_000_000.0
                    cues.append({
                        "type": chunk["type"],
                        "text": chunk.get("text", "").strip(),
                        "start": start_sec,
                        "end": start_sec + duration_sec
                    })

        print(f"[VoiceAgent] Voiceover generated and saved to: {output_path.name}")
        return cues


if __name__ == "__main__":
    agent = VoiceAgent()
    out = config.TEMP_DIR / "sample_voice.mp3"
    cues = agent.generate_speech("If you wake up at 3 AM every night, your body is sending you a clear signal.", out)
    print(f"Generated {len(cues)} cues:")
    for c in cues:
        print(f"[{c['start']:.2f}s -> {c['end']:.2f}s]: {c['text']}")
