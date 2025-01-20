from app.routes import bp

@bp.route('/decrypt', methods=['GET'])
def decrypt():
    return 'decrypted text'