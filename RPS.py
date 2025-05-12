def player(prev_play, opponent_history=[], my_history=[]):
    # Define counter moves
    counter = {"R": "P", "P": "S", "S": "R"}
    
    # Initialize histories if needed
    if not opponent_history:
        opponent_history.clear()
    if not my_history:
        my_history.clear()
    
    # Add previous play to history
    if prev_play:
        opponent_history.append(prev_play)
    
    # Default first move
    if not prev_play:
        my_move = "P"
        my_history.append(my_move)
        return my_move
    
    # Get the length of play history
    n = len(opponent_history)
    
    # Strategy for Abbey
    # Abbey predicts based on our last two moves, so we'll create patterns
    # where we control what she expects, then surprise her
    if len(my_history) >= 2:
        # Create a pattern where we play the same two moves repeatedly 
        # then break the pattern every third move
        if n % 3 == 0:
            # Always play R for the first in a set of 3
            my_move = "R"
        elif n % 3 == 1:
            # Always play P for the second in a set of 3
            my_move = "P"
        else:
            # Third move - Abbey will predict we play "R" (repeating the pattern)
            # Abbey would counter with "P", so we play "S" to beat her "P"
            my_move = "S"
        
        my_history.append(my_move)
        return my_move
    
    # If we don't have enough history yet, use a more basic strategy
    # Counter the last move
    my_move = counter[prev_play]
    my_history.append(my_move)
    return my_move