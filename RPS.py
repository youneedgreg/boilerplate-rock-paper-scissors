def player(prev_play, opponent_history=None):
    if opponent_history is None:
        opponent_history = []
    
    # Record opponent's previous play
    if prev_play:
        opponent_history.append(prev_play)
    
    # Default move for the first round
    if not opponent_history:
        return "R"
    
    # Create a dictionary to map each move to its counter
    counter_move = {"P": "S", "R": "P", "S": "R"}
    
    # Identify which bot we're playing against based on their pattern
    if len(opponent_history) >= 5:
        # Check for Quincy's pattern: "R", "R", "P", "P", "S"
        if len(opponent_history) >= 10:
            quincy_pattern = ["R", "R", "P", "P", "S"]
            matches = 0
            for i in range(5):
                if i < len(opponent_history) and opponent_history[-(i+1)] == quincy_pattern[-(i+1) % 5]:
                    matches += 1
            
            if matches >= 4:  # If 4 or more matches, it's likely Quincy
                next_move = quincy_pattern[len(opponent_history) % 5]
                return counter_move[next_move]
    
        # Check for Kris's pattern (always counters our last move)
        kris_matches = 0
        if len(opponent_history) >= 3:
            for i in range(min(3, len(opponent_history) - 1)):
                if i + 1 < len(opponent_history) and opponent_history[-(i+1)] == counter_move[opponent_history[-(i+2)]]:
                    kris_matches += 1
            
            if kris_matches >= 2:  # If it looks like Kris
                # We need to think two steps ahead
                # 1. Kris will counter our last move
                predicted_kris_move = counter_move[opponent_history[-1]]
                # 2. We counter what Kris will play
                return counter_move[predicted_kris_move]
    
        # Check for Mrugesh (plays based on our most frequent move in last 10)
        if len(opponent_history) >= 10:
            last_ten = opponent_history[-10:]
            most_frequent = max(set(last_ten), key=last_ten.count)
            mrugesh_ideal_response = counter_move[most_frequent]
            
            # Test if last few moves match this pattern
            mrugesh_matches = 0
            for i in range(min(3, len(opponent_history) - 10)):
                last_ten_earlier = opponent_history[-(i+11):-(i+1)]
                most_frequent_earlier = max(set(last_ten_earlier), key=last_ten_earlier.count)
                expected_move = counter_move[most_frequent_earlier]
                if opponent_history[-(i+1)] == expected_move:
                    mrugesh_matches += 1
            
            if mrugesh_matches >= 2:  # If it looks like Mrugesh
                # We'll counter what Mrugesh is likely to play next
                return counter_move[mrugesh_ideal_response]
    
    # Abbey strategy - predicts based on last two moves
    # For Abbey, we'll use a different approach
    if len(opponent_history) >= 4:
        # Track patterns of our moves followed by opponent's response
        patterns = {}
        for i in range(len(opponent_history) - 2):
            pattern = opponent_history[i:i+2]
            response = opponent_history[i+2] if i+2 < len(opponent_history) else ""
            pattern_key = "".join(pattern)
            if pattern_key not in patterns:
                patterns[pattern_key] = {}
            if response:
                if response not in patterns[pattern_key]:
                    patterns[pattern_key][response] = 0
                patterns[pattern_key][response] += 1
        
        # Check if the last two moves are in our pattern dictionary
        last_two = opponent_history[-2:]
        last_two_key = "".join(last_two)
        
        if last_two_key in patterns and patterns[last_two_key]:
            # Predict the most likely next move based on history
            predicted_move = max(patterns[last_two_key], key=patterns[last_two_key].get)
            return counter_move[predicted_move]
    
    # If we couldn't identify a specific bot, use a general strategy
    # Let's counter the most common move in the last 5 plays
    if len(opponent_history) >= 5:
        last_five = opponent_history[-5:]
        most_common = max(set(last_five), key=last_five.count)
        return counter_move[most_common]
    
    # If all else fails, counter the last move
    return counter_move[opponent_history[-1]]