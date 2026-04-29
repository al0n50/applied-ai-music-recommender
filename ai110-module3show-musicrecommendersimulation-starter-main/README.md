# 🎵 Music Recommender Simulation (VibeFinder 1.0)

## Project Summary

In this project, I built **VibeFinder 1.0**, a content-based music recommender simulation. It transforms a user's musical taste profile (genre, mood, energy, and acousticness) into a personalized playlist by calculating mathematical similarity scores against a custom catalog of 15 songs. 

For the final phase of this project, I engineered an **AI Guardrail & Confidence Scoring System** to wrap around the base recommendation logic. The project highlights both how explicit scoring rules can successfully surface relevant tracks, and how reliability wrappers are essential to prevent edge cases from breaking an AI system.

### 🏗️ System Architecture
*(The visual data flow of the recommendation engine and reliability guardrails)*

![System Architecture](assets/system_architecture.png)

---

## How The System Works

**Understanding Real-World vs. Simulated Recommendations:**
Real-world recommendation engines (like Spotify or TikTok) rely heavily on "collaborative filtering"—finding patterns in millions of users' listening habits and playlists. However, they also use "content-based filtering," which analyzes the actual audio features of a track. This simulation focuses entirely on content-based filtering. It ignores what other people are listening to and strictly compares a user's explicit preferences against the specific metadata of the songs in our catalog.

**Data Representation:**
To make these comparisons, our system relies on two main data objects:
* **Song Features:** Each song in the catalog is evaluated based on its `genre` (e.g., Pop, Rock), `mood` (e.g., happy, chill, intense), `energy` (a scale from 0.0 to 1.0), and `acousticness` (a scale from 0.0 to 1.0).
* **UserProfile Features:** The system represents a user's taste as a dictionary containing their `favorite_genre`, `favorite_mood`, `target_energy`, and `target_acousticness`.

**Algorithm Recipe & Scoring:**
The Recommender loops through the CSV catalog and calculates a numeric score for each song based on how closely its features match the User Profile. The point breakdown is as follows:
* **Genre Match:** +2.0 points for an exact string match. (Genre is weighted heavily to act as a primary filter).
* **Mood Match:** +1.0 point for an exact string match.
* **Energy Match:** Up to +1.0 point. Calculated using the formula `1.0 - abs(target_energy - song_energy)`.
* **Acousticness Match:** Up to +1.0 point. Calculated using the formula `1.0 - abs(target_acousticness - song_acousticness)`.

**The Ranking Rule:** Once every song is scored, the system sorts the catalog in descending order based on those scores. The top K songs (e.g., the top 2 or 3) are then selected and returned as the final recommendations.

---

## 🛡️ Reliability & AI Guardrails

To ensure the system acts like a production-ready application, I implemented Site Reliability Operations techniques:
1. **Input Guardrails:** Before the recommender touches the data, an intercept function verifies the data integrity. If a profile is missing required keys or contains mathematically impossible parameters (like an energy level above 1.0), the request is blocked.
2. **Confidence Scoring:** The system evaluates the final math. If a returned song scores below a 2.5, it triggers a "Low Confidence" warning to the user, preventing the system from hallucinating a "good match" when the database lacks appropriate tracks.
3. **Automated Logging:** All successful initializations, guardrail blocks, and low-confidence warnings are silently tracked in a `recommender_system.log` file.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows