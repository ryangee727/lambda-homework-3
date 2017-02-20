from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/enternew')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods = ['POST'])
def addfood():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    msg = ""

    name = request.form['name']
    calories = request.form['calories']
    cuisine = request.form['cuisine']
    is_vegetarian = request.form['is_vegetarian']
    is_gluten_free = request.form['is_gluten_free']

    try:
        cur.execute('INSERT INTO foods (name,calories,cuisine,is_vegetarian,is_gluten_free) VALUES(?,?,?,?,?)', (name,calories,cuisine, is_vegetarian, is_gluten_free))
        conn.commit()
        msg = "Record Added"
    except Exception as e:
        print(e)
        conn.rollback()
        msg = "Error Adding Record"
    finally:
        return render_template('result.html', message = msg)
        conn.close()

@app.route('/favorite')
def favorite():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    fav = "Sushi"
    try:
        res = cur.execute('Select DISTINCT * from foods where name =:name',{'name':fav})
        msg = "\nRecord retrieved."
        for record in res:
            msg += "\n"+ record[0] + " is my favorite food."
    except Exception as e:
        print(e)
        msg = "Error retrieving Record"
    finally:
        return render_template('result.html', message = msg)
        conn.close()

@app.route('/search')
def search():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        srch = request.args.get('name')
        res = cur.execute("Select * from foods where name =:name",{'name':srch})
        msg = ""
        empty = True
        for record in res:
            empty = False
            msg += "\n"+record[0]+" is " + record[1] + " calories."
        if empty:
            msg += "There are no records for " + srch
    except Exception as e:
        print(e)
        msg = "Error retrieving Record"
    finally:
        return render_template('result.html', message = msg)
        conn.close()

@app.route('/drop')
def drop():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    try:
        cur.execute("Drop Table foods")
        msg = "Table Dropped."
    except Exception as e:
        print(e)
        msg = "Error Dropping Table."
    finally:
        return render_template('result.html', message = msg)
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
