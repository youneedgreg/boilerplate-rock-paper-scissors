def player(prev_play, opponent_history=[], my_history=[]):
    # Initialize histories if first call
    if not opponent_history:
        opponent_history.clear()
    if not my_history:
        my_history.clear()
    
    # The ideal counter for each move
    counter_move = {"R": "P", "P": "S", "S": "R"}
    
    # Add previous play to history
    if prev_play:
        opponent_history.append(prev_play)
    
    # Default first move
    if not prev_play:
        choice = "R"
        my_history.append(choice)
        return choice
    
    # Abbey-beating strategy
    # Create a predictable pattern, then break it to confuse abbey
    if len(opponent_history) > 0 and len(opponent_history) % 10 == 0:
        # Every 10th move, play scissors
        choice = "S"
        my_history.append(choice)
        return choice
    
    if len(my_history) >= 2 and len(opponent_history) >= 2:
        # Look for Kris pattern - always counters your previous move
        if opponent_history[-1] == counter_move.get(my_history[-1], ""):
            # If opponent countered our last move (likely Kris)
            # We'll counter the counter of our current move
            next_expected = counter_move.get(my_history[-1], "R")
            choice = counter_move.get(next_expected, "R")
            my_history.append(choice)
            return choice
    
    # Quincy detection and counter
    if len(opponent_history) >= 5:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        matches = 0
        
        # Check last 5 moves against Quincy's pattern
        for i in range(min(5, len(opponent_history))):
            pattern_index = (len(opponent_history) - 1 - i) % 5
            if opponent_history[-(i+1)] == quincy_pattern[pattern_index]:
                matches += 1
        
        if matches >= 4:
            # It's probably Quincy, so counter his next expected move
            next_index = len(opponent_history) % 5
            choice = counter_move.get(quincy_pattern[next_index], "R")
            my_history.append(choice)
            return choice
    
    # General strategy that works against all bots
    # Every 3rd move, use double counter strategy
    if len(opponent_history) % 3 == 0:
        choice = counter_move.get(counter_move.get(prev_play, "R"), "R")
    else:
        # Simple counter strategy for other moves
        choice = counter_move.get(prev_play, "R")
    
    my_history.append(choice)
    return choice