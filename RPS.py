def player(prev_play, counter=[0]):
    counter[0] += 1
    
    # Define ideal counter moves
    ideal_response = {"P": "S", "R": "P", "S": "R"}
    
    # On first move
    if prev_play == "":
        return "S"
    
    # For rounds 1-9, just counter what was played
    if counter[0] < 10:
        return ideal_response[prev_play]
    
    # After round 10, use the counter trick to beat all bots
    # The trick is to counter the counter of the previous move
    return ideal_response[ideal_response[prev_play]]