def player(prev_play, opponent_history=[]):
    # Initialize the counter move dictionary
    counter_move = {"R": "P", "P": "S", "S": "R"}
    
    # First move
    if not prev_play:
        return "R"
    
    # Add the current play to the history
    opponent_history.append(prev_play)
    
    # Strategies optimized for each bot
    n = len(opponent_history)
    
    # 1. Strategy for Kris - always plays the counter to our last move
    if n >= 3:
        last_three = opponent_history[-3:]
        kris_counter = True
        
        # Check if all the recent moves are exact counters to our previous moves
        for i in range(1, min(3, n)):
            if i < n and opponent_history[-i] != counter_move.get(opponent_history[-(i+1)], ""):
                kris_counter = False
                break
        
        if kris_counter:
            # For Kris, we need to predict what he'll play next and counter it
            # Kris will counter our last move
            kris_next = counter_move.get(prev_play, "R")
            # So we counter Kris's predicted move
            return counter_move.get(kris_next, "P")
    
    # 2. Strategy for Abbey - uses our last two moves to predict our third
    if n >= 10:
        # Create a model of what move comes after each pair of moves
        pairs = {}
        for i in range(n - 2):
            key = opponent_history[i] + opponent_history[i+1]
            if key not in pairs:
                pairs[key] = {"R": 0, "P": 0, "S": 0}
            
            if i + 2 < n:
                next_move = opponent_history[i+2]
                pairs[key][next_move] += 1
        
        # Use the last two moves to predict what Abbey thinks we'll play next
        last_two = opponent_history[-2] + opponent_history[-1]
        if last_two in pairs and sum(pairs[last_two].values()) > 0:
            # Find the most likely move according to history
            prediction = max(pairs[last_two], key=pairs[last_two].get)
            # Abbey will counter what she predicts
            abbey_next = counter_move.get(prediction, "R")
            # We counter Abbey's predicted move
            return counter_move.get(abbey_next, "P")
    
    # 3. Strategy for Quincy - cycles through ["R", "R", "P", "P", "S"]
    if n >= 6:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        pattern_matches = 0
        
        # Check how well recent moves match Quincy's pattern
        for i in range(min(5, n)):
            expected = quincy_pattern[(n - i - 1) % 5]
            if opponent_history[-(i+1)] == expected:
                pattern_matches += 1
        
        if pattern_matches >= 4:
            # Predict Quincy's next move based on the pattern
            quincy_next = quincy_pattern[n % 5]
            return counter_move.get(quincy_next, "P")
    
    # 4. Strategy for Mrugesh - uses our most frequent move from last 10
    if n >= 10:
        # Identify the most frequent move in the last 10
        last_ten = opponent_history[-10:]
        most_common = max(set(last_ten), key=last_ten.count)
        
        # Predict what Mrugesh will play
        mrugesh_next = counter_move.get(most_common, "R")
        return counter_move.get(mrugesh_next, "P")
    
    # If all else fails, use a basic strategy:
    # Look at the last few moves, detect any patterns, and counter accordingly
    if n >= 3:
        # Counter the most common recent move
        last_three = opponent_history[-3:]
        if last_three.count("R") >= 2:
            return "P"
        elif last_three.count("P") >= 2:
            return "S"
        elif last_three.count("S") >= 2:
            return "R"
    
    # Simple fallback: counter the last move
    return counter_move.get(prev_play, "P")