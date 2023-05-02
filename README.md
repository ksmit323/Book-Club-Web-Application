# Boys Book Club
## Video Demo:  <https://youtu.be/GZ6LOvSxoX8>
## Description:

### Project Summary

My Final project is a website for a book club that my friends and I organized.  The name of our book club is Boys Book Club as right now it is just a "guy" thing that we do to spend time together.  However, we are fairly disorganized, we struggle to choose a book to read and we spend a lot of time in limbo just trying to get every one on the same page (pun intended).  Therefore, it was an easy choice for me to design a website as my final project to help create a more structured setting to our book club.  While the website itself is very generic and basic with not a lot of bells and whistles, it will allow users to sign up, make suggestions, create a table to view everyone's choices, vote on which book we would like to read and render the results of that vote.  

I intentionally kept the design to a minimum as I want the website to be focused on functionality and less on appearance. This website aims to minimize all the struggles we have wasting time to get everyone to agree on a book.

### Logging in or Registering

My goal for the final project is to make our book club a more enjoyable experience through this website interface.  So how does it work?  The website starts out prompting the user to login or register.  If the user is already registered, they will be prompt for a username and password.  Otherwise, they will need to register.  They can do so by inputting a username and a password.  The password will need to be entered again to verify correctness.  

The backend coding will automatically check if the user's chosen username is available.  If so, and the passwords match, the user will be logged in and taken to the homepage.  If the user has successfully regisetered, they will be redirected to the homepage with a FLASH message, verifying a successful registration.

### Homepage

Now that the user is logged in, they will arrive at the homepage.  The homepage itself is not interactive in anyway but simply gives a brief summary of what the website is designed for.  From the homepage the user can access all the tools available on the website by clicking one of the webpage buttons at the top of the screen.  The user will see that the homepage consists of six different buttons they will be allowed to cycle through on the website.  

The six buttons are "Make Your Suggestions", "Change Your Suggestions", "Everyone's Recommendations", "Vote for your books", "Voting Results" and "Log Out".  Each button has its own unique features that will allow the user to interact with the website.  Let's go through each buttom and find out what they do and why they are designed the way they are.

**Design Considerations**:
By far the most important design consideration for the whole website is how the buttons at the top are laid out.  I want the user to experience a natural process of going left to right in a seemless transition of making a book suggestion, viewing other users' choices, submitting their votes and viewing the voting results.  Therefore, the buttons are laid out in such a way that the user will go step by step from left to right before coming to the end of the tools they need to successfully choose a book, vote on a book and see the results of the election.

### Making a Book Suggestion

First, I would like to say that I designed the buttons to "read" from left to right based on the steps the user should take to sucessfully vote.  For example, the first step the user must do is suggest a book.  Therefore, the first button to the far left is "Make Your Suggestions", a webpage where the user will submit their suggestions.  So, we will start here.  Once the user clicks on the "Make Your Suggestions" webpage, they will be prompted for three text boxes.  The first is the user's name.  This will be important when the table is rendered to view everyone's suggetions.  The next two text boxes are for the user's book suggestions.  Each user is allowed to suggest two books.  They are NOT required to suggest two books, however.  Each text box is designed to be customizable in size so that the user may increase the size of the text box just in case the book title is really long and they would like to see everything they typed all at a once.

**Design Considerations:**
I only want a user to have two suggestions.  Anymore and I thought that would be too inundating.  Also, I had to consider ways the user may erroneously input suggestions.  The website will not allow the user to input the same suggestion for both choices.  Also, very important to note, that the user will NOT be able to go back into this page once they have made their suggestions.  They will no longer have access to this page once they submit.  However, they will be allowed to change their suggestions on a different part of the website.  If the user tries to access this page after making a suggestion, they will be returned to the home page with a FLASH message explaining their error.

### Change Your Suggestions

Following along to the next part of the website, the user may change their mind about what books they want.  Here, the user will be allowed to change one or both of their recommendations.  They can do so as many times as they like until the voting commences.  The text box here is also customizable in shape to accomodate any large book titles.  

However, the user must make a suggestions first before they can change their suggestions.  If the user erroneously decides to click on this webpage before making any suggestions, they will be redirected to the homepage with a FLASH message explaining the error.

**Design Considerations:**
It's important to note that the user can change their first or their second suggestion.  They will have the option to interchange one or the other and all the relevant information for rendering purposes will update automatically to accomodate the reader's fickled choices.  Also, the user will be redirected to a APOLOGY page if they erroneously use this tool.  The user must insert at least one suggestion to prevent an error and of course as stated before, they must have already made a suggestion to prevent another error.

### Everyone's Recommendations

Once the user succesfully records their suggestions, they will hopefully be intrigued to see what other users have suggested.  If so, they can view everyone's recommendations on this page.  Once the user clicks this button, they will be directed to a page that will display a table with all the suggestions made so far includig who made the suggestions.  Even if the user changes their suggestions, it will update automatically if they return back to this page.

**Design Considerations:**
The most important consideration here was that there was plenty of space in each row just in case the book titles were super long.  I wanted to be sure they would fit nicely enough and still be readable.  Therefore, the table consumes the majority of the width of the page.

### Vote For Your Books

Now that the user has made their suggestions and viewed all those who have suggested thus far, they can continue on to the next tool, which is to vote on the book or books they would like the club to read.  Here, the user will have the option to make up to three suggestions of which books they would prefer. Here are some VERY important considerations.  One, the user CANNOT vote on their own book suggestions.  In fact the webpage will not even allow that option.  Each input box is a dropdown menu of all the books the user can choose with the exception of their own recommendations.  Two, the user can choose three suggestions but they do not have to.  They can also choose the same book twice if they really want to despite that may leading to a wasted vote. Once the user has voted, they CANNOT change their vote unless contacting the administrator (me!).  This is a very intentional design characteristic.

**Design Considerations:**
I decided that the user can choose up to three books because of the voting system I have implemented.  This will be discussed further in the next section of this README file.  Otherwise, the most important design decision was NOT to allow the voter to change their votes.  The whole point of this website is to expedite a grueling process of everyone agreeing on a book.  Therefore, the votes are final in an effort to push this process along quicker.  Lastly, the user must input a suggestion or else they will be redirected to the APOLOGY page explaining their error.

### Voting Results

Once all the registered users have voted, the logged in user may click this button to review the final election results.  However, if the user tries to view this page before all the registered users have voted, they will be redirected to the homepage with a FLASH message explaining the error.  

The voting system is entirely based on the **"runoff" election policy**.  I wrote the code in a separate Python file to be imported as a function to print a winner. However, if there is a tie, then the user will be informed that there was a tie and there is no winner.  At this point, our members have decided to select one of the tied books at random to be chosen as the winner.

**Design Considerations:**
I chose to do a "runoff" style election for two really specific reasons.  First, I truly wanted to stay away from a pluarilty vote.  Although this would have been MUCH simpler to code, I don't believe the plurality vote would be truly indicative of the group's voting choices.  For example, if a book won by only one vote, yet the second place book might have been preferably by the majority of the group, then we chose a book that doesn' reflect the most of what we all wanted.  Therefore, I wanted an election policy that would emcompass more of the majority.  Tideman already gave me horrible indigestion once so I stuck with Runoff to accomplish this.  The second reason is that I wanted my users to be allowed to vote for more than one book as I personally know it can be extremely challenging to choose just one book.  I wanted the user to have a more satisfying experience of voting for multiple books instead of being forced to choose one.

### Miscellaeneous

Other design choices included various pictures and a tagline throughout the website to lighten the mood and keep a sense of humor about the experience going.  Also, the user may quickly notice that there is an APOLOGY page that will be redirected to if the user continuously mistreats the webpages.  There are quite a few instances where this can happen so it was important for me to try and catch as many accidental or intentional misuses of the website as I could.

