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

    # Physical Layer Transform Datas to Binary Signals
    # Transform character to ASCII Code int, (Not using)
    def TransformToElectronicSignal(self, char):
        #if char == " ": return 32;
        #if char == "!": return 33;
        #if char == "\"": return 34;
        #if char == "#": return 35;
        #if char == "$": return 36;
        #if char == "%": return 37;
        #if char == "&": return 38;
        #if char == "\'": return 39;
        #if char == "(": return 40;
        #if char == ")": return 41;
        #if char == "*": return 42;
        #if char == "+": return 43;
        #if char == ",": return 44;
        #if char == "-": return 45;
        #if char == ".": return 46;
        #if char == "/": return 37;
        #if char.isdigit(): return int(char) + 48;
        #if char == ":": return 58;
        #if char == ";": return 59;
        #if char == "<": return 60;
        #if char == "=": return 61;
        #if char == ">": return 62;
        #if char == "?": return 63;
        #if char == "@": return 64;
        #if char == "A": return 65;
        #........skip..........
        #if char == "~": return 126;
        return ord(char); # ord() method transform char to ASCII int

    # Int to Binary String method (Not using)
    def binaryTransform(self, integer):
        return "{0:b}".format(integer);

    def PhysicalLayerDemodulate(self, signals):
        data = "";
        for signal in signals:
            data += chr(int(signal, 2));
        return data;

    def PhysicalLayerModulate(self, data):
        signals = [];
        for char in data:
            signals.append("{0:b}".format((ord(char))));
        return signals;

    # the sendMessage() method executed,
    # sending content is modulated through PresentationLayer(level6) to DataLinkLayer(level2)
    def sendMessage(self, content, receiverAddress, Groups):
        content = self.ApplicationLayerModulate(content);
        content = self.PresentationLayerModulate(content);
        content = self.SessionLayerModulate(content);
        content = self.TransportLayerModulate(content);
        content = self.NetworkLayerModulate(content, receiverAddress);
        content = self.DataLinkLayerModulate(content);
        # In Physical Layer, Data is changed to Binary Signal
        signals = self.PhysicalLayerModulate(content);
        # and PhysicalLayer(level1) send the modulated signals to Groups(OSIs list[people_1, people_2,..., Kate, Bill])
        self.move(signals, Groups);

    # move() method have PhysicalLayer(level1)'s roll [move through OSI Group]
    def move(self, signals, OSIs):
        # Sended message move through OSIs in Group (PhysicalLayer[level1])
        for OSI in OSIs:
            # Sended signals are demodulated in Physical Layer
            content = self.PhysicalLayerDemodulate(signals);
            # contentShow is used to confirm finally
            contentShow = self.PhysicalLayerDemodulate(signals);
            # DataLinkLayer(level2) demodulate the message
            content = OSI.DataLinkLayerDemodulate(content);
            # In NetworkLayer(level3), confirm OSI's IP_address whether that is equal to receiver's IP_address
            if OSI.ipAddress in content[-15:]:
                print(f"Sended Signals in Physical Layer : {''.join(signals)}");
                print(f"BinarySignal to String(Demodulated Data only Physical Layer) : {contentShow}\n");
                receiverAddress = OSI.ipAddress;
                # if find the receiver, the message move to TransportLayer(level4) and go through HighLevel Demodulators
                # In medium, print() is confirming medium demodulated data
                print(f"Demodulated Data in DataLink Layer : {content}");
                content = OSI.NetworkLayerDemodulate(content, receiverAddress);
                print(f"Demodulated Data in Network Layer : {content}");
                content = OSI.TransportLayerDemodulate(content);
                print(f"Demodulated Data in Transport Layer : {content}");
                content = OSI.SessionLayerDemodulate(content);
                print(f"Demodulated Data in Session Layer : {content}");
                content = OSI.PresentationLayerDemodulate(content);
                print(f"Demodulated Data in Presentation Layer : {content}\n");
                # Now, the content is completely demodulated except Application Layer Demodulating
                # Receiver execute the application, can see the message
                OSI.Applicate(self, content);
            else:
                # if IP_address is not equal to receiver's IP_address, return to DataLinkLayer(level2)
                # At returning, repeat modulate
                content = OSI.DataLinkLayerModulate(content);