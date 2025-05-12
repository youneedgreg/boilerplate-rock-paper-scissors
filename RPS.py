def player(prev_play, opponent_history=[]):
    # Add previous play to history
    if prev_play:
        opponent_history.append(prev_play)
    
    # Default move for the first round
    if len(opponent_history) <= 1:
        return "P"  # Starting with paper gives a small advantage
    
    # Ideal counters for each move
    counter_move = {"P": "S", "R": "P", "S": "R"}
    
    # Strategy for Quincy (cycles through ["R", "R", "P", "P", "S"])
    # No need to modify this part as it's already working perfectly
    
    # Strategy for Kris - always counter the opponent's previous move
    if len(opponent_history) >= 2:
        # Detect if opponent is likely Kris
        kris_pattern = True
        for i in range(min(5, len(opponent_history) - 1)):
            if opponent_history[-(i+1)] != counter_move.get(opponent_history[-(i+2)], ""):
                kris_pattern = False
                break
        
        if kris_pattern or len(opponent_history) < 10:
            # Against Kris, we need to anticipate what they'll play next
            # Kris will play counter to our last move
            anticipated_move = counter_move.get(opponent_history[-1], "R")
            # We counter Kris's anticipated move
            return counter_move.get(anticipated_move, "P")
    
    # Strategy for Abbey
    # Abbey predicts based on patterns of our last 2 moves
    if len(opponent_history) >= 4:
        # Create markov chain to track patterns
        markov = {}
        for i in range(len(opponent_history) - 2):
            key = opponent_history[i] + opponent_history[i+1]
            if key not in markov:
                markov[key] = {"R": 0, "P": 0, "S": 0}
            
            if i+2 < len(opponent_history):
                markov[key][opponent_history[i+2]] += 1
        
        # Look at last 2 plays to predict next move
        last_key = opponent_history[-2] + opponent_history[-1]
        if last_key in markov:
            # Find the most likely next move based on history
            predicted_move = max(markov[last_key], key=markov[last_key].get)
            # Abbey will counter what she predicts we'll play
            abbey_next_move = counter_move.get(predicted_move, "R")
            # We counter Abbey's anticipated move
            return counter_move.get(abbey_next_move, "P")
        
        # If we can't predict from markov, try a different approach
        # Abbey will try to counter what we've played most recently, so mix it up
        if opponent_history[-1] == opponent_history[-2]:
            # If we played the same thing twice, she'll expect us to play it again
            # So we play what beats the counter to our recent moves
            anticipated_abbey = counter_move.get(opponent_history[-1], "R")
            return counter_move.get(anticipated_abbey, "P")
    
    # Strategy for Mrugesh (plays based on most frequent in last 10)
    # This part is already working well
    if len(opponent_history) >= 10:
        last_ten = opponent_history[-10:]
        most_frequent = max(set(last_ten), key=last_ten.count)
        
        # Mrugesh will play the counter to our most frequent move
        mrugesh_move = counter_move.get(most_frequent, "R")
        # We counter Mrugesh's anticipated move
        return counter_move.get(mrugesh_move, "P")
    
    # Default strategy - play what would beat the opponent's most recent move
    return counter_move.get(opponent_history[-1], "P")