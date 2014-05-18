import logging

class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, reject):
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record):
        if self.reject:
            return (record.levelno != self.passlevel)
        else:
            return (record.levelno == self.passlevel)




logger = logging.getLogger('arm')
logger.setLevel(logging.INFO)


warn_handler = logging.StreamHandler()
warn_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s (ARM) :: %(message)s')
warn_handler.setFormatter(formatter)

info_handler = logging.StreamHandler()
info_handler.setLevel(logging.INFO)
info_filter = SingleLevelFilter(logging.INFO, False)
info_handler.addFilter(info_filter)
formatter = logging.Formatter('%(message)s')
info_handler.setFormatter(formatter)


logger.addHandler(warn_handler)
logger.addHandler(info_handler)


class RoleException(Exception):
    pass


class Role(object):
    
    def __init__(self, local_store, *args, **kwargs):
        self.local_store = local_store
        for k,v in kwargs.iteritems():
            setattr(self, k, v)
            
    def get_name(self):
        if hasattr(self, 'github_user') and hasattr(self, 'github_repo'):
            return "%s.%s" % (getattr(self, 'github_user'), getattr(self, 'github_repo'))
        raise RoleException('Role does not have unique name')
        
    def get_path(self):
        return self.local_store
    
    def get_dependencies(self):

        needs = []
        
        if not hasattr(self, 'dependencies'):
            print "Warning : role's dependencies are not specified `%s`" % self.get_name()

        for dependency in getattr(self, 'dependencies',[]):
            if type(dependency) != str:
                print "Warning : '%s' has improperly defined dependencies." % self.get_name()
                continue
            needs.append(dependency)
            print "NEEDS : %s" % needs
        return needs

LIBRARY_ROLE_PATH = 'library_roles/'