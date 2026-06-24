print("\n\n================================================================================================\nHello  Welcome to Income Tax Portal\n================================================================================================")
txinc=int(input("Enter ur taxable income :"))

if txinc<1200000:
    print("\nTax is Nil")
elif txinc>=1200000 and txinc<2000000:
    tax=txinc*0.15
    print(f"\n Your Tax is : {tax}")    
elif txinc>=2000000 and txinc<5000000:   
    tax=txinc*0.20    
    print(f"\n Your Tax is : {tax}")   
else:
    tax=txinc*0.30
    print(f"\n Your Tax is : {tax}")   
    

