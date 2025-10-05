from flask import Flask, render_template, request
import pickle
import numpy as np
app = Flask(__name__)

popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title']),
                           author=list(popular_df['Book-Author']),
                           image=list(popular_df['Image-URL-S']),
                           votes=list(popular_df['Num-Ratings']),
                           rating=list(popular_df['avg-Ratings']),
                           yop=list(popular_df['Year-Of-Publication'])
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    u_input = request.form.get('u_input')
    num_suggestions = int(request.form.get('num_suggestions', 10))  # default to 10 if not given

    # if book not found
    if u_input not in pt.index:
        return render_template('recommend.html', data=None, message=f'No recommendations found for "{u_input}".')

    # if found, continue normally
    index = np.where(pt.index == u_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:num_suggestions+1]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        data.append(item)

    return render_template('recommend.html', data=data, message=None)



if __name__ == '__main__':
    app.run(debug=True)