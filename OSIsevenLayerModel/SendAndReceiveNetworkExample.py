from OSImodel import OSI;

# Generate a thousand of OSI classes and appending OSIs list
# The OSIs' name is people_1 ~ people_1000
OSIs = [OSI(f"people_{i}") for i in range(1, 1001)];

# Generate OSI classes named Kate, Bill (Sender & Receiver)
Kate = OSI("Kate");
Bill = OSI("Bill");

# Put Kate and Bill in OSIs list
OSIs.append(Kate);
OSIs.append(Bill);

# Confirm the process operate well
for OSI in OSIs:
    print(OSI.userName, OSI.ipAddress);
print("\n");

# Kate send a message the content is "Hello Bill" to Bill
Kate.sendMessage("Hello Bill", Bill.ipAddress, OSIs);