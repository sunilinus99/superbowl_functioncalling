import openai
import os
import pandas as pd
import json


openai.api_key = {OPEN_AI_API_KEY}

# Function to retrieve Super Bowl winner from a CSV file
def get_super_bowl_winner_from_csv(year):
    # Load the CSV file into a DataFrame
    csv_file_path = '/Users/sunilinus/Downloads/superbowl.csv'
    df = pd.read_csv(csv_file_path)
    
    # Extract the year from the 'Date' column (last 4 digits)
    df['Year'] = df['Date'].str[-4:].astype(int)
    
    # Search for the row where the year matches the input year
    result = df[df['Year'] == year]
    
    if not result.empty:
        winner = result.iloc[0]['Winner']
        return winner
    else:
        return "No data available for that year."

# Define the function that OpenAI can call
functions = [
    {
        "name": "get_super_bowl_winner_from_csv",
        "description": "Retrieve the Super Bowl winner for a specific year from a CSV file.",
        "parameters": {
            "type": "object",
            "properties": {
                "year": {
                    "type": "integer",
                    "description": "The year of the Super Bowl (e.g., 2023)."
                }
            },
            "required": ["year"]
        }
    }
]

# Function to handle OpenAI request with function calling
def ask_openai_with_function_calling(question):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ],
        functions=functions,
        function_call="auto",  # Automatically call the correct function
        max_tokens=150,
        temperature=0.7,
    )

    # If a function call is present in the response
    if response['choices'][0]['finish_reason'] == 'function_call':
        function_name = response['choices'][0]['message']['function_call']['name']
        function_args = response['choices'][0]['message']['function_call']['arguments']
        
        # Parse function_args from JSON string to dictionary
        function_args = json.loads(function_args)

        if function_name == 'get_super_bowl_winner_from_csv':
            year = int(function_args['year'])
            return get_super_bowl_winner_from_csv(year)

    return response['choices'][0]['message']['content'].strip()

# Main chatbot logic with function calling
def chatbot_with_function_calling():
    print("Welcome to the Super Bowl chatbot with function calling! Ask me about Super Bowl winners or anything else (type 'exit' to quit):")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Ask OpenAI with function calling capability
        gpt_response = ask_openai_with_function_calling(user_input)
        print(f"Bot: {gpt_response}")

# Run the chatbot
if __name__ == "__main__":
    chatbot_with_function_calling()
