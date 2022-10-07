from flask import *
import pymysql
from datetime import datetime
from twt import readtwitinfo
app=Flask(__name__)
con=pymysql.connect(host="localhost",user="root",passwd="",port=3306,db="sentiment_analysis")
cmd=con.cursor()
app.secret_key="ab"
# @app.route('/')
# def start():
#     return render_template("index.html")
@app.route('/')
def log():
    return render_template("loginhome.html")


@app.route('/ad')
def ad():
    return render_template("adminindex.html")
@app.route('/ud')
def ud():
    return render_template("userindex.html")
@app.route('/hh')
def hh():
    return render_template("help.html")



@app.route('/loggg')
def loggg():
    return render_template("loginpage.html")
@app.route('/login',methods=['get','post'])
def login():
    username=request.form['textfield']
    password=request.form['textfield2']
    cmd.execute("select * from login where username='"+username+"' and password='"+password+"'")
    s=cmd.fetchone()
    if s is None:
        return '''<script>alert("invalid password");window.location="/"</script>'''
    elif s[3]=="admin":
        return '''<script>alert("success");window.location="/homepage"</script>'''
    elif s[3]=="user":
        session['lid']=s[0]
        return '''<script>alert("success");window.location="/user_homepage"</script>'''
    else:
        return '''<script>alert("failed");window.location="/"</script>'''




@app.route('/homepage')
def homepage():
    return render_template("homepage.html")
@app.route('/view_user')
def view_user():
    cmd.execute("SELECT `view user`.*,`login`.* FROM `login` JOIN `view user` ON `view user`.`Login_id`=`login`.`Id` ")
    s=cmd.fetchall()
    return render_template("view user.html",val=s)
@app.route('/logout',methods=['post'])
def logout():
    return render_template("loginpage.html")
@app.route('/feedback')
def feedback():
    cmd.execute("SELECT `feedback`.*,`view user`.`Username` FROM `feedback` JOIN `view user` ON `feedback`.`user_id`=`view user`.`Login_id`")
    s=cmd.fetchall()
    return render_template("feedback.html",val=s)
@app.route('/Registration')
def Registration():
    return render_template("Registration.html")
@app.route('/Registration1',methods=['post'])
def Registration1():
    Username=request.form['textfield']
    Housename=request.form['textfield2']
    Place=request.form['textfield3']
    Post=request.form['textfield4']
    Pin=request.form['textfield5']
    Mob_Number=request.form['textfield6']
    Email_id=request.form['textfield7']
    Username=request.form['textfield8']
    Password=request.form['textfield9']
    cmd.execute("insert into login values(null,'"+Username+"','"+Password+"','user')")
    id=con.insert_id()
    cmd.execute("insert into `view user` values(null,'"+Username+"','"+Housename+"','"+Place+"','"+Post+"','"+Pin+"','"+Mob_Number+"','"+Email_id+"','"+str(id)+"')")
    con.commit()
    return '''<script>alert("registered");window.location="/"</script>'''


@app.route('/user_homepage')
def user_homepage():
    return render_template("user homepage.html")
@app.route('/user_feedback')
def user_feedback():
    return render_template("userfeedback.html")
@app.route('/send_feedback',methods=['post'])
def send_feedback():
    feedback=request.form['textfield']
    cmd.execute("insert into feedback values (null,'"+feedback+"',curdate(),'"+str(session['lid'])+"')")
    con.commit()
    return '''<script>alert("feedback send");window.location='/user_homepage'</script>'''
@app.route('/search')
def search():
    con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="sentiment_analysis")
    cmd = con.cursor()
    id=request.args.get('id')
    cmd.execute("SELECT `Product`,`Twitter handle` FROM `product` WHERE `Id`='"+str(id)+"'")
    s=cmd.fetchone()
    res=readtwitinfo(s[0]+" "+s[1],str(id))
    cmd.execute("SELECT * FROM `twitter` WHERE `Product_id`='"+str(id)+"' AND `Polarity score`>0")
    pres=cmd.fetchall()

    cmd.execute("SELECT * FROM `twitter` WHERE `Product_id`='"+str(id)+"' AND `Polarity score`<0")
    nres=cmd.fetchall()

    cmd.execute("SELECT * FROM `twitter` WHERE `Product_id`='"+str(id)+"' AND `Polarity score`=0")
    nures=cmd.fetchall()

    xaxis=["positve","negative","neutral"]
    yaxis=[len(pres),len(nres),len(nures)]

    import matplotlib.pyplot as plt
    plt.switch_backend('agg')
    # creating the dataset
    data = {'C': 20, 'C++': 15, 'Java': 30,
            'Python': 35}
    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(xaxis, yaxis, color='#000080',
            width=0.4)

    plt.xlabel(s[0])
    plt.ylabel("rating")
    plt.title("product rating")

    fn = datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
    plt.savefig("static/graph/" + fn)

    res=[s[0],len(pres),len(nres),len(nures)]

    return render_template("search.html",f=fn,i=res)
@app.route('/adduser')
def adduser():
    cmd.execute("SELECT * from  product")
    s = cmd.fetchall()
    return render_template("adduser_search.html",val=s)
@app.route('/product_add',methods=['get','post'])
def product_add():
    return render_template("product new.html")
@app.route('/product_add1',methods=['get','post'])
def product_add1():
    Product_Name=request.form['textfield']
    Description=request.form['textfield2']
    Twitter_handle=request.form['textfield3']


    cmd.execute("insert into product values(null,'" +Product_Name+ "','" +Twitter_handle+ "','"+Description+"')")
    con.commit()
    return '''<script>alert("success");window.location="user_homepage"</script>'''
@app.route('/twitter_handle')
def twitter_handle():
    return render_template("twitter handle.html")
@app.route('/view_comparison')
def view_comparison():
    cmd.execute("SELECT * FROM product ")
    s = cmd.fetchall()
    return render_template("view comparison.html", val=s)
@app.route('/comparison',methods=['post'])
def comparison():
    con = pymysql.connect(host="localhost", user="root", passwd="", port=3306, db="sentiment_analysis")
    cmd = con.cursor()
    ids=request.form.getlist('checkbox')
    print(ids)
    pname=[]
    rating=[]
    pname1 = []
    for i in ids:
        cmd.execute("SELECT product.Product,AVG(`Polarity score`)FROM product JOIN twitter ON twitter.Product_id=product.Id WHERE product.Id="+str(i)+"")
        res=cmd.fetchone()

        pname.append(res[0])
        if str(res[1])!='None':
            rating.append(res[1])
        else:
            rating.append(0)

    p1 = []
    n1 = []
    nu1 = []
    j=0

    for i in ids:
        cn=0
        cp=0
        cnu=0
        cmd.execute("SELECT * FROM `twitter` WHERE `Product_id`='"+str(i)+"' ORDER BY `Id` DESC LIMIT 200 ")
        s=cmd.fetchall()
        for r in s:
            if float(r[3])>0:
                cp=cp+1
            elif float(r[3])<0:
                cn=cn+1
            elif float(r[3])==0:
                cnu=cnu+1
        p1.append(cp)
        n1.append(cn)
        nu1.append(cnu)
        pname1.append(pname[j]+" ("+str(len(s))+")")
        j=j+1
    print(pname,rating)
    import numpy as np
    import matplotlib.pyplot as plt
    plt.switch_backend('agg')
    X = pname1


    X_axis = np.arange(len(pname))

    plt.bar(X_axis - 0.2, p1, 0.2, label='Positive')
    plt.bar(X_axis + 0.0, n1, 0.2, label='Negative')
    plt.bar(X_axis + 0.2, nu1, 0.2, label='Neutral')

    plt.xticks(X_axis, X)
    plt.xlabel("Product Name")
    plt.ylabel("Number of tweets")
    plt.title("Number of postive,negative & neutral")
    plt.legend()
    fn=datetime.now().strftime("%Y%m%d%H%M%S")+".png"
    plt.savefig("static/graph/"+fn)
    return render_template("result.html",p=pname,r=rating,f=fn)


@app.route('/blockuser',methods=['get','post'])
def blockuser():
    id = request.args.get('id')
    cmd.execute("update login set type='blocked' where Id='" + str(id) + "'")
    con.commit()
    return '''<script>alert("Blocked");window.location="/view_user"</script>'''
@app.route('/Forgotpassword',methods=['get','post'])
def Forgotpassword():
   return render_template('forgotpassword.html')
@app.route('/forgotpassword1',methods=['get','post'])
def forgotpassword1():
    uname=request.form["textfield"]
    Email=request.form["textfield2"]
    cmd.execute("SELECT login.`Password` FROM `login`JOIN `view user` ON `view user`.Login_id=login.Id WHERE login.Username='"+uname+"' AND `view user`.`Email-id`='"+Email+"'")
    s=cmd.fetchone()
    if s is None :
        return '''<script>alert("Invalid user name or email");window.location="/"</script>'''
    else:
        import smtplib
        from email.mime.text import MIMEText
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('mohamedanascp@gmail.com', 'Anascp@47')
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Your USERNAME :" + uname + " And  PASSWORD:" + s[0])
        print(msg)
        msg['Subject'] = 'Forgot Password'
        msg['To'] = Email
        msg['From'] = 'mohamedanascp@gmail.com'
        try:
            gmail.send_message(msg)


        except Exception as e:
            print("COULDN'T SEND EMAIL",e)
        return '''<script>alert("please check your mail");window.location="/"</script>'''

    return render_template('forgotpassword.html')
@app.route('/unblockuser',methods=['get','post'])
def unblockuser():
    id = request.args.get('id')
    cmd.execute("update login set type='user' where Id='" + str(id) + "'")
    con.commit()
    return '''<script>alert("unblocked");window.location="/view_user"</script>'''

@app.route('/delete',methods=['get','post'])
def delete():
    id = request.args.get('id')
    cmd.execute("DELETE FROM `product` WHERE `Id`='" + str(id) + "'")
    con.commit()
    return '''<script>alert("deleted");window.location="/user_homepage"</script>'''
def sent(rev,pid):
    import nltk
    con = pymysql.connect(host='localhost', port=3306, user='root', password='', db='sentiment_analysis')
    cmd = con.cursor()
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    pstv=0
    ngtv=0
    ntl=0
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(rev)
    a = float(ss['pos'])
    b = float(ss['neg'])
    c = float(ss['neu'])
    rating = 2.5
    if (ss['neu'] > ss['pos'] and ss['neu'] > ss['neg']):
        pass
    if (ss['neg'] > ss['pos']):
        negva = 5 - (5 * ss['neg'])
        if negva > 2.5:
            negva = negva - 2.5
        rating = negva
    else:
        negva = 5 * ss['pos']
        if negva < 2.5:
            negva = negva + 2.5
        rating = negva
    cmd.execute("INSERT INTO twitter VALUES (NULL,'"+str(pid)+"','"+rev+"','"+str(rating)+"')")
    con.commit()
    return "ol"













# sent("bad product",1)
app.run(debug=True)
