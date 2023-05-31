from flask import (
    redirect,
    request,
    session,
    render_template,
    url_for,
    Blueprint,
)

main = Blueprint('main', __name__)

@main.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        name = request.form.get('name')
        if not name:
            return redirect('/chat')
        session['user_name'] = name
        return redirect(url_for('.window'))
    return render_template('chat.html')

@main.route('/window')
def window():
    name = session.get('user_name', None)
    if not name:
        return redirect('/chat')
    return render_template('window.html')