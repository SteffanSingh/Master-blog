import json
from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

with open("data.json", "r") as fileObject:
    data = fileObject.read()
    blog_posts = json.loads(data)




@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=enumerate(blog_posts))

@app.route("/add", methods= ["GET", "POST"])
def add():
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

        blog_posts.append(new_post)

        with open("data.json", "w") as fileObject:
            fileObject.write(json.dumps(blog_posts, indent=4))

        return redirect(url_for("index"))
    return render_template('add.html')

@app.route("/delete/<int:post_id>")
def delete(post_id):

    for index,blog in enumerate(blog_posts):
        print(type(blog))
        if blog["id"] == post_id:
            blog_posts.remove(blog)

    with open("data.json", "w") as fileObject:
        fileObject.write(json.dumps(blog_posts, indent=4))
    return redirect(url_for("index"))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
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


if __name__ == '__main__':
    app.run()
