# Rename to config.py

class Config:
    ########################
    # Server configuration #
    ########################
    FLAGS               = ["-Xms2G", "-Xmx2G"]
    MINECRAFT_PORT      = 25565
    STARTUP_TIME_LIMIT  = 30
    
    # Server files
    JARFILE             = "server.jar"
    JAVAPATH            = "java"
    WORKDIR             = "~/minecraft_server/"
    
    # Process logging
    LOGFILE             = 'logs/mcservice.log'
    
    # Port for access to webapp and api
    WEB_API_PORT        = 8080
    URL_PREFIX          = '/minecraft'

    # Duration the login and access key are valid (in minutes)
    KEY_VALID_DURATION  = 30
    
    # Permissions
    PERM_GETSTATUS      = 0
    PERM_RUNSERVER      = 2
    PERM_STOPSERVER     = 5
    PERM_SEECONSOLE     = 8
    PERM_RUNCOMMAND     = 8
    
    ##########################
    # Database configuration #
    ##########################
    DATABASENAME    = "mydatabase"
    DB_USER         = "myuser"
    DB_PASSPHRASE   = "mypassword"
    DB_ADDRESS      = "localhost"
    DATABASE_URL    = f"mysql://{DB_USER}:{DB_PASSPHRASE}@{DB_ADDRESS}/{DATABASENAME}"
