def player(prev_play, counter=[0], opponent_history=[]):
    # Increment the counter for each play
    counter[0] += 1
    
    # Define ideal counter moves
    ideal_response = {"P": "S", "R": "P", "S": "R"}
    
    # Add to opponent history
    if prev_play:
        opponent_history.append(prev_play)
    
    # First move
    if not prev_play:
        return "P"  # Start with paper
    
    # After accumulating some history, determine which bot we're playing against
    if len(opponent_history) >= 5:
        # Check for Kris pattern (counters our last move)
        kris_counter = 0
        for i in range(min(5, len(opponent_history) - 1)):
            if i + 1 < len(opponent_history) and opponent_history[-(i+1)] == ideal_response.get(opponent_history[-(i+2)], "R"):
                kris_counter += 1
        
        if kris_counter >= 3:
            # Counter Kris's expected counter to our previous move
            expected_kris_move = ideal_response.get(prev_play, "R")
            return ideal_response.get(expected_kris_move, "R")
        
        # Check for Abbey pattern
        # Abbey uses our last two moves to predict our next move
        # Let's use a specific pattern that works well against Abbey
        if counter[0] % 10 < 5:
            # First 5 moves in cycle: alternate R and P
            if counter[0] % 2 == 0:
                return "R"
            else:
                return "P"
        else:
            # Next 5 moves: mostly S with some R
            if counter[0] % 10 == 5 or counter[0] % 10 == 8:
                return "R"
            else:
                return "S"
    
    # Default strategy for early game and other bots
    play_number = counter[0] % 4
    
    if play_number == 0:
        # Every fourth play, use the double-counter strategy
        return ideal_response.get(ideal_response.get(prev_play, "R"), "R")
    else:
        # Other plays, just counter directly
        return ideal_response.get(prev_play, "R")