import pymysql
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, redirect, url_for
import os
# 连接数据库
connection = pymysql.connect(host='localhost', port=3306, user='root', password='Mqx20041205', db='homework', charset='utf8')



# 创建游标对象
cursor = connection.cursor()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/playerview/<string:name>', methods=['GET','POST'])
def sel(name):

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM playerview WHERE name=%s", (name,))
        data = cursor.fetchall()
        cursor.execute("SELECT * FROM player WHERE name=%s", (name,))
        player = cursor.fetchone()
    return render_template('sel.html', data=data,player=player)

# coach
@app.route('/coach', methods=['GET'])
def coach():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM coach")
        coachs = cursor.fetchall()
    return render_template('coach.html', coachs=coachs)

@app.route('/coach/add', methods=['GET', 'POST'])
def add_coach():
    if request.method == 'POST':
        coachname = request.form.get('coachname')
        clubname = request.form.get('clubname')
        coachnation = request.form.get('coachnation')
        coachage = request.form.get('coachage')
        
        with connection.cursor() as cursor:
            sql = "INSERT INTO coach (coachname,clubname,coachnation,coachage) VALUES ('%s','%s','%s',%s)" %(coachname,clubname,coachnation,coachage)
            print(sql)
            cursor.execute(sql)
            connection.commit()
        return redirect(url_for('coach'))
    else:
        return render_template('add_coach.html')


@app.route('/coach/edit/<string:coachname>', methods=['GET', 'POST'])
def edit_coach(coachname):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM coach WHERE coachname=%s", (coachname,))
        coach = cursor.fetchone()
    if request.method == 'POST':
        x=coachname
        coachname = request.form('coachname')
        clubname = request.form('clubname')
        coachnation = request.form('coachnation')
        coachage = request.form('coachage')
        
        with connection.cursor() as cursor:
            cursor.execute("UPDATE coach SET coachname=%s, clubname=%s, coachnation=%s, coachage=%s WHERE coachname=%s",
                           (coachname,clubname,coachnation,coachage,x))
            connection.commit()
        return redirect(url_for('coach'))

    return render_template('edit_coach.html', coach=coach)

@app.route('/coach/delete/<string:coachname>')
def delete_coach(coachname):
    try:
        with connection.cursor() as cursor:
            cursor.execute("START TRANSACTION")
            cursor.execute("DELETE FROM coach WHERE coachname = %s", (coachname,))
            cursor.execute("COMMIT")
    except Exception as e:
        connection.rollback()
    return redirect(url_for('coach'))

# data
@app.route('/data', methods=['GET'])
def data():

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM data")
        datas = cursor.fetchall()
    return render_template('data.html', datas=datas)

@app.route('/data/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        goals=request.form.get('goals')
        assists = request.form.get('assists')
        yellowcard = request.form.get('yellowcard')
        redcard = request.form.get('redcard')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO data (goals,assists,yellowcard,redcard) VALUES (%s,%s,%s,%s)",
                           (goals,assists,yellowcard,redcard))
            connection.commit()
        return redirect(url_for('data'))
    else:
        return render_template('add_data.html')

@app.route('/data/edit/<int:goals>', methods=['GET', 'POST'])
def edit_data(goals):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM data WHERE goals=%s", (goals,))
        data = cursor.fetchone()

    if request.method == 'POST':
        goals=request.form.get('goals')
        assists = request.form.get('assists')
        yellowcard = request.form.get('yellowcard')
        redcard = request.form.get('redcard')
        with connection.cursor() as cursor:
            cursor.execute("UPDATE data  WHERE goals=%s",
                           (assists,yellowcard,redcard,goals))
            connection.commit()
        return redirect(url_for('data'))

    return render_template('edit_data.html', data=data)
@app.route('/data/delete/<int:goals>')
def delete_data(goals):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM data WHERE goals=%s", (goals,))
        connection.commit()
    return redirect(url_for('data'))

# player
@app.route('/player', methods=['GET'])
def player():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM player")
        players = cursor.fetchall()
    return render_template('player.html', players=players)

@app.route('/player/add', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name=request.form.get('name')
        clubname = request.form.get('clubname')
        goals=request.form.get('goals')
        nation= request.form.get('nation')
        age = request.form.get('age')
        position = request.form.get('position')
        number = request.form.get('number')
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO player (name,clubname,goals,nation,age,position,number)"
                           " VALUES (%s,%s,%s,%s,%s,%s,%s)",
                           (name,clubname,goals,nation,age,position,number))
            connection.commit()
        return redirect(url_for('player'))
    else:
        return render_template('add_player.html')

@app.route('/player/edit/<string:name>', methods=['GET', 'POST'])
def edit_player(name):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM player WHERE name=%s", (name,))
        player = cursor.fetchone()
    if request.method == 'POST':
        name_new = request.form.get('name')
        clubname = request.form.get('clubname')
        goals=request.form.get('goals')
        nation = request.form.get('nation')
        age = request.form.get('age')
        position = request.form.get('position')
        number = request.form.get('number')
        
        with connection.cursor() as cursor:
            cursor.execute("UPDATE player SET name=%s, clubname=%s, goals=%s,nation=%s, age=%s, position=%s, number=%s WHERE name=%s",
                           (name_new, clubname, goals, nation, age, position, number, name))
            connection.commit()
        return redirect(url_for('player'))
    return render_template('edit_player.html', player=player)


@app.route('/player/delete/<string:name>')
def delete_player(name):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM player WHERE name=%s", (name,))
    return redirect(url_for('player'))

# club
@app.route('/club', methods=['GET'])
def club():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `club`")
        clubs = cursor.fetchall()
    return render_template('club.html', clubs=clubs)

@app.route('/club/add', methods=['GET', 'POST'])
def add_club():
    if request.method == 'POST':
        clubname = request.form.get('clubname')
        coachname=request.form.get('coachname')
        city = request.form.get('city')
        homecourt = request.form.get('homecourt')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO `club` (clubname, coachname, city, homecourt) VALUES (%s, %s,%s, %s)",
                           (clubname, coachname, city, homecourt))
            connection.commit()
        return redirect(url_for('club'))
    else:
        return render_template('add_club.html')


@app.route('/club/edit/<string:clubname>', methods=['GET', 'POST'])
def edit_club(clubname):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM `club` WHERE clubname=%s", (clubname,))
        club = cursor.fetchone()
    if request.method == 'POST':
        new_clubname = request.form.get('clubname')
        coachname=request.form.get('coachname')
        city = request.form.get('city')
        homecourt = request.form.get('homecourt')

        with connection.cursor() as cursor:
            cursor.execute("UPDATE `club` SET clubname=%s, coachname=%s, city=%s, homecourt=%s WHERE clubname=%s",
                           (new_clubname, coachname,city, homecourt, clubname))
            connection.commit()
        return redirect(url_for('club'))

    return render_template('edit_club.html', club=club)

@app.route('/club/delete/<string:clubname>')
def delete_club(clubname):
    try:
        with connection.cursor() as cursor:
            cursor.execute("START TRANSACTION")
            cursor.execute("DELETE FROM `club` WHERE clubname=%s", (clubname,))
            cursor.execute("DELETE FROM `coach` WHERE clubname=%s", (clubname,))
            cursor.execute("DELETE FROM `player` WHERE clubname=%s", (clubname,))
            cursor.execute("COMMIT")
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")  # 可改成记录到日志
    return redirect(url_for('club'))


if __name__ == '__main__':
    app.run(debug=True)

# 关闭游标和数据库连接
cursor.close()
connection.close()
