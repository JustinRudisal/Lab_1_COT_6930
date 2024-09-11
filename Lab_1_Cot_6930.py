# Author: Justin Rudisal
# Self-prompting script for recursive prompt engineering. The average cost to fully run this once-through is around $0.15

from openai import OpenAI
import time
import sys
import threading


client = OpenAI(api_key="Insert your Open AI API key here")

initial_prompt = (
    "CyberWeb is an emerging concept focusing on enhancing personal online security using generative AI. Our class project "
    "aims to develop a proof-of-concept that showcases how generative AI can be used within the software development lifecycle. "
    "Given that this is a college project with a two-month timeline, we need to create a feasible prototype that emphasizes AI-driven "
    "solutions. The main idea revolves around a browser-based tool or extension that utilizes generative AI to enhance user privacy and security "
    "online. The tool should be simple, demonstrate clear use of generative AI, and fit within the scope of a class project. The goal is to create "
    "a concept that is not only functional but also highlights the practical application of AI in real-world cybersecurity scenarios."
)

# Number of iterations to perform self-prompting
ITERATIONS = 5
# Number of variations to generate per iteration
VARIATIONS = 3

# Used to guide the AI’s responses towards our project goals
message_log = [
    {
        "role": "system",
        "content": "You are an AI assistant helping to develop a class project concept within a two-month timeframe. "
        "The project, called CyberWeb, should focus on using generative AI within the software development lifecycle, "
        "particularly emphasizing privacy and security. The goal is to create a prototype or proof-of-concept that demonstrates "
        "how generative AI can address real-world cybersecurity issues in a simple, impactful way. Keep suggestions achievable, "
        "with an emphasis on leveraging AI's unique capabilities to create innovative solutions.",
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
    animation_thread = threading.Thread(
        target=loading_animation
    )
    animation_thread.start()

    variations = []
    try:
        for i in range(VARIATIONS):
            response = client.chat.completions.create(
                model="gpt-4o-2024-08-06", messages=message_log
            )
            answer = response.choices[0].message.content
            variations.append(answer)
            time.sleep(
                0.5
            )
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
        follow_up_prompt = f"You liked the following idea: '{preferred_variation}'. Refine this concept further considering the feedback: {feedback}. Focus on making it achievable within two months and demonstrate how generative AI can be leveraged effectively."
    elif feedback.strip():
        follow_up_prompt = feedback
    else:
        follow_up_prompt = (
            f"Based on the response: '{variations[0]}', refine this idea by improving its feasibility, innovation, "
            f"and alignment with generative AI capabilities. How can this idea be best presented as a class project?"
        )

    generated_ideas.append(follow_up_prompt)
    self_prompt(follow_up_prompt, depth - 1)


print("Starting self-prompting process: \n")
self_prompt(initial_prompt, ITERATIONS)

summary_prompt = (
    "Based on the following generated ideas:\n\n"
    + "\n\n".join(generated_ideas)
    + "\n\nConsolidate these ideas into a cohesive and actionable startup pitch that addresses the initial problem."
)
message_log.append({"role": "user", "content": summary_prompt})

print("Generating the final cohesive idea, please wait...")

final_response = client.chat.completions.create(
    model="gpt-4o-2024-08-06", messages=message_log
)
final_answer = final_response.choices[0].message.content

print("\n--- Finalized Idea ---\n")
print(final_answer)

print("Self-prompting process completed.")
