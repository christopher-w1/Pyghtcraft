import os

class Config:
    ########################
    # Server configuration #
    ########################
    FLAGS               = ["-Xms2G", "-Xmx2G"]
    MINECRAFT_PORT      = 25255
    STARTUP_TIME_LIMIT  = 30
    
    # Server files
    JARFILE             = "server.jar"
    JAVAPATH            = "java"
    WORKDIR             = "/home/minecraft/server/"
    
    # Process logging
    LOGFILE             = 'logs/mcservice.log'
    
    # Port for access to this API
    WEB_API_PORT        = 8001
    URL_PREFIX          = '/api'
    
    # Permissions
    PERM_RUNSERVER      = 2
    PERM_STOPSERVER     = 5
    PERM_GETSTATUS      = 0
    PERM_SEECONSOLE     = 8
    PERM_RUNCOMMAND     = 8
    
    ##########################
    # Database configuration #
    ##########################
    DB_USER         = "user"
    DB_PASSPHRASE   = "something"
    DB_ADDRESS      = "localhost"
    DATABASENAME    = "somedatabase"
    DATABASE_URL    = f"mysql://{DB_USER}:{DB_PASSPHRASE}@{DB_ADDRESS}/{DATABASENAME}"