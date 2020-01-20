## The deployment:
Note
This is being introduced late in the tutorial, but in your future projects you should always start with this.
## The layout:
Each page in the application will have the same basic layout around a different body. Instead of writing the entire HTML structure in each template, each template will extend a base template and override specific sections.

## Static files
The authentication views and templates work, but they look very plain right now. Some CSS can be added to add style to the HTML layout you constructed. The style won’t change, so it’s a static file rather than a template.


## stop at:
http://flask.palletsprojects.com/en/1.1.x/tutorial/blog/