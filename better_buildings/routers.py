#database routers ALSO DO NOT TOUCH 
class SchoolDatabaseRouter:
    def db_for_read(self, model, **hints):
        """Directs read operations to the database specified in the hints."""
        if 'database' in hints:
            return hints['database']
        return 'default'

    def db_for_write(self, model, **hints):
        """Directs write operations to the database specified in the hints."""
        if 'database' in hints:
            return hints['database']
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """Allows relations between models."""
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Determines if a model can be migrated to a specific database."""
        if db == 'default':
            return True
        return False
