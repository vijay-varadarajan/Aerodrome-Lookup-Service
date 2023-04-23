from tabulate import tabulate

list = [['Name','ID'],["Himanshu",1123], ["Rohit",1126], ["Sha",111178]]
print(tabulate(list[1:], headers=list[0], tablefmt="rounded_outline"))