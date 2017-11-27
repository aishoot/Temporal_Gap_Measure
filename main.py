"""======================================================
The main program of the temporal gap detection experiment
======================================================"""

import tkinter as tk
from gapGUI import GapDectionGUI

root = tk.Tk()
app = GapDectionGUI(root)
root.mainloop()