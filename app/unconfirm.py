'''

from app import app
from flask_security import login_required

@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('/')
    flash('Please confirm your account!', 'warning')
    return render_template('templates/unconfirmed.html')
'''