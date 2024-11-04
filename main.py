from flask import Flask, render_template, request, redirect, url_for, session
from functions import (
    initialize_game,
    move_up,
    move_down,
    move_left,
    move_right,
    check_game_over,
)
import random

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = 'NoneThisTime'

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize the game if not already done
    if 'grid' not in session or 'score' not in session:
        session['grid'] = initialize_game()
        session['score'] = 0
    grid = session['grid']
    score = session['score']
    game_over = False
    message = ''
    # Handle user POST
    if request.method == 'POST':
        if 'restart' in request.form:
            session.pop('grid', None)
            session.pop('score', None)
            return redirect(url_for('index'))
        else:
            try:
                move = request.form['move'].lower()
                if move not in ['w', 'a', 's', 'd']:
                    raise ValueError("Invalid input. Please enter 'w', 'a', 's', or 'd'.")

                if move == 'w':
                    grid, gained_score = move_up(grid)
                elif move == 's':
                    grid, gained_score = move_down(grid)
                elif move == 'a':
                    grid, gained_score = move_left(grid)
                elif move == 'd':
                    grid, gained_score = move_right(grid)

                score += gained_score
                session['score'] = score

                # Add a new random 2 to the grid
                empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
                if empty_cells:
                    i, j = random.choice(empty_cells)
                    grid[i][j] = 2
                    session['grid'] = grid

                # Check for win condition
                for row in grid:
                    if 2048 in row:
                        message = "Congratulations! You reached 2048!"
                        game_over = True
                        break

                # Check for game over
                if check_game_over(grid):
                    message = "Game Over! No more moves available."
                    game_over = True

            except Exception as e:
                message = str(e)

    return render_template('index.html', grid=grid, score=score, message=message, game_over=game_over)

if __name__ == '__main__':
    app.run(debug=True)
