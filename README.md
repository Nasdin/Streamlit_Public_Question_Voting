# Streamlit Real-Time Question voting dashboard

Hosted Link - https://share.streamlit.io/nasdin/streamlit_public_question_voting/main/anonymous_questions.py

Streamlit is usually thought of a static dashboard without any intercommunication capabilities.

Data provided is also seen as immutable i.e New data onto a chart is added as new rows or new lines to the app.
However with a few simple tricks, we are able to modify a page in real-time when new data enters without the users having to restart or reload the streamlit page.


## This proof of concept demonstrates that you can use Streamlit to:

1. Communicate across other sessions accessing the same streamlit website via posting a question
2. Upvote questions made by others or yourself
3. View in real-time as questions are added and appended to the bottom of the list by other users
4. View in real-time that upvotes are updated without having to reload/refresh the page to recreate the elements.

Finally, a real-time 2-way front-end in Python is possible.



