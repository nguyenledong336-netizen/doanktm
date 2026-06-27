import sys
import tkinter as tk
from gui.cua_so_chinh import CuaSoChinh

def main():
    root = tk.Tk()
    app = CuaSoChinh(root)
    root.mainloop()

if __name__ == "__main__":
    main()