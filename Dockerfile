FROM seartipy/pf:latest

# Install myapp
COPY . /app/
RUN chown -R myuser:myuser /app/*

# activate the myapp environment

CMD ["pytest"]
