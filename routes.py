from flask import render_template, request, redirect, url_for
from models import Note

def register_routes(app, db):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            tag = request.form['tag']

            note = Note(title=title, content=content, tag=tag)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('index'))

        tag_filter = request.args.get('tag')
        if tag_filter:
            notes = Note.query.filter_by(tag=tag_filter).all()
        else:
            notes = Note.query.all()

        tags = list({note.tag for note in Note.query.all() if note.tag})
        return render_template('index.html', notes=notes, tags=tags)

    @app.route('/delete/<int:note_id>')
    def delete(note_id):
        Note.query.filter_by(id=note_id).delete()
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/note/<int:note_id>')
    def detail(note_id):
        note = Note.query.get(note_id)
        return render_template('note_detail.html', note=note)
