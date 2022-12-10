# A VoIP-based Call Center/PBX using the Asterisk communications center
The system acts mainly as a call centre to connect external callers with agents. 
First, the caller has to call the company numbe. 
Then the customer is given the option to choose which language he/she wants to communicate with either Arabic, English, or French. 
After the customer enters the number corresponding to the language he/she wishes to speak in, the server directs the caller to one of the available agents.
![image](https://user-images.githubusercontent.com/90156505/206863756-afc4aa54-325a-4ce9-9b62-1fe009d43998.png)

## Configuration and Coding
There are a number of files that are edited or created to implement the Asterisk server functionality of the Call Center and the PBX. 
This section is a detailed overview of the system files and how they interact with each other. 

###sip.conf
The (sip.conf) file is used to create and identify users of the system.
![image](https://user-images.githubusercontent.com/90156505/206863943-e14e6d17-f4da-410f-9d63-592b7f0d8e2e.png)
Figure: example Agent 1 from Arabic Queue declaration in the sip.conf file

Each user in the (sip.conf) has a type. The three main types are peer, user, and friend. A peer type can only receive calls, whereas a user type can only make calls. 
Friend type can make and receive calls, which is why all users defined in the project are of type friend. 
Context defines the user's interactions on the Asterisk server, and all contexts are defined in the (extensions.conf) file. 
Secret defines the password for the user to log onto the Asterisk server. If the user host is defined as dynamic, then the user has a dynamic IP. 
Each time the user logs onto the server, they can have a different IP. 
The fields (disallow) and (allow) have to do with the voice codecs and are configured the same for all users. 
The (mailbox) field defines the mailbox for the user, using a number and the voicemail context, and this is further elaborated in the (voicemail.conf) file.

###voicemail.conf
![image](https://user-images.githubusercontent.com/90156505/206863996-31d65f96-923e-4c40-92bb-3ee1d2a100f3.png)
Figure: Voicemail boxes defines in the voicemail.conf file for the Agents in the Arabic Queue

The [VoiceMail] box in the (voicemail.conf) file specifies which voicemail goes where. 
In the (sip.conf) file, each user was assigned to a specific voicemail box in the [VoiceMail] context. 
In the (extensions.conf) file, each context defines the interactions and permissions of the users of that context, and each user is assigned a voicemail box if they do not answer the phone in time. 

###extensions.conf
The (extensions.conf) file is the longest and most important file in this Asterisk Server call center and PBX project. The file defines the system behavior and the allowed interactions between system users. It is also used to define numbers to the users and to the call center. 
![image](https://user-images.githubusercontent.com/90156505/206864041-43ac622d-ae31-4be7-862c-74343f2bf5ea.png)
Figure: The [incoming context]

If an outside user registered on the server calls (0777), which is the number of the call center, they will be diverted to an Interactive Voice Response script (IVR), defined in the file as [ivr-1].
![image](https://user-images.githubusercontent.com/90156505/206864064-5fcaa1a7-6814-49a5-87a7-0ebb15d85d17.png)
Figure: the [ivr-1] lets user choose the language

In the IVR, (Background) application is used to play a welcome message to the customer and asking them to choose the language of their preference by entering (1, 2, 3) on the dial keypad. The application (Background) also listens to the user input and will stop the message once the customer has entered a number.  The application (Waitexten) gives the customer 10 seconds to enter a number and choose the language before timing-out and terminating the call. The customer will be directed to the queue based on their choice using the application (Goto). 
![image](https://user-images.githubusercontent.com/90156505/206864091-dbca68bf-18c9-43a7-b937-ac83cee9db1c.png)
Figure: The Arabic Agents queue

If the customer chooses to proceed to the Arabic queue for example, the (Playback) application is used to play a message to the customer notifying them that the call is recorded for quality purposes. All sounds are stored at “/var/lib/asterisk/sounds/en”. The application (Set) is used to take the caller ID as a global variable to use it later in other applications. To record customer calls, applications (Monitor) and (MixMonitor) can be used. The application (MixMonitor) was used to record the sound at the customer end and agent end in the same (.wav) file. All recordings using the (MixMonitor) application can be found in “/var/spool/asterisk/monitor”. The (Queue) application is used to divert the call to a queue that is defined in the file (queues.conf), after which the call is diverted to an agent based on the availability and the queuing strategy defined in the file. 
![image](https://user-images.githubusercontent.com/90156505/206864128-f96c1305-4e91-4c96-be43-9e65be849d42.png)
Figure: code will go to [OutAr] if call not answered and to [callbackAR] if call is answered 

If an agent does not pick up the call in 10 seconds, the customer has the option to leave their number and alternative number through the [OutAR] context, or [OutEn] or [OutFR] depending on the language. For example, in the [OutAR] context, a message will be played back at the customer to ask them to enter their number to be called back later. Application (Read) is used to take a 4-digit number from the customer and application (SayDigits) is used to say the digits to the customer to confirm. A confirmation message is played back to the customer and the application (Read) records their response in the variable (Confirm). If (Confirm = 1) then the server proceeds to ask the customer about their alternative number. If (Confirm = 2) then the server loops back to ask them for their number. 
![image](https://user-images.githubusercontent.com/90156505/206864153-b0115ecd-8981-4f7f-a0ff-0c39ee1d5da5.png)
Figure: the [OutAr] context defines what happens when Arabic Agents don’t pick the call

After the customer has confirmed their main and alternative numbers, a message is played back to the customer telling them that an agent will call them as soon as possible. The numbers, along with the caller ID, will be saved using the application (System) in the “etc/asterisk/Queue.csv” file. Agents can access the file easily using the GUI to call back the customers. In case an agent from the queue picked the call, the server will not go to [OutAR] to ask the customer for their number, instead, it will go to [callbackAR] to call the customer later and ask them for feedback. First, the context will run the (callbackAR) script at “/etc/asterisk”. Application (Set) is used to store the time of the call in a variable (x) with the format (YYYYMMDDHHMinMin), with (HH) being the hours and (MinMin) being the minutes. ![image](https://user-images.githubusercontent.com/90156505/206864173-383f3317-568f-4354-a2bd-3485c2ed961b.png)
Figure: the [callbackAR] is used to call back a customer and ask them about their feedback

The variable (z) will store the time of the call back which can be configured by changing the time between the call and callback (y). A callback file is created and moved to “/var/spool/asterisk/outgoing/” and then the call is terminated. The callback file will call back the customer after the specified time has elapsed. The callback process is automated to save agents time using recorded sounds and taking ratings from the customer based on their last interaction with the call centre. All ratings are recorded in “/etc/asterisk/Complaint.csv” and can be accessed by the GUI. If the customer rating is less than (5/10), the customer is offered the option to leave a message. All customer messages from the callback are recorded in the voicemail box (600@VoiceMail) and can be accessed by quality employees who are registered on the server as [Complaints]. Everyone who works in the company can leave a voicemail to another employee if they have access to call them. Voicemail of each member is defined in the (sip.conf) file, but access to the main voicemail service is defined in each context in the (extensions.conf) file. All contexts have the following line: (( exten => 2000,1,VoiceMailMain(@VoiceMail) )) 
This enables members of the Agent, Manager, and CEO contexts, for example, to access and listen to the voicemail they received by dialing (2000) and typing their voicemail ID and secret number.

###features.conf
This file defines how to transfer and record calls when given the permission to do so.
![image](https://user-images.githubusercontent.com/90156505/206864217-77d15ecc-7206-409b-8ee1-50f42ea49d7d.png)
Internal calls inside the company can be recorded if the caller party or the called party initiates the (automixmon) feature by dialing (*1). The (feature.conf) file also defines the dial key to transfer a call from a customer within the company. Transfers can be attended or blind, although it is advised to only transfer the call actively after making sure the party receiving the transfer is on the line for the customer satisfaction. Agent can dial (*2) followed by the number of the callee receiving the transferred call. This will put the customer on hold and call the party receiving the transfer. When the receiving party picks up and the agent hangs up, the call is transferred to be between the customer and the party receiving the transfer.  

###queue.conf
The (queue.conf) file is where the queues are defined. The queues are accessed using the (extensions.conf) file based on the customer's language choice. Every queue has a call distribution strategy which is set to (random) for all available agents. Other strategies exist like (ringall) and (rrmemory), but random is a good strategy for call centre management. Timeout defines the number of seconds before the customer is diverted out from the queue to leave their number and be called back later by an agent.   
![image](https://user-images.githubusercontent.com/90156505/206864303-bbc9c99c-5d9b-4f36-98db-8289190f3301.png)
Figure: the English Agent Queue defined with a random distribution strategy and a 10s timeout


##Graphical User Interface (GUI)
For the GUI of the project, the Python Tkinter GUI toolkit was used. Two main functionalities exist in the GUI, which are adding agents and searching for log files.
![image](https://user-images.githubusercontent.com/90156505/206864334-9de6cfe8-20a6-44b1-ac36-806e9ac479a7.png)
When adding agents manually, without the use of GUI, someone must add the agent as a new user in the (sip.conf) file and define the type and the context as agent. In addition, the (extensions.conf) file should be updated to add the new agent in the context of all other members of the call center company to allow them to call the new agent. Finally, the new agent should be added to a queue in the (queue.conf) file to receive calls from customers. If all this work is done manually, it introduces the risk of damaging the server files. The GUI (Add Agent) tab takes the name of the agent,  type, queue, secret number, mailbox, and extension and adds them automatically to the (sip.conf), (extensions.conf), and (queue.conf) files. This reduces the risk of damaging the files and makes the process easier and faster. 
![image](https://user-images.githubusercontent.com/90156505/206864346-5961e2aa-1922-4eee-9d10-b3fba5108c23.png)
Figure: the code to add new agent to the (sip.conf) file

After the GUI user enter the fields, the function open() is used to open the (sip.conf) file and add text to it to add the new agent.![image](https://user-images.githubusercontent.com/90156505/206864366-a12cabb9-d0ed-4a09-a4a4-07d1dea6622b.png)
Figure: the code to add the new agent to all other contexts

The code to add a new agent to all other contexts in the (extensions.conf) file uses the function (data.replace) to find the context in the document and add the new user in it. The same technique is used to add the agent in the (queue.conf) file. 
![image](https://user-images.githubusercontent.com/90156505/206864397-1f7bd466-b0e3-419a-8d28-3740a3eecc65.png)
Searching for the logs manually is a tedious task, especially for someone unfamiliar with the system. In order to make using the server more efficient and user friendly, we made a tab (Logs) that can instantaneously access the call log, complaints log, and the queue log. The call log is where all calls are recorded with the date and the ID of the caller and called parties. The complaints log is where customers ratings are recorded after the call back routine. The queue log is where the customers leave their main and alternative numbers to be called back later by agents, in case an agent did not pick up the call in 10 seconds. In the GUI, we define three buttons, each button is linked to its specified log. Once the button is clicked, it initiates the log to open on the operating system itself, not within the python script IDE. Further improvements to the GUI could be made to increase server usability. For example, the GUI could remove any member from the company and add members with all types and not just of type agent. 

![image](https://user-images.githubusercontent.com/90156505/206864420-d02ebf1e-5cd4-4669-b6a3-5d3b4a059aba.png)
Figure: code to configure buttons in the (Logs) tab in the GUI
