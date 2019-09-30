import random;

# OSI 7 Layer Model class Structure

class OSI:
    # Generator
    def __init__(self, userName):
        # ipAddress is IPv4 version, generated randomly every time generated OSI class
        self.ipAddress = f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}";
        self.userName = userName;

    # Modulating and Demodulate methods in DataLinkLayer(level2) to PresentationLayer(level6)
    # MoDem method Simply attach or detach some string excepting NetworkLayer
    # Look Methods below
    def DataLinkLayerModulate(self, data):
        data = data + "datalink";
        return data;
    # NetworkLayer have to operate confirming receiver's IP_address so when modulate, put receiver's IP_address
    # then this Layer attach the address to data [This is NetworkLayer's header]
    def NetworkLayerModulate(self, data, receiverAddress):
        data = data + receiverAddress;
        return data;

    def TransportLayerModulate(self, data):
        data = data + "transport";
        return data;

    def SessionLayerModulate(self, data):
        data = data + "session";
        return data;

    def PresentationLayerModulate(self, data):
        data = data + "presentation";
        return data;

    def ApplicationLayerModulate(self, data):
        data += "application";
        return data;

    def DataLinkLayerDemodulate(self, data):
        data = data.replace("datalink", "");
        return data;

    def NetworkLayerDemodulate(self, data, receiverAddress):
        data = data.replace(receiverAddress, "");
        return data;

    def TransportLayerDemodulate(self, data):
        data = data.replace("transport", "");
        return data;

    def SessionLayerDemodulate(self, data):
        data = data.replace("session", "");
        return data;

    def PresentationLayerDemodulate(self, data):
        data = data.replace("presentation", "");
        return data;

    # If receive message, printing the Sender & Receiver's information and message content for Applicate method
    def Applicate(self, sender, data):
        # Demodulate data for ApplicationLayer header
        data = data.replace("application", "");
        print(f"ReceiverIP : {self.ipAddress}\nReceiverName : {self.userName}\nMessage : {data}\n");
        print(f"SenderIP : {sender.ipAddress}\nSenderName : {sender.userName}");

    # the sendMessage() method executed,
    # sending content is modulated through PresentationLayer(level6) to DataLinkLayer(level2)
    def sendMessage(self, content, receiverAddress, Groups):
        content = self.PresentationLayerModulate(content);
        content = self.SessionLayerModulate(content);
        content = self.TransportLayerModulate(content);
        content = self.NetworkLayerModulate(content, receiverAddress);
        content = self.DataLinkLayerModulate(content);
        # and PhysicalLayer(level1) send the modulated data to Groups(OSIs list[people_1, people_2,..., Kate, Bill])
        self.move(content, receiverAddress, Groups);

    # move() method have PhysicalLayer(level1)'s roll [move through OSI Group]
    def move(self, content, receiverAddress, OSIs):
        # Sended message move through OSIs in Group (PhysicalLayer[level1])
        for OSI in OSIs:
            # DataLinkLayer(level2) demodulate the message
            content = OSI.DataLinkLayerDemodulate(content);
            # In NetworkLayer(level3), confirm OSI's IP_address whether that is equal to receiver's IP_address
            if OSI.ipAddress == receiverAddress:
                # if find the receiver, the message move to TransportLayer(level4) and go through HighLevel Demodulators
                content = OSI.NetworkLayerDemodulate(content, receiverAddress);
                content = OSI.TransportLayerDemodulate(content);
                content = OSI.SessionLayerDemodulate(content);
                content = OSI.PresentationLayerDemodulate(content);
                # Now, the content is completely demodulated
                # Receiver execute the application, can see the message
                OSI.Applicate(self, content);
            else:
                # if IP_address is not equal to receiver's IP_address, return to DataLinkLayer(level2)
                # At returning, repeat modulate
                content = OSI.DataLinkLayerModulate(content);