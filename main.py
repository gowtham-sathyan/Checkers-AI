import sys
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from alphabeta.algorithm import alphabeta
import time, csv, os

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

#instructions for getting commend line inputs
try:
    depth = int(sys.argv[1])
    redHeuristics = sys.argv[2]
    whiteHeuristics = sys.argv[3]

    if depth<1:
        print("In this game, the depth option should be 1 or above")
        exit(0)
    if 'H' not in redHeuristics or int(redHeuristics[1:]) not in [1,2,3,4]:
        print("Heuristic should begin with H and should any one of the numbers 1, 2, 3 or 4.")
        exit(0)
    if 'H' not in whiteHeuristics or int(whiteHeuristics[1:]) not in [1,2,3,4]:
        print("Heuristic should begin with H and should any one of the numbers 1, 2, 3 or 4.")
        exit(0)
except:
    print("You need to give 3 command line arguments.\n1. Depth (1 or above)\n2. Heuristic for red pieces (H1, H2, H3 or H4).\n3. Heuristic for white pieces (H1, H2, H3 or H4)")
    exit(0)

if(os.path.exists("output.csv")):
    csv_file=open("output.csv","a", newline='')
    output_writer=csv.writer(csv_file)
else:
    csv_file=open("output.csv","w+", newline='')
    output_writer=csv.writer(csv_file)
    output_writer.writerow(['Depth','Red Heuristic','White Heuristic','Average time per move for Red', 'Average time per move for White', 'Result'])

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    whiteCount = 0
    redCount = 0
    whiteTime = 0
    redTime = 0
    boards = []
    while run:
        clock.tick(FPS)
        if game.turn == WHITE:#check which player's turn it is
            whiteCount += 1#turn tracker
            start=time.time()
            value, new_board = alphabeta(game.get_board(), depth, WHITE, True, game, -100000, 100000, whiteHeuristics)#call alpha beta for that player
            whiteTime += time.time() - start
            #value, new_board = minimax(game.get_board(), 4, WHITE, True, game)
            game.ai_move(new_board)
            # new_board.print_board()
            boards.append(new_board.board)
            # print(new_board.red_kings)
            # print(new_board.white_kings)
            # print(" ")

        # pygame.time.delay(100)
        #
        
        if game.turn == RED:#check which player's turn it is
            redCount += 1#turn tracker
            start = time.time()
            value, new_board = alphabeta(game.get_board(), depth, RED, True, game, -100000, 100000, redHeuristics)#call alpha beta for that player
            redTime += time.time() - start
            #value, new_board = minimax(game.get_board(), 4, RED, True, game)
            game.ai_move(new_board)
            # new_board.print_board()
            boards.append(new_board.board)
            # print(new_board.red_kings)
            # print(new_board.white_kings)
            # print(" ")

        if game.winner() != None:#checks if there's been a winner this turn
            print(f'Number of Moves: {whiteCount}')
            print(game.winner())
            run = False
            output_writer.writerow([str(depth), str(redHeuristics), str(whiteHeuristics), str(whiteTime/whiteCount), str(redTime/redCount), str(game.winner())])
            csv_file.close()

        elif whiteCount >= 80:#our draw detection, stops the game after 80 moves for both players
            run = False
            print(f'Number of Moves: {whiteCount}')
            output_writer.writerow([str(depth), str(redHeuristics), str(whiteHeuristics), str(whiteTime/whiteCount), str(redTime/redCount), 'Draw'])
            csv_file.close()
            sys.exit("Draw")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)


        game.update()

    pygame.quit()


main()
