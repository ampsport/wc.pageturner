from zope.interface import implements
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from interfaces import IPageTurnerSettings, IGlobalPageTurnerSettings
from DateTime import DateTime

class Base(object):
    use_interface = None
    
    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(self.context)

        self._metadata = annotations.get('wc.pageturner', None)
        if self._metadata is None:
            self._metadata = PersistentDict()
            self._metadata['last_updated'] = DateTime('1901/01/01').ISO8601()
            annotations['wc.pageturner'] = self._metadata
                    
    def __setattr__(self, name, value):
        if name[0] == '_' or name in ['context', 'use_interface']:
            self.__dict__[name] = value
        else:
            self._metadata[name] = value

    def __getattr__(self, name):
        default = None
        if name in self.use_interface.names():
            default = self.use_interface[name].default

        return self._metadata.get(name, default)
        
class Settings(Base):
    implements(IPageTurnerSettings)
    use_interface = IPageTurnerSettings
    
class GlobalSettings(Base):
    use_interface = IGlobalPageTurnerSettings
    implements(IGlobalPageTurnerSettings)