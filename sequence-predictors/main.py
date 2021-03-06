

from mind_reading_machine.mind_reader import MindReader
from seer.seer import SEER
from experts.experts import ExpertsCombo
from experts.experts_ema import ExpertsEMA
from CWT.CWT import CWT_Expert
from perceptron_algorithm.perceptron import Perceptron
import math
import numpy as np
import matplotlib.pyplot as plt

# Read in data
saya_data_path = "../data/saya_data.txt"
john_data_path = "../data/john.data"
john_text_path = "../data/text_data.txt"
fin_data_path = "../data/sp500close01.data"
fin_data_path = "../data/sp500close01.data"
with open(john_data_path, 'r') as f:
    data = [int(c) for c in f.read().replace('\n', '')]
with open(fin_data_path, 'r') as f:
    fin_data = [int(c) for c in f.read().split(',')]

# Run trials to compute average bot performance
# Record bot score / total runs in results
rounds = 10
shannon_results_john = []
hagel_results_john = []
expert_results_john = []
expert_ema_results_john = []
cwt_results_john = []
perceptron_results_john = []
shannon_results_fin = []
hagel_results_fin = []
expert_results_fin = []
expert_ema_results_fin = []
cwt_results_fin = []
perceptron_results_fin = []



interval = 20
num_predictions = []
shannon_results_john_temporal = [0]*int(1.0*len(data)/interval+1)
hagel_results_john_temporal = [0]*int(1.0*len(data)/interval+1)
expert_results_john_temporal = [0]*int(1.0*len(data)/interval+1)
expert_ema_results_john_temporal = [0]*int(1.0*len(data)/interval+1)
cwt_results_john_temporal = [0]*int(1.0*len(data)/interval+1)
perceptron_results_john_temporal = [0]*int(1.0*len(data)/interval+1)

# Human (John) data round

for r in xrange(rounds):
    # Performance of bots
    shannon_bot = MindReader()
    hagel_bot = SEER()
    cwt_bot = CWT_Expert(3,5)
    perc_bot = Perceptron(3,0.1)
    
    expert_bot = ExpertsCombo([MindReader(), SEER(), CWT_Expert(3,5), Perceptron(3,0.1)])
    expert_ema_bot = ExpertsEMA([MindReader(), SEER(), CWT_Expert(3,5), Perceptron(3,0.1)], 0.9)
    i = 0
    num_predictions = []
    cwt_bot = CWT_Expert(3, 5)
    perc_bot = Perceptron(3, 0.1)
    expert_bot = ExpertsCombo([MindReader(), SEER(), CWT_Expert(3, 5), Perceptron(3, 0.1)])
    expert_ema_bot = ExpertsEMA([MindReader(), SEER(), CWT_Expert(3, 5), Perceptron(3, 0.1)], 0.9)

    for human_guess in data:
        shannon_bot.take_turn(human_guess)
        hagel_bot.take_turn(human_guess)
        expert_bot.take_turn(human_guess)
        expert_ema_bot.take_turn(human_guess)
        cwt_bot.take_turn(human_guess)
        perc_bot.take_turn(human_guess)

        if i%20==0:
            num_predictions.append(i)
            j = len(num_predictions)-1
            shannon_results_john_temporal[j] +=(shannon_bot.computer_score/(1.0+i))
            hagel_results_john_temporal[j] += (hagel_bot.computer_score/(1.0+i))
            expert_results_john_temporal[j] += (expert_bot.computer_score/(1.0+i))
            expert_ema_results_john_temporal[j] += (expert_ema_bot.computer_score/(1.0+i))
            cwt_results_john_temporal[j] += (cwt_bot.computer_score/(1.0+i))
            perceptron_results_john_temporal[j] += perc_bot.computer_score/(1.0+i)
        i+=1
    shannon_results_john.append(shannon_bot.computer_score / (1.0 + len(data)))
    hagel_results_john.append(hagel_bot.computer_score / (1.0 + len(data)))
    expert_results_john.append(expert_bot.computer_score / (1.0 + len(data)))
    expert_ema_results_john.append(expert_ema_bot.computer_score / (1.0 + len(data)))
    cwt_results_john.append(cwt_bot.computer_score/(1.0 +len(data)))
    perceptron_results_john.append(perc_bot.computer_score/(1.0+len(data)))
    
shannon_results_john_temporal = [(i/(rounds*1.0)) for i in shannon_results_john_temporal]
hagel_results_john_temporal = [(i/(rounds*1.0)) for i in hagel_results_john_temporal]
expert_results_john_temporal = [(i/(rounds*1.0)) for i in expert_results_john_temporal]
expert_ema_results_john_temporal = [(i/(rounds*1.0)) for i in expert_ema_results_john_temporal]
cwt_results_john_temporal = [(i/(rounds*1.0)) for i in cwt_results_john_temporal]
perceptron_results_john_temporal = [(i/(rounds*1.0)) for i in perceptron_results_john_temporal]



# Fin data round
for r in xrange(rounds):
    # Performance of bots
    shannon_bot = MindReader()
    hagel_bot = SEER()
    expert_bot = ExpertsCombo([MindReader(), SEER(), CWT_Expert(3, 5), Perceptron(3, 0.1)])
    expert_ema_bot = ExpertsEMA([MindReader(), SEER(), CWT_Expert(3, 5), Perceptron(3, 0.1)], 0.9)
    cwt_bot = CWT_Expert(10, 2)
    perc_bot = Perceptron(10, 0.5)
    for human_guess in fin_data:
        shannon_bot.take_turn(human_guess)
        hagel_bot.take_turn(human_guess)
        expert_bot.take_turn(human_guess)
        expert_ema_bot.take_turn(human_guess)
        cwt_bot.take_turn(human_guess)
        perc_bot.take_turn(human_guess)
    shannon_results_fin.append(shannon_bot.computer_score / (1.0 * len(fin_data)))
    hagel_results_fin.append(hagel_bot.computer_score / (1.0 * len(fin_data)))
    expert_results_fin.append(expert_bot.computer_score / (1.0 * len(fin_data)))
    expert_ema_results_fin.append(expert_ema_bot.computer_score / (1.0 * len(fin_data)))
    cwt_results_fin.append(cwt_bot.computer_score / (1.0 * len(fin_data)))
    perceptron_results_fin.append(perc_bot.computer_score / (1.0 * len(fin_data)))

means_john = []
means_john.append(np.mean(shannon_results_john))
means_john.append(np.mean(hagel_results_john))
means_john.append(np.mean(expert_results_john))
means_john.append(np.mean(expert_ema_results_john))
means_john.append(np.mean(cwt_results_john))
means_john.append(np.mean(perceptron_results_john))

stds_john = []


stds_john.append(2 * np.std(shannon_results_john) / math.sqrt(rounds))
stds_john.append(2 * np.std(hagel_results_john) / math.sqrt(rounds))
stds_john.append(2 * np.std(expert_results_john) / math.sqrt(rounds))
stds_john.append(2 * np.std(expert_ema_results_john) / math.sqrt(rounds))
stds_john.append(2 * np.std(cwt_results_john) / math.sqrt(rounds))
stds_john.append(2 * np.std(perceptron_results_john) / math.sqrt(rounds))

means_fin = []
means_fin.append(np.mean(shannon_results_fin))
means_fin.append(np.mean(hagel_results_fin))
means_fin.append(np.mean(expert_results_fin))
means_fin.append(np.mean(expert_ema_results_fin))
means_fin.append(np.mean(cwt_results_fin))
means_fin.append(np.mean(perceptron_results_fin))
print np.mean(cwt_results_fin)
stds_fin = []
stds_fin.append(2 * np.std(shannon_results_fin) / math.sqrt(rounds))
stds_fin.append(2 * np.std(hagel_results_fin) / math.sqrt(rounds))
stds_fin.append(2 * np.std(expert_results_fin) / math.sqrt(rounds))
stds_fin.append(2 * np.std(expert_ema_results_fin) / math.sqrt(rounds))
stds_fin.append(2 * np.std(cwt_results_fin) / math.sqrt(rounds))
stds_fin.append(2 * np.std(perceptron_results_fin) / math.sqrt(rounds))


# Plot bar graph of bot performance

def plot_bars():
    plt.clf()
    nbots = 6
    ind = np.arange(nbots)
    bar_width = 0.35

    fig, ax = plt.subplots()

    rect_john = ax.bar(ind, means_john, bar_width, color='MediumSlateBlue',
                       yerr=stds_john, error_kw={'ecolor': 'Tomato', 'linewidth': 2})

    rect_fin = ax.bar(ind + bar_width, means_fin, bar_width, color='y', yerr=stds_fin,
                      error_kw={'ecolor': 'b', 'linewidth': 2})

    axes = plt.gca()
    axes.set_ylim([0, 1.1])
    axes.set_xlim([-bar_width, nbots - 1 + 3 * bar_width])

    ax.set_ylabel('Score (computer score / total predictions)')
    ax.set_title('Bot sequence prediction scores (with 95% CI)')
    ax.set_xticks(ind + bar_width)
    ax.set_xticklabels(('Shannon', 'Hagelbarger', 'Experts\nCombo',
                        'Experts\n(EMA)', 'CWT', 'Perceptron'))


    ax.legend((rect_john[0], rect_fin[0]), ('John\'s Data', 'Daily SP500 Close Prices (Up/Down)'))


    def auto_label(rects):
        """Label bars"""
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height, "%.2f" %
                    height, ha='center', va='bottom')

        auto_label(rect_john)
        auto_label(rect_fin)

    plt.show()

def plot_temporal():
    plt.clf()

    plt.plot(num_predictions,shannon_results_john_temporal,num_predictions,hagel_results_john_temporal,num_predictions,expert_results_john_temporal,num_predictions,expert_ema_results_john_temporal,num_predictions,cwt_results_john_temporal,num_predictions,perceptron_results_john_temporal)
    plt.show()

