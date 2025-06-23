def broke_above_twice(history, threshold):
    count = 0
    above = False
    for cap in history:
        if cap >= threshold:
            if not above:
                count += 1
                above = True
        else:
            above = False
    return count >= 2
