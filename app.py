import json
from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

def readJson():
    with open("data.json", "r") as fileObject:
        data = fileObject.read()
        blog_posts = json.loads(data)
    return  blog_posts



@app.route('/')
def index():
    """The function to display the list of blogs from the json file """
    blog_posts = readJson()
    return render_template('index.html', posts=enumerate(blog_posts))

@app.route("/add", methods= ["GET", "POST"])
def add():
    """The function to add the blog in blog list"""
    blog_posts = readJson()
    if request.method == "POST":
        new_post = {}
        id = (uuid.uuid1()).int

        title = request.form["title"]

        content = request.form["content"]

        author = request.form["author"]
        new_post["id"] = id
        new_post["title"] = title
        new_post["content"] = content
        new_post["author"] = author
        new_post["likes"] = 0

        blog_posts.append(new_post)

        with open("data.json", "w") as fileObject:
            fileObject.write(json.dumps(blog_posts, indent=4))

        return redirect(url_for("index"))
    return render_template('add.html')

@app.route("/like/<int:post_id>")
def like(post_id):
    blog_posts = readJson()
    """The function to  implement the like and increase the number of likes """
    post = [blog for blog in blog_posts if blog["id"] == post_id ][0]
    print(post)

    if post["id"] == post_id:
        post["likes"] += 1
        with open("data.json", "w") as fileObject:
            fileObject.write(json.dumps(blog_posts, indent=4))
        return redirect(url_for("index"))
    render_template("error.html")




@app.route("/delete/<int:post_id>")
def delete(post_id):
    """ The function to delete the blog from the blog list"""
    blog_posts = readJson()
    for index,blog in enumerate(blog_posts):

        if blog["id"] == post_id:
            blog_posts.remove(blog)

        return render_template("error.html")

    with open("data.json", "w") as fileObject:
        fileObject.write(json.dumps(blog_posts, indent=4))
    return redirect(url_for("index"))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """The function to update the specified the blog with given id"""
    # Fetch the blog posts from the JSON file
    blog_posts = readJson()
    post = [blog for blog in blog_posts if blog["id"] == post_id ][0]
    if post is None:
        # Post not found
        return "Post not found", 404
    if request.method == 'POST':
    # Update the post in the JSON file
        id = post_id
        author =request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        post['id'] = post_id
        post['author'] = author
        post["content"] = content
        post["title"] = title


        with open("data.json", "w") as fileObject:
            fileObject.write(json.dumps(blog_posts, indent=4))
        # Redirect back to index
        return redirect(url_for("index"))
    return render_template('update.html', post=post)

#main function
if __name__ == '__main__':
    app.run()
