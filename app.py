from flask import (
    Flask, redirect, render_template, flash, jsonify, request
)
from contacts_model import Contact

Contact.load_db()

# ========================================================
# Flask App
# ========================================================

app = Flask(__name__)

app.secret_key = b'hypermedia rocks'


@app.route("/")
def index():
    return redirect("/contacts")


@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    if search is not None:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template("list.html", contacts=contacts_set)

@app.route("/contacts/new", methods=['GET'])
def contacts_new_get():
    return render_template("new.html", contact=Contact())

@app.route("/contacts/new", methods=['POST'])
def contacts_new():
    c = Contact(None, request.form['first_name'], request.form['last_name'], request.form['phone'],
                request.form['email'])
    if c.save():
        flash("Created New Contact!")
        return redirect("/contacts")
    else:
        return render_template("new.html", contact=c)

@app.route("/contacts/<contact_id>")
def contacts_view(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("show.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["GET"])
def contacts_edit_get(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("edit.html", contact=contact)


@app.route("/contacts/<contact_id>/edit", methods=["POST"])
def contacts_edit_post(contact_id=0):
    c = Contact.find(contact_id)
    c.update(request.form['first_name'], request.form['last_name'], request.form['phone'], request.form['email'])
    if c.save():
        flash("Updated Contact!")
        return redirect("/contacts/" + str(contact_id))
    else:
        return render_template("edit.html", contact=c)

@app.route("/contacts/<contact_id>/delete", methods=["GET"])
def contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    contact.delete()
    flash("Deleted Contact!")
    return redirect("/contacts")

@app.route("/contacts/count")
def contacts_count():
    count = Contact.count()
    return "(" + str(count) + " total Contacts)"

# ===========================================================
# JSON Data API
# ===========================================================

@app.route("/api/v1/contacts", methods=["GET"])
def json_contacts():
    contacts_set = Contact.all()
    return {"contacts": [c.__dict__ for c in contacts_set]}


@app.route("/api/v1/contacts", methods=["POST"])
def json_contacts_new():
    c = Contact(None, request.form.get('first_name'), request.form.get('last_name'), request.form.get('phone'),
                request.form.get('email'))
    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}, 400


@app.route("/api/v1/contacts/<contact_id>", methods=["GET"])
def json_contacts_view(contact_id=0):
    contact = Contact.find(contact_id)
    return contact.__dict__


@app.route("/api/v1/contacts/<contact_id>", methods=["PUT"])
def json_contacts_edit(contact_id):
    c = Contact.find(contact_id)
    c.update(request.form['first_name'], request.form['last_name'], request.form['phone'], request.form['email'])
    if c.save():
        return c.__dict__
    else:
        return {"errors": c.errors}, 400


@app.route("/api/v1/contacts/<contact_id>", methods=["DELETE"])
def json_contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    contact.delete()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run()



