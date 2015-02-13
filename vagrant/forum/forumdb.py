#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Database connection


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()
    query = "SELECT * from posts"
    cur.execute(query)
    all_posts = cur.fetchall()
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in all_posts]
    posts.sort(key=lambda row: row['time'], reverse=True)
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''

    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()
    query = "INSERT INTO posts (content) values ('%s')"%(content,)
    cur.execute(query)
    DB.commit()
    DB.close()

  


