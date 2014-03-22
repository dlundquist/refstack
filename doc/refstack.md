RefStack Configuration
===========================

This is our documentation for how we get this set up::

  # Git you clonin'
  git clone http://github.com/stackforge/refstack

  cd refstack

  # Setup or update the database
  # NOTE: you are going to have to modify the db connection string in
  #       `alembic.ini` to get this working
  # PROTIP: if you just want to test this out, use `-n alembic_sqlite` to
  #         make a local sqlite db
  #         $ alembic -n alembic_sqlite upgrade head
  alembic upgrade head

  # Plug this bad boy into your server infrastructure.
  # We use nginx and gunicorn, you may use something else if you are smarter
  # than we are.
  # For the most basic setup that you can try right now, just kick off
  # gunicorn:
  gunicorn -b 0.0.0.0:8000 refstack.web:app

  # To actually configure this winner, check out the config section and
  # crack open refstack.cfg in vim.
  # `vim refstack.cfg`

  # Now browse to http://localhost:8000