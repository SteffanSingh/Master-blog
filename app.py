import json


from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

with open("data.json", "r") as fileObject:
    data = fileObject.read()
    blog_posts = json.loads(data)




@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)

@app.route("/add", methods= ["GET", "POST"])
def add():

    if request.method == "POST":
        new_post = {}
        id = len(blog_posts)+1
        title = request.form["title"]
        content = request.form["content"]
        author = request.form["author"]
        new_post["id"] = id
        new_post["title"] = title
        new_post["content"] = content
        new_post["author"] = author
        blog_posts.append(new_post)
        with open("data.json", "w") as fileObject:
            fileObject.write(blog_posts)
        return redirect(url_for("index"))
    return render_template('add.html')


if __name__ == '__main__':
    app.run()
