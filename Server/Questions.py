from PersistentStorage import PersistentStorage
from Data.Data import election_database_attribute, technology_database_attribute, sport_database_attribute


election_questions = [
    dict(
        query = dict(
            columns = ['Winner'],
            tableName = 'constituency',
            condition = 'Constituency_Name = "Behat"',
        ),
        ansColumn = 'Winner',
        question = 'Who is the winner of Behat Constituency',
    ),

    dict(
        query = dict(
            columns = ['Winner'],
            tableName = 'constituency',
            condition = 'Constituency_Name = "Nakur"'
        ),
        ansColumn = 'Winner',
        question = 'Who is the winner of Nakur Constituency',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'constituency',
            condition = 'Party = "BJP"'
        ),
        ansColumn = 'count(*)',
        question = 'total number of seats won by BJP',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'constituency',
            condition = 'Party = "SP"'
        ),
        ansColumn = 'count(*)',
        question = 'total number of seats won by SP',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'constituency',
            condition = 'Party = "RLD"'
        ),
        ansColumn = 'count(*)',
        question = 'total number of seats won by RLD',
    ),

    dict(
        query = dict(
            columns = ['Constituency_Name'],
            tableName = 'constituency',
            condition = 'Winner = "Rajeev Gumber"'
        ),
        ansColumn = 'Constituency_Name',
        question = 'Rajeev Gumber won which constituency',
    ),

    dict(
        query = dict(
            columns = ['Constituency_Name'],
            tableName = 'constituency',
            condition = 'Winner = "Prakash Dwivedi"'
        ),
        ansColumn = 'Constituency_Name',
        question = 'Prakash Dwivedi won which constituency',
    ),

    dict(
        query = dict(
            columns = ['Party'],
            tableName = 'constituency',
            condition = 'Winner = "Vishambhar Singh"'
        ),
        ansColumn = 'Party',
        question = 'From which party, winner Vishambhar Singh belongs',
    ),

    dict(
        query = dict(
            columns = ['Party'],
            tableName = 'constituency',
            condition = 'Winner = "Dr. Manoj Kumar"'
        ),
        ansColumn = 'Party',
        question = 'From which party, winner Dr. Manoj Kumar belongs',
    ),

    dict(
        query = dict(
            columns = ['Constituency_Name'],
            tableName = 'constituency',
            condition = 'Constituency_Id = 7'
        ),
        ansColumn = 'Constituency_Name',
        question = 'Which constituency have constituency id 7',
    ),

    dict(
        query = dict(
            columns = ['Constituency_Name'],
            tableName = 'constituency',
            condition = 'Constituency_Id = 58'
        ),
        ansColumn = 'Constituency_Name',
        question = 'Which constituency have constituency id 58',
    ),

    dict(
        query = dict(
            columns = ['Constituency_Id'],
            tableName = 'constituency',
            condition = 'Constituency_Name = "Kairana"'
        ),
        ansColumn = 'Constituency_Id',
        question = 'What is the constituency ID of Kairana',
    ),
]

sports_questions = [
    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'Sports_Name = "Cricket"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news are related to cricket',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'Sports_Name = "Badminton"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news belong to sport Badminton',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'Sports_Name = "Tennis"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news are related to Tennis',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'Sports_Name = "Football"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news are related to sport Football',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'Sports_Name = "Basketball"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news are related to Basketball',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'News_Source = "The Hindu"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news are there from newspaper The Hindu',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = '1=1',
        ),
        ansColumn = 'count(*)',
        question = 'How many total news are there in the table',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'News_Source = "Times of India"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news are there from newspaper Times of India',
    ),

    dict(
        query = dict(
            columns = ['count(*)'],
            tableName = 'mytable',
            condition = 'News_Source = "Hindustan Times"',
        ),
        ansColumn = 'count(*)',
        question = 'How many news are from Hindustan Times',
    ),
]


technology_questions = [
    dict(
        query = dict(
            columns = ['Author'],
            tableName = '`tech news`',
            condition = 'Technology = "Fashion and NFTs"',
        ),
        ansColumn = 'Author',
        question = 'Which author wrote an article on Fashion and NFTs?',
    ),

    dict(
        query = dict(
            columns = ['Place'],
            tableName = '`tech news`',
            condition = 'Author = "IANS"',
        ),
        ansColumn = 'Place',
        question = 'In which place did the IANS write an article?',
    ),

    dict(
        query = dict(
            columns = ['Headline'],
            tableName = '`tech news`',
            condition = 'Newspaper = "The Indian Express" AND Place = "New Delhi" AND Technology = "Networking"',
        ),
        ansColumn = 'Headline',
        question = 'Jio partners with which university for 6G Technology?',
    ),

    dict(
        query = dict(
            columns = ['Headline'],
            tableName = '`tech news`',
            condition = 'Newspaper = "The Hindu" AND Place = "New Delhi" AND Technology = "Metaverse"',
    ),
        ansColumn = 'Headline',
        question = 'Which headset shipments grow 10 times by 2025?',
    ),

    dict(
        query = dict(
            columns = ['Headline'],
            tableName = '`tech news`',
            condition = 'Newspaper = "The Hindu" AND Place = "New Delhi" AND Technology = "electronics" AND Author = "Aditya Saroha"',
        ),
        ansColumn = 'Headline',
        question = 'Which companies partner up to build customized AR chips?',
    ),

    dict(
        query = dict(
            columns = ['Headline'],
            tableName = '`tech news`',
            condition = 'Newspaper = "The Hindu" AND Place = "China" AND Author = "AP"',
        ),
        ansColumn = 'Headline',
        question = 'World faces shortage of which metal element for vehicle batteries?',
    ),

    dict(
        query = dict(
            columns = ['Headline'],
            tableName = '`tech news`',
            condition = 'Newspaper = "The Hindu" AND Place = "New Delhi" AND Technology = "electronics" AND Author = "Aditya Saroha"',
        ),
        ansColumn = 'Headline',
        question = 'Which company is examined by U.S. for national security risks?',
    ),

    dict(
        query = dict(
            columns = ['Author'],
            tableName = '`tech news`',
            condition = 'Author = "IANS"'
        ),
        ansColumn = 'Technology',
        question = 'Author IANS wrote on which technology topic?',
    ),

    dict(
        query = dict(
            columns = ['Author'],
            tableName = '`tech news`',
            condition = 'Author = "Shruti Dhapola"',
        ),
        ansColumn = 'Technology',
        question = 'Author Shruti Dhapola wrote on which technology topic?',
    ),

    dict(
        query = dict(
            columns = ['Author'],
            tableName = '`tech news`',
            condition = 'Author = "Abhishek Chatterjee"',
        ),
        ansColumn = 'Technology',
        question = 'Author Abhishek Chatterjee wrote on which technology topic?',
    ),
]