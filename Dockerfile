FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY app /app

RUN pip install Flask-JSON
RUN echo $' \n\
[uwsgi]\n\
module = fracbar.yamb.main\n\
callable = app' >> /app/uwsgi.ini


