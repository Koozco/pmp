from pmp.experiments.multigoal_charts import draw_chart
from pmp.rules import Bloc, Borda, ChamberlinCourant
from pmp.rules import MultigoalBlocBorda as BB
from pmp.rules import MultigoalCCBorda as CCB


repetitions = 10
k = 2
n = 30
m = 40

filename = 'bb-chart-k{}-n{}-m{}'.format(k, n, m)
draw_chart(filename, k, n, m, repetitions,  Bloc(), Borda(), BB, 2, log_errors=False)

filename = 'ccb-chart-k{}-n{}-m{}'.format(k, n, m)
draw_chart(filename, k, n, m, repetitions, ChamberlinCourant(), Borda(), CCB, 2, log_errors=False)
