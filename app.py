from flask import Flask, render_template


app = Flask(__name__)

with open("data.json", "r") as fileObject:
    blog_posts = fileObject.read()




@app.route('/')
def index():
    # add code here to fetch the job posts from a file
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run()
