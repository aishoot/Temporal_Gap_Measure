"""======================================================
The main program of the temporal gap detection experiment
======================================================"""

# Copyright (c) Nov. 2017
# Chao Peng, Yufan Du, Peking University, Beijing, China
# All rights reserved.

import tkinter as tk
from gapGUI import GapDectionGUI

root = tk.Tk()
app = GapDectionGUI(root)
root.mainloop()
