# ------Gen Ai Final Decision Will put thye max hard work to learn Gen AI 
# Ex------

# flavours=["ginger","Out of Stack","Lemon","Discontinued","Tulsi"]

# for flavor in flavours:
#     if flavor=="out of stock":
#         continue
#     if flavor=="Discontinued":
#         break
#     print(f"{flavor} itrm found")
# print("Out side of loop")    

# --------------------------------------------

# for num in range(1, 6):
#     if num == 3:
#         continue  # This skips the print statement for 3
#     print(f"Current number: {num}")

# output:
# Current number: 1
# Current number: 2
# Current number: 4
# Current number: 5

# ----------------------------------------------------------

# staff=[("Amit",18),("Zara",17),("Raj",15)]    #Tupples inside lists[]
# for name , age in staff:
#     if age >16:
#         print(f"They are {name}")


# -------------------------------------------------------------------

# Walrus =====--- :=
# x=5 is a statement an expresion returns a value eg 3+3

# ----------------------------------------------------------------------------
# Base-----

# val=13
# remainder =val%5    #

# if remainder:    #remainder 0 if then no output condition fails
#     print(f"Not divisible, remainder is {remainder}")



# Using Walrus----------------------
# if (remainder:=val%5):  #walrus assigns the next part to the first and checks the condition
#     print(f"Not divisible,remainder is:{remainder}")


# Avail_sizes=["small","medium","large"]

# WE can Directly asiign the variable value to be checked

# ex

# if(req_size:= input("Enter ur choice :")) in Avail_sizes:
#     print(f"Serving :{req_size} chai")
# else:
#     print(f"Size is unavailable :-{req_size}")


# flavors=["masala","ginger","lemon","mint"]
# print("Available flavour:",flavors)
# while (flavor :=input("Choose ur flavor :")) not in flavors:
#     print(f"Sorry,{flavor} is not available")
# print (f"You choose {flavor} chai")    




# Using Dictionaries Instead of repeated cases
# ----------------------------------------------------
# users = [ 
#     {"id":1,"total": 100,"coupon":"P20"},
#     {"id":2,"total": 150,"coupon":"F20"},
#     {"id":3,"total": 200,"coupon":"P50"},
# ],

# discounts={
#     "P20": (0.2,0),
#     "F10": (0.5,0),
#     "P50": (0,10)
# }


# for user in users:
#     percent,fixed = discounts.get(user["coupon"],(0,0))
#     discount = user["total"]*percent*fixed
#     print(f"{user["id"]} paid {user["total"]} and got discount for next visit of rupees {discount}")