class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://ticketapp_hasx_user:AtuEYFmzzerPFEgkcK4YH0oGhjqh6Mlf@dpg-cs6h2pbqf0us73ed0v70-a/ticketapp_hasx'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://ticketapp_hasx_user:AtuEYFmzzerPFEgkcK4YH0oGhjqh6Mlf@dpg-cs6h2pbqf0us73ed0v70-a.frankfurt-postgres.render.com/ticketapp_hasx'
    #postgresql://ticketapp_hasx_user:AtuEYFmzzerPFEgkcK4YH0oGhjqh6Mlf@dpg-cs6h2pbqf0us73ed0v70-a.frankfurt-postgres.render.com/ticketapp_hasx
    SECRET_KEY = 'e5022a73b6028678814f5b666893dc67dfde054158c29ca80f0b6ba3abf2ecad833768c49e7468f0331253d68e2935683a5f4fadbdd871e08e4fab9327b2d78b'
    JWT_SECRET_KEY = '7e2deaa768d57e626e48049ae10a368a3e31535060d075b4c2f783dcca0e138a'
    JWT_TOKEN_LOCATION = ['headers']
    SCHEDULER_API_ENABLED = True 