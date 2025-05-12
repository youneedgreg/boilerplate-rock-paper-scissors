def player(prev_play, player_history=[], opponent_history=[], ideal_response={"R": "P", "P": "S", "S": "R"}):
    # Initialize player history if it doesn't exist
    if not player_history:
        player_history.append("")
        opponent_history.append("")
    
    # Store the last play
    if prev_play:
        opponent_history.append(prev_play)
    
    # Make a default first move
    if not prev_play:
        guess = "R"
        player_history.append(guess)
        return guess
    
    # Create a predictable pattern for Abbey to learn, then break it
    n = len(opponent_history)
    
    # For Abbey detection
    # Abbey maintains a history of my moves and predicts based on my last two
    # Let's exploit this by creating a pattern she can learn, then breaking it
    
    # First, determine which bot we're likely playing against:
    
    # Check for Kris - always counters your last move
    kris_counter = 0
    if n >= 4:
        for i in range(1, min(4, n-1)):
            if opponent_history[-i] == ideal_response.get(player_history[-(i+1)], ""):
                kris_counter += 1
    
    # If it looks like Kris (counters your last move)
    if kris_counter >= 3 or (n < 10 and kris_counter >= 2):
        # Kris will play the counter to our last move
        kris_likely_play = ideal_response.get(player_history[-1], "P")
        # We counter what Kris will play
        guess = ideal_response.get(kris_likely_play, "S")
        player_history.append(guess)
        return guess
    
    # Check for Quincy's pattern
    quincy_pattern = ["R", "R", "P", "P", "S"]
    quincy_matches = 0
    
    if n >= 5:
        for i in range(min(5, n-1)):
            if opponent_history[-(i+1)] == quincy_pattern[(n-i-1) % 5]:
                quincy_matches += 1
    
    # If it looks like Quincy's pattern
    if quincy_matches >= 4:
        next_quincy = quincy_pattern[n % 5]
        guess = ideal_response.get(next_quincy, "P")
        player_history.append(guess)
        return guess
    
    # Mrugesh strategy - plays based on most frequent in last 10
    if n >= 10:
        last_ten = opponent_history[-10:]
        most_frequent = max(set(last_ten), key=last_ten.count)
        
        # Mrugesh will counter our most frequent move
        mrugesh_move = ideal_response.get(most_frequent, "P")
        guess = ideal_response.get(mrugesh_move, "S")
        player_history.append(guess)
        return guess
    
    # Special strategy for Abbey
    # Create a pattern for Abbey to learn, then exploit it
    
    # Play a repeating pattern that Abbey can detect
    if n % 10 < 4:
        guess = "R"
    elif n % 10 < 8:
        guess = "P"
    else:
        # Abbey will expect us to play "R" after several "P"s
        # But we'll play "S" to counter her counter
        guess = "S"
    
    player_history.append(guess)
    return guess