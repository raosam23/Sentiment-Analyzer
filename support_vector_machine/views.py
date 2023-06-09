from django.shortcuts import render
from django.http import HttpResponse
import io
import os
from django.conf import settings
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def create_pie_chart(request, positive, negative, neutral):
    file_name = request.session.get('file_name')
    plt.close('all')
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [positive, negative, neutral]
    colors = ['#00ff00', '#ff0000', '#fff']
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set_title(f'Sentiments for {file_name} using Support Vector')
    fig.patch.set_facecolor('#FAD9C1')
    ax.set_facecolor('#FAD9C1')

    image_file_name = f'{file_name}_svm_pie.png'

    piechart_directory = os.path.join(settings.MEDIA_ROOT, 'piechart')
    image_file_path = os.path.join(piechart_directory, image_file_name)

    if default_storage.exists(image_file_path):
        image_file_path = default_storage.path(image_file_path)
    else:
        # Save figure as BytesIO object
        image_data = io.BytesIO()
        plt.savefig(image_data, format='png')
        image_data.seek(0)

        # Create ContentFile from BytesIO object
        content_file = ContentFile(image_data.read())
        image_file_path = default_storage.save(image_file_path, content_file)
        plt.close(fig)
    return image_file_name

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()
    # Tokenize text
    tokens = word_tokenize(text.lower())

    # Remove stopwords and stem remaining words
    stemmed_tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]

    # Join stemmed tokens back into a single string
    preprocessed_text = ' '.join(stemmed_tokens)

    return preprocessed_text

def computing_support_vector(request):
    file_name = request.session.get('file_name')
    test_url = os.path.join(settings.MEDIA_ROOT, 'csvfiles', file_name)
    train_url = os.path.join(settings.MEDIA_ROOT, 'train', 'train.csv')
    train_data = pd.read_csv(train_url)
    test_data = pd.read_csv(test_url)

    train_data = train_data.dropna()
    test_data = test_data.dropna()

    train_data['Tweet'] = train_data['Tweet'].apply(preprocess_text)
    test_data['Tweet'] = test_data['Tweet'].apply(preprocess_text)

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(train_data['Tweet'])
    X_test = vectorizer.transform(test_data['Tweet'])
    y_train = train_data['sentiment']

    svm = SVC(kernel='linear', decision_function_shape='ovr', random_state=0)
    svm.fit(X_train, y_train)

    y_pred = svm.predict(X_test)


    result_data_svm = pd.concat([test_data, pd.DataFrame({'sentiment' : y_pred})], axis=1)

    csv_data = result_data_svm.to_csv(index=False)
    csv_file = ContentFile(csv_data.encode())
    sentiment_file_name = f'{file_name}_sentiments_svm_predictions.csv'

    sentiment_directory = os.path.join(settings.MEDIA_ROOT, 'sentimentscsv')
    sentiment_file_directory = os.path.join(sentiment_directory, sentiment_file_name)

    if default_storage.exists(sentiment_file_directory):
        file_path = default_storage.path(sentiment_file_directory)

    else:
        file_path = default_storage.save(sentiment_file_directory, csv_file)

    positive = round(((sum(y_pred == 'positive')/len(y_pred)) * 100), 2)
    negative = round(((sum(y_pred == 'negative')/len(y_pred)) * 100), 2)
    neutral = round(((sum(y_pred == 'neutral')/len(y_pred)) * 100), 2)
    image_file_name = create_pie_chart(request, positive, negative, neutral)
    return render(request, 'support_vector_machine/sentiment_results.html', {"image_file_name" : image_file_name})
# Create your views here.

def support_vector(request) -> render:
    file_name = request.session.get('file_name')
    return render(request, 'support_vector_machine/support_vector.html', {'file_name' : file_name})

def compute_support_vector(request):
    return computing_support_vector(request)