# UNIT 24.5 - Exercise
In this sub-unit I opted to the refactor the original solution (provided by Springboard) and refactor it to add some features I've been interested to learn.

The benefits of this approach were that I had to understand how the original solution works to make the additions I wanted to introduce. The drawbaks were that some features required on the exercise weren't implemented (eg. check username dupllicity).

The new features (not required in the exercise) include the ones in the list below:
    
    * Closure to contain the logged user
    * Login, Log out, and other routes refactores to work with the logged user
    * Almost all functions and methods were refactores to work with the new decorators
    * Decorators for @authenticated and @authorized
    * Authorization at user level
    * Authorization in the views
    * Repository layer to deal with the database (instead of the routes)
    * Massive use of Boostrap for styling
    * Static folder (accesses via 'for_url()'
    * Scss for styling
    * 'Feedback List' and 'Current User' to the navbar
    * Feedback List with each item formatted as Card
    * Fixes on the navbar styling
    * Feedback List using container-fluid and other techniques.
    * Upgraded requirements.txt
    * Using flash massages with categories
    * Others

The application also will seed the datatabase (named "unit_24") with the following users, each one having two feedbacks:

| Username | Authorizations |
| :--- | :--- |
| jane | Admin, can use all resources |
| john | Regular user, but is authorized to edit any feedbacks |
| fester | Reguar user, with no special authorizations. This means that he can only add, edit, or delete his own resources |

To run the application (make sure that the virtual environment has all the requirements installed and is activate) use:

    Flask run
or

    python app.py

