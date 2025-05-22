from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import paramiko

# === Génération des clés ===
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# === Export au format OpenSSH ===
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.OpenSSH,
    encryption_algorithm=serialization.NoEncryption()
)

public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.OpenSSH,
    format=serialization.PublicFormat.OpenSSH
)

# Sauvegarde locale des clés
with open("id_ed25519", "wb") as f:
    f.write(private_bytes)

with open("id_ed25519.pub", "wb") as f:
    f.write(public_bytes)

# === Connexion SSH avec Paramiko pour copier la clé publique ===
hostname = "ssh-kenzi.alwaysdata.net"
username = "kenzi"
password = "TON_MOT_DE_PASSE_HERE"  # ⚠️ à remplacer manuellement

# Lecture de la clé publique
with open("id_ed25519.pub", "r") as f:
    pub_key = f.read()

# Connexion et écriture distante
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, username=username, password=password)

sftp = ssh.open_s_
