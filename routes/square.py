import logging
from flask import request, jsonify
from routes import app

logger = logging.getLogger(__name__)

@app.route('/digital-colony', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("Data sent for evaluation: {}".format(data))
    result = []
    for i in data:
        generations = int(i['generations'])
        colony = i['colony']
        result.append(solve(colony, generations))
    logging.info("Weights result: {}".format(result))
    return jsonify(result)

def solve(colony, generations):
    # Use integers instead of strings for better performance
    colony = [int(digit) for digit in colony]
    
    memo_pairs = {}

    # Calculate initial weight once (sum of digits in the colony)
    weight = sum(colony)

    # Generate 50 generations
    for _ in range(generations):
        colony, weight = next_generation(colony, memo_pairs, weight)

    return weight  # Return the weights for 10th and 50th generations

def next_generation(colony, memo_pairs, weight):
    n = len(colony)
    if n < 2:
        return colony, weight

    new_colony = []
    new_weight = weight  # Copy the current weight to modify

    # Iterate over the colony, generate new pairs
    for i in range(n):
        if i < n - 1:
            a = colony[i]
            b = colony[i + 1]
            
            # Check memoization first
            if (a, b) in memo_pairs:
                signature = memo_pairs[(a, b)]
            else:
                # Calculate the signature if not memoized
                if a == b:
                    signature = 0
                elif a > b:
                    signature = a - b
                else:
                    signature = 10 - abs(a - b)
                
                # Memoize the pair signature for future use
                memo_pairs[(a, b)] = signature
            
            # Calculate the new digit and update weight
            new_digit = (weight + signature) % 10
            new_colony.append(a)
            new_colony.append(new_digit)

            # Update the weight with the new digit
            new_weight += new_digit
        else:
            # Add the last element as is, no new digit generated here
            new_colony.append(colony[i])

    return new_colony, new_weight
