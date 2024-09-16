# Author: Justin Rudisal
# Self-prompting script for recursive prompt engineering. The average cost to fully run this once-through is around $0.15

import datetime
import threading
import time
import sys
from openai import OpenAI

client = OpenAI(api_key="INSET_YOUR_API_KEY")

# Initial prompt placeholder that will be set based on user's choice
initial_prompt = ""

# Number of iterations to perform self-prompting
ITERATIONS = 5
# Number of variations to generate per iteration
VARIATIONS = 3

# Used to guide the AI’s responses towards our project goals
message_log = [
    {
        "role": "system",
        "content": (
            "You are an AI assistant helping to develop a class project concept within a two-month timeframe. "
            "The project, called CyberWeb, is supposed to be a tool that solves a current real-world problem that "
            "isn't already covered by other tools. During the creation of this tool, the SDLC should focus "
            "on using generative AI and replacing human labor. The project itself should pay a particular "
            "focus on privacy and security. The goal is to create a prototype or proof-of-concept that demonstrates "
            "how generative AI can address real-world cybersecurity issues in a simple, impactful way. Keep "
            "suggestions achievable, with an emphasis on leveraging AI's unique capabilities to create innovative "
            "solutions."
        ),
    }
]

generated_ideas = []
loading = False


def loading_animation():
    """Function to display a loading animation with moving ellipses."""
    while loading:
        for dot_count in range(4):
            sys.stdout.write(
                "\rGenerating responses, please wait"
                + "." * dot_count
                + " " * (3 - dot_count)
            )
            sys.stdout.flush()
            time.sleep(0.5)


def get_human_feedback(variations):
    """Function to get human feedback and preferred variation after each iteration."""
    print("\nGenerated Variations:\n")
    for i, variation in enumerate(variations, start=1):
        print(f"Variation {i}:\n{variation}\n")

    preferred_choice = input(
        "Which variation did you like the most? (Enter the number, or 0 if none): "
    )
    try:
        preferred_choice = int(preferred_choice)
        if 0 < preferred_choice <= len(variations):
            preferred_variation = variations[preferred_choice - 1]
        else:
            preferred_variation = None
    except ValueError:
        preferred_variation = None

    feedback = input(
        "Provide feedback for the next iteration (or press Enter to continue without feedback): "
    )

    return preferred_variation, feedback


def generate_variations(prompt):
    """Function to generate multiple variations for a given prompt."""
    global loading
    loading = True
    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()

    variations = []
    try:
        for i in range(VARIATIONS):
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06", messages=message_log
            )
            answer = response.choices[0].message.content
            variations.append(answer)
            time.sleep(0.5)
    finally:
        loading = False
        animation_thread.join()

    print("\nResponses generated.\n")
    return variations


def self_prompt(prompt, depth):
    """Recursive function to generate new prompts and responses iteratively."""
    if depth == 0:
        return

    message_log.append({"role": "user", "content": prompt})

    variations = generate_variations(prompt)

    preferred_variation, feedback = get_human_feedback(variations)

    if preferred_variation:
        follow_up_prompt = (
            f"You liked the following idea: '{preferred_variation}'. Refine this concept further "
            f"considering the feedback: {feedback}. Focus on making it achievable by a team of students within two "
            f"months and demonstrate how generative AI can be leveraged effectively."
        )
    elif feedback.strip():
        follow_up_prompt = feedback
    else:
        follow_up_prompt = (
            f"Based on the response: '{variations[0]}', refine this idea by improving its feasibility, innovation, "
            f"and alignment with generative AI capabilities. How can this idea be best presented as a class project?"
        )

    generated_ideas.append(follow_up_prompt)
    self_prompt(follow_up_prompt, depth - 1)


def generate_ai_initial_prompt():
    """Function to generate an AI-generated initial prompt."""
    print("Generating an AI-generated initial prompt, please wait...")
    system_prompt = (
        "You are an AI assistant that helps to generate initial startup idea prompts for a self-prompting script. "
        "Generate an initial prompt that aligns with the project goals, focusing on developing a class project concept "
        "within a two-month timeframe, using generative AI within the software development lifecycle. The concept of "
        "the project should be particularly emphasizing privacy and security. The project should be meeting a "
        "marketable demand that is not already addressed by existing tools."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": "Please generate an initial prompt for the self-prompting script.",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06", messages=messages
    )
    initial_prompt = response.choices[0].message.content
    return initial_prompt


# Main script starts here
print("Please choose an initial prompt option:")
print("1. Provide a self-written custom initial prompt")
print("2. Use an AI-generated initial prompt")
print("3. Use the hardcoded initial prompt")
choice = input("Enter the number of your choice (1-3): ")

if choice == "1":
    initial_prompt = input("Please enter your custom initial prompt: ")
elif choice == "2":
    initial_prompt = generate_ai_initial_prompt()
    print("\nGenerated Initial Prompt:\n")
    print(initial_prompt)
else:
    # Use the hardcoded initial prompt
    initial_prompt = (
        "CyberWeb is an emerging concept focusing on enhancing personal online security using generative AI. Our "
        "class project aims to develop a proof-of-concept that showcases how generative AI can be used within the "
        "software development lifecycle. Given that this is a college project with a two-month timeline, we need to "
        "create a feasible prototype that emphasizes AI-driven solutions. The main idea revolves around a "
        "browser-based tool or extension that utilizes generative AI to enhance user privacy and security online. The "
        "tool should be simple, demonstrate clear use of generative AI, and fit within the scope of a class project. "
        "The goal is to create a concept that is not only functional but also highlights the practical application of "
        "AI in real-world cybersecurity scenarios."
    )

print("\nStarting self-prompting process: \n")
self_prompt(initial_prompt, ITERATIONS)

summary_prompt = (
    "Based on the following generated ideas:\n\n"
    + "\n\n".join(generated_ideas)
    + "\n\nConsolidate these ideas into a cohesive and actionable startup pitch that addresses the initial problem. "
    "The pitch should be concise, engaging, and clearly demonstrate the value proposition of the project. The pitch "
    "should be similar to something like how you would present it to potential investors or stakeholders."
)
message_log.append({"role": "user", "content": summary_prompt})

print("Generating the finalized pitch idea, please wait...")

final_response = client.chat.completions.create(
    model="gpt-4o-2024-08-06", messages=message_log
)
final_answer = final_response.choices[0].message.content

print("\n--- Finalized Idea ---\n")
print(final_answer)

print("Self-prompting process completed.")

# Save the full conversation log to a file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
conversation_log_filename = f"conversation_log_{timestamp}.txt"
with open(conversation_log_filename, 'w', encoding='utf-8') as f:
    for message in message_log:
        role = message['role']
        content = message['content']
        f.write(f"{role.upper()}:\n{content}\n\n")

# Save the final pitch to a file
final_pitch_filename = f"final_pitch_{timestamp}.txt"
with open(final_pitch_filename, 'w', encoding='utf-8') as f:
    f.write(final_answer)
