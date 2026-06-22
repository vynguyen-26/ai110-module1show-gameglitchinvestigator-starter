# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game with everything hidden, I thought it was working fine because I couldn't see the hints, or because the developer bug info was also hidden.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. Wrong hint bound (range) for input when comparing with the secret key. 
2. No consistency for score logic, sometimes incorrect input gets +5
3. Out of range input was accepted
4. Score in message output is different from the score inside Developer Debug info
5. Cannot play new game after lost or win the game. Has to reload the page
6. Score for new game is the same as the previous round if the page is not reload

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|   1   |     Go Higher     |   Go Lower      |      Go Lower
|   5   |     Go Higher     |   Go Lower      |      Go Lower 
|  104  |   Not accepted    |   Accepted      |      Go Higher

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

Claude Code

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

For the score calculation system, I AI suggested "A simple, predictable model: start at 0, every wrong guess costs the same (−5 regardless of direction), and a win awards 100 − 10 × (guesses − 1) with a floor of 10 (so a first-guess win = 100, second guess = 90, etc.). And make New Game truly reset everything." I verified the result my actually playing the game to tested and write the test cases.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

The out of range input given TypeError: parse_guess() takes 1 positional argument but 3 were given. For that problem it sugessted that I should reload the app because Streamlit reloaded app.py (the new 3-arg call) but kept the old cached logic_utils module (the original 1-arg parse_guess). I did reload the app, and it still didn't work, so I asked it again, and I had to stop the running server and then rerun streamlit run app.py 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

When it is critical and affects the product's outcome, it is wrong to deviate from the product's purpose.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

The range of difficulty levels and the number of attempts for each level

- Did AI help you design or understand any tests? How?
Yes, the AI helps me design test cases for the new game by analyzing all the fixed bugs and generating them based on the new fixes.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Streamlit reruns the entire app from the beginning every time you click or type. Session state is like a little notebook that helps Streamlit remember important things, like your score, choices, or previous answers, even after the app starts over.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects? 
- This could be a testing habit, a prompting strategy, or a way you used Git.

Analyze the problem carefully and revisit the website multiple times to test and ensure no bugs were overlooked.

- What is one thing you would do differently next time you work with AI on a coding task?

Next time, I would fix one bug at a time with a clear description of the problem and the fix details

- In one or two sentences, describe how this project changed the way you think about AI generated code.

This project has taught me that I should fix one bug at a time. Also, I must describe the problem clearly and tell the AI specifically what to fix, with specific details, so it can go in the right direction.
