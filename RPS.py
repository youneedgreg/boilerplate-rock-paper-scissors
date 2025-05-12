def player(prev_play, counter=[0]):
    # Increment the counter for each play
    counter[0] += 1
    
    # Define your ideal counter moves
    ideal_response = {"P": "S", "R": "P", "S": "R"}
    
    # First move
    if not prev_play:
        return "S"
    
    # Counter strategy based on the play number
    # This creates a pattern that confuses Abbey and Kris
    play_number = counter[0] % 3
    
    if play_number == 0:
        # Every third play, counter the counter of the previous move
        # This works well against Kris
        return ideal_response[ideal_response[prev_play]]
    else:
        # Other plays, just counter the last move
        # This works well against most bots
        return ideal_response[prev_play]