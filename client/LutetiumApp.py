import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from tkinter import simpledialog
try:
    import Lutetium as lu
except:
    mbox.showerror("Lutetium Client", "There was an error connecting to the database.\nPlease check connection.\nTimeoutError")
    exit()
from datetime import datetime
V = 0.2
app = tk.Tk()
app.title("Lutetium Client")
def mainloop():
    mainframe = tk.Frame(app)
    mainframe.pack(padx=5, pady=2, fill=tk.BOTH)
    menuBar = tk.Frame(mainframe,width=100, height=100)
    listArea = tk.Frame(mainframe,width=100, height=100)
    menuBar.pack(side=tk.LEFT)
    listArea.pack(side=tk.RIGHT)
    tk.Label(listArea, text="Downloads", font="consolas").pack()
    treeStyle = ttk.Style()
    treeStyle.configure("Treeview",font="consolas")
    itemlist = ttk.Treeview(listArea, columns=("dlID", "dlName", "dlURL", "dlType", "dlStatus"), show="headings")
    headings = [["dlID", "ID"], ["dlName", "Name"], ["dlURL", "URL"], ["dlType", "Type"], ["dlStatus", "Status"]]
    for heading in headings:
        itemlist.heading(heading[0], text=heading[1])
    itemlist.pack()
    bottomInfoText = tk.StringVar()
    tk.Label(listArea, textvariable=bottomInfoText, font="consolas").pack(side="bottom")
    def fillItemList():
        allitems = lu.getitems("*")
        try:
            itemlist.delete(*itemlist.get_children())
        except:
            pass

        treeSafeList = []
        for item in allitems:
            match item[3]:
                case 0:
                    type = "wget"
                case 1:
                    type = "YTDL"
            match item[4]:
                case 0:
                    status = "Awaiting download"
                case 1:
                    status = "Downloaded"
                case 2:
                    status = "Error occurred during download"
            treeSafeList.append([item[0],item[1], item[2],type,status])
        for item in treeSafeList:
            itemlist.insert("", tk.END, values=item)
        bottomInfoText.set(f"Data retrieved from database at {datetime.now().strftime('%H:%M:%S')}")
    fillItemList()
    def deleteItem():
        rowid = itemlist.focus()
        if len(itemlist.item(rowid)["values"]) == 0:
            mbox.showerror(title="Lutetium Client - Delete item", message="Please select an item and try again.")
        else:
            lu.alteritem("r", itemlist.item(rowid)["values"][0])
            fillItemList()
    def alterItem(mode):
        rowid = itemlist.focus()
        if len(itemlist.item(rowid)["values"]) == 0:
            mbox.showerror(title="Lutetium Client - Delete item", message="Please select an item and try again.")
        else:
            complete = False
            match mode:
                case "name":
                    while not complete:
                        alterbox = simpledialog.askstring("Lutetium Client", f"Please enter a new name for {itemlist.item(rowid)['values'][1]}")
                        if alterbox == None:
                            return
                        elif len(alterbox) == 0:
                            mbox.showerror("Lutetium Client", "An input is required.")
                        else:
                            lu.alteritem("e_n", itemlist.item(rowid)["values"][0], alterbox)
                            complete = True
                case "URL":
                    while not complete:
                        alterbox = simpledialog.askstring("Lutetium Client", f"Please enter a new URL for {itemlist.item(rowid)['values'][1]} ({itemlist.item(rowid)['values'][2]})")
                        if alterbox == None:
                            return
                        elif len(alterbox) == 0:
                            mbox.showerror("Lutetium Client", "An input is required.")
                        else:
                            lu.alteritem("e_u", itemlist.item(rowid)["values"][0], alterbox)
                            complete = True
                case "type":
                    typeEditWin = tk.Toplevel()
                    typeEditFrame = tk.Frame(typeEditWin)
                    typeEditFrame.pack(fill=tk.BOTH)
                    typeVar = tk.StringVar()
                    typeVar.set("Select a download method")
                    typeOpt = ["YTDL", "wget"]
                    typeMenu = tk.OptionMenu(typeEditFrame, typeVar, *typeOpt)
                    typeMenu.pack()
                    def typeEditContinue():
                        if len(typeVar.get()) == "Select a download method":
                            mbox.showerror("Lutetium Client", "An input is required.")
                        else:
                            match typeVar.get():
                                case "YTDL":
                                    TypeVarInt = 1
                                case "wget":
                                    TypeVarInt = 0
                            lu.alteritem("e_t", itemlist.item(rowid)["values"][0], TypeVarInt)
                            typeEditWin.destroy()
                            fillItemList()
                    tk.Button(typeEditFrame, text="Continue", command = lambda: typeEditContinue()).pack(side=tk.LEFT)
                    def SelectionCancel():
                        typeEditWin.destroy()
                        return
                    tk.Button(typeEditFrame, text="Cancel", command=lambda: SelectionCancel()).pack(side=tk.LEFT)
                    typeEditWin.mainloop()
        fillItemList()

    def alterItemCombined():
        editSelectionWin = tk.Toplevel()
        editSelectionFrame = tk.Frame(editSelectionWin)
        editSelectionFrame.pack(fill=tk.BOTH, pady=5, padx=5)
        modeVar = tk.StringVar()
        modeVar.set("Select attribute to edit")
        modeOpt = ["name", "URL", "type"]
        modeMenu = tk.OptionMenu(editSelectionFrame, modeVar, *modeOpt)
        modeMenu.pack()
        def SelectionContinue():
            if modeVar.get() == "Select attribute to edit":
                mbox.showerror("Lutetium Client", "No element has been selected.")
            else:
                editSelectionWin.destroy()
                alterItem(modeVar.get())
        tk.Button(editSelectionFrame, text="Continue", command = lambda: SelectionContinue()).pack(side=tk.LEFT)
        def SelectionCancel():
            editSelectionWin.destroy()
            return
        tk.Button(editSelectionFrame, text="Cancel", command=lambda: SelectionCancel()).pack(side=tk.LEFT)
        editSelectionWin.mainloop()
    def addItem():
        addWin = tk.Toplevel()
        addWin.title('Lutetium Client - Add')
        addFrame = tk.Frame(addWin)
        addFrame.pack(fill=tk.BOTH, padx=5, pady=5)
        tk.Label(addFrame, text="Download Name:").pack()
        nameInput = tk.Entry(addFrame)
        nameInput.pack()
        tk.Label(addFrame, text="Download link:").pack()
        urlInput = tk.Entry(addFrame)
        urlInput.pack()
        tk.Label(addFrame, text="Hide download URL?").pack()
        HideLinkQ = tk.BooleanVar()
        hideBox = tk.Checkbutton(addFrame, variable=HideLinkQ, onvalue=True, offvalue=False)
        hideBox.pack()
        typeVar = tk.StringVar()
        typeVar.set("Select a download method")
        typeOpt = ["YTDL", "wget"]
        typeMenu = tk.OptionMenu(addFrame, typeVar, *typeOpt)
        typeMenu.pack()
        def SubmitAdd():
            if len(nameInput.get()) == 0 or len(urlInput.get()) == 0 or typeVar.get() == "Select a download method":
                mbox.showerror("Lutetium Client", "Name, URL, and method require an input.")
            else:
                match typeVar.get():
                    case "YTDL":
                        TypeVarInt = 1
                    case "wget":
                        TypeVarInt = 0
                lu.additem(nameInput.get(), urlInput.get(), HideLinkQ.get(), TypeVarInt)
                addWin.destroy()
                fillItemList()
        addSubmit = tk.Button(addFrame, text="Add", command=lambda: SubmitAdd())
        addSubmit.pack()
        addWin.mainloop()
    def about():
        aboutWin = tk.Toplevel()
        aboutFrame = tk.Frame(aboutWin)
        aboutFrame.pack(fill=tk.BOTH, padx=5, pady=5)
        tk.Label(aboutFrame, text="Lu", font=("consolas", 34, "bold")).pack()
        tk.Label(aboutFrame, text="Lutetium\nBy James King", font=("consolas", 16)).pack()
        tk.Label(aboutFrame, text=f"Lutetium App: V{V}\nLutetium Core: V{lu.V}", font=("consolas", 12)).pack()
        tk.Label(aboutFrame, text="β experimental release", font=("consolas", 12, "italic")).pack()
        def closeAbout():
            aboutWin.destroy()
        tk.Button(aboutFrame, text="Exit", command = lambda: closeAbout()).pack()
        aboutWin.mainloop()
    tk.Label(menuBar, text="Options", font="consolas").pack()
    tk.Button(menuBar, text="Add item", command = lambda: addItem()).pack()
    tk.Button(menuBar, text="Edit item", command=lambda: alterItemCombined()).pack()
    tk.Button(menuBar, text="Remove item", command = lambda: deleteItem()).pack()
    tk.Button(menuBar, text="Refresh", command = lambda: fillItemList()).pack()
    tk.Button(menuBar, text="About", command = lambda: about()).pack()
    tk.Button(menuBar, text="Exit", command = lambda: exit()).pack()
mainloop()
app.mainloop()
