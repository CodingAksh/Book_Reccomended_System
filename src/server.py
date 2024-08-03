from flask import Flask, request, render_template
from app import recommendation_books

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    recommendations = []
    if request.method == 'POST':
        book_name = request.form['book_name']
        book_quantity = request.form['book_quantity']
        try:
            recommended_books, poster_urls = recommendation_books(book_name, int(book_quantity))
            recommendations = zip(recommended_books, poster_urls)
        except (IndexError, ValueError):
            pass  # Handle errors appropriately in a real app
    
    return render_template('recommendation.html', recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
