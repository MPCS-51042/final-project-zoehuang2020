# Proposals
My ideas for my final project are...

1. I would like to build a tool for Booth MBA students to optimize their bidding strategy based on their choice of concentration and past bidding points history. For each course, we use past years’ bidding points to predict the current year bidding point by fitting a simple least square model using the Scipy package. The tool only has one required input - the user’s choice of MBA concentrations. If the list of concentrations can not be completed in 2 years, the tool will return a text that says “Sorry, you won't be able to graduate with concentration x,y and z”. Otherwise, the tool will print out a course schedule and bidding points suggestion for each course. The graduation requirements can be found here. Past bidding points can be found on IBid.

To do: 
Proof of concept on the integration with iBid, or if that doesn’t work, implement a way for people to enter their past bids/courses.
Proof of concept either on scraping the graduation requirements, or if that doesn’t work, manually put them in some kind of data model to pull from in your code. 
Figure out how you want someone to interact with it. GUI? Command line? 
Get your model working. This might take some time if you’re new to scipy.
Test it on a few different student schedules/bid attempts and make sure all your cases are covered


Project Plan:
1. By week 4, gather IBid data,graduation requirements and lists of courses required for each concentration
2. By week 5, build the model to predict bidding points based on past bidding history. Maybe also some visulizations to show the trend?
3. By week 7, build the tool to print out course planning and bidding history
4. By week 8, have the UI ready
5. By week 9, bug fixing 
