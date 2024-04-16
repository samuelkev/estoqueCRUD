from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
from view import *
from colors import *
from PIL import ImageTk, Image

window = Tk()
window.title("Sistema de Estoque")
window.resizable(FALSE, FALSE)
window.configure(background=co9)

window_width = 850
window_height = 548

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

upFrame = Frame(window, width=850, height=55, bg=co2, relief="flat")
upFrame.grid(row=0, column=0)

midFrame = Frame(window, width=630, height=220, bg=co1, relief="flat")
midFrame.grid(row=1, column=0, sticky=NW)

midRightFrame = Frame(window, width=218, height=220, bg=co1, relief="flat")
midRightFrame.grid(row=1, column=0, sticky=NE)

downFrame = Frame(window, width=80, height=400, bg=co1,relief="flat",)
downFrame.grid(row=2, column=0, sticky=NS)

nameApp = Label(upFrame, text="Sistema de Estoque", anchor=NW, font=("Ivy 16 bold"), bg=co2, fg=co1, relief="flat")
nameApp = nameApp.place(x=10, y=12)

global tree
global SEARCH
SEARCH = StringVar()

def search_info():
    if SEARCH.get()!="":
        tree.delete(*tree.get_children())
        con = lite.connect("estoquefinal.db")
        if searchOption.get() == "Nome Produto":
            cursor = con.execute("SELECT * FROM estoque WHERE nome LIKE ?", ("%" + str(SEARCH.get().strip()) + "%",))
        elif searchOption.get() == "Num Série":
            cursor = con.execute("SELECT * FROM estoque WHERE num_serie=?", (SEARCH.get().strip(),))
        elif searchOption.get() == "Cliente":
            cursor = con.execute("SELECT * FROM estoque WHERE cliente LIKE ?", ("%" + str(SEARCH.get().strip()) + "%",))
        elif searchOption.get() == "Projeto":
            cursor = con.execute("SELECT * FROM estoque WHERE projeto LIKE ?", ("%" + str(SEARCH.get().strip()) + "%",))
        elif searchOption.get() == "Nota Fiscal":
            cursor = con.execute("SELECT * FROM estoque WHERE nota=?", (SEARCH.get().strip(),))
        info = cursor.fetchall()
        for item in info:
            tree.insert("", "end", values=(item))


def show_all():
    tree.delete(*tree.get_children())
    con = lite.connect("estoquefinal.db")
    cursor = con.execute("SELECT * FROM estoque")
    info = cursor.fetchall()
    for data in info:
        tree.insert("", "end", values=(data))


global image, image_string, image_label
def show_image():
    global image, image_string, image_label
    
    image = fd.askopenfilename()
    image_string = image

    image = Image.open(image)
    image = image.resize((126, 130))
    image = ImageTk.PhotoImage(image)
    image_label = Label(midFrame, image=image, bd=0, bg=co1)
    image_label.place(x=262, y=20)


def insert_main():
    try:
        global image, image_string, image_label

        nome = productNameEntry.get().strip()
        num_serie = productNum.get().strip()
        cliente = clientName.get().strip()
        projeto = projectName.get().strip()
        quantidade = productAmount.get().strip()
        defeito = productDefects.get().strip()
        nota = productInvoice.get().strip()
        data = entryDate.get().strip()
        image = image_string

        quantidade = int(quantidade) - int(defeito)

        info_list = [nome, num_serie, cliente, projeto, quantidade, defeito, nota, data, image]

        for i in info_list:
            if i == "":
                messagebox.showerror("Erro", "Preencha todos os campos")
                return
            
        insert_info(info_list)

        messagebox.showinfo("Sucesso","Os dados foram inseridos!")  

        productNameEntry.delete(0, "end")
        productNum.delete(0, "end")
        clientName.delete(0, "end")
        projectName.delete(0, "end")
        productAmount.delete(0, "end")
        productDefects.delete(0, "end")
        productInvoice.delete(0, "end")
        entryDate.delete(0, "end")
        image_label.destroy()
        show_info_table()
    except NameError:
        messagebox.showerror("Erro", "Preencha todos os campos!")


def update_main():
    try:
        global image, image_string, image_label
        tree_itens = tree.focus()
        tree_dic = tree.item(tree_itens)
        tree_lista = tree_dic["values"]
        valor_id = tree_lista[0]

        productNameEntry.delete(0, "end")
        productNum.delete(0, "end")
        clientName.delete(0, "end")
        projectName.delete(0, "end")
        productAmount.delete(0, "end")
        productDefects.delete(0, "end")
        productInvoice.delete(0, "end")
        entryDate.delete(0, "end")

        productNameEntry.insert(0, tree_lista[1])
        productNum.insert(0, tree_lista[2])
        clientName.insert(0, tree_lista[3])
        projectName.insert(0, tree_lista[4])
        productAmount.insert(0, tree_lista[5])
        productDefects.insert(0, tree_lista[6])
        productInvoice.insert(0, tree_lista[7])
        entryDate.insert(0, tree_lista[8])

        image = tree_lista[9]
        image_string = image

        image = Image.open(image)
        image = image.resize((126, 130))
        image = ImageTk.PhotoImage(image)
        image_label = Label(midFrame, image=image, bd=0)
        image_label.place(x=262, y=20)


        def update():
            global image, image_string, image_label

            nome = productNameEntry.get()
            num_serie = productNum.get()
            cliente = clientName.get()
            projeto = projectName.get()
            quantidade = productAmount.get()
            defeito = productDefects.get()
            nota = productInvoice.get()
            data = entryDate.get()
            image = image_string

            info_list = [nome, num_serie, cliente, projeto, quantidade, defeito, nota, data, image, valor_id]

            for i in info_list:
                if i == "":
                    messagebox.showerror("Erro", "Preencha todos os campos")
                    return
            update_info(info_list)
            messagebox.showinfo("Sucesso","Os dados foram atualizados!")  

            productNameEntry.delete(0, "end")
            productNum.delete(0, "end")
            clientName.delete(0, "end")
            projectName.delete(0, "end")
            productAmount.delete(0, "end")
            productDefects.delete(0, "end")
            productInvoice.delete(0, "end")
            entryDate.delete(0, "end")
            image_label.destroy()
            show_info_table()
            updateButton.destroy()

        updateButton = Button(midRightFrame, text="Salvar atualização".upper(), width=20, compound=CENTER, anchor=CENTER, relief=RAISED, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co1, fg=co0, command=update)
        updateButton.place(x=42, y=155)
    except IndexError:
        messagebox.showerror("Erro", "Selecione um produto na tabela!")


def delete_main():
    try:
        tree_itens = tree.focus()
        tree_dic = tree.item(tree_itens)
        tree_lista = tree_dic["values"]
        valor_id = tree_lista[0]

        delete_info([valor_id])

        productNameEntry.delete(0, "end")
        productNum.delete(0, "end")
        clientName.delete(0, "end")
        projectName.delete(0, "end")
        productAmount.delete(0, "end")
        productDefects.delete(0, "end")
        productInvoice.delete(0, "end")
        entryDate.delete(0, "end")
        image_label.destroy()
        show_info_table()
        messagebox.showinfo("Sucesso", "Os dados foram deletados!")
        show_info_table()
    except IndexError:
        messagebox.showerror("Erro", "Selecione um produto na tabela!")


def show_info():
        global image, image_string, image_label
        tree_itens = tree.focus()
        tree_dic = tree.item(tree_itens)
        tree_lista = tree_dic["values"]
        valor_id = tree_lista[0]

        productNameEntry.delete(0, "end")
        productNum.delete(0, "end")
        clientName.delete(0, "end")
        projectName.delete(0, "end")
        productAmount.delete(0, "end")
        productDefects.delete(0, "end")
        productInvoice.delete(0, "end")
        entryDate.delete(0, "end")

        productNameEntry.insert(0, tree_lista[1])
        productNum.insert(0, tree_lista[2])
        clientName.insert(0, tree_lista[3])
        projectName.insert(0, tree_lista[4])
        productAmount.insert(0, tree_lista[5])
        productDefects.insert(0, tree_lista[6])
        productInvoice.insert(0, tree_lista[7])
        entryDate.insert(0, tree_lista[8])

        image = tree_lista[9]
        image_string = image

        image = Image.open(image)
        image = image.resize((126, 130))
        image = ImageTk.PhotoImage(image)
        image_label = Label(midFrame, image=image, bd=0)
        image_label.place(x=262, y=20)


def clean_info():
    productNameEntry.delete(0, "end")
    productNum.delete(0, "end")
    clientName.delete(0, "end")
    projectName.delete(0, "end")
    productAmount.delete(0, "end")
    productDefects.delete(0, "end")
    productInvoice.delete(0, "end")
    entryDate.delete(0, "end")
    image_label.destroy()


productNameLabel = Label(midFrame,text="Nome do Produto", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
productNameLabel.place(x=20, y=20)
productNameEntry = Entry(midFrame, width=36, justify="left", relief="solid")
productNameEntry.place(x=20, y=42)

clientName = Label(midFrame, text="Nome do Cliente", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
clientName.place(x=20, y=62)
clientName = Entry(midFrame, width=36, justify="left", relief="solid")
clientName.place(x=20, y=84)

projectName = Label(midFrame, text="Nome do Projeto", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
projectName.place(x=20, y=104)
projectName = Entry(midFrame, width=36, justify="left", relief="solid")
projectName.place(x=20, y=126)

productNum = Label(midFrame, text="Número do Produto", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
productNum.place(x=20, y=146)
productNum = Entry(midFrame, width=36, justify="left", relief="solid")
productNum.place(x=20, y=168)

productAmount = Label(midFrame, text="Quantidade", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
productAmount.place(x=410, y=20)
productAmount = Entry(midFrame, width=15, justify="left", relief="solid")
productAmount.place(x=410, y=42)

productDefects = Label(midFrame, text="Defeitos", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
productDefects.place(x=525, y=20)
productDefects = Entry(midFrame, width=15, justify="left", relief="solid")
productDefects.place(x=525, y=42)

productInvoice = Label(midFrame, text="Nota Fiscal", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
productInvoice.place(x=410, y=62)
productInvoice = Entry(midFrame, width=15, justify="left", relief="solid")
productInvoice.place(x=410, y=84)

entryDate = Label(midFrame, text="Data", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
entryDate.place(x=525, y=62)
entryDate = Entry(midFrame, width=15, justify="left", relief="solid")
entryDate.place(x=525, y=84)

imageButton = Button(midFrame, command=show_image, text="Carregar Foto".upper(), width=20, compound=CENTER, anchor=CENTER, relief=RAISED, overrelief=RIDGE, font=("Ivy 7 bold"), bg=co1, fg=co0)
imageButton.place(x=260, y=168)

searchLabel = Label(midRightFrame, text="Pesquisar por:", anchor=NW, font=("Ivy 10 bold"), bg=co1, fg=co4, relief="flat")
searchLabel.place(x=20, y=20)
searchEntry = Entry(midRightFrame, width=25, justify="left", relief="solid", textvariable=SEARCH)
searchEntry.place(x=20, y=42)
searchButton = Button(midRightFrame, text="⌕", height=0, width=2, anchor=CENTER, relief=RAISED, overrelief=RIDGE, bg=co1, fg=co4, command=search_info)
searchButton.place(x=185, y=38)

insertButton = Button(midRightFrame, text="Inserir", width=10, font=("Ivy 9 bold"), bg=co2, fg=co1, relief="raised", overrelief="ridge", command=insert_main)
insertButton.place(x=20, y=80)

editButton = Button(midRightFrame, text="Editar", width=10, font=("Ivy 9 bold"), bg=co6, fg=co1, relief="raised", overrelief="ridge", command=update_main)
editButton.place(x=120, y=80)

deleteButton = Button(midRightFrame, text="Deletar", width=10, font=("Ivy 9 bold"), bg=co7, fg=co1, relief="raised", overrelief="ridge", command=delete_main)
deleteButton.place(x=120, y=120)

showInfoButton = Button(midRightFrame, text="Visualizar", width=10, font=("Ivy 9 bold"), bg=co3, fg=co1, relief="raised", overrelief="ridge", command=show_info)
showInfoButton.place(x=20, y=120)

cleanButton = Button(midRightFrame, text="Limpar", width=10, font=("Ivy 9 bold"), bg=co1, fg=co4, relief="raised", overrelief="ridge", command=clean_info)
cleanButton.place(x=21, y=180)

showAllInfo = Button(midRightFrame, text="Ver Tudo", width=10, font=("Ivy 9 bold"), bg=co1, fg=co4, relief="raised", overrelief="ridge", command=show_all)
showAllInfo.place(x=120, y=180)

searchOption = ttk.Combobox(midRightFrame, width=11)
searchOption["values"] = ("Nome Produto", "Num Série", "Cliente", "Projeto", "Nota Fiscal")
searchOption.place(x=120, y=18)

def show_info_table():
    tableHeadings = ["ID","Nome", "Número de Série", "Cliente", "Projeto", "Quantidade","Defeitos", "Nota Fiscal", "Data"]

    global tree

    info_list = read_info()
    tree = ttk.Treeview(downFrame, selectmode="extended", columns=tableHeadings, show="headings", height=12)
    tree.grid(row=0, column=0, sticky=NSEW)

    verticalScroll = ttk.Scrollbar(downFrame, orient="vertical", command=tree.yview)
    verticalScroll.grid(row=0, column=1, sticky=NS)
    tree.configure(yscrollcommand=verticalScroll.set)

    horizontalScroll = ttk.Scrollbar(downFrame, orient="horizontal", command=tree.xview)
    horizontalScroll.grid(row=1, column=0, sticky=EW)
    tree.configure(xscrollcommand=horizontalScroll.set)

    hd=["center","center", "center","center","center","center","center","center", "center"]
    h=[30,130, 120,120,100,74,70,100,84]
    n=0

    for col in tableHeadings:
        tree.heading(col, text=col.title(), anchor=CENTER)
            # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        n+=1

    for item in info_list:
        tree.insert("", "end", values=item)
show_info_table()

window.mainloop()