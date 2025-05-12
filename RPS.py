def player(prev_play, player_history=[]):
    # Store player's moves to create patterns for predictive bots
    if not player_history:
        # Initialize the history if it's the first call
        player_history.clear()
        player_history.extend(["", "", "", ""])  # [own_last_move, own_current_move, opponent_last_move, opponent_current_move]
    
    # Update move history
    player_history[2] = player_history[3]  # opponent_last_move = opponent_current_move
    player_history[3] = prev_play  # opponent_current_move = prev_play
    player_history[0] = player_history[1]  # own_last_move = own_current_move
    
    # Define the ideal counter for each move
    ideal_counter = {"R": "P", "P": "S", "S": "R"}
    
    # First move (no previous play from opponent)
    if prev_play == "":
        player_history[1] = "R"
        return "R"
    
    # Strategy against Quincy (cycles through "R", "R", "P", "P", "S")
    quincy_pattern = ["R", "R", "P", "P", "S"]
    quincy_matches = 0
    
    # Check for Quincy's pattern in last 5 moves
    for i in range(min(5, len(player_history[3:]))):
        if len(player_history[3:]) > i and player_history[3:][-(i+1)] == quincy_pattern[-(i+1) % 5]:
            quincy_matches += 1
    
    # If we're confident it's Quincy, counter his next predicted move
    if quincy_matches >= 4:
        # Calculate what step in the pattern we're at
        step = len(player_history[3:]) % 5
        next_move = quincy_pattern[step]
        player_history[1] = ideal_counter[next_move]
        return ideal_counter[next_move]
    
    # Strategy against Kris (always counters our last move)
    if player_history[0] and player_history[3] == ideal_counter[player_history[0]]:
        # If it looks like Kris (countered our last move)
        # We need to anticipate what Kris will play next
        kris_next = ideal_counter[player_history[1]]  # Kris will counter our current move
        counter_to_kris = ideal_counter[kris_next]  # We'll counter what Kris will play
        player_history[1] = counter_to_kris
        return counter_to_kris
    
    # Strategy against Abbey (predicts based on our last two moves)
    # Create a repeating pattern then break it to trick Abbey
    if len(player_history[3:]) >= 8:
        # Create a cycle of length 8
        cycle = len(player_history[3:]) % 8
        
        # First 6 moves follow a pattern
        if cycle < 6:
            if cycle % 3 == 0:
                player_history[1] = "R"
                return "R"
            elif cycle % 3 == 1:
                player_history[1] = "P"
                return "P"
            else:
                player_history[1] = "S"
                return "S"
        else:
            # Break the pattern on moves 6 and 7 to confuse Abbey
            # Abbey will expect us to continue the pattern, but we'll counter her counter
            expected_move = "R" if cycle == 6 else "P"
            abbey_counter = ideal_counter[expected_move]
            our_counter = ideal_counter[abbey_counter]
            player_history[1] = our_counter
            return our_counter
    
    # Strategy against Mrugesh (plays based on most frequent move in last 10)
    if len(player_history[3:]) >= 10:
        # First, ensure we've created a clear frequency pattern in our last 10 moves
        # We'll make "R" the most common move
        if len(player_history[3:]) % 3 == 0:
            player_history[1] = "S"  # Play scissors occasionally
            return "S"
        elif len(player_history[3:]) % 3 == 1:
            player_history[1] = "P"  # Play paper occasionally
            return "P"
        else:
            # Mrugesh will expect us to play "R" most and will counter with "P"
            # So we'll counter his "P" with "S"
            player_history[1] = "S"
            return "S"
    
    # Default strategy: counter the opponent's last move
    next_move = ideal_counter[prev_play]
    player_history[1] = next_move
    return next_move