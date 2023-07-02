import csv
import yaml
import random
import keyboard
import os
from psychopy import visual, event, gui, core
from typing import Dict


RESULTS1 = [["NUMER PROBY", "EKSPERYMENT", "CZAS REAKCJI", "ZGODNOSC", "BODZIEC", "REAKCJA", "BLOK"]]


def load_config():
    with open("config.yaml") as file:
        data = yaml.safe_load(file)
    return data


def reactions(keys):
    event.clearEvents()
    key = event.waitKeys(keyList=config["KEYS"])
    return key[0]


def experiment_keys(keys):
    event.clearEvents()
    exp_key = event.waitKeys(keyList=config["REACTION_KEYS"])
    return exp_key[0]


def finish_experiment(win):
    message = visual.TextStim(win, text="", height=40)
    message.text = "Zakończyłeś eksperyment"
    message.draw()
    win.flip()
    core.wait(3)
    win.close()
    core.quit()


def show_text(info, win, keys=None):
    if keys is None:
        keys = ["space"]
    info.draw()
    win.flip()
    reactions(keys)


def write_results_to_csv(results, info):
    filename = f"{info['ID']}_{info['Wiek']}_{info['Płeć']}.csv"
    mode = 'a' if os.path.exists(filename) else 'w'
    with open(filename, mode, newline='') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(['Wyniki badania:'])
        for result in results:
            writer.writerow(result)


def bodsiec():
    cos1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 8]
    a = 2023
    while True:
        cos = random.choice(cos1)
        if (cos % 2 == 0):
            a = random.randrange(2, 1000, 2)
            stim = visual.TextStim(win=window, height=40, text=a, color=config['STIM_COLOR2'])
            stim.setPos((0, 0))
            stim.draw()
        else:
            a = random.randrange(1, 1000, 2)
            stim = visual.TextStim(win=window, height=40, text=a, color=config['STIM_COLOR2'])
            stim.setPos((0, 0))
            stim.draw()
        return a


window = visual.Window(units="pix", color="grey", fullscr=False)
mouse = event.Mouse(win=window, visible=True)
clock = core.Clock()

config = load_config()
print(config)

inst_tr1 = visual.TextStim(win=window, text=("Za chwilę przystąpisz do wykonywania zadania. Polega ono na wciskaniu prawej strzałki, kiedy na ekranie wyświetli się liczba parzysta. Jeżeli podana liczba jest nieparzysta, nie wciskaj nic - zaczekaj na ponowne pojawienie się punktu fiksacji. \n Naciśnij spację by przejść dalej"), height=20)
inst_tr12 = visual.TextStim(win=window, text="Zadanie będzie się składać z 2 bloków, a każdy z trzech serii - przed każdym dostaniesz o nim informacje i możliwość krótkiej przerwy. Postaraj się wykonać zadanie najdokładniej i reaguj najszybciej jak potrafisz. Przed pojawieniem się liczby pojawi się mały krzyżyk na środku ekranu- jest to punkt fiksacji, który ma za zadanie pomóc ci się skupić. Nie spuszczaj go z oczu! \n Naciśnij spację by przejść dalej lub poinformuj osobą prowadzącą, jeżeli masz jakieś wątpliwości" , height=20)
inst_tr2 = visual.TextStim(win=window, text="Trening!\n Teraz zacznie się próba treningowa- pamiętaj, reagujesz tylko na liczby parzyste, prawą strzałką na klawiaturze. Naciśnij spację by rozpocząć trening", height=20)
inst_exp = visual.TextStim(win=window,
                           text="Trening za tobą! Jeżeli nadal masz jakieś wątpliwości zgłoś to badaczowi, jeśli nie "
                                "możesz zaczynać eksperyment (Uwaga - teraz nie dostaniesz informacji zwrotnej o "
                                "poprawności swoich reakcji) \n Powodzenia! \n Naciśnij spację by rozpocząć eksperyment", height=20)
inst_break = visual.TextStim(win=window, text="Za tobą pierwszy blok, możesz teraz chwilę odpocząć. "
                                              "Jeżeli jesteś gotowy, aby przejść dalej - naciśnij spację", height=20)
inst_end = visual.TextStim(win=window, text="Dziękujemy za udział w eksperymencie", height=20)
pozytywna_odp = visual.TextStim(win=window, text="DOBRZE!", color='green', height=40)
negatywna_odp = visual.TextStim(win=window, text="ŹLE!", color='black', height=40)
inst_break_fast = visual.TextStim(win=window, text="Jeżeli jesteś gotowy, aby przejść dalej - naciśnij spację",
                                  height=20)
inst_seria_pierwsza = visual.TextStim(win=window, text="Za tobą pierwsza seria, możesz teraz chwilę odpocząć. Jeżeli jesteś gotowy, aby przejść dalej - naciśnij spację", height=20)
inst_seria_kolejna = visual.TextStim(win=window, text="Za tobą kolejna seria, możesz teraz chwilę odpocząć. Jeżeli jesteś gotowy, aby przejść dalej - naciśnij spację", height=20)
fix = visual.TextStim(win=window, text="+", pos=(0, 0), height=40, color=config["FIX_CROSS_COLOR"])
stim = visual.TextStim(win=window, height=60, color=config['STIM_COLOR2'])


def part_of_training(n_trials, experiment):
    for i in range(n_trials):
        keys = event.getKeys();
        if 'f7' in keys:
            print("'F7' key pressed!")
            f7_pressed = True
            finish_experiment(window)
            break
        mouse.setVisible(False)
        fix.draw()
        window.flip()
        core.wait(0.8)
        b = bodsiec()
        b
        window.callOnFlip(clock.reset)
        window.flip()
        rt = 0
        acc = 100
        r = 0
        blok = "trening"

        while clock.getTime() < config["TRIAL_TIME"]:
            if keyboard.is_pressed('right') is not False:
                r = 1
                if b % 2 == 0:
                    rt = clock.getTime()
                    acc = 1
                    pozytywna_odp.draw()
                    break
                else:
                    acc = 0
                    negatywna_odp.draw()
                    break
        else:
            if keyboard.is_pressed('right') is False:
                r = 0
                if b % 2 == 0:
                    acc = 0
                    negatywna_odp.draw()

                else:
                    acc = 1
                    pozytywna_odp.draw()

        window.flip()
        core.wait(((random.randint(800, 900)) * 0.001))

        RESULTS1.append([i + 1, experiment, rt, acc, b, r, blok])


def part_of_experiment(n_trials, experiment):
    for i in range(n_trials):
        keys = event.getKeys();
        if 'f7' in keys:
            print("'F7' key pressed!")
            f7_pressed = True
            finish_experiment(window)
            break
        mouse.setVisible(False)
        fix.draw()
        window.flip()
        core.wait(0.8)
        b = bodsiec()
        b
        window.callOnFlip(clock.reset)
        window.flip()
        rt = 0
        acc = 100
        r = 15
        blok = "normalny"
        while clock.getTime() < config["TRIAL_TIME"]:
            if keyboard.is_pressed('right') is not False:
                r = 1
                if b % 2 == 0:
                    rt = clock.getTime()
                    acc = 1
                    break
                else:
                    acc = 0
                    break
        else:
            if keyboard.is_pressed('right') is False:
                r = 0
                if b % 2 == 0:
                    acc = 0

                else:
                    acc = 1

        window.flip()
        core.wait(((random.randint(800, 900)) * 0.001))

        RESULTS1.append([i + 1, experiment, rt, acc, b, r, blok])


def part_of_experiment_fast(n_trials, experiment):
    for i in range(n_trials):
        keys = event.getKeys();
        if 'f7' in keys:
            print("'F7' key pressed!")
            f7_pressed = True
            finish_experiment(window)
            break
        mouse.setVisible(False)
        fix.draw()
        window.flip()
        core.wait(0.8)
        b = bodsiec()
        b
        window.callOnFlip(clock.reset)
        window.flip()
        rt = 0
        acc = 100
        r = 75
        blok = "szybki"
        while clock.getTime() < config["TRIAL_TIME"]:
            if keyboard.is_pressed('right') is not False:
                r = 1
                if b % 2 == 0:
                    rt = clock.getTime()
                    acc = 1
                    break
                else:
                    acc = 0
                    break
        else:
            if keyboard.is_pressed('right') is False:
                r = 0
                if b % 2 == 0:
                    acc = 0

                else:
                    acc = 1
        window.flip()
        core.wait(((random.randint(700, 800)) * 0.001))
        RESULTS1.append([i + 1, experiment, rt, acc, b, r, blok])


info: Dict = {"ID": "", "Wiek": "", "Płeć": ["M", "K"]}
gui.DlgFromDict(dictionary=info, title="Kwadraciki")

# TRAINING
show_text(info=inst_tr1, win=window)
show_text(info=inst_tr12, win=window)
show_text(info=inst_tr2, win=window)
part_of_training(n_trials=config["N_TRIALS_TRAINING"], experiment=False)

# EXPERIMENT_NORMAL
show_text(info=inst_exp, win=window)
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True)

# SERIES
show_text(info=inst_seria_pierwsza, win=window)

# EXPERIMENT_NORMAL
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT2"], experiment=True)

# SERIES
show_text(info=inst_seria_kolejna, win=window)

# EXPERIMENT_NORMAL
part_of_experiment(n_trials=config["N_TRIALS_EXPERIMENT3"], experiment=True)

# BREAK
show_text(info=inst_break, win=window)

# EXPERIMENT_FAST
part_of_experiment_fast(n_trials=config["N_TRIALS_EXPERIMENT1"], experiment=True)

# SERIES
show_text(info=inst_seria_pierwsza, win=window)

# EXPERIMENT_FAST
part_of_experiment_fast(n_trials=config["N_TRIALS_EXPERIMENT2"], experiment=True)

# SERIES
show_text(info=inst_seria_kolejna, win=window)

# EXPERIMENT_FAST
part_of_experiment_fast(n_trials=config["N_TRIALS_EXPERIMENT2"], experiment=True)

# END
show_text(info=inst_end, win=window)

# WRITE TO CSV
write_results_to_csv(RESULTS1, info)

