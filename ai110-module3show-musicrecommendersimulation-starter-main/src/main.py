"""
Command line runner for the Music Recommender Simulation.
"""
from src.recommender import load_songs, recommend_songs

def main() -> None:
    # 1. Load the dataset
    songs = load_songs("data/songs.csv") 
    print(f"✅ Loaded {len(songs)} songs into the catalog.\n")

    # 2. Phase 4: Define at least three distinct user profiles for stress testing
    profiles = {
        "High-Energy Pop Fan": {
            "favorite_genre": "pop", 
            "favorite_mood": "happy", 
            "target_energy": 0.85,
            "target_acousticness": 0.10
        },
        "Chill Lofi Student": {
            "favorite_genre": "lofi", 
            "favorite_mood": "chill", 
            "target_energy": 0.35,
            "target_acousticness": 0.85
        },
        "Deep Intense Rocker (Adversarial/Edge Case)": {
            "favorite_genre": "rock", 
            "favorite_mood": "sad",  # Conflicting preference test: rock is rarely sad in our data
            "target_energy": 0.90,
            "target_acousticness": 0.05
        }
    }

    # 3. Generate recommendations for each profile
    for profile_name, user_prefs in profiles.items():
        print(f"🎧 Top recommendations for: {profile_name} 🎧")
        print("-" * 60)
        
        recommendations = recommend_songs(user_prefs, songs, k=3)

        for i, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            print(f"{i}. {song['title']} by {song['artist']} (Score: {score:.2f})")
            print(f"   Because: {explanation}")
            print(f"   [Data: Genre={song['genre']} | Mood={song['mood']} | Energy={song['energy']}]\n")

if __name__ == "__main__":
    main()