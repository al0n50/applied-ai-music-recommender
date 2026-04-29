"""
Command line runner for the Music Recommender Simulation with AI Guardrails.
"""
import logging
from src.recommender import load_songs, recommend_songs

# 1. Setup Logging for Site Reliability tracking
logging.basicConfig(filename='recommender_system.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def ai_guardrail_check(user_prefs, profile_name):
    """Reliability testing: Prevents system crashes from bad inputs."""
    required_keys = ['favorite_genre', 'favorite_mood', 'target_energy']
    
    for key in required_keys:
        if key not in user_prefs:
            logging.error(f"Guardrail triggered for '{profile_name}': Missing parameter '{key}'")
            return False
            
    # Check for adversarial inputs or extreme edge cases
    if user_prefs.get('target_energy', 0) > 1.0 or user_prefs.get('target_energy', 0) < 0.0:
        logging.error(f"Guardrail triggered for '{profile_name}': Energy out of bounds.")
        return False
        
    return True

def main() -> None:
    # Load the dataset
    try:
        songs = load_songs("data/songs.csv")
        print(f"✅ Loaded {len(songs)} songs into the catalog.\n")
        logging.info("System initialized successfully. Catalog loaded.")
    except Exception as e:
        logging.critical(f"Failed to load catalog: {e}")
        return

    # 2. Define custom profiles to stress-test the system
    profiles = {
        "Studio Ghibli Relaxer": {
            "favorite_genre": "classical",
            "favorite_mood": "calm",
            "target_energy": 0.15,
            "target_acousticness": 0.95
        },
        "Night Drive ModLog Coder": {
            "favorite_genre": "synthwave",
            "favorite_mood": "moody",
            "target_energy": 0.70,
            "target_acousticness": 0.20
        },
        "Corrupted Edge Case (Adversarial)": {
            "favorite_genre": "metal",
            # Intentionally missing 'target_energy' to test the guardrail
        }
    }

    # 3. Generate recommendations and evaluate confidence
    for profile_name, user_prefs in profiles.items():
        print(f"🎧 Top recommendations for: {profile_name} 🎧")
        print("-" * 60)
        
        logging.info(f"Processing profile: {profile_name}")
        
        # Guardrail Check before processing
        if not ai_guardrail_check(user_prefs, profile_name):
            print("⚠️ AI Guardrail Blocked: Invalid or incomplete profile parameters. Check system logs for details.\n")
            continue

        recommendations = recommend_songs(user_prefs, songs, k=2)
        
        for i, rec in enumerate(recommendations, 1):
            song, score, explanation = rec
            
            # Confidence Scorer evaluates if the math actually found a good match
            confidence_level = "High" if score >= 2.5 else "Low (Possible Poor Match)"
            if score < 2.5:
                logging.warning(f"Low confidence recommendation served to {profile_name}: '{song['title']}'")

            print(f"{i}. {song['title']} by {song['artist']} (Score: {score:.2f} | Confidence: {confidence_level})")
            print(f"   Because: {explanation}")
            print(f"   [Data: Genre={song['genre']} | Mood={song['mood']} | Energy={song['energy']}]\n")

if __name__ == "__main__":
    main()