# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0** ---

## 2. Intended Use  

This recommender is designed to suggest 3 to 5 songs from a specific catalog based on a user's explicitly stated musical preferences. It assumes the user knows exactly what they want in terms of genre, mood, energy level, and acousticness. This system is strictly an educational simulation for classroom exploration and is not intended for real-world or commercial use.

---

## 3. How the Model Works  

VibeFinder 1.0 uses a "content-based filtering" approach. It completely ignores what other people are listening to and only looks at the mathematical relationship between the user's preferences and the song's attributes. 

For every song in our catalog, the system acts as a judge and awards points:
* It gives a massive +2.0 points if the genre is an exact match.
* It gives +1.0 point if the mood is an exact match.
* It calculates a "similarity score" (from 0 to 1 point) based on how close the song's energy and acousticness levels are to the user's target numbers. 

Once every song is graded, it sorts the list from highest to lowest score and presents the top tracks.

---

## 4. Data  

The system uses a highly constrained dataset (`data/songs.csv`) containing exactly 15 songs. It includes baseline representation for genres like Pop, Rock, Lofi, Classical, Hip Hop, R&B, and Metal. 

I expanded the starter dataset from 10 to 15 songs to introduce more variety, but it is still fundamentally limited. It is missing vast amounts of global music, sub-genres, and lacks nuanced indicators of musical taste like tempo, lyrical themes, or vocal styles.

---

## 5. Strengths  

The system works exceptionally well for users whose tastes perfectly align with the core, mainstream genres heavily represented in the dataset (like Pop or Lofi). Its biggest strength is its transparency—because it uses a simple point system, it is incredibly easy to explain *why* a specific song was recommended to the user.

---

## 6. Limitations and Bias 

The recommender suffers from a massive "filter bubble" bias. Because the scoring rule awards 2 full points for a simple genre match, the system aggressively overfits to the user's favorite genre. It will almost always recommend a mediocre song from the preferred genre over a fantastic song from a different genre that perfectly matches the user's mood and energy. It treats users as if their tastes are rigidly confined to a single category.

---

## 7. Evaluation  

I evaluated the system by running three distinct user profiles through the CLI: a "High-Energy Pop Fan", a "Chill Lofi Student", and an adversarial "Deep Intense Rocker" (who wanted Rock music that was high-energy but strictly *sad*). 

The results were surprising for the edge-case Rocker. Because our dataset doesn't have sad rock, the system just pushed intense/aggressive rock tracks to the top. The heavy weight of the Genre (+2.0) and Energy match effectively steamrolled the user's Mood preference, proving that the system struggles heavily with conflicting or nuanced tastes.

---

## 8. Future Work  

If I were to improve this model next, I would:
1. **Reduce the Genre Weight:** Lowering the genre score from 2.0 to something like 0.5 would encourage cross-genre discovery based on pure vibes (energy/mood).
2. **Implement a Diversity Penalty:** I would add logic to penalize a song's score if its artist is already in the top 3, ensuring a more varied list of recommendations.
3. **Add Collaborative Filtering:** Introduce a "user likes" metric so the system could recommend songs based on what similar users enjoyed, rather than relying solely on raw audio data.

---

## 9. Personal Reflection  

My biggest learning moment was realizing how easily a developer can accidentally program bias into an AI system just by assigning arbitrary mathematical weights. Simply deciding that "genre is worth 2 points" effectively blocked my users from discovering new types of music. It changed how I think about real apps like Spotify or TikTok; their engineers have to make incredibly careful, subjective judgments about how to balance "giving the user what they want" versus "helping them discover something new." Even in an algorithm, human judgment matters immensely.