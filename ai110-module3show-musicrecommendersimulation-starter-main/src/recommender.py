import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored_songs = []
        for song in self.songs:
            score = 0.0
            if user.favorite_genre.lower() == song.genre.lower():
                score += 2.0
            if user.favorite_mood.lower() == song.mood.lower():
                score += 1.0
            
            # Energy similarity score
            score += max(0.0, 1.0 - abs(user.target_energy - song.energy))
            
            # Acousticness similarity score based on boolean preference
            target_ac = 1.0 if user.likes_acoustic else 0.0
            score += max(0.0, 1.0 - abs(target_ac - song.acousticness))
            
            scored_songs.append((score, song))
        
        # Sort descending by score (index 0 of the tuple)
        scored_songs.sort(key=lambda x: x[0], reverse=True)
        
        # Extract and return just the top K Song objects
        return [song for score, song in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if user.favorite_genre.lower() == song.genre.lower():
            reasons.append("genre match (+2.0)")
        if user.favorite_mood.lower() == song.mood.lower():
            reasons.append("mood match (+1.0)")
        
        e_score = max(0.0, 1.0 - abs(user.target_energy - song.energy))
        reasons.append(f"energy match (+{e_score:.2f})")
        
        target_ac = 1.0 if user.likes_acoustic else 0.0
        a_score = max(0.0, 1.0 - abs(target_ac - song.acousticness))
        reasons.append(f"acousticness match (+{a_score:.2f})")
        
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert string numerals to appropriate types for math
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if user_prefs.get('favorite_genre') and user_prefs['favorite_genre'].lower() == song['genre'].lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if user_prefs.get('favorite_mood') and user_prefs['favorite_mood'].lower() == song['mood'].lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    if 'target_energy' in user_prefs:
        energy_score = max(0.0, 1.0 - abs(user_prefs['target_energy'] - song['energy']))
        score += energy_score
        reasons.append(f"energy match (+{energy_score:.2f})")

    if 'target_acousticness' in user_prefs:
        acoustic_score = max(0.0, 1.0 - abs(user_prefs['target_acousticness'] - song['acousticness']))
        score += acoustic_score
        reasons.append(f"acoustic match (+{acoustic_score:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        # Create a tuple of (song dictionary, calculated score, string of reasons)
        scored_songs.append((song, score, explanation))
        
    # Sort by the calculated score (index 1 of the tuple) in descending order
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    return scored_songs[:k]