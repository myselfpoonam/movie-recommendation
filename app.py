from flask import Flask, request,render_template,request
import pickle
import pandas as pd
from patsy import dmatrices

movies = pickle.load(open('model/movies.pkl','rb'))

movies = pd.DataFrame(movies)

similarity = pickle.load(open('model/similarity.pkl','rb'))

def recommend(movie):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movies_name = []
        for i in distances[1:10]:
            recommended_movies_name.append(movies.iloc[i[0]].title)
        return recommended_movies_name
     
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("aboutus.html")


@app.route('/contantus')
def contantus():
    return render_template("contant.html")
 
@app.route('/recommendation' , methods = ['GET','POST'])
def recommendation():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
        try:
            if request.form:
                movies_name = request.form['movies']
                print(movies_name)
                recommended_movies_name  = recommend(movies_name)
                print(recommended_movies_name)
                
                status = True
                return render_template("prediction.html", movies_name = recommended_movies_name, movie_list = movie_list, status = status)
        
        except Exception as e:
            error = {'error': e}
            return render_template("prediction.html",error = error, movie_list = movie_list, status = status )
    else:

        return render_template("prediction.html", movie_list = movie_list, status = status)      



if __name__ == '_main_':
    app.debug = True
    app.run() 