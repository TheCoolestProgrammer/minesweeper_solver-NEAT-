from init import App
import os
import neat
import pickle
import time

def eval_genomes(genomes, config):
    app = App()
    networks = []
    ge = []
    for i, genome in genomes:
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        ge.append(genome)


    for i, network in enumerate(networks):
        app.create_new_game()
        border = app.visibility_area // 2
        x,y = border,border
        while True:
            time.sleep(0.5)
            if app.is_game_over():
                break
            # # else:
            # #     print("123")
            if x == app.field_width-border:
                x=border
                y+=1
            # # if y == app.field_height-border:
            # #     y=border
            # field = [app.field[y2][x-border:x+border+1] for y2 in range(y-border,y+border+1)]
            # # log.writelines("_________поле_____________\n")
            # print("__________поле_______________________")
            # for j in field:
            #     print(j)
            #     # log.writelines(str(j)+"\n")
            # field = [j for i in field for j in i]
            # print("__________ход нейронки_______________")
            # # log.writelines("_________нейронка думает, что стоит ходить так_____________\n")
            # res = network.activate(field)
            # res = [res[app.visibility_area * i:app.visibility_area * (i + 1)] for i in range(app.visibility_area)]
            # for j in res:
            #     print(j)
            #     # log.write(str(j)+"\n")
            # opened_cells, wrong_touches = app.open_cells(x,y,border,res)
            # ge[i].fitness=opened_cells -wrong_touches
            # app.update_data()
            # x+=1

            opened_cells,wrong_opened_cells=app.open_cells2(x,y,border,network)
            ge[i].fitness = opened_cells-wrong_opened_cells
            x+=1
    app.create_new_game()

def run_neat(config):
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    # global p

    winner = p.run(eval_genomes, 100)
    with open("best_minesweeper_solver.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    # app = App()
    # app.update_data()
    # for i in app.field:
    #     print(i)

    # file=open("minesweeper_log.txt","w")
    # file.write("")
    # file.close()
    # log = open("minesweeper_log.txt", "a", encoding="UTF-8")
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    run_neat(config)
