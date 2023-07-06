from flask import render_template, flash, redirect, url_for, request, make_response, session
from veikals import app, db
from veikals.forms import LoginForm, RegistrationForm, AddPreceForm , SelectPreceForm, EmptyForm, PasutijumaForm, EditPasutijumsForma, PievienotPreciGrozamForm
from veikals.models import User, Prece, AnonimUser, Pasutijums, PasutijumsPrece, Bilde
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime, timezone
from google.cloud import storage
from PIL import Image
import io




@app.route('/')
def index():
    preces = db.session.execute(db.select(Prece)).scalars()
    return render_template('index.html', preces=preces, template_name='index.html')

    
@app.route('/veikals')
@app.route('/veikals/<pr_klase>/<pr_grupa>')
def veikals(pr_klase=None, pr_grupa=None):
    preces = get_selected_preces_and_paginate(pr_klase, pr_grupa)
    return render_template('veikals.html', **preces, pr_klase=pr_klase)


@app.route('/<prece_klase>/<prece_grupa>/<pr_id>', methods=['GET', 'POST'])
def prece_info(prece_klase, prece_grupa, pr_id):
    # create form
    pievienotPreciGrozamForm = PievienotPreciGrozamForm()
    # if method is POST, if add to grozs button is pressed 
    if pievienotPreciGrozamForm.validate_on_submit():
        # serch prece in db
        prece_id = request.form.get('prece_id')
        discount = request.form.get('discount')
        prece = db.session.execute(db.select(Prece).where(Prece.id == prece_id)).first()
        # if prece not found return to main page
        if prece is None:
            flash('Prece ar id nr:{} nav atrasta.'.format(prece_id))
            return redirect(url_for('index'))
        else:
            #
            flash('Prece pievienota grozam')     
            res = make_response(redirect(url_for('prece_info', prece_klase = prece_klase, prece_grupa=prece_grupa, pr_id=pr_id)))
            return add_id_and_discount_to_cookie(prece_id, discount, res)
        
    # if method is GET
    else:
        prece = db.session.execute(db.select(Prece).where(Prece.id == pr_id)).scalar()
        # check if prece is found
        if prece is None:
            flash('Prece ar is NONE')
            return redirect(url_for('index'))
        else:
            titulbildes_id = prece.titulbildes_id
            # Get titulbile
            titulbilde = db.session.execute(db.select(Bilde).where(Bilde.id == titulbildes_id)).scalar()
        
            # get all bildes for selected prece from db
            bildes = db.session.execute(db.select(Bilde).where(Bilde.prece_id == pr_id)).scalars()
            
            return render_template('prece_info.html', prece=prece, bildes=bildes, titulbilde=titulbilde, pievienotPreciGrozamForm=pievienotPreciGrozamForm)


@app.route('/iznemt_preci/<pr_id>/<discount>', methods=['POST'])
def iznemt_preci(pr_id, discount):
    form = EmptyForm()
    if form.validate_on_submit():
        # find prece in db
        prece = db.session.execute(db.select(Prece).where(Prece.id == pr_id)).first()
        # check if prece is found
        if prece is None:
            flash('Prece ar id nr:{} nav atrasta.'.format(pr_id))
            return redirect(url_for('grozs'))
        else:
            res = make_response(redirect(url_for('grozs')))
            updated_prece_cookie = get_prece_cookie_without_selected_prece(pr_id, discount)
            try:
                res.set_cookie('Prece_Id&Disc', updated_prece_cookie)
            except:
                res.set_cookie('Prece_Id&Disc', max_age=0)
                pass

            return res
    else:
        return redirect(url_for('grozs'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Veiksmīga reģistrācija!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/grozs', methods=['GET', 'POST'])
def grozs():
    ef = EmptyForm()
    cookies = request.cookies
    # Save id&disc cookie str in variable
    prece_in_grozs_cookie_string = cookies.get('Prece_Id&Disc')
    preces_groza_list = None
    # Chek if grozs not empty
    if prece_in_grozs_cookie_string:
        # Convert cookie str to tuple list
        id_disc_tuple_list = convert_cookie_str_to_tuple_list(prece_in_grozs_cookie_string)
        # Get prece count in grozs cookie
        prece_count = len(id_disc_tuple_list)
        # Load list of needed preces for grozs from db and add discount to object
        preces_groza = load_pirkumu_grozs(id_disc_tuple_list)
        # Iterate id&discount list to build dictionary for all preces in grozs
        # Needed for for showing one prece multiple times in grozs
        preces_groza_list = []
        for id in id_disc_tuple_list:
            # Get prece object for iter prece
            p = get_prece(id ,preces_groza)
            # Add object to list
            preces_groza_list.append(p)

    else:
        id_disc_tuple_list = None
        prece_count = None
    # Make response      
    res = make_response(render_template(
        'grozs.html', 
        prece_count=prece_count,
        preces_groza=preces_groza_list,
        ef=ef,
        ))
    res.set_cookie("Prece_Count",value=str(prece_count), max_age=50000)    
    return res


@app.route('/pasutijuma_forma', methods=['GET', 'POST'])
def pasutijuma_forma():
    res = make_response(redirect('pasutijuma_parskats'))
    pf = PasutijumaForm()
    if pf.validate_on_submit():
        # Create new user, if not in session
        if 'anonim_user_id' not in session:
            # Store user data in db. Get back session object 
            anonim_user = create_new_user_with_form_data(pf)
            # Add user id to session
            session.permanent = True
            session['anonim_user_id'] = anonim_user.id
        # Update user data
        else:
            update_existing_user_with_form_data(pf)
        # Get cookie
        cookies = request.cookies
        # Save id cookie str in variable
        prece_in_grozs_cookie_string = cookies.get('Prece_Id&Disc')
        prece_in_grozs_cookie_string_count = cookies.get('Prece_Count')
        # Chek cookie if grozs not empty        
        if prece_in_grozs_cookie_string and prece_in_grozs_cookie_string_count:
            # Create prece id and discount tuple list from cookie str
            tuple_list = convert_cookie_str_to_tuple_list(prece_in_grozs_cookie_string)
            if tuple_list:
                # Create pasutijums in db and save its id in session
                create_pasutijums(tuple_list)
                # Set cookie to xpire
                res.set_cookie("Prece_Count", max_age=0)
                res.set_cookie("Prece_Id&Disc", max_age=0)
        return res
    else:
        return render_template('pasutijuma_forma.html', pf=pf)


@app.route('/pasutijuma_parskats')
def pasutijuma_parskats():
    if 'anonim_user_id' in session and 'pasutijums_id' in session:
        ef = EmptyForm()
        # Get curent user object       
        anonim_user = db.session.get(AnonimUser, session['anonim_user_id'])
        # Get last pasutijums object
        pasutijums = db.session.get(Pasutijums, session['pasutijums_id'])
        # Get preces for pasutijums
        preces_pasutijumam = db.session.execute(db.select(PasutijumsPrece).where(PasutijumsPrece.pasutijums_id == session['pasutijums_id'])).scalars()

    return render_template('pasutijuma_parskats.html', ef=ef, pasutijums=pasutijums, anonim_user=anonim_user, preces_pasutijumam=preces_pasutijumam) 
        

@app.route('/edit_prece', methods=['GET', 'POST'])
@login_required
def edit_prece():
    apf = AddPreceForm()
    spf = SelectPreceForm()

    
    # If form submited
    if spf.is_submitted():
        # get target from form
        post_target = request.form.get('target')
        
        # If POST = add_new_prece
        if post_target == 'add_new_prece':
            add_new_prece(apf)
            return redirect(url_for('edit_prece'))

        # If POST = edit_selected_prece
        elif post_target == 'edit_selected_prece':
            #create_articul(apf)
            edit_selected_prece(apf)
            return redirect(url_for('edit_prece'))
        
        # If POST = delete_selcetd_prece
        elif post_target == 'delete_selcetd_prece':
            delete_selected_prece()
            return redirect(url_for('edit_prece'))
        
        # Save selected prece id in session
        else:
            session['SELECTED_PRECE_ID'] = request.form.get('id') or spf.select_prece_form.data
            return redirect(url_for('edit_prece'))
        
    elif request.method == 'GET':
        # Setup prece form. Fil with data from db if requested.
        form = setup_add_prece_form_field(apf)
        # Get bildes from db
        preces_bildes = get_bildes_for_selected_prece()
        # Print list of preces from db using paginate
        selector_preces = create_selector_and_paginate_stored_preces(spf)        
        # Get titulbilde id for selected prece if any prece selected
        if session['SELECTED_PRECE_ID'] != 0:
            titulbildes_url = get_titulbildes_url_for_selected_prece()
        else:
            # If no prece selected set titulbildes_id to None    
            titulbildes_url = None
    return render_template('edit_prece.html', **selector_preces, **form, preces_bildes=preces_bildes, titulbildes_url=titulbildes_url)


@app.route('/visi_pasutijumi', methods=['GET', 'POST'])
@login_required
def visi_pasutijumi():
    ef = EmptyForm()
    if ef.validate_on_submit():
        id = request.form.get('id')
        session['pasutijums_id'] = id
        return redirect(url_for('edit_pasutijums'))
    else:
        pasutijumi = db.session.execute(db.select(Pasutijums).order_by(Pasutijums.pasutijuma_datums.desc())).all()
        return render_template('visi_pasutijumi.html', pasutijumi=pasutijumi, ef=ef)
            

@app.route('/edit_pasutijums', methods=['GET', 'POST'])
@login_required
def edit_pasutijums():
    epf = EditPasutijumsForma()
    # Modify pasutijums data in db if form submited
    if epf.is_submitted():
        try:
            # Change pasutijums status
            if epf.edit_status.data:
                updated_pasutijums = (
                    db.update(Pasutijums)
                    .where(Pasutijums.id == session['pasutijums_id'])
                    .values(
                    status=epf.edit_status.data,
                    )
                )
                # Add updated_pasutijums object to session
                db.session.execute(updated_pasutijums)
                # Save session to db
                db.session.commit()
                flash('Pasūtījuma status izmainīts!')
            # Delete pasutijums
            elif epf.delete_pasutijums.data:
                pasutijums = db.session.get(Pasutijums, session['pasutijums_id'])
                db.session.delete(pasutijums)
                db.session.commit()
                return redirect(url_for('visi_pasutijumi'))
            
            return redirect(url_for('edit_pasutijums'))
        except:
            flash('Kļūda! Formas dati nav saglabāti')
            return redirect(url_for('edit_pasutijums'))
    # If form not submited load data from db to display in form
    else:
        pasutijums = db.session.get(Pasutijums, session['pasutijums_id'])
        user_data = db.session.get(AnonimUser, pasutijums.anonim_user_id)
        preces_pasutijumam = db.session.execute(db.select(PasutijumsPrece).where(PasutijumsPrece.pasutijums_id == session['pasutijums_id'])).scalars()
        return render_template('edit_pasutijums.html', pasutijums=pasutijums, epf=epf, user_data=user_data, preces_pasutijumam=preces_pasutijumam)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is loged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # If not logged in
    if form.validate_on_submit():
        # Query database


        stmt = db.select(User).where(User.username == form.username.data)
        user_id = db.session.execute(stmt).first()
        # Check: Is user gives correct username? 
        if user_id:
            user = db.session.get(User, user_id[0].id)
        else:
            flash('Invalid username')
            return redirect(url_for('login'))
        
        # Check: Is user gives correct apssword? 
        if user.check_password(form.password.data) is False:
            flash('Invalid password')
            return redirect(url_for('login'))
        # Login 
        login_user(user, remember=form.remember_me.data)        
        # Manage redirections back to page where login was called
        next = request.args.get('next')
        if not next or url_parse(next).netloc != '':
            next = url_for('index')
        return redirect(next)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file from the request
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    # If filename is empty, show an error flash message and redirect
    if not filename:
        flash('Fails nav augsupieladeta!')
        return redirect(url_for('edit_prece'))

    # If file type is not allowed, show an error flash message and redirect
    if not allowed_file(filename):
        flash('Fails nav augsupieladeta!')
        return redirect(url_for('edit_prece'))

    # Upload the file to GCS and get the public URL
    url = upload_file_to_gcs(uploaded_file, filename)
    flash('Bilde augsupieladeta!')

    # Get the ID of the prece from the session
    prece_id = session['SELECTED_PRECE_ID']

    # Save the bilde URL and prece ID to the database
    prece_bilde = Bilde(
        prece_id=prece_id,
        bilde_name=filename,
        bilde_url=url
    )
    db.session.add(prece_bilde)
    db.session.commit()

    # Generate the thumbnail
    thumbnail_size = (600, 600)
    thumbnail = generate_thumbnail(uploaded_file, thumbnail_size)

    # Upload the thumbnail to the thumbnail GCS bucket and get the public URL
    thumbnail_url = upload_thumbnail_to_gcs(thumbnail, filename)

    # Update the prece_bilde object with the thumbnail URL and commit changes
    prece_bilde.thumbnail_url = thumbnail_url
    db.session.commit()

    return redirect(url_for('edit_prece'))

    
@app.route('/delete_bilde', methods=['POST'])
def delete_bilde():
    # Delete the bilde from gcs
    bilde_name = request.form.get('bilde_name')
    delete_bilde_from_gcs(bilde_name)    
    # Get the id of the bilde from post request
    bilde_id = int(request.form.get('id'))
    # Delete the bilde data from sqldb
    bilde = db.session.get(Bilde, bilde_id)
    prece = db.session.get(Prece, bilde.prece_id)
    db.session.delete(bilde)
    # Delete titulbildes url from Prece table if deleted bilde is titulbildes
    if bilde_id == prece.titulbildes_id:
        prece.titulbildes_id = None
        prece.titulbildes_url = None
        db.session.add(prece)
    db.session.commit()
    flash('Bilde izdzēsta!')
    return redirect(url_for('edit_prece'))


@app.route('/set_title_bilde', methods=['POST'])
def set_title_bilde():
    # Get the id of the bilde from post request
    bilde_id = request.form.get('id')
    # Get url of the bilde from post request
    bilde_url = request.form.get('bilde_url')
    # Get the prece id from session
    prece_id = session['SELECTED_PRECE_ID']
    # Get the prece from db
    prece = db.session.get(Prece, prece_id)
    # Set the title bilde id to the prece table
    prece.titulbildes_id = bilde_id
    prece.titulbildes_url = bilde_url
    # Save the prece to db
    db.session.commit()
    flash('Titulbilde saglabāta!')
    return redirect(url_for('edit_prece'))


##########################################################################################################

# Functions

def get_titulbildes_url_for_selected_prece():
    # Get the id of the prece from session
    prece_id = session['SELECTED_PRECE_ID']
    #prece_id = 9
    # Get the prece from db
    prece = db.session.get(Prece, prece_id)
    # Get the titulbildes url from prece
    titulbildes_url = prece.titulbildes_url
    return titulbildes_url


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def get_bildes_for_selected_prece():
    # Get the id of the prece from session
    prece_id = session['SELECTED_PRECE_ID']
    # Get the bildes data from db
    bildes = db.session.scalars(db.select(Bilde).where(Bilde.prece_id == prece_id)).all()
    return bildes


def delete_bilde_from_gcs(blob_name):
    """Deletes an image from the bucket along with its thumbnail image, if provided."""

    # Create a client instance
    client = storage.Client()

    # Get the bucket and main image file to delete
    bucket_name = app.config['BUCKET_NAME']
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    if blob.exists():
        blob.delete()
        flash('Bilde izdzēsta no Google Cloud Storage!')

    # Delete the thumbnail image 
    thumbnail_bucket_name = app.config['THUMBNAIL_BUCKET_NAME']
    thumbnail_bucket = client.bucket(thumbnail_bucket_name)
    thumbnail_blob = thumbnail_bucket.blob(blob_name)

    if thumbnail_blob.exists():
        thumbnail_blob.delete()
        flash('Thumbnail bilde izdzēsta no Google Cloud Storage!')


# Get bildes from gcs
def get_bildes_from_gcs():
    # Create a client instance
    client = storage.Client()

    # Get the bucket and file to delete
    bucket_name = app.config['BUCKET_NAME']

    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    return blobs



def add_new_prece(apf):
    prece = Prece(
        cena=apf.cena.data,
        izejmateriali=apf.izejmateriali.data,
        apraksts=apf.apraksts.data,
        krasa=apf.krasa.data,
        izmers=apf.izmers.data,
        klase=apf.klase.data,
        grupa=apf.grupa.data,
        veids=apf.veids.data,
    )    
    # Add prece_data object to session
    db.session.add(prece)
    # Save session to db
    db.session.commit() 
    # Create articule and add it to prece object
    prece.artikuls = create_articul(prece.id, apf)
    # Save changes
    db.session.commit()        
    return


def edit_selected_prece(apf):
    id = session['SELECTED_PRECE_ID']
    if id != 0:

        update_prece = (
            db.update(Prece)
            .where(Prece.id == id)
            .values(
                cena=apf.cena.data, 
                izejmateriali=apf.izejmateriali.data,
                apraksts=apf.apraksts.data,
                krasa=apf.krasa.data,
                izmers=apf.izmers.data,
                klase=apf.klase.data,
                grupa=apf.grupa.data,
                veids=apf.veids.data,
            )
        )
        db.session.execute(update_prece)
        db.session.commit()
        session['SELECTED_PRECE_ID'] = 0
    return


def delete_selected_prece():
    id = session['SELECTED_PRECE_ID']
    if id != 0:
        # Delete all bildes from gcs for selected prece
        bildes = db.session.scalars(db.select(Bilde).where(Bilde.prece_id == id)).all()
        for bilde in bildes:
            delete_bilde_from_gcs(bilde.bilde_name)
        # Delete prece from db
        pasutijums = db.session.get(Prece, id)
        db.session.delete(pasutijums)
        # Delete all bildes from db for selected prece
        db.session.execute(db.delete(Bilde).where(Bilde.prece_id == id))
        db.session.commit()
        session['SELECTED_PRECE_ID'] = 0
    return          


def create_selector_and_paginate_stored_preces(spf):

    # Load data for select button list of preces.
    prece_list_to_select = db.session.execute(db.select(Prece)).scalars()
    prece_list_to_select = list(prece_list_to_select)
    # Dynamicly set list of id for select button
    spf.select_prece_form.choices = [(row.id, f"Id:{row.id}, Artikuls:{row.artikuls}") for row in prece_list_to_select]
    # Get page number from request
    page = request.args.get('page', 1, type=int)
    # Get all preces from db
    pagination = db.paginate(db.select(Prece).order_by(Prece.id.desc()), page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)

    

    next_url = url_for('edit_prece', page=pagination.next_num) \
        if pagination.has_next else None
    prev_url = url_for('edit_prece', page=pagination.prev_num) \
        if pagination.has_prev else None
    

    return { 
        'spf': spf, 
        'prece_list_to_select': prece_list_to_select,
        'pagination': pagination.items,
        'next_url': next_url, 
        'prev_url': prev_url, 
    }


def setup_add_prece_form_field(apf):
    if 'SELECTED_PRECE_ID' not in session:
        session['SELECTED_PRECE_ID'] = 0
    # Create dictionary for id and atribute (access later in html)
    id_atr = {'id': session['SELECTED_PRECE_ID'], 'atr': 0}
    # Add data to fields if requested else load empty form
    if session['SELECTED_PRECE_ID'] != 0:   
        try:
            # Get data for chosen prece        
            prece = db.session.get(Prece, session['SELECTED_PRECE_ID'])
            # Save data in form fields
            apf.klase.data = prece.klase
            apf.grupa.data = prece.grupa
            apf.veids.data = prece.veids
            apf.izejmateriali.data = prece.izejmateriali
            apf.apraksts.data = prece.apraksts
            apf.krasa.data = prece.krasa
            apf.izmers.data = prece.izmers
            apf.cena.data = prece.cena
            # Save articul value
            id_atr['atr'] = prece.artikuls
        except:
            session['SELECTED_PRECE_ID'] = 0
    return { 
        'id_atr': id_atr,
        'apf': apf, 
    }
    

def create_articul(my_id, apf):
    my_id = my_id
    klase=apf.klase.data,
    grupa=apf.grupa.data,
    veids=apf.veids.data,
    # Get value as string
    klase=klase[0]
    grupa=grupa[0]
    veids=veids[0]
    # Get strings first char
    klase=klase[0]
    grupa=grupa[0]
    veids=veids[0]
    # Create articul
    new_articul = f"{my_id}#K{klase}G{grupa}V{veids}"
    return new_articul


def get_selected_preces_and_paginate(klase, grupa):
    page = request.args.get('page', 1, type=int)
    if klase != None:
        preces = db.paginate(
            db.select(Prece).where((Prece.klase == klase) & (Prece.grupa == grupa)), 
            page=page, per_page=app.config['POSTS_PER_PAGE'], 
            error_out=False)
    else:
        preces = db.paginate(db.select(Prece), page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
        

        
    next_url = url_for('veikals', page=preces.next_num) \
        if preces.has_next else None
    prev_url = url_for('veikals', page=preces.prev_num) \
        if preces.has_prev else None
    
    #return pagination.items
    return { 
        'preces': preces.items,
        'next_url': next_url, 
        'prev_url': prev_url, 
    }


def load_pirkumu_grozs(id_disc_tuple_list):
    # Check if id_disc_tuple_list is not empty
    if id_disc_tuple_list:
        # Make dictionary from tuple list where discount is key and id is value
        id_disc_dict = dict(id_disc_tuple_list)
        # Extract id's from tuple list
        id_disc_tuple_list = [i[0] for i in id_disc_tuple_list]
        # Create query for selected preces
        stmt = (db.select(Prece).where(Prece.id.in_(id_disc_tuple_list)))
        # Execute query
        preces_groza = db.session.execute(stmt).scalars()
        # Store results in list
        preces_groza = list(preces_groza)
        # Add discount to preces_groza
        ###for prece in preces_groza:
            ###prece.discount = id_disc_dict[prece.id]
        # Return list of preces
        return preces_groza
    else:
        pass


def add_id_and_discount_to_cookie(prece_id, discount, res):
    # Create string with prece_id and discount
    prece_id_disc_str = f"#{prece_id}%{discount}&"

    # Get all cookies
    cookies = request.cookies
    # Get selected prece cookie
    prece_cookie = cookies.get('Prece_Id&Disc')
    # Get prece count in grozs cookie, for update later
    prece_count = cookies.get('Prece_Count')
    # If count exist add +1 to it
    if prece_count and prece_count.isdigit():
        prece_count = int(prece_count) + 1
        res.set_cookie("Prece_Count",value=str(prece_count), max_age=50000)
    # Create new cookie and add value 1
    else:
        res.set_cookie("Prece_Count", value='1', max_age=50000)
    # Chek if user already selected any prece
    if prece_cookie:
        # Merge old and new cookie values
        new_cookie_value = f"{prece_id_disc_str}{prece_cookie}"
        res.set_cookie("Prece_Id&Disc", value=new_cookie_value, max_age=50000)
    else:
        res.set_cookie("Prece_Id&Disc",value=prece_id_disc_str, max_age=50000)
    return res


def get_prece_cookie_without_selected_prece(prece_id_to_remove, with_discount_to_remove): 
    # Get all cookies
    cookies = request.cookies
    # Get selected prece cookie
    prece_cookie = cookies.get('Prece_Id&Disc')
    # Chek if cookie is empty
    if not prece_cookie:
        pass
    else:
        new_cookie_string = ''
        # Create list from cookie string
        prece_cookie_list = prece_cookie.split('&')
        # Set flag, change if prece skiped sub cookie adding to new cookie
        sub_cookie_adding_skipped = False 
        # Loop over list and remove selected prece
        for prece in prece_cookie_list:
            if prece:
                prece_discount_from_cookie = None
                # Get prece id from cookie string
                prece_id_from_cookie = prece.split('#')[1].split('%')[0]
                # Get discount from cookie string
                prece_discount_from_cookie = prece.split('%')[1]
                # Check if prece id from cookie is equal to selected prece id
                # If not equal add prece to new cookie string
                if prece_id_from_cookie != prece_id_to_remove or with_discount_to_remove != prece_discount_from_cookie or sub_cookie_adding_skipped:
                    # Add sub cookie string to new cookie
                    new_cookie_string += f"{prece}&"
                else:
                    # Change flag
                    sub_cookie_adding_skipped = True
        return new_cookie_string


def convert_cookie_str_to_tuple_list(prece_in_grozs_cookie_string):
    start_build_new_sub_tuple = True
    id_tuple_string = None
    prece_tuple = ()
    prece_tuple_list = []
    # Iterate over each cookie string charater
    for char in prece_in_grozs_cookie_string:
        # Check curent char, if it is marker for curent sub tuple end
        if char == '&':
            # construct tuple from string
            prece_tuple = construct_tuple(id_tuple_string)
            # Add tuple to list
            prece_tuple_list.append(prece_tuple)
            # Reset flags and variables
            start_build_new_sub_tuple = True
        else:
            # Construct sub tuple string
            if start_build_new_sub_tuple:
                if char.isdigit():
                    id_tuple_string = f"{char}"
                    start_build_new_sub_tuple = False
            else:
                id_tuple_string = f"{id_tuple_string}{char}"
    return prece_tuple_list


def construct_tuple(id_tuple_string):
    id_tuple_string = tuple(map(int, id_tuple_string.split('%')))
    print(type(id_tuple_string))
    # Construct tuple
    return id_tuple_string


def create_new_user_with_form_data(pf):
    try:
        # Save user data in db
        anonim_user = AnonimUser(
            email=pf.email.data,
            uzvards=pf.uzvards.data,
            vards=pf.vards.data,
            telefons=pf.telefons.data,
            valsts=pf.valsts.data,
            pilseta=pf.pilseta.data,
            adrese=pf.adrese.data,
            pasta_index=pf.pasta_index.data,
        )
        # Add prece_data object to session
        db.session.add(anonim_user)
        # Save session to db
        db.session.commit()        
        return anonim_user
    except:
        flash('Kļūda! Formas dati nav saglabāti')
        return redirect(url_for('grozs'))


def update_existing_user_with_form_data(pf):
    try:
        usr = db.session.get(AnonimUser, session['anonim_user_id'])
        # Update user data in db
        updated_anonim_user = (
            db.update(AnonimUser)
            .where(AnonimUser.id == session['anonim_user_id'])
            .values(
            vards=pf.vards.data or usr.vards,
            email=pf.email.data or usr.email,
            uzvards=pf.uzvards.data or usr.uzvards,
            telefons=pf.telefons.data or usr.telefons,
            valsts=pf.valsts.data,
            pilseta=pf.pilseta.data or usr.pilseta,
            adrese=pf.adrese.data or usr.adrese,
            pasta_index=pf.pasta_index.data or usr.pasta_index,
            )
        )
        # Add prece_data object to session
        db.session.execute(updated_anonim_user)
        # Save session to db
        db.session.commit()    
        return
    except:
        flash('Kļūda! Formas dati nav saglabāti')
        return redirect(url_for('grozs'))


def create_pasutijums(id_tuple):
    user_id = session['anonim_user_id']
    current_user = db.session.get(AnonimUser, user_id)
    # Create pasutijums object
    pasutijums = Pasutijums(current_user.id, datetime.now(timezone.utc).isoformat(timespec='minutes'))
    # Add to session
    db.session.add(pasutijums)
    db.session.commit()
    # Add pasutijums id to session
    session['pasutijums_id'] = pasutijums.id
    cena_sum_for_all_preces = 0
    # Create pasutijums_prece for each tuple
    # Iterate over each prece id in tuple
    for id in id_tuple:
        # Get prece object from db
        prece = db.session.get(Prece, id[0])
        # Calculate cena sum for all preces
        cena_sum_for_all_preces = cena_sum_for_all_preces + ((prece.cena / 100) * (100 - id[1]))
        # Create pasutijums_prece object
        pp = PasutijumsPrece(pasutijums, prece)
        # Add discount to PasutijumsPrece object
        pp.atlaide = id[1]
        db.session.add(pp)
    # Add cena sum to object
    pasutijums.summa = cena_sum_for_all_preces
    # Add to session
    db.session.add(pasutijums)
    # Save in db
    db.session.commit()
    return


def get_prece(prece_id_and_discount, preces_groza_list):
    new_prece = {}
    for prece in preces_groza_list:
        if prece_id_and_discount[0] == prece.id:
            new_prece = {'discount' : prece_id_and_discount[1], 
                         'id' : prece.id, 
                         'cena' : prece.cena, 
                         'artikuls' : prece.artikuls,
                         'apraksts' : prece.apraksts,
                         'izejmateriali' : prece.izejmateriali,
                         'krasa' : prece.krasa,
                         'izmers' : prece.izmers,
                         'titulbildes_url': prece.titulbildes_url,}
            return new_prece
    return


def generate_thumbnail(image_path, thumbnail_size):
    try:
        with Image.open(image_path) as image:
            image.thumbnail(thumbnail_size)
            thumbnail = io.BytesIO()
            image.save(thumbnail, format='JPEG')
            thumbnail.seek(0)
            return thumbnail
    except IOError:
        # Handle error case when image cannot be opened or thumbnail cannot be generated
        return None
    

# Function to upload file to Google Cloud Storage (GCS)
def upload_file_to_gcs(file, filename):
    bucketname = app.config['BUCKET_NAME']
    gcs_client = storage.Client()
    bucket = gcs_client.get_bucket(bucketname)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)
    return blob.public_url

# Function to upload thumbnail to a separate GCS bucket
def upload_thumbnail_to_gcs(file, filename):
    thumbnail_bucketname = app.config['THUMBNAIL_BUCKET_NAME']
    thumbnail_gcs_client = storage.Client()
    thumbnail_bucket = thumbnail_gcs_client.get_bucket(thumbnail_bucketname)
    thumbnail_blob = thumbnail_bucket.blob(filename)
    thumbnail_blob.upload_from_file(file, content_type='image/jpeg')
    return thumbnail_blob.public_url