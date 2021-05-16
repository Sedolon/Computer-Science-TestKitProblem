from Distribution_Main_Building import distribute
from Distribution_Leuphana import distribute_leuphana
from Sort_Test_Kits import sort


try:
    sort()
    distribute()
    distribute_leuphana()
except Exception as e:
    print("Sth. went wrong. Probably you chose a wrong date!")
    print(e)


