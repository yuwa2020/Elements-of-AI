

## Part-1

(1) a description of how you formulated each problem; 

We thought that a detailed description of the game could help the LLM make more concise decisions in tic-tac-what. Therefore, for the human template, we added as much information as possible to the LLM prompt. The main thing we did was ensure the output was very short and concise since if it's long, the LLM tends to give unnecessary information or produce a strange format that cannot be parsed by other code. So we ended up with a JSON file containing only the row and column.(Question 1)

For Questiont 2, the first question of the code is almost the same as question 1. However, in the last question of the step-by-step part code( Asking in this prompt in the end: ""What move should I make to avoid forming a line of 3 X's?""), the LLM consistently responded differently, so I needed to make the code flexible enough to parse which move the LLM chose.

Questiont 3: This is very straightforward to follow the question to build both the random player and LLM model that I built in questions 1 and 2. The main issue is that the LLM does not follow the format.


(2) a brief description of how your program works; 
- Question 1 code is similar to the base code provided for this assignment. The changed part is the human template, and in order to test multiple test cases, I made the `run_llm` function to run the code smoothly.

For the `simulate_game` function is that simulates a single round of gameplay for the given model and game rules. Here's how it works:


- Initialization:
The function starts by setting up the initial conditions of the game. This includes initializing an empty game board and specifying whose turn it is to play (e.g., "Player 1" or "Player 2").
Game parameters like board size, win condition (e.g., forming a line of length 3), and player details are also defined at this stage.

- Game Loop:
The function runs a loop where players take turns until the game reaches a conclusion (win, lose, or draw).
During each turn, the program checks the current game state and dynamically decides the next move for each player.

- Player Move Simulation:
The function uses logic or a pre-trained model to simulate the players' decision-making process. For instance, the model might predict the optimal next move based on the current state of the board.
Moves are validated to ensure they are legal (e.g., within the board boundaries and not overwriting an existing piece).

- Win/Loss/Draw Check:
After each move, the function evaluates the game board to check if a player has won by forming a line of the required length or if the game ends in a draw.
If a win or draw is detected, the loop terminates, and the result is recorded.

- Result Storage:
Once the game ends, the outcome (win/loss/draw) is stored in a results variable or file for later analysis. This ensures that the game outcomes can be evaluated and compared in subsequent experiments.

- Output:
The function outputs the final state of the board and the result of the game. This can be logged for debugging or displayed to the user for clarity.


However, in the submitted code, it only uses the Win/Loss/Draw Check part to check whether the LLM loses the game or not. 


- Question 2: In this part, it only mentions the last part of the code (asking in this prompt at the end: "What move should I make to avoid forming a line of 3 X's?").
We created two prompts, `chat_prompt_1` and `chat_prompt_2`. The `chat_prompt_1` asks to think step by step and consider more than 4 possible move places. Then, in `chat_prompt_2`, it asks to extract JSON data from the text. As mentioned in the base code, even with two prompts, it still fails to parse in the correct format. As a result, we made a function called `output_converting_board` which tries to extract only row and column information from the list. Then, `output_converting_board_specific` tries to extract the first row and column which can be used for the next move. This is a lazy method, but without it, it was impossible for the LLM to get a consistent response.

- Question 3: The `play_game` function is basically running this part. It receives both `board_size` and `sentence_length`. `current_player` determines the player, either 'Random' player or 'LLM' player. For the 'Random' player, it gets available moves from the `game.available_moves` function and then parses it to `random_choice`, which chooses a random move from the available moves. Then, it checks whether the game board meets either player's win condition in the `game.check_win` function, which checks rows, columns, and diagonals for a sequence of Xs. If it exists, the game ends and shows the current player loses. If not, it also checks whether the game is a draw or not, and then moves to the next round, changing the `current_player` to 'LLM'.

If the `current_player` is 'LLM', it gets the board information first and puts it into the LLM as in questions 1 and 2, and then checks whether the player loses or not. Then it goes to the next round to 'Random'.


(3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made. These comments are especially important if your code does not work perfectly, since it is a chance to document the energy and thought you put into your solution.

The first thing we faced the problem and implemented in the code is that it is already written down in part (1), but we tried to simplify the LLM output as much as possible since the hardest part is the inconsistency of the LLM response, which made it hard to run the code.

Second, The problem we faced is especially in the for loop on Question (3) of making a random player versus LLM. If I tried to create a for loop, it causes the LLM to stop functioning.
```
Error message:
ConnectionError: HTTPConnectionPool(host='localhost', port=11434): Max retries exceeded with url: /api/generate/ (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7851288df1c0>: Failed to establish a new connection: [Errno 111] Connection refused')): 
```

This happens presumably because the Python code requests the GPU. Generating text sometimes takes time, but the for loop can finish one loop instantly, causing a problem when the response does not finish and new queries are asked. So I used `import time` and `time.sleep` to wait until the server creates a response.

## other Issues Faced and Problems Encountered

- Connection Errors:
Initially, the Ollama server was not properly responding to requests despite confirming it was running. We repeatedly faced ConnectionRefusedError and MaxRetryError while trying to interact with the LLM (Llama3) through the local endpoint (127.0.0.1:11434).
Even after ensuring the server was active (curl http://127.0.0.1:11434), the integration with the Python script kept failing, highlighting a potential communication mismatch or instability in the local server setup.

- Server Port and Network Issues:
The server was confirmed to be listening on the expected port (via netstat), but requests from the Python code still resulted in errors. This raised questions about firewall or security restrictions, or potential service timeout due to high latency in response generation.

- LLM Response Format:
When the server responded successfully, the LLM's output often included explanations or non-standard formats rather than the expected numerical move (0-2). 
The LLM sometimes returned invalid moves (e.g., positions already occupied or out of range), showing that the general-purpose model wasn't trained for domain-specific tasks like Tic-Tac-Toe.

- Prompt Tuning Challenges:
Writing effective prompts to elicit valid and specific responses from the LLM was a significant challenge. Initial prompts failed to guide the model toward simply outputting a valid move number. Adjusting the prompt wording was necessary but did not fully resolve the issue.

- Model Understanding of Game Logic:
It became apparent that the pre-trained Llama3 model lacked contextual understanding of Tic-Tac-Toe rules. The model sometimes failed to recognize valid moves, leading to repeated invalid outputs despite clear instructions in the prompt. This highlighted the limitations of using general-purpose LLMs for game-specific tasks without fine-tuning.

- Debugging the Ollama Setup:
Setting up and debugging the Ollama environment was another source of delays. While the documentation was helpful for installation and initial setup, we ran into issues with:
Confirming that the server was properly serving requests (ollama serve process visibility).
Restarting and re-pulling the model occasionally helped but required time-consuming retries.

- Fallback Logic for LLM Errors:
To handle cases where the LLM failed to provide a valid move, fallback logic was implemented. This included repeating the request or simulating random moves, but this added complexity to the code and made it harder to cleanly integrate the LLM responses.

- Testing and Validation:**
Testing the game logic with LLM responses was difficult because of the unpredictable nature of the model’s outputs. Debugging required us to separate static test cases for the game logic from LLM-related errors, which consumed additional time.
A consistent flow of errors during testing made it harder to determine whether the issues were with the game logic or the LLM integration.


### Efforts Made to Overcome Challenges

- Prompt Engineering:
Experimented with various prompt formats to improve the LLM’s understanding of game-specific tasks. Instructions were simplified and clarified to reduce ambiguity.

- Systematic Testing:
Isolated the game logic and tested it separately using static test cases to ensure the core functionality was intact before integrating the LLM.
Created test scenarios to evaluate the LLM’s responses and their impact on gameplay.


## 1. Which test cases does your implementation pass (i.e chooses the winning move) and fail? Does it also pass on a 4x4 board with sequence length of 4 (build a similar test case if required).
### 3*3 board
## Observation
- Test Case 1 - 4/5: Pass in the program, but it is actually placing on an existing position -> Fail, 1/5: Fail: Completes a line of specified length (3).
- Test Case 2 - 4/5: Completes a line of specified length (3), 1/5: Pass
- Test Case 3 - 5/5: Pass in the program, but it is actually placing on an existing position -> Fail
- Test Case 4 -  5/5: Pass in the program, but it is actually placing on an existing position -> Fail
- Test Case 5 -  4/5: Completes a line of specified length (3), 1/5: Fail: Completes a line of specified length (3).

| Test Case | Pass | Fail | Comments |
|-----------|------|------|----------|
| Test Case 1 | 0/5 | 5/5 | Pass in the program, but it is actually placing on an existing position -> Fail. Completes a line of specified length (3). |
| Test Case 2 | 1/5 | 4/5 | Completes a line of specified length (3). |
| Test Case 3 | 0/5 | 5/5 | Pass in the program, but it is actually placing on an existing position -> Fail. |
| Test Case 4 | 0/5 | 5/5 | Pass in the program, but it is actually placing on an existing position -> Fail. |
| Test Case 5 | 0/5 | 5/5 | Completes a line of specified length (3). |

Most of the time, my implementation fails or sometimes even places an ‘X’ on a spot that is already occupied.


### 4*4 board
## Observation



- Test Case 1 - 3/5:  Pass, 2/5: Pass in the program, but it is actually placing on an existing position -> Fail,
- Test Case 2 - 4/5:  Pass, 1/5: Pass in the program, but it is actually placing on an existing position -> Fail,
- Test Case 3 - 3/5:  Pass, 2/5: Pass in the program, but it is actually placing on an existing position -> Fail,
- Test Case 4 - 5/5: Pass in the program, but it is actually placing on an existing position -> Fail,
- Test Case 5 - 5/5: Fail


| Test Case | Pass | Fail | Comments |
|-----------|------|------|----------|
| Test Case 1 | 3/5 | 2/5 | Pass in the program, but it is actually placing on an existing position -> Fail. |
| Test Case 2 | 4/5 | 1/5 | Pass in the program, but it is actually placing on an existing position -> Fail. |
| Test Case 3 | 3/5 | 2/5 | Pass in the program, but it is actually placing on an existing position -> Fail. |
| Test Case 4 | 0/5 | 5/5 | Pass in the program, but it is actually placing on an existing position -> Fail. |
| Test Case 5 | 0/5 | 5/5 | Fail. |


As the game becomes more difficult, the LLM more frequently tries to place an 'X' on a spot that is already occupied. It also tries to place losing moves. The 4x4 grid is more complicated than the 3x3 grid, which makes this simple prompt more difficult for the LLM to handle.

Overall, the LLM performed poorly in this part.

# 2. How does changing the prompt impact the performance of the model and what changes help the model choose better moves? (Example - when you ask the model to think step by step, etc.)

- Asking in this prompt in the end:""Choose the next best move to avoid losing."" - 5/5: Pass in the program, but it is actually placing on an existing position -> Fail, This means that this method is not suitable. 

- Asking in this prompt in the end: ""Think step by step, and choose the next best move."" - - 5/5: Pass in the program, but it is actually placing on an existing position -> Fail, This means that this method is not suitable. The interesting observation is that LLM tried to place in the spot all the time in all five tries. This prompt has made some consistency to the LLM. 


- Asking in this prompt in the end: ""Select a move that does not form a line of 3 X's."" - 4/5: Pass in the program, but it is actually placing on an existing position, 1/5 fail: The interesting observation is that asking LLM not to form a line of 3 X's can actually make 3 X in the last cases. So, this is not helpful for LLM. 


- Asking in this prompt in the end: ""What move should I make to avoid forming a line of 3 X's?"" - 5/5: Pass in the program, but it is actually placing on an existing position -> Fail, Same as one before prompt,  TThe interesting observation is that the LLM tried to place it in the same spot every time across all five attempts same as this prompt: ""Think step by step, and choose the next best move."" 

| Prompt | Pass | Fail | Comments |
|--------|------|------|----------|
| "Choose the next best move to avoid losing." | 0/5 | 5/5 |Pass in the program, but it is actually placing on an existing position -> Fail,  This means that this method is not suitable. |
| "Think step by step, and choose the next best move." | 0/5 | 5/5 | Pass in the program, but it is actually placing on an existing position -> Fail. This means that this method is not suitable.  |
| "Select a move that does not form a line of 3 X's." | 0/5 | 5/5 | Pass in the program, but it is actually placing on an existing position, 1/5 fail |
| "What move should I make to avoid forming a line of 3 X's?" | 0/5 | 5/5 | Pass in the program, but it is actually placing on an existing position -> Fail | 



- At this time, for the first response, do not specify JSON format and get a step-by-step respone: 3/6: Pass in the program, but it is actually placing on an existing position -> 4/6: Fail, Fail
I believed that using a step-by-step prompt and asking the LLM again to format to a specific type would yield better results than using a concise prompt. However, I found that this approach led to worse outcomes. 

Despite following the step method, the LLM still places the spot that will lead to a loss.

During this part, I realized that this LLM is probably trained on the normal tic-tac-toe, which uses a 3x3 board and has two pieces, X and O. O goes first, followed by X, and the first person to get 3 in a row wins. In this modified game, there is only X, no O, and the first player to make a line of 'n' Xs in a row loses. So the goal for each move is to place an X on the board that doesn’t make a line of 'n' Xs in a row. I think this is not trained on the LLM, which makes it very hard to make a winning move, so it might have to be trained again or fine-tuned for this game.


# 3. On a 3x3 board, can your model win against a random player in a game starting with an empty board? or, how many moves does it play before it begins to fail.


Test result:
Random player loses: 4/8
LLM player loses: 4/8
After 9 try -> LLM no longer follows the output format

| Player          | Wins | Losses | Comments                                      |
|-----------------|------|--------|-----------------------------------------------|
| Random player   | 4/8  | 4/8    |                                               |
| LLM player      | 4/8  | 4/8    | After 9 tries, LLM no longer follows the output format. |


This shows that the LLM is almost the same as the random player's score since the score is 4 out of 8. This means that my prompt for this assignment is not able to improve the LLM's performance over a random move player. The LLM sometimes made better moves.

Observation: The LLM started to fail after 2 moves for 3 times and after 3 moves for 1 time against the random player. This shows that a complex board makes it hard for the LLM to understand the game.


### Key Learnings

- LLM Integration is Not Plug-and-Play:
While LLMs like Llama3 are powerful, using them for specific tasks like Tic-Tac-Toe requires significant adaptation in prompts, response handling, and fallback logic. Pre-trained models often need fine-tuning to perform reliably in specialized domains.


## Part-2
(1) a description of how you formulated each problem; 
There are two parts of the code. First, using input data to read and calculate distance based on the specified method. Then it determines the classes based on the majority vote. Finally, it calculates the accuracy.

(2) a brief description of how your program works; 
The function `K_Nearest_Neighbors` gets files of train and test data. Then, for each test point, it calculates the distance using the `calculate_distance` function.

The `calculate_distance` function calculates the distance between two points. I implemented three distance metrics: Euclidean, Manhattan, and Minkowski.

Euclidean distance:
$$
d(p, q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2} 
$$


Manhattan distance:
$$
d(p, q) = \sum_{i=1}^{n} |p_i - q_i|
$$

Minkowski distance:
$$
d(p, q) = \left( \sum_{i=1}^{n} |p_i - q_i|^p \right)^{\frac{1}{p}}
$$
where p = 3 in this code. This is because if I use p=2, it is the same as the Manhattan distance. 

After finishing the calculation, it sorts the distances using `distance.sort`. This idea is used after reading this website: https://levelup.gitconnected.com/sorting-in-python-using-keys-d2622edd7a92?gi=9cedea628424

Then it selects the specified number of k-nearest neighbors.

Then it counts the class among the k-nearest neighbors. The counting method is used after reading this official Python document: https://docs.python.org/3/library/collections.html

This method of `Counter` and `most_common` return a list of the n most common elements and if elements with equal counts are ordered in the order first encountered.

After finishing this, it calculates the accuracy of the test set.


(3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made. These comments are especially important if your code does not work perfectly, since it is a chance to document the energy and thought you put into your solution.

There were not any difficulties in this assignment, but choosing the right distance metrics was a bit tricky. Since the dataset is 2D, only a few options were available, so we chose Euclidean, Manhattan, and Minkowski distances.

- Other Issues Faced and Problems Encountered

*1. Error with Distance Metric:*
While implementing the K_Nearest_Neighbors function, we encountered an error when using manhattan as the distance metric. The issue was caused because the scipy.spatial.distance.cdist function does not recognize manhattan as a valid metric.

**Solution:**
After consulting the SciPy documentation, we discovered that cdist refers to manhattan as cityblock.
We replaced the string "manhattan" with "cityblock" in the distance metric argument.

**Code Snippet:**

- Fix for manhattan distance error
distances = cdist(X_test, X_train, metric='cityblock')

*2. Dataset Challenges:*
Parsing the JSON dataset files and converting them into numpy arrays required extra effort, especially to ensure compatibility with both training and test sets.
Additionally, ensuring the data was split correctly between training (X_train, y_train) and testing (X_test, y_test) was essential to avoid data leakage.

**Solution:**
Created a dedicated utility to load and preprocess the dataset for uniform handling across all experiments.

**Code Snippet:**

def load_data(dataset_path):
    with open(dataset_path) as f:
        data = json.load(f)
    return np.array(data["X_train"]), np.array(data["y_train"]), np.array(data["X_test"]), np.array(data["y_test"])

*3. Hyperparameter Testing Overhead:*
Evaluating the model for different values of k (e.g., 3, 6, 9) and varying distance metrics (euclidean, cityblock) required multiple simulations, making it time-intensive.

**Solution:**
Wrote a loop to automate ablation studies across combinations of k and metrics. This reduced manual effort and allowed for systematic testing.
Added print statements to track the progress and results of each run.

**Code Snippet:**
- Automating ablation studies
k_values = [3, 6, 9]
distance_metrics = ['euclidean', 'cityblock']

for k in k_values:
    for metric in distance_metrics:
        accuracy = K_Nearest_Neighbors(args.dataset_path, k, metric)
        print(f"Accuracy for k={k}, metric={metric}: {accuracy:.4f}")




I am not using any existing ML libraries.


Fill the accuracies in the following table -
1. How and why does the accuracy change across datasets?

--distance_metric 'euclidean'
| dataset_name |K=3|K-6|K=9|
|:-------------|:--|:--|:--|
|dataset_1     | 100.0 |100.0  |100.0  |
|dataset_2     | 72.0 |72.0  |74.0  |
|dataset_3     | 54.0 |44.0  |42.0  |

--distance_metric 'manhattan'
| dataset_name |K=3|K-6|K=9|
|:-------------|:--|:--|:--|
|dataset_1     | 100.0 |100.0  |100.0  |
|dataset_2     | 72.0 |72.0  |74.0  |
|dataset_3     | 40.0 |36.0  |44.0  |

--distance_metric 'minkowski'
| dataset_name |K=3|K-6|K=9|
|:-------------|:--|:--|:--|
|dataset_1     | 100.0 |100.0  |100.0  |
|dataset_2     | 70.0|72.0  |74.0  |
|dataset_3     | 56.0 |44.0  |42.0  |


### Analysis

Dataset 1: All distance metrics achieve 100% accuracy.
- Interpretation: This dataset is likely simple with clearly separable classes.

Dataset 2: Accuracy is around 70%, slightly improving as k increases.
- Interpretation: Compared to Dataset 1, this dataset overlaps classes but is relatively easy to categorize.

Dataset 3: Accuracy is relatively low, around 40-50%. The best accuracy is 56.0% with Minkowski (k=3), and the worst is 36% with Manhattan (k=6).
- Interpretation: This dataset is likely complex with overlapping and noisy data, which lowers the accuracy.

The differences in accuracy can be attributed to the dataset itself and the different k values. For dataset 1, it is a fairly easy classification task, with clearly separable data points. In dataset 2, it is moderately complex but still achieves a better result of about 70%, which might be due to some data points overlapping with others, making it difficult for k-nearest neighbors to separate them. For dataset 3, the accuracy is the worst across all data, ranging from a high of 56% to a low of 36%. This is likely due to k-nearest neighbors heavily relying on the assumption that similar points are close to one another. Additionally, highly noisy data, such as incorrect data, can distort the classification, especially for dataset_3 might contribute to accuracy change. 

2. What insights can you draw about how and why model accuracy changes across different values of k?

### Insights on k Values

Dataset 1: Accuracy remains consistent across all k values.
- Insight: If the dataset has clear separation between data points, the k value does not significantly impact classification.

Dataset 2: Accuracy slightly improves as k increases, especially from k=3 to k=9.
- Insight: Considering more data points can provide better classification in datasets with slight overlap.

Dataset 3: Accuracy generally decreases as k increases, except for Manhattan distance.
- Insight: For complex datasets, it might be better to choose a lower k value for k-nearest neighbors.

In my teammates, she also tried different methods for tied conditions.
```Part-2/main-aashi.py```

aashi's code
--distance_metric 'euclidean'
| dataset_name |K=3|K-6|K=9|
|:-------------|:--|:--|:--|
|dataset_1     | 100.0 |100.0  |100.0  |
|dataset_2     | 72.0 |72.0  |74.0  |
|dataset_3     | 42.0 |48.0  |44.0  |

--distance_metric 'manhattan' (run code as ```--distance_metric "cityblock")
| dataset_name |K=3|K-6|K=9|
|:-------------|:--|:--|:--|
|dataset_1     | 100.0 |100.0  |100.0  |
|dataset_2     | 72.0 |72.0  |74.0  |
|dataset_3     | 38.0 |36.0  |44.0  |

--distance_metric 'minkowski'
| dataset_name |K=3|K-6|K=9|
|:-------------|:--|:--|:--|
|dataset_1     | 100.0 |100.0  |100.0  |
|dataset_2     | 70.0|72.0  |74.0  |
|dataset_3     | 42.0 |46.0  |40.0  |


This code, in the case of a tie, selects the first category that appears in the dataset (if the tie is between 1, 2, and 3, it will select 1).

The results also suggest that low k values are better for complex datasets, but in this case, a moderate k value of 6 is the best.



3. How does the choice of distance metric impact the performance of the model?

Dataset 1 and 2 do not affect the distance metric for the performance of the model.

Dataset 3: Significant differences between distance metrics.
- **Euclidean Distance:** Generally better in this dataset compared to other metrics. This might be because the dataset aligns with Euclidean distance, possibly indicating that the dataset is related to geographical distance information.
- **Manhattan Distance:** Performed worse. This might be due to its calculation method that uses paths along grid lines, which might not be suitable for this dataset.
- **Minkowski Distance:** Performs similarly to Euclidean distance. This metric uses curved lines for distance, which sometimes results in better performance than Euclidean distance, such as k=3 of dataset_3. 

**Overall:** In this dataset, Euclidean or Minkowski distance is the best option to choose.


