from flask import Flask, request, jsonify
import os
from openai import OpenAI
from dotenv import load_dotenv

# Charger la clé API depuis le fichier .env
load_dotenv()

# Initialiser le client OpenAI avec la clé API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# Simulation d'une base de données des utilisateurs connectés
utilisateurs_connectes = {}

@app.route('/connexion', methods=['POST'])
def connexion():
    """Permet à un utilisateur de se connecter"""
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return jsonify({"message": "ID utilisateur manquant"}), 400
        
    utilisateurs_connectes[user_id] = True
    return jsonify({"message": "Connexion réussie ! Vos avis sont en cours de traitement."})

@app.route('/avis', methods=['POST'])
def traiter_avis():
    """Traite les avis des utilisateurs connectés et génère une réponse"""
    data = request.json
    user_id = data.get("user_id")
    avis_liste = data.get("avis")
    
    if user_id not in utilisateurs_connectes:
        return jsonify({"message": "Utilisateur non connecté"}), 401
        
    if not avis_liste or not isinstance(avis_liste, list):
        return jsonify({"message": "Aucun avis fourni"}), 400
    
    # Générer une réponse pour chaque avis
    reponses = [{"avis": avis, "reponse": generer_reponse_avis(avis)} for avis in avis_liste]
    
    return jsonify({"message": "Avis traités avec succès", "reponses": reponses})

def generer_reponse_avis(avis):
    """Utilise ChatGPT pour générer une réponse automatique aux avis"""
    try:
        # Utilisation de la nouvelle syntaxe de l'API OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui répond aux avis Google de manière professionnelle et personnalisée. Ta réponse doit refléter l'esprit de l'entreprise, être empathique et remercier le client pour son feedback."},
                {"role": "user", "content": f"Voici un avis client auquel tu dois répondre : '{avis}'"}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erreur lors de la génération de réponse : {str(e)}"

# Ajouter une route pour vérifier que l'API est bien configurée
@app.route('/test-api', methods=['GET'])
def test_api():
    """Vérifie que l'API OpenAI est correctement configurée"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Test de connexion"}
            ],
            max_tokens=5
        )
        return jsonify({"status": "success", "message": "API OpenAI correctement configurée"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Erreur de configuration API: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
    
@app.route('/', methods=['GET'])
def accueil():
    return "✅ L'API fonctionne parfaitement !"
   
    
    
    
    