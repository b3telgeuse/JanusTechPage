from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.tree import Trees
from flask_app.models.user import User



@app.route('/addTree/')
def addTree():
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        return render_template('addTree.html', user=theUser)



@app.route('/createTree/', methods=['post'])
def createTree():
    data = {
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'datePlanted': request.form['datePlanted'],
        'user_id': request.form['user_id'],
    }
    Trees.save(data)
    return redirect('/about/')



@app.route('/tree/<int:trees_id>/view/')
def viewTree(trees_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        treeData = {
            'id': trees_id
        }
        theUser = User.getOne(data)
        theTree = Trees.getOne(treeData)
        theUsers = User.getAll()
        return render_template('viewTree.html', user=theUser, tree=theTree, users=theUsers)



@app.route('/tree/<int:trees_id>/edit/')
def editTree(trees_id):
    if 'user_id' not in session:
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        theUser = User.getOne(data)
        treeData = {
            'id': trees_id
        }
        theTrees = Trees.getOne(treeData)
        return render_template('editTree.html', user=theUser, tree=theTrees)



@app.route('/tree/<int:trees_id>/update/', methods=['post'])
def updateTree(trees_id):
    data = {
        'id': trees_id,
        'species': request.form['species'],
        'location': request.form['location'],
        'reason': request.form['reason'],
        'datePlanted': request.form['datePlanted'],
    }
    Trees.update(data)
    return redirect(f'/tree/{trees_id}/view/')



@app.route('/tree/<int:trees_id>/delete/')
def deleteTree(trees_id):
    data = {
        'id': trees_id
    }
    Trees.delete(data)
    return redirect('/about/')


