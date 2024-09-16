
# CyberWeb Self-Prompting Script

## Author
**Justin Rudisal**

## Project Overview
CyberWeb is a class project focused on using generative AI to enhance online security. This self-prompting script is designed to recursively generate and refine prompt variations for developing cybersecurity tools like browser extensions. The primary goal is to build a prototype that showcases generative AI’s practical application in enhancing user privacy and security online.

### Key Features
- **Self-Prompting**: Uses recursive prompt engineering to develop and refine ideas.
- **Human Feedback Integration**: Allows for manual input and feedback to guide the AI's output.
- **Multi-Iteration Design**: Runs multiple iterations of prompt generation to refine project concepts.

## Cost
The average cost to run the script fully once is approximately $0.15, based on the API usage for generating responses.

## Requirements
- Python 3.x
- OpenAI Python Client Library (`openai`)
- An OpenAI API key

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/JustinRudisal/Lab_1_COT_6930.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Lab_1_COT_6930
   ```
3. Install required dependencies:
   ```bash
   pip install openai
   ```
4. Insert your OpenAI API key in the script where indicated:
   ```python
   client = OpenAI(api_key="Insert your OpenAI API key here")
   ```

## Usage
1. **Running the Script**: Execute the script using Python:
   ```bash
   python Lab_1_Cot_6930.py
   ```
2. **Initial Prompt**: The script starts with a predefined initial prompt about the CyberWeb project.
3. **Iterations and Feedback**:
   - The script generates variations of prompts and asks the user to select the preferred version.
   - Users can provide feedback that will influence the next iteration of generated prompts.
4. **Final Output**: After all iterations, the script consolidates generated ideas into a final concept, which can be used for project presentations.

## Workflow
1. **Initialization**: Loads an initial prompt focusing on the project’s objective.
2. **Recursive Prompt Generation**: Generates variations based on the initial prompt and feedback over multiple iterations.
3. **Human Feedback**: Collects input on which variation is preferred and any additional feedback.
4. **Final Summary**: Compiles the refined ideas into a cohesive final project pitch or summary.

## Technical Overview
- **Modules Used**:
  - `openai`: For generating responses using the GPT models.
  - `threading`: To display a loading animation during response generation.
  - `sys`, `time`: For script control and animation effects.
- **Prompt Engineering**:
  - Utilizes recursive prompting to refine project ideas.
  - Incorporates user feedback at each stage to guide the AI's direction.
- **Extensions and Variations**:
  - Designed to explore concepts like real-time phishing detection and privacy policy summarization using generative AI.

## Project Goals
1. **Achieve a Functional Prototype**: A browser-based tool demonstrating the use of generative AI in cybersecurity.
2. **Highlight Key AI Capabilities**: Focus on unique applications of AI, such as phishing detection and privacy policy summarization.
3. **Feasibility within Class Scope**: Ensure the project remains achievable within a two-month class timeline.

## Expected Output
The final output should be a refined project concept with clear, actionable steps, ready for presentation and further development.

## License
This project is licensed under the MIT License. See the LICENSE file for more information.
