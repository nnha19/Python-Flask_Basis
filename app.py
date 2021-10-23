from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db =SQLAlchemy(app)

class Todo(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     content = db.Column(db.String(200), nullable=False)
     date_created = db.Column(db.DateTime, default=datetime.utcnow)
        
     def __repr__(self):
          return '<Task %r>' % self.id


@app.route("/",methods=["POST","GET"])
def index():
    if request.method =="POST":
     task_content =request.form["content"]
     new_task = Todo(content=task_content)
     try :
         db.session.add(new_task)
         db.session.commit()
         return redirect("/")
     except :
        return ("Something went wrong. Try again.")
    else:
        tasks= Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html",tasks=tasks)
       
      
@app.route("/delete/<int:id>")
def deleteTodo(id):
    task_to_delete =Todo.query.get_or_404(id)

    try :
       db.session.delete(task_to_delete)
       db.session.commit()
       return redirect("/")
    except :
      return("There was an issue deleting the task.")

@app.route("/update/<int:id>",methods=["POST","GET"])
def update(id):
    task_to_update =Todo.query.get_or_404(id)
    if request.method =="GET":
        return render_template("updateTask.html",task=task_to_update)
    else:
         try :
            task_to_update.content =request.form["content"]
            db.session.commit()
            return redirect("/")
         except :
             return ("Something went wrong.")
    

if __name__ =="main" :
    app.run(debug =True)
