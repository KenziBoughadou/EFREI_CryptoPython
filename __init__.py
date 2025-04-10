from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Affiche votre page d'accueil

# --- Version avec clé statique ---
# Génération d'une clé unique pour la session
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    """
    Encrypte la valeur passée en argument en utilisant la clé statique.
    """
    valeur_bytes = valeur.encode()  # Conversion de la chaîne en bytes
    token = f.encrypt(valeur_bytes)  # Encryption
    return f"Valeur encryptée : {token.decode()}"  # Retourne le résultat en chaîne de caractères

@app.route('/decrypt/<string:token>')
def decryptage(token):
    """
    Décrypte le token passé en argument en utilisant la clé statique.
    """
    try:
        decrypted = f.decrypt(token.encode())
        return f"Valeur décryptée : {decrypted.decode()}"
    except Exception as e:
        return f"Erreur de décryptage : {e}"

# --- Version avec clé personnelle fournie par l'utilisateur ---

@app.route('/encrypt_key/<string:key_user>/<string:valeur>')
def encryptage_personnalise(key_user, valeur):
    """
    Encrypte une valeur avec une clé personnalisée fournie par l'utilisateur.
    Attention : la clé doit être une chaine Base64 de 32 octets.
    """
    try:
        # On crée un objet Fernet avec la clé personnelle fournie
        f_user = Fernet(key_user.encode())
        token = f_user.encrypt(valeur.encode())
        return f"Valeur encryptée avec clé personnelle : {token.decode()}"
    except Exception as e:
        return f"Erreur d'encryptage avec clé personnelle : {e}"

@app.route('/decrypt_key/<string:key_user>/<string:token>')
def decryptage_personnalise(key_user, token):
    """
    Décrypte une valeur avec une clé personnalisée fournie par l'utilisateur.
    Attention : la clé doit être une chaine Base64 de 32 octets.
    """
    try:
        f_user = Fernet(key_user.encode())
        decrypted = f_user.decrypt(token.encode())
        return f"Valeur décryptée avec clé personnelle : {decrypted.decode()}"
    except Exception as e:
        return f"Erreur de décryptage avec clé personnelle : {e}"

if __name__ == '__main__':
    app.run(debug=True)
