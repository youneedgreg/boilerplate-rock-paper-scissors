def player(prev_play, opponent_history=[], my_history=[]):
    # Initialize history lists if needed
    if not opponent_history:
        opponent_history.clear()
    if not my_history:
        my_history.clear()
    
    # Add previous play to history
    if prev_play:
        opponent_history.append(prev_play)
    
    # Define counter moves
    ideal_response = {"R": "P", "P": "S", "S": "R"}
    
    # First move
    if not prev_play:
        choice = "P"
        my_history.append(choice)
        return choice
    
    # Strategy against Abbey
    # Abbey predicts our next move based on our previous pattern, then counters it
    # We'll use a pattern that makes Abbey predictable
    
    # We'll use special strategy against Abbey that uses meta-patterns
    # Cycle length of 4 moves
    if len(opponent_history) >= 8:
        cycle = len(opponent_history) % 4
        
        if cycle == 0:
            choice = "S"  # First move in cycle
        elif cycle == 1:
            choice = "S"  # Second move in cycle
        elif cycle == 2:
            # Abbey will expect us to play S again, and counter with R
            # So we'll play P to beat her R
            choice = "P"
        else:  # cycle == 3
            # Mix it up again
            choice = "R"
        
        my_history.append(choice)
        return choice
    
    # Kris detection and counter
    # Kris always counters our last move
    if len(my_history) >= 2 and len(opponent_history) >= 2:
        # Check if the last move was countering our previous move
        if opponent_history[-1] == ideal_response.get(my_history[-1], "R"):
            # It's likely Kris, so we'll counter his expected counter
            kris_next = ideal_response.get(opponent_history[-1], "R")
            choice = ideal_response.get(kris_next, "R")
            my_history.append(choice)
            return choice
    
    # Quincy detection and counter
    if len(opponent_history) >= 5:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        matches = 0
        
        for i in range(min(5, len(opponent_history))):
            pattern_index = (len(opponent_history) - 1 - i) % 5
            if opponent_history[-(i+1)] == quincy_pattern[pattern_index]:
                matches += 1
        
        if matches >= 4:
            # It's probably Quincy, so counter his next expected move
            next_index = len(opponent_history) % 5
            choice = ideal_response.get(quincy_pattern[next_index], "R")
            my_history.append(choice)
            return choice
    
    # Final fallback: alternate between countering previous move and 
    # countering the counter of previous move
    if len(opponent_history) % 2 == 0:
        choice = ideal_response.get(prev_play, "R")  # Simple counter
    else:
        choice = ideal_response.get(ideal_response.get(prev_play, "R"), "R")  # Double counter
    
    my_history.append(choice)
    return choice