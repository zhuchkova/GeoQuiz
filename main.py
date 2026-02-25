import list_of_cities
from player_handling import add_score_for
from display_with_border import *
import welcome
import score
import quiz
from llm import analyze_knowledge


#### global variable ####
players = []




def main():
    players = welcome.initialize_game()
    rounds = 5
    round_counter = 1
    all_results = []  # Track all questions and results
    while round_counter <= rounds:
        for player in players:
            correct_answer = False
            cprint(f"{player['name']} its your turn", C.RED)
            if round_counter == 1:
                correct_answer, points, question_text = quiz.city_capital_question()
            elif round_counter == 2:
                correct_answer, points, question_text = quiz.country_population_question()
            elif round_counter == 3:
                correct_answer, points, question_text = quiz.country_area_question()
            elif round_counter == 4:
                correct_answer, points, question_text = quiz.city_population_question()
            elif round_counter == 5:
                correct_answer, points, question_text = quiz.city_area_question()
            if correct_answer:
                score.update_player_score(player,points)
            all_results.append({
                'player': player['name'],
                'question': question_text,
                'correct': correct_answer,
                'points': points
            })
        round_counter += 1

    score.display_final_results(players)
    
    # Get LLM feedback on player performance
    print()
    print("=" * 80)
    print("PERFORMANCE ANALYSIS")
    print("=" * 80)
    print("⏳ Generating personalized feedback (estimated: 20-60 seconds)...")
    
    # Build player summary - simple version
    player_summary = ""
    for player_data in players:
        player_summary = player_summary + f"{player_data['name']} scored {player_data['score']} points, "
    
    # Build detailed results for LLM 
    detailed_results = ""
    for result in all_results:
        # Check if answer was correct
        if result['correct']:
            status = "Correct"
        else:
            status = "Wrong"
        
        # Get the full question text
        question = result['question']
        
        # Add this result to our detailed results
        detailed_results = detailed_results + f"{result['player']}: {status} - {question}\n"
    
    prompt = f"""
            You are a witty Geography Professor. Analyze this player data: {player_summary}
            
            There were 5 questions asked and the maximal number of points for each player is 5.
            
            Detailed results:
            {detailed_results}

            For each player, provide a unique, 3-4 sentence feedback message based on their performance:

            THE MNEMONIC BRANCH (If Score < 100%):
            Focus on one specific question they got wrong.
            Provide a clever mnemonic, jingle, or wordplay to help them remember the correct answer.
            Example: "To remember Paris is bigger than Dublin, just think: A 'Pair-is' (Paris) always larger than a single!"

            THE TRIVIA BRANCH (If Score is 100%):
            Praise them with a unique title (e.g., 'Cartography King', 'Global Legend').
            Provide one "Mind-Blowing Fun Fact" about any city or country mentioned in the quiz to reward their knowledge.

            STYLE REQUIREMENTS:
            Rotate between different teaching styles: use rhymes for one player, visual tricks for another, and punny jokes for a third.
            Keep the tone catchy, friendly, and brief.
            Ensure every response is distinct—even if two players have the same score, their 'jingle' or 'fact' should be different.

            Return the results as a clean list of messages.
            """
    analyze_knowledge(prompt)



if __name__ == '__main__':
    main()