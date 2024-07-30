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
    WEB_API_PORT        = 80
    URL_PREFIX          = '/minecraft'
    
    # Permissions
    PERM_GETSTATUS      = 0
    PERM_RUNSERVER      = 2
    PERM_STOPSERVER     = 5
    PERM_SEECONSOLE     = 8
    PERM_RUNCOMMAND     = 8
    
    ##########################
    # Database configuration #
    ##########################
    DB_USER         = "username"
    DB_PASSPHRASE   = "password"
    DB_ADDRESS      = "localhost"
    DATABASENAME    = "pyghtcraft"
    DATABASE_URL    = f"mysql://{DB_USER}:{DB_PASSPHRASE}@{DB_ADDRESS}/{DATABASENAME}"
