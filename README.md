# E-VEIKALS
#### Video Demo:  <https://youtu.be/vnR7Xxh3e9k>
#### Description:A small e-shop to sell handicrafts.
Regarding the project:
This is a web application built with the Python framework Flask. This version works on Google App Engine in the standard environment. It utilizes Google Cloud SQL PostgreSQL and Cloud Storage for storing product images in the store. Two buckets have been created for the images. The original images are stored in one bucket, while the small-sized images, generated from the original image during the upload process, are stored in the other bucket.	
### main.py:	
sets entry pint to Flask app.
		
### config.py Overview
The `config.py` file contains two configuration classes for your Flask application and database connection. Here's a brief overview of the code:

#### Config Class
The `Config` class represents the configuration settings for your Flask application. It includes the following attributes:

- `BUCKET_NAME`: Retrieves the Google Cloud Storage bucket name from the environment variable `GOOGLE_STORAGE_BUCKET`.
- `THUMBNAIL_BUCKET_NAME`: Retrieves the thumbnail bucket name from the environment variable `THUMBNAIL_BUCKET_NAME`.
- `SECRET_KEY`: Retrieves the secret key from the environment variable `SECRET_KEY`, or uses the default value `'you-will-never-guess'` if not found.
- `SELECTED_PRECE_ID`: Represents the selected prece ID with an initial value of `0`.
- `ALLOWED_EXTENSIONS`: A set of allowed file extensions for file uploads, including `'png'`, `'jpg'`, `'jpeg'`, and `'gif'`.
- `SESSION_PERMANENT`: Sets the `SESSION_PERMANENT` attribute to `False` to make the session non-permanent.
- `SESSION_TYPE`: Specifies the type of session storage to be used, in this case, `'filesystem'`.
- `POSTS_PER_PAGE`: Defines the number of posts per page, set to `8`.

#### Savienojums Class
The `Savienojums` class represents the configuration settings for your database connection. It includes the following attributes:

- `db_user`: Retrieves the database username from the environment variable `DB_USER`.
- `db_pass`: Retrieves the database password from the environment variable `DB_PASS`.
- `db_name`: Retrieves the database name from the environment variable `DB_NAME`.
- `unix_socket_path`: Retrieves the UNIX socket path from the environment variable `INSTANCE_UNIX_SOCKET`.

It also includes a `db_uri` attribute that generates the database URI string using the values retrieved from the environment variables. The format of the URI string is `"postgresql://<username>:<password>@/<database>?host=<socket_path>"`. Finally, the `SQLALCHEMY_DATABASE_URI` attribute is set to the generated `db_uri`.

These configuration classes provide a way to organize and centralize your application and database settings. Adjust the values according to your specific environment and requirements.


### migrations/: 
Directory where is stored config, scripts, and versions of database upgrade, downgrade procedures. Used for Alembic framework.
- Use in CLI: 
  - flask db migrate -m "new db version title" (to create migration script)
  - flask db upgrade (apply changes to the db)
	
### vaikals/: 
	Directoy where Flask app lives.

### veikals/static/css/style.css:
The CSS code included in this file, `style.css`, contains various styles for different elements in your web application. Here's a brief overview of the code:

- **Card Styles**:
  - The `.card:hover` selector sets the background color of a card element when it is hovered.
  - The `.card-img` and `.masonry-item` selectors set the overflow property of the corresponding elements to "hidden".
  - The `.card-img img` and `.masonry-item img` selectors define a transition effect on the images within the card and masonry items.
  - The `.card-img:hover img` and `.masonry-item:hover img` selectors scale the images within the card and masonry items on hover.

- **Navbar Styles**:
  - The `.navbar-brand-centered` selector positions the navbar brand element at the center using absolute positioning and transform.

- **Product Count Styles**:
  - The `.product-count` selector styles the product count element used on the "grozs" (shopping cart) with a red background, white text, and a circular shape.

- **Masonry Styles**:
  - The `.masonry-grid` selector sets the display property of the masonry grid to flex and enables wrapping of its items.
  - The `.masonry-item` selector defines the width and margin properties of the masonry items.
  - The `.masonry-item img` selector sets the width of the images within the masonry items to 100% and maintains their aspect ratio.

- **Footer Styles**:
  - The `html` and `body` selectors define the height and margin properties for the HTML and body elements.
  - The `.content` selector sets the minimum height of the content area to adjust for the footer's height.
  - The `.footer` selector adds padding and margin-top to the footer element.
  - The `.footer-nav li` and `.footer-nav li a` selectors style the list items and links within the footer.
  - The `.footer .social-link i` selector styles the social links within the footer with padding, font size, and color transition.
  - The `.footer .social-link:hover i` selector changes the color of the social links on hover.

- **Responsive Styles**:
  - The `@media` queries apply specific CSS styles for a custom breakpoint at a maximum width of 480px.
  - The `.custom-col` selector adjusts the width and flex properties of the custom columns for the specified breakpoint.

This code snippet provides a set of CSS styles that you can use to customize the appearance of various elements in your web application. Feel free to modify these styles to match your design requirements and integrate them into your project.

		
### veikals/static/js/cookies.js:

The JavaScript code snippet included in this file provides functionality for managing cookies and displaying a product count element based on the stored cookie value. Here's a brief overview of the code:

- **Prece Count Element**: The code checks for a cookie named 'Prece_Count' using the `getCookie` function. If the cookie value is greater than 0, it creates a product count element and appends it to the element with the ID 'grozs'. The count is displayed using the 'product-count' class.

- **Cookie Management Functions**: The file also includes several utility functions for managing cookies:
  - `setCookie(name, value, days)`: Sets a cookie with the given name, value, and expiration time in days.
  - `getCookie(name)`: Retrieves the value of a cookie with the specified name.
  - `deleteCookie(name)`: Deletes a cookie by setting its expiration time to a past date.


This code snippet can be used to implement functionality related to cookie management and displaying a product count element based on the stored cookie value in your web application. You can customize the code according to your specific requirements and integrate it into your project.
		
				
### veikals/static/js/masonry.pkgd.min.js: 
The `masonry.pkgd.min.js` file is a packaged version of the Masonry library, which is a cascading grid layout library. It allows you to create dynamic grid layouts with responsive behavior. The file is version 4.2.2 of Masonry, created by David DeSandro and released under the MIT License.

The library provides functions and methods that can be used to initialize Masonry layouts, call methods on Masonry instances, and handle events. It depends on the jQuery Bridget plugin for jQuery integration and the EvEmitter and getSize utilities.

To use the Masonry library, you need to include this JavaScript file in your HTML document and make sure to have jQuery, jQuery Bridget, EvEmitter, and getSize dependencies loaded as well.

For more information and usage examples, you can visit the official Masonry website at [https://masonry.desandro.com](https://masonry.desandro.com).


### veikals/static/js/veikals.js Overview

The code in `veikals.js` performs the following functions:

1. It waits for all images to finish loading before proceeding with the rest of the code. This ensures that the code operates on fully loaded images.

2. It initializes a masonry grid layout using the jQuery library. The `.masonry-grid` class is applied to the container element, and the `.masonry-item` class is applied to individual items within the grid. Additional options can be adjusted, such as the gutter size between items and the column width.

3. It enables the use of Fancybox, a JavaScript library for displaying images and other media in a lightbox overlay. Elements with the class `.fancybox` will be initialized to work with Fancybox. This allows users to click on an element (presumably an image) and view it in a larger overlay.

To use this code in your project, make sure you have included the necessary dependencies, such as jQuery and Fancybox. Then, include the `veikals.js` file in your HTML document, and the code will be executed accordingly to provide the desired functionality.

Remember to adjust any class names or options to match your specific HTML structure and requirements.


### veikals/__init__.py overview

The `__init__.py` file contains Python code that sets up a Flask web application. 
The code in `__init__.py` performs the following functions:

1. It imports necessary modules and classes from Flask and other dependencies. This includes `Flask` for creating the application, `Config` and `Savienojums` for configuration settings, `SQLAlchemy` for database operations, `Migrate` for database migrations, `LoginManager` for user authentication, and `CSRFProtect` for CSRF protection (currently commented out).

2. It creates a Flask application instance named `app`.

3. It configures the application to automatically reload templates when they are modified. This is useful during development.

4. It registers custom filters for use in templates. These filters, `usd`, `eur`, and `discount`, can be used to format currency values and calculate discounts.

5. It loads configuration settings from `Savienojums` and `Config` objects. These objects likely define settings such as database connection details and application-specific configurations.

6. It sets the lifetime of permanent sessions to three days using the `timedelta` object.

7. It creates a SQLAlchemy database instance (`db`) associated with the Flask application.

8. It creates a migration object (`migrate`) associated with the Flask application and the SQLAlchemy database instance.

9. It creates a LoginManager object (`login`) associated with the Flask application and sets the login view to `'login'`, indicating the endpoint for the login page.

10. It optionally sets up CSRF protection using the `CSRFProtect` object (currently commented out). This is useful when working with forms that handle file uploads and require a CSRF token.

11. It imports routes, models, errors, and helpers from the `veikals` package. These modules likely define the various routes, database models, error handlers, and utility functions for the application.

To use this code in your project, make sure you have Flask and the required dependencies installed. Customize the configuration settings in the `Config` and `Savienojums` objects as needed. Then, include the `__init__.py` file in your project's root directory, and the Flask application will be set up and ready to run.

Remember to adjust any import statements or filenames to match your specific project structure and requirements.


### veikals/errors.py overview:
The `errors.py` file contains error handlers for handling HTTP errors in your Flask application.

The code in `errors.py` performs the following functions:

1. It imports the `render_template` function from Flask and the `app` and `db` objects from the `veikals` package.

2. It defines an error handler for the 404 Not Found error. When a 404 error occurs, the `not_found_error` function is triggered. It returns the rendered template `'404.html'` and sets the HTTP status code to 404.

3. It defines an error handler for the 500 Internal Server Error. When a 500 error occurs, the `internal_error` function is triggered. It rolls back the database session using `db.session.rollback()` to ensure data consistency, then returns the rendered template `'500.html'` and sets the HTTP status code to 500.

To use these error handlers in your Flask application, make sure you have the necessary templates `'404.html'` and `'500.html'` in your templates directory. Customize these templates to provide an appropriate error message or page design.

To register the error handlers, ensure that the `errors.py` file is imported in the `__init__.py` file of your Flask application. This allows the error handlers to be registered with the Flask application instance.

With these error handlers in place, when a 404 or 500 error occurs in your application, Flask will invoke the appropriate error handler function and return the corresponding template, providing a user-friendly error page.


### veikals/forms.py overview:

The `forms.py` file contains several form classes for handling user input and data validation in your Flask application.
The code in `forms.py` defines the following form classes:

1. `PasutijumaForm`: Represents a form for placing an order. It includes fields for email, name, surname, phone, country, city, address, and postal code.

2. `RegistrationForm`: Represents a form for user registration. It includes fields for username, email, password, and password confirmation. It also includes validation methods to check the availability of the username and email in the database.

3. `LoginForm`: Represents a form for user login. It includes fields for username, password, and a "Remember Me" checkbox.

4. `SelectPreceForm`: Represents a form for selecting a product by its ID or article. It includes a dropdown field and a submit button.

5. `AddPreceForm`: Represents a form for adding a new product. It includes fields for selecting the product's class, group, type, materials, description, color, size, and price.

6. `AddBildeForm`: Represents a form for adding images. It includes a file upload field.

7. `EmptyForm`: Represents a simple form with a submit button and an additional button for adding items.

8. `PievienotPreciGrozamForm`: Represents a form for adding a product to the shopping cart. It includes fields for the product ID and discount percentage.

9. `EditPasutijumsForma`: Represents a form for editing an order. It includes a dropdown field for changing the order status and buttons for submitting the changes or deleting the order.

These form classes are built using the `FlaskForm` class from the `flask_wtf` package and various form fields and validators from the `wtforms` package.

To use these forms in your Flask application, you'll need to import them into your views or routes and render them in your templates. Each form class represents a specific form with its fields and validation rules. Customize these forms as needed to fit your application's requirements.

Note: Make sure to have the necessary form templates and static files (CSS, JavaScript) to support the rendering and functionality of these forms.



### veikals/helpers.py overview:
The `helpers.py` file contains custom filters and functions for formatting values in Jinja2 templates.
The code in `helpers.py` defines the following helper functions:

1. `usd(value)`: Formats the given `value` as USD currency. It returns a string representation with the value formatted with two decimal places and preceded by a dollar sign ($).

2. `eur(value)`: Formats the given `value` as EUR currency. It returns a string representation with the value formatted with two decimal places and preceded by a euro sign (€).

3. `discount(value, discount)`: Calculates the discounted price based on the original `value` and a given `discount` percentage. It returns a string representation of the discounted value in EUR currency format. The discount is calculated by subtracting the percentage discount from the original value and formatting the result with two decimal places and the euro sign (€).

These helper functions can be used in your Jinja2 templates to format values such as prices or discounts. To use them, import the `helpers.py` module and call the desired function within your templates using the appropriate template syntax.

Make sure to have the `helpers.py` module available in your project's structure and ensure that the Jinja2 templates referencing these helper functions are correctly configured and rendered within your Flask application.


### veikals/models.py overview:
The `models.py` file defines the database models used in your application.
The code in `models.py` includes the following models:

1. `User`: Represents a user in the application. It contains fields such as `id`, `email`, `username`, `vards`, `uzvards`, `telefons`, `valsts`, `pilseta`, `adrese`, and `pasta_index`. It also includes a `password_hash` field for storing the hashed password. The model includes methods for setting and checking the password, as well as relationships to `Pasutijums` and `Bilde` models.

2. `AnonimUser`: Represents an anonymous user in the application. It includes fields similar to the `User` model, such as `email`, `uzvards`, `vards`, `telefons`, `valsts`, `pilseta`, `adrese`, and `pasta_index`. It also has a relationship to the `Pasutijums` model.

3. `Bilde`: Represents an image associated with a product (`Prece`). It includes fields for `id`, `bilde_name`, `bilde_url`, `thumbnail_url`, and `prece_id`.

4. `Pasutijums`: Represents an order placed by a user. It includes fields such as `id`, `pasutijuma_datums`, `summa`, and `status`. It has relationships to `User`, `AnonimUser`, and `PasutijumsPrece` models.

5. `Prece`: Represents a product in the application. It includes fields such as `id`, `artikuls`, `cena`, `izejmateriali`, `apraksts`, `krasa`, `izmers`, `klase`, `grupa`, `veids`, `titulbildes_id`, and `titulbildes_url`. It has relationships to `Bilde` and `PasutijumsPrece` models.

6. `PasutijumsPrece`: Represents the association between a `Pasutijums` and a `Prece` in an order. It includes fields such as `id`, `artikuls`, `cena`, `cena_ar_atlaidi`, `atlaide`, `veids`, `grupa`, `klase`, `izmers`, `krasa`, and `pasutijums_id`. It has relationships to `Pasutijums` and `Prece` models.

The file also includes a `load_user` function decorated with `@login.user_loader`, which is used by Flask-Login to load a user based on their `id`.

Ensure that the `models.py` file is correctly configured and integrated into your Flask application, and that the necessary database migrations have been performed before running the application.




### veikals/routes.py overview:
The `routes.py` file contains the route definitions and functions for handling different URLs in the Flask application. Here's a summary of the routes and their respective functions:

1. Route: `'/'`
   - Function: `index()`
   - Description: Renders the `'index.html'` template with a list of preces (products) retrieved from the database.

2. Routes: `'/veikals'`, `'/veikals/<pr_klase>/<pr_grupa>'`
   - Function: `veikals(pr_klase=None, pr_grupa=None)`
   - Description: Renders the `'veikals.html'` template with a list of preces based on the provided `pr_klase` and `pr_grupa` parameters. If not provided, all preces are displayed.

3. Route: `'/<prece_klase>/<prece_grupa>/<pr_id>'`
   - Function: `prece_info(prece_klase, prece_grupa, pr_id)`
   - Description: Renders the `'prece_info.html'` template with details about a specific prece identified by `prece_klase`, `prece_grupa`, and `pr_id` parameters. It also handles adding the prece to the grozs (shopping cart) using a form.

4. Route: `'/iznemt_preci/<pr_id>/<discount>'`
   - Function: `iznemt_preci(pr_id, discount)`
   - Description: Removes a prece from the grozs (shopping cart) based on the provided `pr_id` and `discount` parameters.

5. Route: `'/register'`
   - Function: `register()`
   - Description: Handles user registration by rendering the `'register.html'` template and creating a new User object in the database.

6. Route: `'/grozs'`
   - Function: `grozs()`
   - Description: Renders the `'grozs.html'` template with the current contents of the grozs (shopping cart) retrieved from cookies.

7. Route: `'/pasutijuma_forma'`
   - Function: `pasutijuma_forma()`
   - Description: Handles the pasutijuma (order) form submission, creates a new Pasutijums object in the database, and saves relevant information in session and cookies.

8. Route: `'/pasutijuma_parskats'`
   - Function: `pasutijuma_parskats()`
   - Description: Renders the `'pasutijuma_parskats.html'` template with details about a pasutijums (order) retrieved from the database.

9. Route: `'/edit_prece'`
   - Function: `edit_prece()`
   - Description: Handles editing and management of preces (products) by rendering the `'edit_prece.html'` template and performing various operations like adding, editing, and deleting preces.

10. Route: `'/visi_pasutijumi'`
    - Function: `visi_pasutijumi()`
    - Description: Renders the `'visi_pasutijumi.html'` template with a list of all pasutijumi (orders) retrieved from the database.

11. Route: `'/edit_pasutijums'`
    - Function: `edit_pasutijums()`
    - Description: Handles editing and management of pasutijums (orders) by rendering the `'edit_pasutijums.html'` template and allowing changes to the pasutijums status or deletion.

12. Route: `'/login'`
   - Method: `GET`, `POST`
   - Function: `login()`
   - Description: Handles user login functionality. If the user is already logged in, it redirects to the `'index'` route. If the login form is submitted and valid, it queries the database to check if the username is correct. If the username is valid, it checks if the password is correct. If both username and password are valid, the user is logged in using `login_user()` function, and then it handles redirection back to the previous page or the `'index'` route.

13. Route: `'/logout'`
   - Method: `GET`
   - Function: `logout()`
   - Description: Handles user logout functionality. It logs out the current user using `logout_user()` function and redirects to the `'index'` route.

14. Route: `'/upload'`
   - Method: `POST`
   - Function: `upload()`
   - Description: Handles file upload functionality. It receives an uploaded file from the request, checks if the file is allowed based on the `allowed_file()` function, and then uploads the file to a Google Cloud Storage (GCS) bucket using the `upload_file_to_gcs()` function. It saves the file URL and associated product ID in the database, generates a thumbnail of the uploaded image, uploads the thumbnail to a thumbnail GCS bucket, and updates the database with the thumbnail URL. Finally, it redirects back to the `'edit_prece'` route.

15. Route: `'/delete_bilde'`
   - Method: `POST`
   - Function: `delete_bilde()`
   - Description: Handles deletion of an image file. It receives the name of the image file to delete, deletes the file from the GCS bucket using the `delete_bilde_from_gcs()` function, retrieves the image ID from the request, deletes the image data from the database, and updates the product table if the deleted image was the title image. Finally, it redirects back to the `'edit_prece'` route.

16. Route: `'/set_title_bilde'`
   - Method: `POST`
   - Function: `set_title_bilde()`
   - Description: Handles setting the title image for a product. It receives the image ID and URL from the request, retrieves the product ID from the session, retrieves the product from the database, sets the title image ID and URL in the product table, and saves the changes to the database. Finally, it redirects back to the `'edit_prece'` route.

## Custom Functions Overview

This `routes.py` file contains several custom functions that perform various operations related to handling prece (product) data and managing images...

1. `get_titulbildes_url_for_selected_prece()`: Retrieves the URL of the titulbildes (cover image) for the selected prece based on the prece ID stored in the session.

2. `allowed_file(filename)`: Checks if the provided `filename` is allowed based on the allowed file extensions specified in the application configuration.

3. `get_bildes_for_selected_prece()`: Retrieves the bildes (images) data for the selected prece from the database based on the prece ID stored in the session.

4. `delete_bilde_from_gcs(blob_name)`: Deletes an image and its associated thumbnail image (if provided) from the Google Cloud Storage (GCS) bucket. Uses the Google Cloud Storage client to interact with the bucket.

5. `get_bildes_from_gcs()`: Retrieves all the bildes (images) stored in the Google Cloud Storage (GCS) bucket. Uses the Google Cloud Storage client to interact with the bucket.

6. `add_new_prece(apf)`: Adds a new prece (product) to the database based on the data provided in the `apf` object. Creates an associated articule and saves the changes to the database.

7. `edit_selected_prece(apf)`: Updates the selected prece in the database based on the data provided in the `apf` object. The prece to edit is determined by the prece ID stored in the session.

8. `get_titulbildes_url_for_selected_prece()`: Retrieves the `titulbildes_url` (title image URL) for the selected "prece" (item) from the session.

9. `allowed_file(filename)`: Checks if the given `filename` is allowed based on its extension, as specified in the `ALLOWED_EXTENSIONS` configuration.

10. `get_bildes_for_selected_prece()`: Retrieves the "bildes" (images) data from the database for the selected "prece" (item).

11. `delete_bilde_from_gcs(blob_name)`: Deletes an image from Google Cloud Storage (GCS) bucket along with its thumbnail image, if provided.

12. `get_bildes_from_gcs()`: Retrieves the list of images from the Google Cloud Storage (GCS) bucket.

13. `add_new_prece(apf)`: Adds a new "prece" (item) to the database based on the data provided in the `apf` form.

14. `edit_selected_prece(apf)`: Updates the data of the selected "prece" (item) in the database based on the data provided in the `apf` form.

15. `delete_selected_prece()`: Deletes the selected "prece" (item) from the database, along with its associated images from Google Cloud Storage (GCS).

16. `create_selector_and_paginate_stored_preces(spf)`: Creates a selector and paginates the stored "preces" (items) for displaying in the user interface. It also provides the necessary data for navigation between pages.

17. `setup_add_prece_form_field(apf)`: Sets up the form fields for adding/editing a "prece" (item) based on the selected prece's ID.

18. `create_articul(my_id, apf)`: Creates an "articul" (identifier) for a new "prece" (item) based on the provided ID and form data.

19. `get_selected_preces_and_paginate(klase, grupa)`: Retrieves the selected "preces" (items) based on the specified "klase" and "grupa" (class and group) for pagination.

20. `load_pirkumu_grozs(id_disc_tuple_list)`: Loads the "preces" (items) in the shopping cart based on the provided list of IDs and discounts.

21. `add_id_and_discount_to_cookie(prece_id, discount, res)`: Adds the ID and discount of a "prece" (item) to a cookie for maintaining the shopping cart state.

22. `get_prece_cookie_without_selected_prece(prece_id_to_remove, with_discount_to_remove)`: Retrieves the shopping cart cookie without the selected "prece" (item) based on its ID and discount.

23. `convert_cookie_str_to_tuple_list(prece_in_grozs_cookie_string)`: This function converts a cookie string into a list of tuples. It iterates over each character in the cookie string, checks for markers to identify the end of a sub tuple, constructs a tuple from the string, and appends it to the list of tuples.

24. `construct_tuple(id_tuple_string)`: This function takes a string and constructs a tuple from it. The string is split by '%' and converted to integers before being used to create the tuple.

25. `create_new_user_with_form_data(pf)`: This function creates a new user with form data. It saves the user's data in the database, adds the `anonim_user` object to the session, and commits the session to the database.

26. `update_existing_user_with_form_data(pf)`: This function updates an existing user with form data. It retrieves the user's data from the database, updates the relevant fields with the form data, and commits the changes to the database.

27. `create_pasutijums(id_tuple)`: This function creates a `Pasutijums` object based on the provided `id_tuple`. It retrieves the current user from the session, creates a `pasutijums` object with the user's ID and the current datetime, adds it to the session, calculates the total price for all items in the `id_tuple`, creates a `PasutijumsPrece` object for each item in the `id_tuple`, and adds them to the session. Finally, the `pasutijums` object is saved in the database.

28. `get_prece(prece_id_and_discount, preces_groza_list)`: This function retrieves a specific `prece` object from a list of `preces_groza_list` based on the provided `prece_id_and_discount`. It iterates over the list, compares the IDs, and returns the matching `prece` object along with its details.

29. `generate_thumbnail(image_path, thumbnail_size)`: This function generates a thumbnail image from the provided `image_path` using the specified `thumbnail_size`. It opens the image, resizes it to the thumbnail size, saves it as a JPEG image, and returns the thumbnail.

30. `upload_file_to_gcs(file, filename)`: This function uploads a file to Google Cloud Storage (GCS). It takes the file object and the desired filename, retrieves the GCS bucket and blob, and uploads the file to the specified location in GCS. It returns the public URL of the uploaded file.

31. `upload_thumbnail_to_gcs(file, filename)`: This function uploads a thumbnail image to a separate GCS bucket. It is similar to `upload_file_to_gcs`, but specifically designed for thumbnail images. It returns the public URL of the uploaded thumbnail.
