from pmp.experiments.multigoal_charts import draw_chart
from pmp.rules import Bloc, Borda, ChamberlinCourant
from pmp.rules import MultigoalBlocBorda as BB
from pmp.rules import MultigoalCCBorda as CCB


repetitions = 100
k = 2
n = 20
m = 20
# draw_chart(k, n, m, repetitions, Bloc(), Borda(), BB)
draw_chart(k, n, m, repetitions, ChamberlinCourant(), Borda(), CCB)
