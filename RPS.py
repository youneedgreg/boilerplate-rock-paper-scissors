def player(prev_play, opponent_history=[]):
    # Set of ideal counters
    counter = {"R": "P", "P": "S", "S": "R"}
    
    # First move
    if not prev_play:
        return "R"
    
    # Remember this play
    opponent_history.append(prev_play)
    
    # Detect which bot we're playing against
    n = len(opponent_history)
    
    # Anti-Kris strategy
    # Kris always counters our last move, so we can exploit this
    if n > 3:
        # Pattern check for Kris
        kris_count = 0
        for i in range(1, min(6, n)):
            if i+1 <= n and opponent_history[-i] == counter.get(prev_play, "R"):
                kris_count += 1
        
        if kris_count >= 3 or (n < 20 and kris_count >= 2):
            # We need to think 2 steps ahead:
            # 1. What will Kris play based on our last move?
            kris_next = counter.get(prev_play, "R")
            # 2. What beats that?
            return counter.get(kris_next, "R")
    
    # Abbey uses our last two moves to predict our next move
    # Let's create a pattern that will trick Abbey, but be predictable to us
    if n >= 10:
        # Every 8 moves, create this pattern to exploit:
        cycle = n % 8
        
        if cycle == 0: return "R"
        if cycle == 1: return "P"
        if cycle == 2: return "P"  # Abbey will expect R after PP
        if cycle == 3: return "S"  # But we'll play S to surprise
        if cycle == 4: return "S"
        if cycle == 5: return "R"
        if cycle == 6: return "R"  # Abbey will expect S after RR
        if cycle == 7: return "P"  # But we'll play P to surprise
    
    # Quincy strategy
    # Quincy cycles through ["R", "R", "P", "P", "S"]
    if n > 5:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        quincy_matches = 0
        
        for i in range(min(5, n)):
            if opponent_history[-(i+1)] == quincy_pattern[(n - i - 1) % 5]:
                quincy_matches += 1
        
        if quincy_matches >= 4:
            next_quincy_move = quincy_pattern[n % 5]
            return counter.get(next_quincy_move, "P")
    
    # Mrugesh strategy
    # Plays based on most frequent in last 10 moves
    if n >= 10:
        last_ten = opponent_history[-10:]
        most_frequent = max(set(last_ten), key=last_ten.count)
        
        # Mrugesh will play the counter to our most frequent move
        next_mrugesh_move = counter.get(most_frequent, "R")
        
        # Counter what Mrugesh is likely to play
        return counter.get(next_mrugesh_move, "P")
    
    # If we can't determine the bot or it's early in the game
    # Look at the last 3 moves for a pattern
    if n >= 3:
        last_three = opponent_history[-3:]
        if last_three.count("R") >= 2:
            return "P"  # Counter likely rock
        elif last_three.count("P") >= 2:
            return "S"  # Counter likely paper
        elif last_three.count("S") >= 2:
            return "R"  # Counter likely scissors
    
    # Basic counter strategy for early game
    return counter.get(prev_play, "P")