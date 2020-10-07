from tkinter import *
from tkinter import messagebox
from random import *
import pickle
from threading import *
from datetime import *
import os
from pymysql import *
import re

class Customer():
    cuslist=[]
def autoload1():
    fs=open('Cutomer_order_history.txt','rb')
    Customer.cuslist=pickle.load(fs)
    fs.close()
concat=''
def btnclick(number):
    global concat
    concat+=str(number)
    calc.set(concat)

def reset_func():
    calc.set('')
    global concat
    concat=''

def eval_func():
    try:
        global concat
        concat=str(eval(calc.get()))
        calc.set(concat)
    except Exception:
        messagebox.showerror('RESTAURANT BILLING SYSTEM','Syntax Error')
def exit_func():
    exit()
def res_func():
    global q
    q=0
    txt_reciept.delete('1.0',END)
    qty_entery.delete(0,END)
    cost_entry.delete(0,END)
    total_entry.delete(0,END)
    sgst_entry.delete(0,END)
    cgst_entry.delete(0,END)
    lbl['text'] = 'Qty' + ' : '+'0'
    lbl.update()
def edit_func():
    def add_func():
        conn=connect(host='localhost',database='my_db',user='root',password='tinku123')
        cursor=conn.cursor()
        cursor.execute(f"insert into food_items values({item_id.get()},'{item.get()}','{price.get()}')")
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo('Info','Data Added Successfully')
        item_id.set('')
        item.set('')
        price.set('')
        edit_window.focus()
    def save_func():
        conn=connect(host='localhost',database='my_db',user='root',password='tinku123')
        cursor=conn.cursor()
        cursor.execute(f'update tax set sgst={float(sgst_var.get())},cgst={float(cgst_var.get())}')
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo('Info','Data Modified Successfully')
        edit_window.focus()
    edit_window=Toplevel(root)
    edit_window.focus()

    frame1=Frame(edit_window,bd=10,relief=RIDGE,width=100,height=100)
    frame1.pack(side=TOP)

    frame2=Frame(edit_window,bd=10,relief=RIDGE,width=100,height=100)
    frame2.pack(side=TOP)

    id_label = Label(frame1, text='Item ID:', font=('lithograph', 12, 'bold'), fg='blue')
    id_label.grid(row=0, column=0, sticky=W,padx=10,pady=10)

    item_label = Label(frame1, text='Item Name:', font=('lithograph', 12, 'bold'), fg='blue')
    item_label.grid(row=1, column=0, sticky=W,padx=10,pady=10)

    price_label = Label(frame1, text='Item Price:', font=('lithograph', 12, 'bold'), fg='blue')
    price_label.grid(row=2, column=0, sticky=W,padx=10,pady=10)

    item_id = StringVar()
    id_entry = Entry(frame1, textvariable=item_id, width=30, font=('lithograph', 12, 'bold'))
    id_entry.grid(row=0, column=1,columnspan=3,padx=10,pady=10)

    item = StringVar()
    item_entry = Entry(frame1, textvariable=item, width=30, font=('lithograph', 12, 'bold'))
    item_entry.grid(row=1, column=1,columnspan=3, padx=10, pady=10)

    price = StringVar()
    price_entry = Entry(frame1, textvariable=price, width=30, font=('lithograph', 12, 'bold'))
    price_entry.grid(row=2, column=1,columnspan=3, padx=10, pady=10)

    add_btn = Button(frame1, text='Add Item', bd=5, width=8, font=('lithograph', 12, 'bold'), bg='GreenYellow',command=add_func)
    add_btn.grid(row=3, column=0, padx=20, pady=20)

    modify_btn = Button(frame1, text='Modify Item', bd=5, width=10, font=('lithograph', 12, 'bold'), bg='yellow')
    modify_btn.grid(row=3, column=1, padx=20, pady=20)

    del_btn = Button(frame1, text='Delete Item', bd=5, width=10, font=('lithograph', 12, 'bold'), bg='red')
    del_btn.grid(row=3, column=2, padx=20, pady=20)

    sgst_label = Label(frame2, text='SGST:', font=('lithograph', 12, 'bold'), fg='blue')
    sgst_label.grid(row=0, column=0, sticky=W, padx=10, pady=10)

    cgst_label = Label(frame2, text='CGST:', font=('lithograph', 12, 'bold'), fg='blue')
    cgst_label.grid(row=0, column=2, sticky=W, padx=10, pady=10)

    sgst_var = StringVar()
    sgst_entry = Entry(frame2, textvariable=sgst_var, width=14, font=('lithograph', 12, 'bold'))
    sgst_entry.grid(row=0, column=1, padx=10, pady=10)

    cgst_var= StringVar()
    cgst_entry = Entry(frame2, textvariable=cgst_var, width=13, font=('lithograph', 12, 'bold'))
    cgst_entry.grid(row=0, column=3, padx=12, pady=10)

    save_btn = Button(frame2, text='Save', bd=5, width=8, font=('lithograph', 12, 'bold'), bg='GreenYellow',command=save_func)
    save_btn.grid(row=1, column=3, padx=20, pady=20)

    conn = connect(host='localhost', database='my_db', user='root', password='tinku123')
    cursor = conn.cursor()
    cursor.execute('select * from tax')
    s,c=cursor.fetchone()
    sgst_var.set(s)
    cgst_var.set(c)

def load_func():
    item_listbox.delete(0,END)
    conn=connect(host='localhost',database='my_db',user='root',password='tinku123')
    cursor=conn.cursor()
    data=cursor.execute('select * from food_items')
    for id,item,price in cursor.fetchall():
        item_listbox.insert(END,f'{id}--------------------{item}--------------------{price}')
    item_listbox.bind('<<ListboxSelect>>',on_select)
item_lst=[]
price_lst=[]
qty_lst=[]
items=[]
amt=0
s1=0
c1=0
t=0
def on_select(event):
    global items
    index=item_listbox.curselection()
    data=item_listbox.get(index)
    items=re.split('-{20}',data)
q=0
def add_func():
    global q
    if(qty.get()):
        item_lst.append(items[1])
        price_lst.append(items[2])
        qty_lst.append(qty.get())
        q+=int(qty.get())
        lbl['text']='Qty'+' : '+str(q)
        lbl.update()
        qty.set('')
    else:
        messagebox.showinfo('Info','Please Fill Qty Field')
def total_func():
    global item_lst,price_lst,qty_lst,amt,s1,c1,t
    conn = connect(host='localhost', database='my_db', user='root', password='tinku123')
    cursor = conn.cursor()
    cursor.execute('select * from tax')
    s, c = cursor.fetchone()
    for i in range(len(item_lst)):
        amt+=(float(qty_lst[i]))*(float(price_lst[i]))
    s1=(float(s)*amt)/100
    c1=(float(c)*amt)/100
    t=amt+s1+c1
    cost.set(f'{amt}')
    sgst.set(f'{float(s1)}')
    cgst.set(f'{float(c1)}')
    total.set(f'{t}')

def print_func():
    fs=open('reciept_print1.txt','w')
    global item_lst,price_lst, qty_lst, amt,refrence,s1,c1,t
    conn = connect(host='localhost', database='my_db', user='root', password='tinku123')
    cursor = conn.cursor()
    cursor.execute('select * from tax')
    s, c = cursor.fetchone()
    fs.write('REF NO.\t\t'+f'{refrence}'+'\t'+'DATE:\t'+f'{now.day}/{now.month}/{now.year}\n')
    fs.write('-----------------------------------------\n')
    fs.write('ITEMS\t\tQTY\tRATE\tAMT\n')
    fs.write('-----------------------------------------\n')
    for i in range(len(item_lst)):
        fs.write(f'{item_lst[i]}\t\t\t{qty_lst[i]}\t{price_lst[i]}\t{float(qty_lst[i])*float(price_lst[i])}\n')
    fs.write('SubTotal\t\t\t' + str(amt) + '\n')
    fs.write('SGST\t\t\t' +str(s)+'%' + '\t' + str(s1) + '\n')
    fs.write('CGST\t\t\t' + str(c) + '%' + '\t' + str(c1) + '\n')
    fs.write('GrandTotal\t\t\t' + str(t) + '\n')
    os.startfile('reciept_print1.txt','print')

refrence=0
now=datetime.now()
def reciept_func():
    global item_lst, price_lst, qty_lst, amt,refrence,s1,c1,t
    refrence=randint(10000,99999)
    conn = connect(host='localhost', database='my_db', user='root', password='tinku123')
    cursor = conn.cursor()
    cursor.execute('select * from tax')
    s, c = cursor.fetchone()
    txt_reciept.delete('1.0',END)
    txt_reciept.insert(END,'REF NO.\t\t'+f'{refrence}'+'\t\t'+'DATE:\t'+f'{now.day}/{now.month}/{now.year}')
    txt_reciept.insert(END,'-------------------------------------------------\n')
    txt_reciept.insert(END,'ITEMS\t\t\tQTY\tRATE\tAMOUNT\n')
    txt_reciept.insert(END, '-------------------------------------------------\n')
    for i in range(len(item_lst)):
        txt_reciept.insert(END,f'{item_lst[i]}\t\t\t{qty_lst[i]}\t{price_lst[i]}\t{float(qty_lst[i])*float(price_lst[i])}\n')

    txt_reciept.insert(END, 'SubTotal\t\t\t\t\t' + str(amt) + '\n')
    txt_reciept.insert(END, 'SGST\t\t\t\t' +str(s)+'%' +'\t' + str(s1) + '\n')
    txt_reciept.insert(END, 'CGST\t\t\t\t' +str(c)+'%'+'\t' + str(c1) + '\n')
    txt_reciept.insert(END, 'GrandTotal\t\t\t\t\t' + str(t) + '\n')



# def order_his():
#     def delete_all():
#         Customer.cuslist.clear()
#         fs = open('Cutomer_order_history.txt', 'wb')
#         fs.close()
#         refval.set('')
#         txt_shw.delete('1.0', END)
#         # res_func()
#         messagebox.showinfo('Info','All Customer Deleted')
#         sub.destroy()
#
#     def delete():
#         if(refval.get()!=''):
#
#             for cus in Customer.cuslist:
#                 if (cus.ref == refval.get()):
#                     Customer.cuslist.remove(cus)
#                     fs = open('Cutomer_order_history.txt', 'wb')
#                     pickle.dump(Customer.cuslist,fs)
#                     refval.set('')
#                     txt_shw.delete('1.0', END)
#                     messagebox.showinfo('Info','Customer Deleted successfully')
#                     sub.focus()
#                     return
#             messagebox.showinfo('Info','Customer not found of given Ref No.')
#             sub.focus()
#         else:
#             messagebox.showwarning('Warning','Please Enter Ref No. ')
#             sub.focus()
#
#     def search():
#         if(refval.get()!=''):
#             for cus in Customer.cuslist:
#                 if(cus.ref==refval.get()):
#                     txt_shw.delete('1.0',END)
#                     txt_shw.insert(END,'REF NO.\t\t' + cus.ref + '\t' + 'DATE:\t' + f'{cus.date.day}/{cus.date.month}/{cus.date.year}\n')
#                     txt_shw.insert(END, '-------------------------------------------------------------------\n')
#                     txt_shw.insert(END, 'ITEMS\t\tQTY\tRATE\tAMT\n')
#                     txt_shw.insert(END, '-------------------------------------------------------------------\n')
#                     if (cus.burqty):
#                         txt_shw.insert(END, 'Burger\t\t ' + str(cus.burqty) + '\t' + cus.burger + '\t' + str(
#                             cus.buramt) + '\n')
#                     if (cus.friqty):
#                         txt_shw.insert(END, 'Fries\t\t ' + str(cus.friqty) + '\t' + cus.fries + '\t' + str(
#                             cus.friamt) + '\n')
#                     if (cus.pizzqty):
#                         txt_shw.insert(END, 'Pizza\t\t ' + str(cus.pizzqty) + '\t' + cus.pizza + '\t' + str(
#                             cus.pizzamt) + '\n')
#                     if (cus.cokqty):
#                         txt_shw.insert(END,
#                                            'Coke\t\t ' + str(cus.cokqty) + '\t' + cus.coke + '\t' + str(cus.cokamt) + '\n')
#                     if (cus.iceqty):
#                         txt_shw.insert(END, 'Icecream\t\t ' + str(cus.iceqty) + '\t' + cus.icecream + '\t' + str(
#                             cus.iceamt) + '\n')
#                     if (cus.ecoqty):
#                         txt_shw.insert(END, 'Ecomeal\t\t ' + str(cus.ecoqty) + '\t' + cus.ecomeal + '\t' + str(
#                             cus.ecoamt) + '\n')
#                     if (cus.delqty):
#                         txt_shw.insert(END, 'Deluxemeal\t\t ' + str(cus.delqty) + '\t' + cus.deluxemeal + '\t' + str(
#                             cus.delamt) + '\n')
#                     txt_shw.insert(END, 'SubTotal\t\t\t\t' + str(cus.subttl) + '\n')
#                     txt_shw.insert(END, 'SGST\t\t\t' + str(cus.sgst) + '%' + '\t' + str(cus.sgsttax) + '\n')
#                     txt_shw.insert(END, 'CGST\t\t\t' + str(cus.cgst) + '%' + '\t' + str(cus.cgsttax) + '\n')
#                     txt_shw.insert(END, 'GrandTotal\t\t\t\t' + str(cus.gdttl) + '\n')
#                     return
#             messagebox.showwarning('Warning','No Customer Found of given Ref.')
#             sub.focus()
#         else:
#             messagebox.showwarning('Warning','Please fill Ref No.')
#             sub.focus()
#     sub=Toplevel(root)
#     sub.focus()
#     refval=StringVar()
#     widg_ref=Frame(sub,bd=10,relief=RIDGE,width=500,height=100)
#     widg_ref.pack(side=TOP)
#     shw_dta=Frame(sub)
#     shw_dta.pack(side=TOP)
#
#     txt_shw = Text(shw_dta, font=1, bd=10, bg='white', relief=RIDGE, width=46, height=10)
#     txt_shw.pack(side=TOP)
#
#     lbl_ref=Label(widg_ref,text='Enter Ref. No.',font=1)
#     lbl_ref.grid(row=0,column=0,padx=20,pady=20)
#     ety_ref=Entry(widg_ref,textvariable=refval,width=20,bd=5,font=1)
#     ety_ref.grid(row=0,column=1,columnspan=2,padx=20,pady=20)
#     btn1 =Button(widg_ref,text='Search',width=10,font=1,bg='GreenYellow',bd=5,command=search)
#     btn1.grid(row=1,column=0,padx=20,pady=20)
#     btn2 = Button(widg_ref, text='Delete', width=10, font=1, bg='yellow', bd=5,command=delete)
#     btn2.grid(row=1, column=1, padx=20, pady=20)
#     btn3 = Button(widg_ref, text='Delete All', width=10, font=1, bg='red', bd=5,command=delete_all)
#     btn3.grid(row=1, column=2, padx=20, pady=20)


try:
    th2=Thread(target=autoload1())
    th2.start()
except Exception:
    pass

root=Tk()
root.title('RESTAURANT BILLING SYSTEM')
root.geometry()

#title

title_frame=Frame(root)
title_frame.pack(side=TOP)
title_label=Label(title_frame,text='RESTAURANT BILLING SYSTEM',width=40,font=('arial',50,'bold'),fg='blue',bd=10,relief=RIDGE)
title_label.pack(side=TOP)

#frames

item_frame=Frame(root,bd=10,relief=RIDGE)
item_frame.pack(side=LEFT)

rec_calc_frame=Frame(root,bd=10,relief=RIDGE)
rec_calc_frame.pack(side=RIGHT)

cal_frame=Frame(rec_calc_frame,bd=10,relief=RIDGE)
cal_frame.pack(side=TOP)

rec_btn_frame=Frame(rec_calc_frame,bd=10,relief=RIDGE)
rec_btn_frame.pack(side=BOTTOM)

rec_frame=Frame(rec_calc_frame)
rec_frame.pack(side=BOTTOM)

list_frame=Frame(item_frame,bd=10,relief=RIDGE,width=800,height=400)
list_frame.pack(side=TOP)

output_frame=Frame(item_frame,bd=10,relief=RIDGE,width=800,height=200)
output_frame.pack(side=TOP)

btn_frame=Frame(item_frame,bd=10,relief=RIDGE)
btn_frame.pack(side=TOP)

#labels

qty_label=Label(output_frame,text='Quantity :',font=('lithograph',12,'bold'),fg='blue')
qty_label.grid(row=0,column=0,sticky=W)

cost_label=Label(output_frame,text='Cost of meal:',font=('lithograph',12,'bold'),fg='blue')
cost_label.grid(row=0,column=2,sticky=W)

sgst_label=Label(output_frame,text='SGST:',font=('lithograph',12,'bold'),fg='blue')
sgst_label.grid(row=0,column=4,sticky=W)

cgst_label=Label(output_frame,text='CGST:',font=('lithograph',12,'bold'),fg='blue')
cgst_label.grid(row=0,column=6,sticky=W)

total_label=Label(output_frame,text='Total Cost:',font=('lithograph',12,'bold'),fg='blue')
total_label.grid(row=0,column=8,sticky=W)

lbl=Label(list_frame,text='Qty : 0',font=('lithograph',12,'bold'),fg='blue')
lbl.grid(row=3,column=4,padx=10,pady=10)

# entery
calc=StringVar()
calc_entery=Entry(cal_frame,textvariable=calc,width=41,bd=7,font=('lithograph',12,'bold'),justify='right')
calc_entery.grid(row=0,columnspan=4,padx=5,pady=5)

qty=StringVar()
qty_entery=Entry(output_frame,textvariable=qty,width=5,bd=3,font=('lithograph',12,'bold'),justify='right')
qty_entery.grid(row=0,column=1,padx=5,pady=5)

cost=StringVar()
cost_entry=Entry(output_frame,textvariable=cost,width=9,bd=3,justify='right',font=('lithograph',12,'bold'))
cost_entry.grid(row=0,column=3,padx=5,pady=5)

sgst=StringVar()
sgst_entry=Entry(output_frame,textvariable=sgst,width=6,bd=3,justify='right',font=('lithograph',12,'bold'))
sgst_entry.grid(row=0,column=5,padx=5,pady=5)

cgst=StringVar()
cgst_entry=Entry(output_frame,textvariable=cgst,width=6,bd=3,justify='right',font=('lithograph',12,'bold'))
cgst_entry.grid(row=0,column=7,padx=5,pady=5)

total=StringVar()
total_entry=Entry(output_frame,textvariable=total,width=9,bd=3,justify='right',font=('lithograph',12,'bold'))
total_entry.grid(row=0,column=9,padx=6,pady=5)


#listbox
item_listbox=Listbox(list_frame,width=37,height=9,bg='white',font=('arial black',18,'bold'),selectmode=SINGLE,activestyle='none')
item_listbox.grid(row=0,column=0,columnspan=3,rowspan=4,padx=18,pady=18)

# buttons

item_btn=Button(list_frame,text='Edit Item',bd=10,width=8,font=('lithograph',18,'bold'),bg='red',command=edit_func)
item_btn.grid(row=1,column=4,padx=10,pady=10)

refresh_btn=Button(list_frame,text='Refresh',bd=10,width=8,font=('lithograph',18,'bold'),bg='GreenYellow',command=load_func)
refresh_btn.grid(row=2,column=4,padx=10,pady=10)

load_btn=Button(list_frame,text='Load Item',bd=10,width=8,font=('lithograph',18,'bold'),bg='yellow',command=load_func)
load_btn.grid(row=0,column=4,padx=10,pady=10)

total_btn=Button(btn_frame,text='TOTAL',bd=10,width=11,font=('lithograph',18,'bold'),bg='GreenYellow',command=total_func)
total_btn.grid(row=0,column=1,padx=10,pady=14)

add_btn=Button(btn_frame,text='ADD',bd=10,width=10,font=('lithograph',18,'bold'),bg='orange',command=add_func)
add_btn.grid(row=0,column=0,padx=10,pady=10)

reset_btn=Button(btn_frame,text='RESET',bd=10,width=10,font=('lithograph',18,'bold'),bg='yellow',command=res_func)
reset_btn.grid(row=0,column=3,padx=10,pady=10)

exit_btn=Button(btn_frame,text='EXIT',bd=10,width=10,font=('lithograph',18,'bold'),bg='red',command=exit_func)
exit_btn.grid(row=0,column=4,padx=10,pady=10)

reci_btn=Button(rec_btn_frame,text='RECIEPT',width=15,font=('lithograph',10,'bold'),bg='GreenYellow',command=reciept_func)
reci_btn.grid(row=0,column=0,padx=3)

print_btn=Button(rec_btn_frame,text='PRINT',width=15,font=('lithograph',10,'bold'),bg='red',command=print_func)
print_btn.grid(row=0,column=1)

ord_btn=Button(rec_btn_frame,text='ORDER HIS.',width=15,font=('lithograph',10,'bold'),bg='yellow')
ord_btn.grid(row=0,column=2,padx=3)

btnlist=['7','8','9','+','4','5','6','-','1','2','3','x','0','C','=','/']
commandlist=[lambda :btnclick(7),lambda :btnclick(8),lambda :btnclick(9),lambda :btnclick('+'),
             lambda :btnclick(4),lambda :btnclick(5),lambda :btnclick(6),lambda :btnclick('-'),
             lambda :btnclick(1),lambda :btnclick(2),lambda :btnclick(3),lambda :btnclick('*'),
             lambda :btnclick(0),reset_func,eval_func,lambda :btnclick('/'),]
count=0
for i in range(1,5):
    for j in range(4):
        calc_btn=Button(cal_frame,text=btnlist[count],bd=7,width=10,height=1,font=('lithograph',10,'bold'),command=commandlist[count])
        calc_btn.grid(row=i,column=j)
        count+=1

#textwidget

txt_reciept=Text(rec_frame,bg='white',bd=10,relief=RIDGE)
txt_reciept.pack(side=BOTTOM)

root.mainloop()
