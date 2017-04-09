from Downloader.VisualizeHistory import *

h1 = loadHistory('/home/ekmek/Project II/MGR-Project-Code/Data/ModelFiles/ManualVGG16/results/history_VGG16manual__this-is-behavior-with-seeding.npy')
h2 = loadHistory('/home/ekmek/Project II/MGR-Project-Code/Data/ModelFiles/ManualVGG16/results/history_VGG16manual2500v-noseed.npy')
h3 = loadHistory('/home/ekmek/Project II/MGR-Project-Code/Data/ModelFiles/ManualVGG16/results/history_VGG16manual2500v-withSeedAfter.npy')
visualize_histories([h1, h2, h3], ['seed42', 'noSeed', 'seed42ThenNone'],plotvalues='loss',save=True, save_path='comparison_')
#visualize_histories([h1, h2, h3], ['seed42', 'noSeed', 'seed42ThenNone'],plotvalues='mean_absolute_error',save=True, save_path='comparison_')


