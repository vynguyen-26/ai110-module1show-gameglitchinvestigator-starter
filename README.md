# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.
The purpose of the game is to allow players to guess a number between 1 and 100 across 3 different levels: easy, normal, and hard.

- [ ] Detail which bugs you found.
 1/ Wrong hint bound (range) for input when comparing with the secret key 
 2/ No consistency for score logic, sometimes incorrect input gets +5
 3/ Out of range input was accepted
 4/ Score in message output is different from the score inside Developer Debug info
 5/ Cannot play new game after lost or win the game. Has to reload the page
 6/ Score for new game is the same as the previous round if the page is not reload
 7/ Normal level has more attempts than easy and a larger range than hard
 8/ History list of the previous is not clear for the next new game
 9/ Input must be submitted twice to appear in the history list; therefore, the score will only be added or subtracted when the input is added to the history, resulting in the wrong score being calculated
 10/ A new game on the same page, without a reload, will start with the final score of the previous game and will be marked as 1 attempt, even though there is no input yet, since the old history list is not clear. 

- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
